import csv
import sqlalchemy
import argparse
from sqlalchemy import inspect
from utilities import convert_xls_to_csv, convert_headers
from sqlalchemy import UniqueConstraint

from db_connector import DatabaseConnector


def is_integer(value):
    """
    This function checks if the given value can be converted to an integer.

    Parameters:
    value (str): The value to check.

    Returns:
    bool: True if the value can be converted to an integer, False otherwise.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def create_table_from_csv(csv_file_path, table_name):
    """
    This function creates a table in a database from a CSV file.

    Parameters:
    csv_file_path (str): The path to the CSV file.
    table_name (str): The name of the table to create.

    Returns:
    bool: True if the table was created successfully, False otherwise.
    """
    try:
        db_connector = DatabaseConnector()

        inspector = inspect(db_connector.engine)
        if inspector.has_table(table_name):
            db_connector.metadata.reflect(bind=db_connector.engine)
            db_connector.metadata.tables[table_name].drop(bind=db_connector.engine)

        with open(csv_file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            old_headers = reader.fieldnames
            new_headers = old_headers
            data = list(reader)

            for row in data:
                for old_header, new_header in zip(old_headers, new_headers):
                    row[new_header] = row.pop(old_header, None)

            schema_definition = {}
            schema_definition["ID"] = sqlalchemy.Column(
                "ID", sqlalchemy.Integer, primary_key=True
            )

            for header in new_headers:
                if header != "ID":
                    if any(map(str.isdigit, [row[header] for row in data])):
                        schema_definition[header] = sqlalchemy.Column(
                            header, sqlalchemy.Integer
                        )
                    else:
                        schema_definition[header] = sqlalchemy.Column(
                            header, sqlalchemy.String(255)
                        )

            table = sqlalchemy.Table(
                table_name, db_connector.metadata, extend_existing=True, *schema_definition.values()
            )
            table.create(bind=db_connector.engine, checkfirst=True)

            db_connector.insert_data(table, data)
            return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


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
