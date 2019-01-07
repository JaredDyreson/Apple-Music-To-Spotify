#!/usr/bin/env pytho3.5
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

class urlResponse():
    def __init__(self, url, r=None):
        self.url = url
    def is_good_response(self, response):
        content = response.headers['Content-Type'].lower()
        return (response.status_code == 200
                and content is not None
                and content.find('html') > -1)
    def getUrl(self, url):
        try:
            with closing(get(url, stream=True)) as response:
                if(self.is_good_response(response)):
                    return response.content
                else:
                    return None
        except RequestException as e:
            print("Error, shrug")
