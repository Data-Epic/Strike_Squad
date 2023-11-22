import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from exceptions import ExtractFromSheetsError
from utils import sheet_to_dataframe



# load env variables from .env file
load_dotenv()


class NyTaxiUtility:
      def __init__(self, url:str, worksheet_name:str) -> None:
            self.url = url
            self.worksheet_name = worksheet_name

      def extract_from_google_sheet(self) -> pd.DataFrame:
            try:
                  return sheet_to_dataframe(self.url, self.worksheet_name)
            except Exception as e:
                  raise ExtractFromSheetsError("cannot extract data from Google sheets") from e
      
      # def connect_to_database(self) -> 
            
      # def create_postgres_table(self, data_frame:pd.DataFrame) -> None:


SHEET_URL=os.environ.get("SHEET_URL")
WORKSHEET_NAME=os.environ.get("WORKSHEET_NAME")

new = NyTaxiUtility(SHEET_URL,WORKSHEET_NAME)
print(new.extract_from_google_sheet())
            










# url = os.environ.get("SHEET_URL")
# work_sheet = os.environ.get("WORKSHEET_NAME")
# print(sheet_to_dataframe(url=url, worksheet_name=work_sheet))