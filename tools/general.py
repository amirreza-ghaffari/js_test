from concurrent.futures import ThreadPoolExecutor
import requests
from django.conf import settings


def manager_caller_to_list_numbers(url, number_list, call_type):
    urls = []
    [urls.append(url.format(phone_number='9' + number, call_type=call_type)) for number in number_list]

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'DEFAULT:!DH'

    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(get_url, urls))
    return True


def get_url(url):
    headers = {settings.CALLER_SERVER_AUTH_KEY: settings.CALLER_SERVER_AUTH_VALUE}
    return requests.get(url, headers=headers)
