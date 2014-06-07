from PyQt4.QtCore import QThread, pyqtSignal
from spiders.Spider import Spider
from utils.Regex import Regex
import time

__author__ = 'Rabbi'


class MyLinkedIn(QThread):
    notifyLinkedIn = pyqtSignal(object)
    notifyMember = pyqtSignal(object)
    cookieL = pyqtSignal(object)

    def __init__(self, username, password):
        QThread.__init__(self)
        self.spider = Spider()
        self.regex = Regex()
        self.username = username
        self.password = password

    def run(self):
        if self.login():
            self.getAllGroups()

    def login(self):
        print 'login start'
        self.notifyLinkedIn.emit('<b>Trying to login. Please wait...</b>')
        loginPageData = self.spider.fetchData('https://www.linkedin.com/uas/login?goback=&trk=hb_signin')
        loginPageData = self.regex.reduceNewLine(loginPageData)
        loginPageData = self.regex.reduceBlankSpace(loginPageData)

        ## <input type="hidden" name="session_redirect" value="" id="session_redirect-login"><input type="hidden" name="csrfToken" value="ajax:9073845200579364133" id="csrfToken-login"><input type="hidden" name="sourceAlias" value="0_7r5yezRXCiA_H0CRD8sf6DhOjTKUNps5xGTqeX8EEoi" id="sourceAlias-login">
        self.sessionRedirect = self.regex.getSearchedData(
            '(?i)<input type="hidden" name="session_redirect" value="([^"]*)"',
            loginPageData)
        self.token = self.regex.getSearchedData('(?i)<input type="hidden" name="csrfToken" value="([^"]*)"',
            loginPageData)
        self.alias = self.regex.getSearchedData('(?i)<input type="hidden" name="sourceAlias" value="([^"]*)"',
            loginPageData)

        loginParam = {'csrfToken': self.token,
                      'isJsEnabled': 'true',
                      'session_key': self.username,
                      'session_password': self.password,
                      #                      'session_key': 'rabbi.cse.sust.bd@gmail.com',
                      #                      'session_password': 'ubuntu36',
                      'session_redirect': self.sessionRedirect,
                      'signin': 'Sign In',
                      'sourceAlias': self.alias,
                      'source_app': ''}
        print loginParam
        print 'start login'
        time.sleep(5)
        loginData = self.spider.login('https://www.linkedin.com/uas/login-submit', loginParam)
        loginData = self.regex.reduceNewLine(loginData)
        loginData = self.regex.reduceBlankSpace(loginData)
        #        print loginData
        isLoggedIn = self.regex.isFoundPattern('(?i)<li class="signout">', loginData)

        if isLoggedIn:
            self.notifyLinkedIn.emit('<font color=green><b>Successfully Logged In.</b></font>')
            print 'login success'
            self.cookieL.emit(self.spider)
            return True
        else:
            self.notifyLinkedIn.emit(
                '<font color=red><b>Something wrong with logging in. Please try again or check manually with this username/password</b></font>')
            return False

    def getAllGroups(self):
        print 'start groups'
        self.notifyLinkedIn.emit('<font color=green><b>Start Scraping All Groups.</b></font>')
        self.notifyLinkedIn.emit('<b>Wait for 15 second break...</b>')
        time.sleep(15)
        self.notifyLinkedIn.emit('<b>15 second break finish!!!</b>')
        self.notifyLinkedIn.emit('<font color=green><b>Fetching data for scraping your groups.</b></font>')
        groupsUrl = 'http://www.linkedin.com/myGroups?trk=hb_side_grps_top'
        groupsData = self.spider.fetchData(groupsUrl)
        self.notifyLinkedIn.emit('<font color=green><b>Data fetching complete for scraping your groups.</b></font>')
        if groupsData is not None and len(groupsData) > 0:
            print 'starting groups'
            groupsData = self.regex.reduceNewLine(groupsData)
            groupsData = self.regex.reduceBlankSpace(groupsData)
            print groupsData
            ## <a href="/groups?gid=72881&amp;trk=myg_ugrp_ovr" class="private" title="This group is members only">MySQL Professionals</a>
            groupInfo = self.regex.getAllSearchedData('(?i)<a href="(/groups\?gid=[^"]*)"[^>]*>([^<]*)</a>', groupsData)
            if groupInfo is not None and len(groupInfo) > 0:
                members = []
                for group in groupInfo:
                    groupUrl = 'http://www.linkedin.com' + str(group[0])
                    groupName = str(group[1])
                    self.notifyLinkedIn.emit('<b>Group Name: </b>%s <b>URL: </b>%s' % (groupName, groupUrl))
                    #                    http://www.linkedin.com/groups?members=&gid=65688&trk=anet_ug_memb
                    gid = self.regex.getSearchedData('(?i)gid=(\d+)', group[0])
                    print gid
                    groupUrl = 'http://www.linkedin.com/groups?members=&gid=' + gid + '&trk=anet_ug_memb'
                    members.append((groupName, groupUrl))
                self.notifyMember.emit(members)
            self.notifyLinkedIn.emit('<font color=red><b>Finish Scraping All Groups.</b></font>')
