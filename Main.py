from views.MainView import MainView
from works.MyLinkedIn import MyLinkedIn

__author__ = 'Rabbi'

#def opLinkedIn():
#    linkedIn = LinkedInApi()
#    linkedIn.linkedInOp()

def opMyLinkedIn():
    linkedIn = MyLinkedIn('rabbi.cse.sust.bd@gmail.com', 'ubuntu36')
    linkedIn.login()

#    linkedIn.logout()


if __name__ == "__main__":
#    opMyLinkedIn()
    #    opLinkedIn()
    mainView = MainView()
    mainView.showMainView()