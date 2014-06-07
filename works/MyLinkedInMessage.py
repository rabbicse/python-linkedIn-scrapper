from PyQt4.QtCore import QThread, pyqtSignal
from spiders.Spider import Spider
from utils.Regex import Regex

__author__ = 'Rabbi'


class MyLinkedInMessage(QThread):
    notifyLinkedIn = pyqtSignal(object)

    def __init__(self, spider, memberList, subject, message):
        QThread.__init__(self)
        #        self.spider = Spider()
        self.spider = spider
        self.regex = Regex()
        self.memberList = memberList
        self.subject = unicode(subject)
        self.message = unicode(message)

    def run(self):
        self.sendMessage()
        self.notifyLinkedIn.emit('<font color=red><b>Finish Sending All Messages.</b></font>')

    def sendMessage(self):
        print self.memberList
        for member in self.memberList:
            messageUrl = 'http://www.linkedin.com/inbox/compose/dialog?insider=true&connId=' + str(member[1])
            print messageUrl
#            messageUrl = 'http://www.linkedin.com/inbox/compose/dialog?insider=true&connId=' + '65471931'

#        data = self.spider.fetchData('http://www.linkedin.com/inbox/compose/dialog?insider=true&connId=65471931')
            data = self.spider.fetchData(messageUrl)
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            fromName = self.regex.getSearchedData('(?i)<input type="hidden" name="fromName" value="([^"]*)"', data)
            fromEmail = self.regex.getSearchedData('(?i)<input type="hidden" name="fromEmail" value="([^"]*)"', data)
            #        connectionIds = self.regex.getSearchedData('(?i)<input type="hidden" name="connectionIds" value="([^"]*)"', data)
            csrfToken = self.regex.getSearchedData('(?i)<input type="hidden" name="csrfToken" value="([^"]*)"', data)
            sourceAlias = self.regex.getSearchedData('(?i)<input type="hidden" name="sourceAlias" value="([^"]*)"', data)

            linkedInSubject = u'Hi ' + unicode(member[0]).split(' ')[0] + self.subject
            linkedInMessage = u'Hi ' + unicode(member[0]).split(' ')[0] + u',\n' + self.message
            print linkedInMessage
            params = {'addMoreRcpts': 'false',
                      'ajaxSubmit': 'Send Message',
                      'allowEditRcpts': 'true',
                      'body': linkedInMessage,
                      'connectionIds': str(member[1]),
                      'connectionNames': '',
                      'csrfToken': csrfToken,
                      'fromEmail': fromEmail,
                      'fromName': fromName,
                      'itemID': '',
                      'openSocialAppBodySuffix': '',
                      'showRecipeints': 'showRecipeints',
                      'sourceAlias': sourceAlias,
                      'st': '',
                      'subject': linkedInSubject,
                      'submit': 'Send Message',
                      'viewerDestinationUrl': ''}
            print params

            msgUrl = 'http://www.linkedin.com/msgToConns?displayCreate='
            data = self.spider.fetchData(msgUrl, params)
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            if self.regex.isFoundPattern('(?i)<div class="alert success">', data):
                print 'Message Sent.'
                self.notifyLinkedIn.emit('<font color=green><b>Successfully Sent Message To: %s</b></font>' % member[0])
            else:
                self.notifyLinkedIn.emit('<font color=red><b>Something Wrong during Send Message To</b></font>' % member[0])

        #        params = {'addMoreRcpts': 'false',
        #                  'ajaxSubmit': 'Send Message',
        #                  'allowEditRcpts': 'true',
        #                  'body': 'Script Test',
        #                  'connectionIds': '65471931',
        #                  'connectionNames': '',
        #                  'csrfToken': 'ajax: 6539671039643459056',
        #                  'fromEmail': '467728216',
        #                  'fromName': 'Mehedi Hasan',
        #                  'itemID': '',
        #                  'openSocialAppBodySuffix': '',
        #                  'showRecipeints': 'showRecipeints',
        #                  'sourceAlias': '0_6k2algZhQ6vbvlhlVSByxRKi0OB9NXjxrnJYWBFvfhn',
        #                  'st': '',
        #                  'subject': 'Script Test',
        #                  'submit': 'Send Message',
        #                  'viewerDestinationUrl': ''}
        #<input type="hidden" name="fromName" value="Mehedi Hasan" id="fromName-msgForm">
        # <input type="hidden" name="showRecipeints" value="showRecipeints" id="showRecipeints-msgForm">
        # <input type="hidden" name="fromEmail" value="467728216" id="fromEmail-msgForm">
        # <input type="hidden" name="connectionIds" value="65471931" id="connectionIds-msgForm">
        # <input type="hidden" name="connectionNames" value="" id="connectionNames-msgForm">
        # <input type="hidden" name="allowEditRcpts" value="true" id="allowEditRcpts-msgForm">
        # <input type="hidden" name="addMoreRcpts" value="false" id="addMoreRcpts-msgForm">
        # <input type="hidden" name="itemID" value="" id="itemID-msgForm">
        # <input type="hidden" name="openSocialAppBodySuffix" value="" id="openSocialAppBodySuffix-msgForm">
        # <input type="hidden" name="st" value="" id="st-msgForm">
        # <input type="hidden" name="viewerDestinationUrl" value="" id="viewerDestinationUrl-msgForm">
        # <input type="hidden" name="csrfToken" value="ajax:6539671039643459056" id="csrfToken-msgForm">
        # <input type="hidden" name="sourceAlias" value="0_6k2algZhQ6vbvlhlVSByxRKi0OB9NXjxrnJYWBFvfhn" id="sourceAlias-msgForm">

        """
        msgUrl1 = 'http://www.linkedin.com/msgToConns?displayCreate='
        msgParams = {}
        addMoreRcpts	false
ajaxSubmit	Send Message
allowEditRcpts	true
body	fdgdfgdfgdfg dg d
connectionIds	57414219
connectionNames
csrfToken	ajax:3480949306085123249
fromEmail	467728216
fromName	Mehedi Hasan
goback	.con.npv_57414219_*1_*1_name_r5tN_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1
itemID
openSocialAppBodySuffix
showRecipeints	showRecipeints
sourceAlias	0_6k2algZhQ6vbvlhlVSByxRKi0OB9NXjxrnJYWBFvfhn
st
subject
viewerDestinationUrl
        """

        """addMoreRcpts	false
  ajaxSubmit	Send Message
  allowEditRcpts	true
  body
  connectionIds	65471931
  connectionNames
  csrfToken	ajax:6539671039643459056
  fromEmail	467728216
  fromName	Mehedi Hasan
  itemID
  openSocialAppBodySuffix
  showRecipeints	showRecipeints
  sourceAlias	0_6k2algZhQ6vbvlhlVSByxRKi0OB9NXjxrnJYWBFvfhn
  st
  subject
  submit	Send Message
  viewerDestinationUrl	"""

        ## Message send url
        ## http://www.linkedin.com/inbox/compose/dialog?insider=true&connId=65471931
