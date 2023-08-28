import requests
import unittest
from unittest import mock, TestCase
from unittest.mock import MagicMock, patch

# from src import helpers
from src import helpers
from src import Rates
import json


@mock.patch("helpers.requests.get")
def test_fetch_rates(mock_requests):
    mock_response = MagicMock()
    mock_response.status_code = 200
    with open("./tests/samples/eurofxref-hist-90d.xml") as f:
        xml_file = f.read()
    mock_response.content = xml_file
    # specify the return value of the get() method
    mock_requests.return_value = mock_response
    exchnage_rates = helpers.fetch_rates()
    assert len(exchnage_rates) > 0
    pass


@mock.patch("helpers.dynamo_config")
@mock.patch("Rates.Rates.__new__")
@mock.patch("helpers.fetch_rates")
def test_today_rates(mdynamo_config, mRates, mfetch_rates):
    mdynamo_config = MagicMock(return_value=[])
    mRates = MagicMock(return_value=[])
    mfetch_rates = MagicMock(return_value=[1, 2])
    with patch("helpers.Rates.get_rates") as get_rates:
        get_rates = MagicMock(return_value=[])
        helpers.today_rates()
    pass


@mock.patch("helpers.dynamo_config")
@mock.patch("Rates.Rates.__new__")
@mock.patch("helpers.today_rates")
def test_rate_comparison(mdynamo_config, mRates, mtoday_rates):
    with open("./tests/samples/exchange_api_response.json") as exapi:
        api_response = json.loads(exapi.read())
    mdynamo_config = MagicMock(return_value=[])
    mRates = MagicMock()
    mtoday_rates = MagicMock(return_value=api_response[0])
    helpers.fetch_rates()
    pass
