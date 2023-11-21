import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db")
metadata = MetaData()

Session = sessionmaker(bind=engine)


class DatabaseConnector:
    def __init__(self):
        self.engine = engine
        self.metadata = metadata
        self.metadata.bind = self.engine  # Bind the metadata to the engine
        self.session = sessionmaker(bind=engine)()

    def create_table(self, table_name, schema_definition):
        # Create the 'ID' column separately
        id_column = sqlalchemy.Column('ID', sqlalchemy.Integer, primary_key=True)

        # Construct the Table object with the 'ID' column
        table = sqlalchemy.Table(table_name, self.metadata, id_column, *schema_definition.values())

        # Create the table in the database
        table.create(bind=self.engine)



    def insert_data(self, table_name, data):
        for row in data:
            self.session.execute(table_name.insert(), row)
        self.session.commit()
