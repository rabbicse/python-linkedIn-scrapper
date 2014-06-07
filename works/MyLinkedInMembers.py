from PyQt4.QtCore import QThread, pyqtSignal
from spiders.Spider import Spider
from utils.Regex import Regex
import time

__author__ = 'Rabbi'


class MyLinkedInMembers(QThread):
    notifyLinkedIn = pyqtSignal(object)
    notifyMembers = pyqtSignal(object)
    cookieL = pyqtSignal(object)

    def __init__(self, spider, url, pageRange=None):
        QThread.__init__(self)
        #        self.spider = Spider()
        self.spider = spider
        self.regex = Regex()
        self.url = url
        self.startPage = None
        self.endPage = None
        if self.regex.isFoundPattern('(?i)(\d+)-(\d+)', str(pageRange).strip()):
            pageRangeFormat = self.regex.getSearchedDataGroups('(?i)(\d+)-(\d+)', str(pageRange).strip())
            self.startPage = int(pageRangeFormat.group(1))
            self.endPage = int(pageRangeFormat.group(2))
        elif self.regex.isFoundPattern('(?i)(\d+)', str(pageRange).strip()):
            pageRangeFormat = self.regex.getSearchedDataGroups('(?i)(\d+)', str(pageRange).strip())
            self.startPage = int(pageRangeFormat.group(1))
            self.endPage = self.startPage

    def run(self):
        self.getMembers(self.url)
        self.notifyLinkedIn.emit('<font color=red><b>Finish scraping members.<b></font>')

    def getMembers(self, url, pageNumber=0):
        print 'Members URL: ' + url
        self.notifyLinkedIn.emit('<font color=green><b>Start Scraping All Members.<b></font>')
        self.notifyLinkedIn.emit('<b>Wait For 15 seconds Break...<b>')
        time.sleep(15)
        self.notifyLinkedIn.emit('<b>15 seconds Break Finish.<b>')
        groupData = self.spider.fetchData(str(url).replace('&amp;', '&'))
        groupData = self.regex.reduceNewLine(groupData)
        groupData = self.regex.reduceBlankSpace(groupData)
        print groupData

        print 'page number: ' + str(pageNumber)
        if pageNumber > 0:
            harvestedMembers = []
            allMembers = self.regex.getAllSearchedData('(?i)<li class="member" id="member-[^"]*"[^>]*?>(.*?)</div>',
                groupData)
            for members in allMembers:
                memberId = self.regex.getSearchedData('(?i)data-li-memberId="([^"]*)"', members)
                memberName = self.regex.getSearchedData('(?i)data-li-fullName="([^"]*)"', members)
                memberTitle = self.regex.getSearchedData('(?i)<p class="headline">([^<]*?)</p>', members)
                memberTitle = self.regex.replaceData('(?i)&amp;', '&', memberTitle)
                harvestedMembers.append((memberId, memberName, memberTitle))
                self.notifyLinkedIn.emit('<b>Member ID: </b>%s <b>Member Name: </b>%s' % (memberId, memberName + ' (' + memberTitle + ')'))
            #            members = self.regex.getAllSearchedData(
            #                '(?i)class="send-message" data-li-memberId="([^"]*)" data-li-fullName="([^"]*)"', groupData)
            #            print members
            self.notifyMembers.emit(harvestedMembers)
            #            for member in members:
        #                print member
        #                self.notifyLinkedIn.emit('<b>Member Name: </b>%s <b>Member ID: </b>%s' % (member[1], member[0]))

        urlNext = self.regex.getSearchedData('(?i)<a href="([^"]*)"[^>]*?>\s*?<strong>\s*?next', groupData)
        if urlNext and len(urlNext) > 0:
        #            nextP = int(self.regex.getSearchedData('(?i).*?(\d+)$', urlNext.strip()))
            urlNext = self.regex.replaceData('(?i)&amp;', '&', urlNext)
            urlNext = self.regex.replaceData('(?i)split_page=\d+', 'split_page=', urlNext)
            pageNumber += 1
            if self.startPage <= pageNumber <= self.endPage:
                self.notifyLinkedIn.emit('<b>Wait for 15 second break...</b>')
                time.sleep(15)
                print 'sleep 15 s'
                self.notifyLinkedIn.emit('<b>15 second break finish!!!</b>')
                self.getMembers('http://www.linkedin.com' + urlNext + str(pageNumber), pageNumber)
            elif pageNumber < self.startPage:
                pageNumber = self.startPage
                self.notifyLinkedIn.emit('<b>Wait for 15 second break...</b>')
                time.sleep(15)
                print 'page number less 0 sleep'
                self.notifyLinkedIn.emit('<b>15 second break finish!!!</b>')
                self.getMembers('http://www.linkedin.com' + urlNext + str(pageNumber), pageNumber)

            if self.startPage is None and self.endPage is None:
                pageNumber += 1
                self.notifyLinkedIn.emit('<b>Wait for 15 second break...</b>')
                time.sleep(15)
                print 'page number less 0 sleep'
                self.notifyLinkedIn.emit('<b>15 second break finish!!!</b>')
                self.getMembers('http://www.linkedin.com' + urlNext + str(pageNumber), pageNumber)


