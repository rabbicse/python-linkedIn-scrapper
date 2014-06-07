__author__ = 'Rabbi'

import re

class Regex:
    def __init__(self):
        pass

    def reduceNewLine(self, data):
        data = re.sub('(?i)\n+', ' ', data)
        return data

    def reduceBlankSpace(self, data):
        data = re.sub('(?i)\s+', ' ', data)
        return data

    def reduceNbsp(self, data):
        data = re.sub('(?i)&nbsp;', '', data)
        return data

    def getAllSearchedData(self, pattern, data):
        return re.findall(pattern, data)

    def getSearchedData(self, pattern, data):
        searchedData = re.search(pattern, data)
        if searchedData:
            return searchedData.group(1)
        return ''

    def getSearchedDataGroups(self, pattern, data):
        return re.search(pattern, data)

    def isFoundPattern(self, pattern, data):
        matchedData = re.search(pattern, data)
        if matchedData:
            return True
        return False

    def replaceData(self, pattern, replace, data):
        return re.sub(pattern, replace, data)


