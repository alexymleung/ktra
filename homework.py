import pandas as pd
from sqlalchemy import create_engine, text
import os
import csv
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kproject.settings')
django.setup()

from django.contrib import admin
from django.contrib.auth.models import User
from events.models import Event
from services.models import Service

def main():
    choice = input("What are you want to do? 1 = Data Import, 2 = Data Export: ")

    if choice == '1':
        print("You selected Data Import.")
        filePath = input("Please paste your .csv path here: ")

        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(filePath)

            # Extract file name without extension for table name
            table_name = os.path.splitext(os.path.basename(filePath))[0]

            # Data Cleansing
            # Perform data cleansing (remove duplicates)
            df.drop_duplicates(inplace=True)
            # df.fillna(df.mean(), inplace=True)  # Fill in N/A data

            print("Data cleansing complete. Here is the cleansed data:")
            print(df.head())  # Display the first few rows of the cleansed data

            saveCSV = input("Do you want to save your cleansed data file? 1 = Yes, 2 = No: ")
            if saveCSV == "1":
                output_path = 'cleansed_data.csv'
                df.to_csv(output_path, index=False)
                print(f"Cleansed data saved to {output_path}")
            importTable = ""
            importToDB = input("Do you want to import your data to database? 1 = Yes, 2 = No: ")
            if importToDB == "1":
                while True:
                    print("====================================")
                    print("1. Service")
                    print("2. Event")
                    print("3. Donation")
                    importTable = input("Which model/table you want to import to: ")
                    if importTable == "1":
                        deleteInput = input("Do you want to format table - Service ? 1 = Yes, 2 = No : ")
                        if deleteInput == "1":
                            Service.objects.all().delete()
                            print("Service formatted.")
                        with open(filePath, newline='') as file:
                            reader = csv.reader(file)
                            next(reader)  # Skip the header row
                            for row in reader:
                                title,service_type,description,service_date,service_start_time,service_end_time,fee,quota,is_publish,photo_main,photo_1,photo_2,photo_3,photo_4 = row
                                service = Service(title=title,service_type=service_type,description=description,service_date=service_date,service_start_time=service_start_time,service_end_time=service_end_time,fee=int(fee),quota=quota,is_publish=is_publish,photo_main=photo_main,photo_1=photo_1,photo_2=photo_2,photo_3=photo_3,photo_4=photo_4)
                                service.save()
                        print(f"Successfully imported data to Service from {filePath}")
                        inputAdmin = input("Do you need to register the model in admin cms?1=Yes, 2=No: ")
                        if inputAdmin == "1":
                            if admin.site.is_registered(Service):
                                    print("ServiceAdmin is already registered.")
                            else:
                                class ServiceAdmin(admin.ModelAdmin):
                                    list_display = ('title', 'fee', 'quota')
                                    list_display_link = "title",
                                    search_fields = ('service_date',)
                                admin.site.register(Service, ServiceAdmin)
                                print("ServiceAdmin is registered.")
                            break
                        else:
                            print("End of Homework.")
                            break
                    elif importTable == "2":
                        deleteInput = input("Do you want to format table - Event ? 1 = Yes, 2 = No : ")
                        if deleteInput == "1":
                            Event.objects.all().delete()
                            print("Event formatted.")
                        with open(filePath, newline='') as file:
                            reader = csv.reader(file)
                            next(reader)  # Skip the header row
                            for row in reader:
                                title,event_type,content,is_publish,publish_date,photo_main,photo_1,photo_2,photo_3,photo_4 = row
                                event =Event(title=title,event_type=event_type,content=content,is_publish=is_publish,publish_date=publish_date,photo_main=photo_main,photo_1=photo_1,photo_2=photo_2,photo_3=photo_3,photo_4=photo_4)
                                event.save()
                        print(f"Successfully imported data to Event from {filePath}")
                        inputAdmin = input("Do you need to register the model in admin cms?1=Yes, 2=No: ")
                        if inputAdmin == "1":
                            if admin.site.is_registered(Event):
                                print("EventAdmin is already registered.")
                            else:
                                class EventAdmin(admin.ModelAdmin):
                                    list_display = ('title', )
                                    list_display_link = "title",
                                admin.site.register(Event, EventAdmin)
                                print("EventAdmin is registered.")    
                            break 
                        else:
                            print("End of Homework.")
                            break
                    elif importTable == "3":
                        with open(filePath, newline='') as file:
                            reader = csv.reader(file)
                            next(reader)  # Skip the header row
                            for row in reader:
                                username,email,last_name,first_name,staff_status = row
                                user = User(username=username,email=email,last_name=last_name,first_name=first_name,staff_status=staff_status)
                                user.save()
                        print(f"Successfully imported data to User from {filePath}")
                        inputAdmin = input("Do you need to register the model in admin cms?1=Yes, 2=No: ")
                        if inputAdmin == "1":
                            if admin.site.is_registered(User):
                                print("UserAdmin is already registered.")
                            else:
                                class UserAdmin(admin.ModelAdmin):
                                    list_display = ('id', 'username')
                                    list_display_link = "id",
                                admin.site.register(User, UserAdmin)
                                print("UserAdmin is registered.")
                            break 
                        else:
                            print("End of Homework.CTRL+C to exit.")
                            break
                    else:
                        print("Input Error, Please select 1-3. or CTRL+C to exit.")
                        continue
            else:
                print("End of homework.CTRL+C to exit.")
            

        except Exception as e:
            print(f"An error occurred: {e}")

    elif choice == '2':
        print("You selected Data Export.")
        try:
            host = input("Enter your database host: ")
            port = input("Enter your database port: ")
            username = input("Enter your database username: ")
            password = input("Enter your database password: ")
            database = input("Enter your database name: ")
            
            # Create a database connection
            connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
            engine = create_engine(connection_string)
            
            # Query the data to be exported
            table_name = input("Enter the table name to export data from: ")
            query = f"SELECT * FROM \"{table_name}\";"
            
            # Execute the query and read data into a DataFrame
            df = pd.read_sql(query, con=engine)
            
            # Save the DataFrame to a CSV file
            output_path = f"{table_name}_export.csv"
            df.to_csv(output_path, index=False)
            print(f"Data exported to {output_path}")
            
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
