import time
from PyQt4.QtCore import SIGNAL, Qt, QString
from PyQt4.QtGui import *
import sys
from utils.Csv import Csv
from works.MyLinkedIn import MyLinkedIn
from works.MyLinkedInMembers import MyLinkedInMembers
from works.MyLinkedInMessage import MyLinkedInMessage

__author__ = 'Rabbi'

class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.createGui()
        self.memberDic = {}
        self.excludedMember = None
        dupCsvReader = Csv()
        self.dupCsvRows = dupCsvReader.readCsvRow('linkedIn.csv', 0)
        self.csvWriter = Csv('linkedIn.csv')
        self.allMembers = []

    def createGui(self):
        self.labelUser = QLabel('<b>Username: </b>')
        self.inputUser = QLineEdit()

        self.labelPass = QLabel('<b>Password:</b>')
        self.inputPass = QLineEdit()

        self.labelPageRange = QLabel('<b>Select Your Page Range:<br />Example: 2-5 or 1 </b>')
        self.inputPageRange = QLineEdit()

        self.btnGroup = QPushButton('&Scrap Groups')
        self.btnGroup.clicked.connect(self.btnOkAction)

        self.labelCombo = QLabel('<b>Select Your Group: </b>')
        self.combo = QComboBox()
        self.combo.currentIndexChanged.connect(self.groupChangeEvent)

        self.labelExcludeMember = QLabel('<b>Write Your Excluded Member Name: <br />(ex_member1,ex_member2)</b>')
        self.inputExcludeMember = QLineEdit()

        self.btnMember = QPushButton('&Scrap Members')
        self.btnMember.clicked.connect(self.btnMembersAction)
        self.labelMember = QLabel('<b>Scraped Members: </b>')
        self.browserMember = QTextBrowser()
        self.browserMember.setReadOnly(False)

        self.btnExcludeAll = QPushButton('&Exclude All Member')
        self.btnExcludeAll.clicked.connect(self.excludeAllAction)

        self.labelSubject = QLabel('<b>Message Subject: </b>')
        self.inputSubject = QLineEdit()

        self.labelMessage = QLabel('<b>Write Message: </b>')
        self.browserMessage = QTextBrowser()
        self.browserMessage.setReadOnly(False)

        self.btnSendMessage = QPushButton('&Send Message')
        self.btnSendMessage.clicked.connect(self.sendMessageAction)

        self.browser = QTextBrowser()

        layout = QGridLayout()
        layout.addWidget(self.labelUser, 0, 0)
        layout.addWidget(self.inputUser, 0, 1)
        layout.addWidget(self.labelPass, 1, 0)
        layout.addWidget(self.inputPass, 1, 1)
        layout.addWidget(self.labelPageRange, 2, 0)
        layout.addWidget(self.inputPageRange, 2, 1)

        layout.addWidget(self.btnGroup, 3, 1, Qt.AlignLeft)
        layout.addWidget(self.labelCombo, 4, 0)
        layout.addWidget(self.combo, 4, 1)
        layout.addWidget(self.labelExcludeMember, 5, 0)
        layout.addWidget(self.inputExcludeMember, 5, 1)

        layout.addWidget(self.btnExcludeAll, 6, 0, Qt.AlignLeft)
        layout.addWidget(self.btnMember, 6, 1, Qt.AlignLeft)
        layout.addWidget(self.labelMember, 7, 0)
        layout.addWidget(self.browserMember, 7, 1)

        layout.addWidget(self.labelSubject, 8, 0)
        layout.addWidget(self.inputSubject, 8, 1)

        layout.addWidget(self.labelMessage, 9, 0)
        layout.addWidget(self.browserMessage, 9, 1)

        layout.addWidget(self.btnSendMessage, 10, 1)

        layoutMain = QVBoxLayout()
        layoutMain.addLayout(layout)
        layoutMain.addWidget(self.browser)
        widget = QWidget()
        widget.setLayout(layoutMain)

        self.setCentralWidget(widget)
        self.resize(600, 600)
        self.setWindowTitle('LinkedIn Scrapper.')

    def groupChangeEvent(self):
        self.browserMember.clear()

    def btnOkAction(self):
        self.linkedIn = MyLinkedIn(self.inputUser.text(), self.inputPass.text())
        #        self.linkedIn = MyLinkedIn('rabbi.cse.sust.bd@gmail.com', 'ubuntu36')
        self.linkedIn.notifyLinkedIn.connect(self.notifyInfo)
        self.linkedIn.cookieL.connect(self.setSpiderObj)
        self.linkedIn.notifyMember.connect(self.addGroups)
        self.linkedIn.start()

    def sendMessageAction(self):
        messageMembers = []
        members = self.browserMember.toPlainText().split('\n')
        for member in members:
            messageMembers.append((member, self.memberDic[member]))
        self.linkedInMessage = MyLinkedInMessage(self.spiderObj, messageMembers, self.inputSubject.text(),
            self.browserMessage.toPlainText())
        self.linkedInMessage.notifyLinkedIn.connect(self.notifyInfo)
        self.linkedInMessage.start()


    def btnMembersAction(self):
    #        self.linkedInMember = MyLinkedInMembers(self.spiderObj,
    #            self.combo.itemData(self.combo.currentIndex()).toString(), '2-5')
        self.browserMember.clear()
        self.linkedInMember = MyLinkedInMembers(self.spiderObj,
            self.combo.itemData(self.combo.currentIndex()).toString(), self.inputPageRange.text())
        self.linkedInMember.notifyLinkedIn.connect(self.notifyInfo)
        self.linkedInMember.notifyMembers.connect(self.appendMembers)
        self.linkedInMember.start()

    def excludeAllAction(self):
        if self.allMembers is not None and len(self.allMembers) > 0:
            for member in self.allMembers:
                if member[0] not in self.dupCsvRows:
                    self.dupCsvRows.append([member[0], unicode(member[1]), unicode(member[2])])
                    self.csvWriter.writeCsvRow([member[0], unicode(member[1]), unicode(member[2])])
            self.browserMember.clear()
            self.allMembers = None


    def appendMembers(self, members):
        print self.dupCsvRows
        try:
            self.excludedMember = unicode(self.inputExcludeMember.text()).split(',')
        except Exception, x:
            print x
        for member in members:
            if member[0] is None or len(member[0]) == 0 or member[1] is None or len(member[1]) == 0:
                continue
            if member not in self.allMembers:
                print member
                self.allMembers.append(member)
            if self.excludedMember is not None and unicode(member[1]) is not None and len(
                unicode(member[1])) > 0 and unicode(member[1]) in self.excludedMember and member[0] not in self.dupCsvRows:
                self.dupCsvRows.append([member[0], unicode(member[1]), unicode(member[2])])
                self.csvWriter.writeCsvRow([member[0], unicode(member[1]), unicode(member[2])])

            if self.excludedMember is None or (
                unicode(member[1]) not in self.excludedMember and member[0] not in self.dupCsvRows):
                if unicode(member[1]) is not None and len(unicode(member[1])) > 0:
                    self.browserMember.append(member[1])
                    self.memberDic[QString(member[1])] = member[0]

    def addGroups(self, obj):
        for ob in obj:
            self.combo.addItem(ob[0], ob[1])
        print self.combo.itemData(self.combo.currentIndex()).toString()

    def setSpiderObj(self, obj):
        self.spiderObj = obj


    def notifyInfo(self, data):
        self.browser.append(data)


class MainView:
    def __init__(self):
        pass

    def showMainView(self):
        app = QApplication(sys.argv)
        form = Form()
        form.show()
        sys.exit(app.exec_())
