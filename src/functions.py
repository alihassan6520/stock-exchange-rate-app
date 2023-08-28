import src.helpers as helpers
import json


def current_rates(event, context):
    # ---call the helpers.today_rates
    res = helpers.today_rates()
    return {"statusCode": 200, "body": json.dumps(res)}


def rates_comparison(event, context):
    # ---call the helpers.rate_comparison
    res = helpers.rate_comparison()
    return {"statusCode": 200, "body": json.dumps(res)}
