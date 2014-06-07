from utils.Regex import Regex

__author__ = 'Rabbi'

import oauth2 as oauth
import httplib2
import time, os
import simplejson as json

class LinkedInApi:
    # Fill the keys and secrets you retrieved after registering your app
    consumer_key = 'glgxtsslmkge'
    consumer_secret = 'CzSN6hxIXo11zX6B'
    user_token = '0b6da215-9af4-49a6-97d5-e40bba7607a4'
    user_secret = '40f0dfad-10e6-43fa-b2a3-d43d184f0e4a'

    def __init__(self):
        self.regex = Regex()

    def linkedInOp(self):
        # Use your API key and secret to instantiate consumer object
        consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)

        # Use your developer token and secret to instantiate access token object
        access_token = oauth.Token(
            key=self.user_token,
            secret=self.user_secret)

        client = oauth.Client(consumer, access_token)
        ## For xml
        #        response, content = client.request('http://api.linkedin.com/v1/people/~', 'GET', headers={})
        ## For json
        #        response, content = client.request('http://api.linkedin.com/v1/people/~?format=json', 'GET', headers={}) or
        response, content = client.request('http://api.linkedin.com/v1/people/~', 'GET',
            headers={"x-li-format": 'json'})
        print response
        print content
        j = json.loads(content)
        print j['firstName']
