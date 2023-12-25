import logging
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from exceptions import ExtractFromParquetError, InsertError, ValidationError
from datetime import datetime

load_dotenv()
CONNECTION = os.environ.get('CONNECTIONS')
engine = create_engine(CONNECTION, echo=False)
DATA = os.environ.get('DATASET')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Arts(Base):
    __tablename__ = "museum_arts"

    id = Column(Integer, index=True)
    date_created = Column(DateTime)
    title = Column(String)
    artist = Column(String, primary_key=True)
    constituent_id = Column(Integer, index=True)
    date_acquired = Column(DateTime)
    medium = Column(String)
    credit_line = Column(String)
    classification = Column(String)
    department = Column(String)
    cataloged = Column(String)
    object_id = Column(Integer, primary_key=True)
    height = Column(Float)
    width = Column(Float)


# Base.metadata.create_all(engine)


class ArtsUtility:
    def __init__(self, data):
        self.df = None
        self.data = data

    def read_data(self):
        try:
            self.df = pd.read_parquet(self.data)
            logging.info('Data collected from the parquet file')
        except Exception as e:
            raise ExtractFromParquetError("File does not exist") from e

    # Data ingestion process
    def data_ingestion(self) -> None:
        try:
            for num in range(len(self.df)):
                data_input = Arts(id=num, date_created=self.df['Date'][num], title=self.df['Title'][num],
                                  artist=self.df['Artist'][num], constituent_id=self.df['ConstituentId'][num],
                                  date_acquired=self.df['DateAcquired'][num], medium=self.df['Medium'][num],
                                  credit_line=self.df['CreditLine'][num], classification=self.df['Classification'][num],
                                  department=self.df['Department'][num], cataloged=self.df['Cataloged'][num],
                                  object_id=self.df['ObjectID'][num],
                                  height=self.df['Height (cm)'][num], width=self.df['Width (cm)'][num]
                                  )
                columns = ['Date', 'Title', 'Artist', 'ConstituentId', 'DateAcquired', 'CreditLine',
                           'Classification', 'Department', 'Cataloged', 'Height (cm)', 'Width (cm)', 'Medium']

                if any(self.df[col][num] is not None for col in columns):
                    session.add(data_input)
                else:
                    session.add(None)

                session.commit()
                logging.info("Data ingestion successful")

        except Exception as e:
            raise InsertError("Insertion failed") from e

    def data_validation(self):
        """
            This function validates the data type
            """
        try:
            for num in range(len(self.df)):
                data_types = {
                    'Date': datetime,
                    'Title': str,
                    'Artist': str,
                    'ConstituentId': int,
                    'DateAcquired': datetime,
                    'CreditLine': str,
                    'Classification': str,
                    'Department': str,
                    'Cataloged': str,
                    'Height (cm)': float,
                    'Width (cm)': float,
                    'Medium': str
                }

                if all(isinstance(self.df[col][num], data_type) for col, data_type in data_types.items()):
                    logging.info('Data type validated')
                else:
                    logging.info('Failed')
        except Exception as e:
            raise ValidationError(f"Data type Validation failed") from e


if __name__ == "__main__":
    apps = ArtsUtility(DATA)
    apps.read_data()
    apps.data_validation()
    apps.data_ingestion()
