import cookielib
import urllib2
import mechanize
from logs.LogManager import LogManager
from spiders import config

__author__ = 'Rabbi'

class Browser:
    def __init__(self):
        self.logger = LogManager(__name__)
        self.browser = None
        self.browserCookieJar = None

    def browserLogin(self, url, loginParams, formId=None, saveCookie=False, retry=0):
        """
        Login page just like web browser
        url = '' Ex. http://www.example.com
        loginInfo = {} Ex. {'user': 'user', 'pass': 'pass'}
        """

        try:
            self.browser = self.createBrowser([config.USER_AGENT])
            self.browser.open(url, timeout=config.TIMEOUT)
            if formId is not None:
                self.browser.select_form(predicate=lambda f: 'id' in f.attrs and f.attrs['id'] == formId)
            else:
                self.browser.select_form(nr=0)
            for key in loginParams:
                self.browser.form[key] = loginParams[key]
            self.browser.submit()
            if saveCookie:
                self.browserCookieJar.save(config.COOKIE_FILE)
            return self.browser.response().read()
        except Exception, x:
            self.logger.error(x)
            if retry < config.RETRY_COUNT:
                self.browserLogin(url, loginParams, formId, saveCookie, retry + 1)
        return None

    def browserFetchData(self, url, loadCookie=False, retry=0):
        """
        Fetch data from web pages using mechanize library.i.e, act as a browser
        url='' Ex. http://www.example.com, https://www.example.com
        """
        if self.browser is None:
            self.browser = self.createBrowser([config.USER_AGENT])
        if loadCookie and self.loadCookieFromFile() is False:
            return 'login'

        try:
            self.browser.open(url, timeout=config.TIMEOUT)
            return self.browser.response().read()
        except Exception, x:
            self.logger.debug(x.message)
            if retry < config.RETRY_COUNT:
                self.browserFetchData(url, loadCookie, retry + 1)
        return None

    def createBrowser(self, headers):
        """
        Create Browser object using mechanize library so that it can act as browser
        headers = [] Ex. User-agent etc like, [('User-Agent', HEADERS), ....]
        """
        if self.browserCookieJar is None:
            self.browserCookieJar = cookielib.LWPCookieJar()
        browser = mechanize.Browser()
        browser.set_cookiejar(self.browserCookieJar)

        # Browser options
        browser.set_handle_equiv(True)
        browser.set_handle_gzip(True)
        browser.set_handle_redirect(True)
        browser.set_handle_referer(True)
        browser.set_handle_robots(True)

        # Follows refresh 0 but not hangs on refresh > 0
        browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #browser.set_debug_http(True)
        #browser.set_debug_redirects(True)
        #browser.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        browser.addheaders = headers

        return browser

    def loadCookieFromFile(self):
        try:
            self.browserCookieJar.load(config.COOKIE_FILE)
            return True
        except Exception, x:
            self.logger.error(x)
        return False

    def createCookieJarHandler(self):
        """
        Create cookie jar handler. used when keep cookie at login.
        """
        cookieJar = cookielib.LWPCookieJar()
        return urllib2.HTTPCookieProcessor(cookieJar)