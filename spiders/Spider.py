from logs.LogManager import LogManager
from spiders import config

__author__ = 'Rabbi'

import urllib
import urllib2
import cookielib

class Spider:
    def __init__(self):
        self.logger = LogManager(__name__)
        self.opener = None

    def login(self, url, loginInfo, retry=0):
        """
        Login request for user
        url = '' Ex. http://www.example.com/login
        loginInfo = {} Ex. {'user': 'user', 'pass': 'pass'}
        """
        self.opener = self.createOpener([config.USER_AGENT], self.createCookieJarHandler())
        urllib2.install_opener(self.opener)
        try:
            return self.opener.open(url, urllib.urlencode(loginInfo)).read()
        except Exception, x:
            self.logger.error(x.message)
            if retry < config.RETRY_COUNT:
                self.login(url, loginInfo, retry + 1)
        return None

    def fetchData(self, url, parameters=None, retry=0):
        """
        Fetch data from a url
        url='' Ex. http://www.example.com, https://www.example.com
        parameters={} Ex. {'user': 'user', 'pass': 'pass'}
        """
        if self.opener is None:
            self.opener = self.createOpener([config.USER_AGENT])
            urllib2.install_opener(self.opener)
        try:
            if parameters is None:
                return self.opener.open(url, timeout=config.TIMEOUT).read()
            else:
                return self.opener.open(url, urllib.urlencode(parameters), timeout=config.TIMEOUT).read()
        except Exception, x:
            self.logger.debug(x)
            if retry < config.RETRY_COUNT:
                self.fetchData(url, parameters, retry + 1)
        return None

    def createOpener(self, headers=None, handler=None):
        """
        Create opener for fetching data.
        headers = [] Ex. User-agent etc like, [('User-Agent', HEADERS), ....]
        handler = object Ex. Handler like cookie_jar, auth handler etc.
        return opener
        """
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0))
        if headers is not None:
            opener.addheaders = headers
        if handler is not None:
            opener.add_handler(handler)
        return opener

    def createCookieJarHandler(self):
        """
        Create cookie jar handler. used when keep cookie at login.
        """
        cookieJar = cookielib.LWPCookieJar()
        return urllib2.HTTPCookieProcessor(cookieJar)