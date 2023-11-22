import os
import logging
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from exceptions import ExtractFromSheetsError, ConnectToDatabaseError, CreateTableError
from utils import sheet_to_dataframe


# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

# load env variables from .env file
load_dotenv()


class NyTaxiUtility:
    def __init__(self, url: str, worksheet_name: str) -> None:
        self.url = url
        self.worksheet_name = worksheet_name
        self.db_user = os.environ.get("DB_USER")
        self.db_password = os.environ.get("DB_PASSWORD")
        self.db_name = os.environ.get("DB_NAME")
        self.host = os.environ.get("HOST")
        self.port = os.environ.get("PORT")
        self.df = None
        self.connection = None

    def extract_from_google_sheet(self) -> None:
        try:
            self.df = sheet_to_dataframe(self.url, self.worksheet_name)
            logging.info("Extracted Data from Google Sheets successfully.")

        except Exception as e:
            raise ExtractFromSheetsError(
                "cannot extract data from Google sheets"
            ) from e

    def connect_to_database(self) -> None:
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                port=self.port,
            )
            logging.info("connected to postgres database successfully")

        except Exception as e:
            raise ConnectToDatabaseError("cannot connect to postgres database") from e

    def create_postgres_table(self) -> None:
        query ="""
        CREATE TABLE IF NOT EXISTS companies (
        "Company Name" TEXT NOT NULL, 
        "Company Link" TEXT, 
        "Company LinkedIn" TEXT, 
        CONSTRAINT companies_pk PRIMARY KEY ("Company Name"))
        """

        try:
            # create cursor object
            cursor = self.connection.cursor()

            # exacure raw query
            cursor.execute(query)

            # Commit the changes
            self.connection.commit()

            # Close the cursor object 
            cursor.close()

            logging.info("created table successfully")
        except Exception as e:
            raise CreateTableError("cannot create table") from e


# flow 
SHEET_URL = os.environ.get("SHEET_URL")
WORKSHEET_NAME = os.environ.get("WORKSHEET_NAME")

new = NyTaxiUtility(SHEET_URL, WORKSHEET_NAME)
new.extract_from_google_sheet()
new.connect_to_database()
new.create_postgres_table()
