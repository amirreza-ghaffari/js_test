import requests
from rest_framework import status
from js_test.business_rules import CALLER_SERVER_ADDRESS


def call_list_numbers(people_list, url=None, reason_type=None):
    try:
        params = {
            "people_list": people_list,
            "type": reason_type
        }
        res = requests.Request(method='get', url=url if url else CALLER_SERVER_ADDRESS, params=params)
        return True if res and res.status_code == status.HTTP_200_OK else False
    except Exception as e:
        return False
