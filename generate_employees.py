import faker
import random
import csv
from google.cloud import storage

def generate_dummy_employee_data(num_employees):
    """Generates dummy employee data using Faker.

    Args:
        num_employees: The number of employees to generate.

    Returns:
        A list of dictionaries, each representing an employee with their data.
    """

    fake = faker.Faker()
    employees = []

    for _ in range(num_employees):
        # Generate a random date of birth for an employee (between 18 and 65 years ago)
        date_of_birth = fake.date_of_birth()

        # Hire date can be generated as a random date within the last 10 years
        hire_date = fake.date_this_decade()

        employee = {
            "employee_id": fake.unique.random_int(min=100000, max=999999),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            
            "department": fake.random_element(["Sales", "Marketing", "Engineering", "Human Resources", "Finance"]),
            "salary": fake.random_int(min=30000, max=150000),
            "ssn": fake.ssn(),
            
        }
        employees.append(employee)

    return employees

def write_to_csv(employee_data, filename):
    """Writes employee data to a CSV file.

    Args:
        employee_data: A list of employee dictionaries.
        filename: The name of the CSV file to write to.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=employee_data[0].keys())
        writer.writeheader()
        writer.writerows(employee_data)


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to a Google Cloud Storage bucket.

    Args:
        bucket_name: The name of the GCS bucket.
        source_file_name: The path to the file to upload.
        destination_blob_name: The name of the blob to create in GCS.
    """
    client = storage.Client(project='etl-data-439322')
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"Uploaded {source_file_name} to {destination_blob_name} in bucket {bucket_name}.")

if __name__ == "__main__":
    num_employees = 100
    employee_data = generate_dummy_employee_data(num_employees)

    # Write the data to a CSV file
    csv_filename = 'employee_data.csv'
    write_to_csv(employee_data, csv_filename)

    print(f"Generated {num_employees} employee records and saved to '{csv_filename}'.")

    # Upload the CSV file to Google Cloud Storage
    bucket_name = 'bkt-emp1-data'  # Replace with your bucket name
    upload_to_gcs(bucket_name, csv_filename, csv_filename)  # You can specify a different destination blob name if needed
