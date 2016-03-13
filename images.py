#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

API_URL = "https://api.shutterstock.com"
ACCESS_TOKEN = "v2/YjNjMmVlMTI3YjUxZTJkZTI5ODAvMTU0MDExMzcwL2N1c3RvbWVyLzIvdElBT2dpemlxOFJzTG1NV3BZMkprQkl5VVV2bkJ5SGQ3aGJHSC1NMlZ5bDc1NVJIbml0Q1BISU5UZGRpdlJEbHFuS1dRYXRUM3FOZFpXVEZaNTI5emw1NFRiMVItTzJHbVpwOXQ5eUJLSkxjU1ctcE9kclFlVzdiZTBZbHJaaUluei1SN0ZtbTBTcklrdkxqRTZWb2tDaUpQUGlGWlR5T0tOelNDMGh2S1paZGNMVWkzYmJrY2JFdmpmeW5QN3pk"

def get_images(keyword):
    r = requests.get(
        API_URL + "/v2/images/search",
        params={
            "query": keyword,
        },
        headers={
            "Authorization": "Bearer %s" % ACCESS_TOKEN,
        }
    )

    response = r.json()

    images = [i for i in response['data']]

    return images
