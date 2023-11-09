import os
import sys
import subprocess
import pytest
from typing import List
from dotenv import load_dotenv

# load env variables from .env file
load_dotenv()

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXTRACT_SH_PATH = os.path.join(BASE_PATH, os.environ.get("BASH_SCRIPT_NAME"))
sys.path.insert(0, BASE_PATH)
from main import Workbook

def subprocess_run(argument: List[str]) -> str:
    """_summary_
           This runs a bash script in a subprocess based on on the input arguments
    Args:
        argument (List[str]): takes list of string arguments

    Returns:
        str: output from bash run
    """
    arguments = argument

    return subprocess.run(
        ["bash", EXTRACT_SH_PATH, *arguments],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


# pytest fixture for class instantiation
@pytest.fixture
def workbook_instance():
    return Workbook("test_wb", "test_sh", "bestnyah7@gmail.com", "2023", "2")