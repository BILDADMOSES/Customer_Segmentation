import csv
import sqlalchemy
import argparse
from sqlalchemy import inspect
from utilities import convert_xls_to_csv, convert_headers
from db_connector import DatabaseConnector

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def create_table_from_csv(csv_file_path, table_name):
    db_connector = DatabaseConnector()

    # Check if the table exists and drop it
    inspector = inspect(db_connector.engine)
    if inspector.has_table(table_name):
        db_connector.metadata.reflect(bind=db_connector.engine)
        db_connector.metadata.tables[table_name].drop()

    with open(csv_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        old_headers = reader.fieldnames
        new_headers = convert_headers(old_headers)
        data = list(reader)

        # Change headers in the data
        for row in data:
            for old_header, new_header in zip(old_headers, new_headers):
                row[new_header] = row.pop(old_header, None)

        schema_definition = {}

        # Add custom column definition for the primary key 'ID'
        schema_definition['ID'] = sqlalchemy.Column('ID', sqlalchemy.Integer, primary_key=True)

        # Define remaining columns based on data types
        for header in new_headers:
            if header != 'ID':
                if any(map(str.isdigit, [row[header] for row in data])):
                    schema_definition[header] = sqlalchemy.Column(header, sqlalchemy.Integer)
                else:
                    schema_definition[header] = sqlalchemy.Column(header, sqlalchemy.String(255))

        print("Schema Definition:", schema_definition)  # Debugging line

        # Create the table in the database
        table = sqlalchemy.Table(table_name, db_connector.metadata, *schema_definition.values())
        table.create(bind=db_connector.engine, checkfirst=True)

        # Insert data into the table
        db_connector.insert_data(table, data)

def main():
    parser = argparse.ArgumentParser(description="Csv Uploader")
    parser.add_argument("csv_file_path", type=str, help="Path to CSV file")
    parser.add_argument("table_name", type=str, help="Name of table to create")
    args = parser.parse_args()

    csv_file_path = args.csv_file_path
    if args.csv_file_path.endswith(".xls"):
        output_file_path = args.csv_file_path.replace(".xls", ".csv")
        csv_file_path = convert_xls_to_csv(args.csv_file_path, output_file_path)
        print("File is not a CSV")
        print("Converted to CSV and saved at: {}".format(csv_file_path))
    elif not args.csv_file_path.endswith(".csv"):
        print("File is not a CSV or XLS")
        return
    create_table_from_csv(csv_file_path, args.table_name)

if __name__ == "__main__":
    main()
