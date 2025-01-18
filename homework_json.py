import pandas as pd
from sqlalchemy import create_engine, text
import os
import json  # Import json module for handling JSON files
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kproject.settings')
django.setup()

from django.contrib import admin
from django.contrib.auth.models import User
from events.models import Event
from services.models import Service

def main():
    myinput = input("What do you want to do? 1 = Data Import, 2 = Data Export: ")

    if myinput == '1':
        print("You selected Data Import.")
        filePath = input("Please paste your .json path here: ")
        try:
            # Read the JSON file into a DataFrame
            df = pd.read_json(filePath)

            # Data Cleansing
            df.drop_duplicates(inplace=True)
            print("Data cleansing complete. Here is the cleansed data:")
            print(df.head())

            if input("Do you want to save your cleansed data file? 1 = Yes, 2 = No: ") == "1":
                output_path = 'cleansed_data.json'
                df.to_json(output_path, orient='records', lines=True)  # Save as JSON
                print(f"Cleansed data saved to {output_path}")

            if input("Do you want to import your data to the database? 1 = Yes, 2 = No: ") == "1":
                while True:
                    importTable = input("Which model/table do you want to import to (1: Service, 2: Event, 3: User): ")
                    if importTable in ['1', '2', '3']:
                        if importTable == '1':
                            model = Service
                        elif importTable == '2':
                            model = Event
                        else:
                            model = User

                        if input(f"Do you want to format table - {model.__name__}? 1 = Yes, 2 = No : ") == "1":
                            model.objects.all().delete()
                            print(f"{model.__name__} formatted.")

                        # Import data into the model
                        for index, row in df.iterrows():
                            instance = model(**row.to_dict())
                            instance.save()
                        print(f"Successfully imported data to {model.__name__} from {filePath}")

                        if input("Do you need to register the model in admin cms? 1=Yes, 2=No: ") == "1":
                            if admin.site.is_registered(model):
                                print(f"{model.__name__}Admin is already registered.")
                            else:
                                class ModelAdmin(admin.ModelAdmin):
                                    list_display = ('id', 'username') if model == User else ('title',)  # Customize based on model
                                    list_display_link = "id",  # Customize based on model
                                admin.site.register(model, ModelAdmin)
                                print(f"{model.__name__}Admin is registered.")
                        break
                    else:
                        print("Input Error, Please select 1-3.")
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle exceptions appropriately

    elif myinput == '2':
        # The export functionality remains unchanged
        pass
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()