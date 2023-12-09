import logging
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from exceptions import ExtractFromParquetError, InsertError, ValidationError, NullValidation
from datetime import datetime

load_dotenv()
CONNECTION = os.environ.get('connection')
engine = create_engine(CONNECTION, echo=False)
DATA = 'data/new_file.parquet'
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Arts(Base):
    __tablename__ = "arts_db"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    title = Column(String)
    artist = Column(String)
    constituent_id = Column(Integer)
    date_acquired = Column(DateTime)
    medium = Column(String)
    credit_line = Column(String)
    classification = Column(String)
    department = Column(String)
    cataloged = Column(String)
    height = Column(Float)
    width = Column(Float)


# Base.metadata.create_all(engine)


class ArtsDb:
    def __init__(self, data):
        self.df = None
        self.data = data

    def read_data(self) -> None:
        try:
            self.df = pd.read_parquet(self.data)
            logging.info('Data collected from the csv file')

        except Exception as e:
            raise ExtractFromParquetError(
                "File does not exist"
            ) from e

    # Data ingestion process
    def data_ingestion(self) -> None:
        try:
            for num in range(len(self.df)):
                data_input = Arts(date_created=self.df['Date'][num], title=self.df['Title'][num],
                                  artist=self.df['Artist'][num], constituent_id=self.df['ConstituentId'][num],
                                  date_acquired=self.df['DateAcquired'][num], medium=self.df['Medium'][num],
                                  credit_line=self.df['CreditLine'][num], classification=self.df['Classification'][num],
                                  department=self.df['Department'][num], cataloged=self.df['Cataloged'][num],
                                  height=self.df['Height (cm)'][num], width=self.df['Width (cm)'][num]
                                  )
                if (self.df['Date'][num] is not None
                        or self.df['Title'][num] is not None
                        or self.df['Artist'][num] is not None
                        or self.df['ConstituentId'][num] is not None
                        or self.df['DateAcquired'][num] is not None
                        or self.df['CreditLine'][num] is not None
                        or self.df['Classification'][num] is not None
                        or self.df['Department'][num] is not None
                        or self.df['Cataloged'][num] is not None
                        or self.df['Height (cm)'][num] is not None
                        or self.df['Width (cm)'][num] is not None
                        or self.df['Medium'][num] is not None):
                    session.add(data_input)
                else:
                    session.add(None)

                session.commit()

        except Exception as e:
            raise InsertError("Insertion failed") from e

    def data_validation(self):
        """
            This function validates the data type
            """
        try:
            for num in range(len(self.df)):
                if (
                        isinstance(self.df['Date'][num], datetime) and
                        isinstance(self.df['Title'][num], str)
                        and isinstance(self.df['Artist'][num], str)
                        and isinstance(self.df['ConstituentId'][num], int)
                        and isinstance(self.df['DateAcquired'][num], datetime)
                        and isinstance(self.df['CreditLine'][num], str)
                        and isinstance(self.df['Classification'][num], str)
                        and isinstance(self.df['Department'][num], str)
                        and isinstance(self.df['Cataloged'][num], str)
                        and isinstance(self.df['Height (cm)'][num], float)
                        and isinstance(self.df['Width (cm)'][num], float)
                        and isinstance(self.df['Medium'][num], str)):
                    logging.info('Data type validated')
                else:
                    logging.info("Failed")
        except Exception as e:
            raise ValidationError("Data type Validation failed")


if __name__ == "__main__":
    apps = ArtsDb(DATA)
    apps.read_data()
    apps.data_validation()
    apps.data_ingestion()
