import pytest
from main import ArtsUtility, DATA
from exceptions import *

apps = ArtsUtility(DATA)


def test_read_data():
    assert apps.read_data


def test_data_ingestion():
    assert apps.data_ingestion
    with pytest.raises(InsertError, match="Insertion failed"):
        assert apps.data_ingestion()


def test_data_validation():
    assert apps.data_validation
    with pytest.raises(ValidationError, match="Data type Validation failed"):
        assert apps.data_validation()

