import requests
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from boto3.dynamodb.conditions import Key
from src.Rates import Rates
import boto3
import os
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


def dynamo_config():
    if "LOCALSTACK_HOSTNAME" in os.environ:
        host = os.environ.get("LOCALSTACK_HOSTNAME", "localhost")
        region = os.environ.get("region", "us-east-1")
        dynamodb_endpoint = f"http://{host}:4566"
        resource = boto3.resource(
            "dynamodb", endpoint_url=dynamodb_endpoint, region_name=region
        )
    else:
        resource = boto3.resource("dynamodb")
    return resource


def fetch_rates():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
    res = requests.get(url)
    schema = "{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}"
    root = ET.fromstring(res.content)
    children = root.findall(f".//{schema}Cube[@time]")
    rates = []
    days = 2
    for day, child in zip(range(0, days), children):
        slot = {"time": child.attrib["time"]}
        today_rates = []
        for grandchild in child.findall(f".//{schema}Cube"):
            today_rates.append(grandchild.attrib)
        slot["rates"] = today_rates
        rates.append(slot)
    return rates


def today_rates():
    """
    Get todats rates from dynamoDB if not there then fetch by calling rates function
    """
    rates_dynamo = Rates(dynamo_config())
    today = date.today()
    yesterday = today - timedelta(1)
    current_rates = rates_dynamo.get_rates(today)
    if current_rates is []:
        today = today - timedelta(1)
        yesterday = yesterday - timedelta(1)
        current_rates = rates_dynamo.get_rates(today)
    yesterday_rates = rates_dynamo.get_rates(yesterday)
    if not current_rates:
        rates = fetch_rates()
        if not yesterday_rates:
            rates_dynamo.add_rates(rates)
        else:
            rates_dynamo.add_rates([rates[0]])
        return rates[0]
    else:
        return current_rates


def rate_comparison():
    rates_dynamo = Rates(dynamo_config())
    current_rates = today_rates()
    yesterday = str(
        datetime.strptime(current_rates["time"], "%Y-%m-%d").date() - timedelta(1)
    )
    yesterday_rates = rates_dynamo.get_rates(yesterday)
    exchange_rate = []
    for t, y in zip(current_rates["rates"], yesterday_rates["rates"]):
        assert t["currency"] == y["currency"]
        change = float(y["rate"]) - float(t["rate"])
        rate_of_change = {
            "currency": t["currency"],
            "change": change,
            "today": t["currency"],
            "yesterday": y["currency"],
        }
        if change < 0:
            rate_of_change["type"] = "Decreased"
        elif change == 0:
            rate_of_change["type"] = "No Change"
        else:
            rate_of_change["type"] = "Increased"
        exchange_rate.append(rate_of_change)
    return exchange_rate
