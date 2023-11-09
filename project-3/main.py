# pylint: disable=import-error
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2 import service_account
from gspread_dataframe import set_with_dataframe
from exceptions import (
    DataPopulationError,
    NewSheetError,
    NewSpreadsheetError,
    DownloadDataError,
    PreprocessError,
    APIConnectionError,
)
import gspread
import pandas as pd
import logging
import subprocess
import os

# load env variables from .env file
load_dotenv()

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

CREDENTIALS_PATH = os.environ.get("CREDENTIALS_PATH")
BASH_SCRIPT_PATH = os.environ.get("BASH_SCRIPT_PATH")


class Workbook:
    #  initialize gspread connections
    def __init__(
        self, workbook_name: str, sheet_name: str, email: str, year: str, month: str
    ) -> None:
        self.workbook_name = workbook_name
        self.sheet_name = sheet_name
        self.email = email
        self.year = year
        self.month = month

        # avoid attribute-defined-outside-init
        self.sh = None
        self.worksheet = None
        self.processed_data = None
        self.file_path = None
        self.df = None
        self.creds = None
        self.client = None

        # connection parameters
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

    def connect_to_api(self) -> None:
        try:
            # google cloud platform API credentials
            self.creds = service_account.Credentials.from_service_account_file(
                CREDENTIALS_PATH, scopes=self.scope
            )
            # create API client
            self.client = gspread.authorize(self.creds)

            logging.info("Connected to Google Sheets successfully.")
        except Exception as e:
            raise APIConnectionError("Could not connect to Google Sheets") from e

    def _run_bash_process(self) -> Path:
        """_summary_
            utility function to execute bash script using a subprocess to download data
        Returns:
            Path: returns downloaded file path
        """

        # bash script name
        bash_script = BASH_SCRIPT_PATH

        # bash positional arguments
        arguments = [f"{self.year}", f"{self.month}"]

        # run bash as script as subprocess
        result = subprocess.run(
            ["bash", bash_script, *arguments],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        script_output = result.stdout

        # get dowloaded data path from bash run return message eg: "./data/ny_taxi_data_3.parquet"
        download_path = script_output.split("\n")[-2]

        # return downloaded file path
        return Path(download_path)

    def download_data(self) -> None:
        """_summary_
            method to download ny taxi data
        Raises:
            DownloadDataError: If download fails
        """
        try:
            logging.info("begin downloading data!")

            self.file_path = self._run_bash_process()

            logging.info("downloading data successful")

        except Exception as e:
            raise DownloadDataError("could not download data!") from e

    # create a new spread sheet & add email to share
    def create_new_spreadsheet(self) -> None:
        """_summary_
            Method to create new spreadsheet with gspread client

        Raises:
            NewSpreadsheetError: if create sheet fails
        """
        try:
            # create new workbook/spreadsheet
            self.sh = self.client.create(self.workbook_name)

            # add email to share view/roles
            self.sh.share(self.email, perm_type="user", role="writer")

            logging.info("New spreadsheet %s created successfully.", self.workbook_name)

            return self.sh

        except Exception as e:
            raise NewSpreadsheetError("Error creating a new spreadsheet") from e

    # create new work sheet from spreadsheet
    def create_new_sheet(self) -> None:
        try:
            self.df = pd.read_parquet(self.file_path).head(5000)

            self.worksheet = self.sh.add_worksheet(
                self.sheet_name, self.df.shape[0], self.df.shape[1]
            )
            logging.info("New sheet %s created successfully.", self.sheet_name)

        except Exception as e:
            raise NewSheetError("Error creating a new sheet") from e

    def process_data(self) -> None:
        try:
            # make copy of Truth data
            self.processed_data = self.df.copy()

            #  handle null value
            self.processed_data["fare_amount"].fillna(
                self.processed_data["fare_amount"].mean(), inplace=True
            )

            # data-type handle
            self.processed_data["tpep_pickup_datetime"] = pd.to_datetime(
                self.processed_data["tpep_pickup_datetime"]
            )
            self.processed_data["tpep_dropoff_datetime"] = pd.to_datetime(
                self.processed_data["tpep_dropoff_datetime"]
            )

            # remove repeated data
            self.processed_data.drop_duplicates(inplace=True)

            # remove rides with 0 passengers
            self.processed_data = self.processed_data[
                self.processed_data["passenger_count"] > 0
            ]

            # rename columns
            self.processed_data.rename(
                columns={
                    "tpep_pickup_datetime": "pickup_time",
                    "tpep_dropoff_datetime": "dropoff_time",
                },
                inplace=True,
            )
            logging.info("preprocessed data successfully.")
        except Exception as e:
            raise PreprocessError("could not preprocess data") from e

    def populate_sheet_from_csv(self) -> None:
        try:
            set_with_dataframe(self.worksheet, self.processed_data)
            logging.info("Data populated in the sheet successfully.")
        except Exception as e:
            raise DataPopulationError("Error populating sheet from CSV") from e


def main(
    spread_sheet: str, worksheet_name: str, email: str, year: str, month: str
) -> None:
    wb = Workbook(spread_sheet, worksheet_name, email, year, month)
    wb.connect_to_api()
    wb.create_new_spreadsheet()
    wb.download_data()
    wb.create_new_sheet()
    wb.process_data()
    wb.populate_sheet_from_csv()
