import os
import pandas as pd
import gspread
from google.oauth2 import service_account
from dotenv import load_dotenv
from exceptions import CreateDataframeError

# load env variables from .env file
load_dotenv()

CREDENTIALS_PATH = os.environ.get("CREDENTIALS_PATH")



def sheet_to_dataframe(url:str, worksheet_name:str) -> pd.DataFrame:
      """_summary_
        A utility function to extract data from google sheets to a pandas dataframe
      Args:
          url (str): The Google sheet URL 
          worksheet_name (str): The work sheet title/name

      Raises:
          CreateDataframeError: error if data frame fails to be created

      Returns:
          pd.DataFrame: returns a pandas dataframe containing the data
      """
      scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
            ]

      try:
            # google cloud platform API credentials
            creds = service_account.Credentials.from_service_account_file(
                  CREDENTIALS_PATH, scopes=scope
            )
            # create API client
            client = gspread.authorize(creds)

            # open worksheet based on name
            worksheet = client.open_by_url(url).worksheet(worksheet_name)
      
            # Load data from the worksheet into a Pandas DataFrame
            return pd.DataFrame(worksheet.get_all_records())

      except Exception as e:
            raise CreateDataframeError("Could not connect to Google Sheets") from e