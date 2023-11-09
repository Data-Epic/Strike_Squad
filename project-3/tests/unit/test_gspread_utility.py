# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=broad-exception-caught
from dotenv import load_dotenv
import pytest
import sys
import os
import subprocess
from unittest.mock import patch, Mock
from ..utils.utils import subprocess_run, workbook_instance

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXTRACT_SH_PATH = os.path.join(BASE_PATH, os.environ["BASH_SCRIPT_NAME"])
sys.path.insert(0, BASE_PATH)
from exceptions import DownloadDataError, APIConnectionError

# load env variables from .env file
load_dotenv()


def test_bash_arguments() -> None:
    """_summary_
    Tests if bash file exists and is executable
    Tests bash script fails with bad arguments
    """

    # test executable bash script
    assert os.path.isfile(EXTRACT_SH_PATH) and os.access(EXTRACT_SH_PATH, os.X_OK)
    assert os.path.exists(EXTRACT_SH_PATH)

    # test for bad argument
    with pytest.raises(subprocess.CalledProcessError):
        # pylint: disable=implicit-str-concat
        bad_argument = ["2023", "2", "3"]
        result = subprocess_run(bad_argument)

        assert result.returncode == 1


@patch("subprocess.run")
def test_bash_download(mock_run):
    """_summary_
    Mock test that bash download script runs perfectly and retuens download path
    """

    # define mock result
    # pylint: disable=implicit-str-concat
    arguments = ["extract.sh" "2023", "2"]
    # define mock return value
    mock_return_value = subprocess.CompletedProcess(
        args=["bash", EXTRACT_SH_PATH, *arguments],
        returncode=0,
        stdout="./data/ny_taxi_data_2.parquet",
        stderr="",
    )
    mock_run.return_value = mock_return_value

    args = ["2023", "2"]
    result = subprocess_run(args)

    # check if successful run
    assert result.returncode == 0

    # check if standard output contains do download path
    assert "./data/ny_taxi_data_2.parquet" in result.stdout


# pylint: disable=unused-argument
@patch("main.gspread.authorize")
def test_class_instance(mock_authorize, workbook_instance):
    """_summary_
    - Test data validation
    - Mock test client connection
    """
    # mock_authorize.return_value = Mock()

    # test input data instantiation
    assert workbook_instance.email == "bestnyah7@gmail.com"
    assert workbook_instance.year == "2023"

    # # initiate client
    # workbook_instance.connect_to_api()

    # assert workbook_instance.client is not None


# test connect to API failure
@patch("main.service_account.Credentials.from_service_account_file")
def test_connect_to_api_failure(mock_service_account, workbook_instance):
    mock_service_account.side_effect = Exception("Fake error")

    with pytest.raises(APIConnectionError):
        workbook_instance.connect_to_api()


# test download data success
@patch(
    "main.Workbook._run_bash_process",
    return_value="/fake_path/data/ny_taxi_data_2.parquet",
)
def test_download_data_success(mock_run_bash_process, workbook_instance):
    try:
        workbook_instance.download_data()
        assert True
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

    mock_run_bash_process.assert_called_once()
    assert workbook_instance.file_path == "/fake_path/data/ny_taxi_data_2.parquet"


# test download data method failure
@patch("main.Workbook._run_bash_process")
def test_download_data_failure(mock_download_data, workbook_instance):
    mock_download_data.side_effect = Exception("Fake error")

    with pytest.raises(DownloadDataError):
        workbook_instance.download_data()


# test creation of new spredsheet
# @patch("main.gspread.authorize")
# def test_create_new_spreadsheet_success(mock_authorize, workbook_instance):
#     mock_client = Mock()
#     mock_spreadsheet = Mock()

#     mock_client.create.return_value = mock_spreadsheet
#     mock_authorize.return_value = mock_client

#     try:
#         workbook_instance.connect_to_api()
#         workbook_instance.create_new_spreadsheet()
#         assert True
#     except Exception as e:
#         pytest.fail(f"Unexpected exception: {e}")

#     mock_authorize.assert_called_once()
#     assert workbook_instance.sh is not None
