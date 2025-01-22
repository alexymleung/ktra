import pandas as pd
import os
import json
import logging
import django
from datetime import date, datetime
from django.db import connection, transaction
from django.core.exceptions import ValidationError
from django.conf import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_transfer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kproject.settings')
django.setup()

from django.contrib import admin
from django.contrib.auth.models import User
from events.models import Event
from services.models import Service

def serialize_data(queryset):
    """Convert queryset to a list of dictionaries, exclude 'id', and serialize date fields."""
    try:
        data = []
        for item in queryset:
            if not isinstance(item, dict):
                raise ValueError("Queryset items must be dictionaries")
                
            item_dict = item.copy()
            item_dict.pop('id', None)
            
            for key, value in item_dict.items():
                if isinstance(value, (date, datetime)):
                    item_dict[key] = value.isoformat()
                elif isinstance(value, (list, dict)):
                    item_dict[key] = json.dumps(value)
                    
            data.append(item_dict)
        return data
    except Exception as e:
        logger.error(f"Serialization error: {str(e)}")
        raise

def reset_sequence(model):
    """Reset the primary key sequence for the specified model."""
    try:
        with connection.cursor() as cursor:
            table_name = model._meta.db_table
            cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;")
            logger.info(f"Reset sequence for {table_name}")
    except Exception as e:
        logger.error(f"Sequence reset error for {model.__name__}: {str(e)}")
        raise

def truncate_table(model):
    """Truncate the table for the specified model with CASCADE."""
    try:
        with connection.cursor() as cursor:
            table_name = model._meta.db_table
            cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE;")
            logger.info(f"Truncated table {table_name}")
    except Exception as e:
        logger.error(f"Table truncation error for {model.__name__}: {str(e)}")
        raise

class DataTransfer:
    """Main data transfer class handling import/export operations"""
    
    MODEL_MAPPING = {
        '1': Service,
        '2': Event,
        '3': User
    }
    
    def __init__(self):
        self.valid_extensions = getattr(settings, 'DATA_TRANSFER_VALID_EXTENSIONS', ['.json'])
        self.max_file_size = getattr(settings, 'DATA_TRANSFER_MAX_SIZE', 10485760)  # 10MB
        
    def validate_file(self, file_path):
        """Validate file path and size"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not any(file_path.endswith(ext) for ext in self.valid_extensions):
            raise ValueError(f"Invalid file extension. Supported: {', '.join(self.valid_extensions)}")
            
        if os.path.getsize(file_path) > self.max_file_size:
            raise ValueError(f"File size exceeds maximum limit of {self.max_file_size} bytes")
            
        return True

    def import_data(self):
        """Handle data import process"""
        try:
            file_path = input("Please paste your .json path here: ")
            self.validate_file(file_path)
            
            with transaction.atomic():
                df = pd.read_json(file_path)
                df.drop_duplicates(inplace=True)
                logger.info("Data cleansing complete")
                
                if input("Save cleansed data? 1 = Yes, 2 = No: ") == "1":
                    output_path = 'cleansed_data.json'
                    df.to_json(output_path, orient='records', lines=True)
                    logger.info(f"Cleansed data saved to {output_path}")
                    
                if input("Import to database? 1 = Yes, 2 = No: ") == "1":
                    self._process_import(df)
        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            raise

    def _process_import(self, df):
        """Process data import into selected model"""
        while True:
            model_choice = input("Which model to import to (1: Service, 2: Event, 3: User): ")
            if model_choice not in self.MODEL_MAPPING:
                logger.warning("Invalid model choice")
                continue
                
            model = self.MODEL_MAPPING[model_choice]
            
            if input(f"Format table - {model.__name__}? 1 = Yes, 2 = No: ") == "1":
                truncate_table(model)
                reset_sequence(model)
                
            self._import_to_model(df, model)
            break

    def _import_to_model(self, df, model):
        """Import data into specific model"""
        try:
            for index, row in df.iterrows():
                instance = model(**row.to_dict())
                instance.full_clean()  # Validate model instance
                instance.save()
                
            logger.info(f"Successfully imported data to {model.__name__}")
            
            if input("Register model in admin? 1=Yes, 2=No: ") == "1":
                self._register_admin(model)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Import error: {str(e)}")
            raise

    def _register_admin(self, model):
        """Register model in admin if not already registered"""
        if admin.site.is_registered(model):
            logger.info(f"{model.__name__}Admin already registered")
            return
            
        class ModelAdmin(admin.ModelAdmin):
            list_display = ('id', 'username') if model == User else ('title',)
            list_display_link = "id",
            
        admin.site.register(model, ModelAdmin)
        logger.info(f"{model.__name__}Admin registered")

    def export_data(self):
        """Handle data export process"""
        try:
            while True:
                model_choice = input("Which model to export from (1: Service, 2: Event, 3: User): ")
                if model_choice not in self.MODEL_MAPPING:
                    logger.warning("Invalid model choice")
                    continue
                    
                model = self.MODEL_MAPPING[model_choice]
                self._export_model(model)
                break
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            raise

    def _export_model(self, model):
        """Export data from specific model"""
        queryset = model.objects.all().values()
        data = serialize_data(queryset)
        
        output_path = f'{model.__name__.lower()}_data.json'
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            
        logger.info(f"Data exported to {output_path}")

def main():
    """Main entry point"""
    transfer = DataTransfer()

    try:
        choice = input("What do you want to do? 1 = Data Import, 2 = Data Export: ")
        
        if choice == '1':
            logger.info("Starting data import")
            transfer.import_data()
        elif choice == '2':
            logger.info("Starting data export")
            transfer.export_data()
        else:
            logger.warning("Invalid choice selected")
            print("Invalid choice. Please select 1 or 2.")
            
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
