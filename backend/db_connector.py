import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./data/database.db")
metadata = MetaData()

Session = sessionmaker(bind=engine)


class DatabaseConnector:
    def __init__(self):
        """
        Initializes the DatabaseConnector with an engine, metadata, and session.
        """
        try:
            self.engine = engine
            self.metadata = metadata
            self.metadata.bind = self.engine  # Bind the metadata to the engine
            self.session = sessionmaker(bind=engine)()
        except Exception as e:
            print(f"An error occurred in DatabaseConnector initialization: {e}")

    def create_table(self, table_name, schema_definition):
        """
        Creates a table in the database.

        Parameters:
        - table_name: Name of the table to create.
        - schema_definition: Dictionary defining the schema of the table.
        """
        try:
            id_column = sqlalchemy.Column("ID", sqlalchemy.Integer, primary_key=True)
            table = sqlalchemy.Table(
                table_name, self.metadata, id_column, *schema_definition.values()
            )
            table.create(bind=self.engine)
        except Exception as e:
            print(f"An error occurred while creating table {table_name}: {e}")

    def insert_data(self, table_name, data):
        """
        Inserts data into a table.

        Parameters:
        - table_name: Name of the table to insert data into.
        - data: List of dictionaries representing the data to insert.
        """
        try:
            for row in data:
                self.session.execute(table_name.insert(), row)
            self.session.commit()
        except Exception as e:
            print(f"An error occurred while inserting data into {table_name}: {e}")
