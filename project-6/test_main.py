import pytest
from main import ArtsDb, DATA
from exceptions import *

apps = ArtsDb(DATA)


def test_read_data():
    assert apps.read_data


def test_data_ingestion():
    assert apps.data_ingestion


def test_data_validation():
    assert apps.data_validation

