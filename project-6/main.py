import logging
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from exceptions import ExtractFromCSVError, InsertError

load_dotenv()
CONNECTION = os.environ.get('connection')
engine = create_engine(CONNECTION, echo=False)
DATA = 'data/cleaned_data.csv'
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
            self.df = pd.read_csv(self.data)
            logging.info('Data collected from the csv file')

        except Exception as e:
            raise ExtractFromCSVError(
                "cannot extract data from CSV"
            ) from e

    # Data ingestion process
    def ingestion(self) -> None:
        try:
            for num in range(0, 139632):
                data_input = Arts(date_created=self.df['Date'][num], title=self.df['Title'][num],
                                  artist=self.df['Artist'][num], constituent_id=self.df['ConstituentId'][num],
                                  date_acquired=self.df['DateAcquired'][num], medium=self.df['Medium'][num],
                                  credit_line=self.df['CreditLine'][num], classification=self.df['Classification'][num],
                                  department=self.df['Department'][num], cataloged=self.df['Cataloged'][num],
                                  height=self.df['Height (cm)'][num], width=self.df['Width (cm)'][num]
                                  )

                session.add(data_input)

                session.commit()
        except Exception as e:
            raise InsertError("Insertion failed") from e



apps = ArtsDb(DATA)
apps.read_data()
apps.ingestion()
# apps.count()
