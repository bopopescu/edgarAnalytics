from lxml import html
import requests
import edgarDb

class formD():

    def __init__(self, url):
        self.url = url


    def getFormD(self):
        page = requests.get(self.url)
        return page

    def insertFormDRecord(self, theFormDMasterRecord):

        myDbConnector = edgarDb.getEdgarDbConnector()
        edgarDb.insertFilingMasterInfo(myDbConnector, theFormDMasterRecord)


class dailyIndex():

    def __init__(self, indexQuarter, indexDate):
        self.indexQuarter = indexQuarter
        self.indexDate = indexDate
        self.getDailyIndexFile()
        self.getFormUrls()

    def getDailyIndexFile(self):
        indexFileUrl = "https://www.sec.gov/Archives/edgar/daily-index/2019/" + self.indexQuarter + "/master." + self.indexDate + ".idx"
        page = requests.get(indexFileUrl)
        self.indexFile = page

    def getFormUrls(self):
        files = list()
        formsStarted = False
        splitLine = self.indexFile.content.split('\n')
        for line in splitLine:
            if formsStarted and line != "":
                splitValues = line.split("|")
                accessionNumber = splitValues[4].split("/")[-1].split(".")[0]
                editedFileName = splitValues[4].replace('-', '').replace('.txt', '/primary_doc.xml')
                formDict = {'accessionNumber': accessionNumber, 'CIK': splitValues[0], 'CompanyName': splitValues[1], 'FormType': splitValues[2], 'DateFiled': splitValues[3], 'FileName': editedFileName}
                files.append(formDict)
            if line.startswith("-----"):
                formsStarted = True
        self.fileList = files

    def getFormFilteredUrls(self, keys):
        keys = keys
        filteredList = list()
        for item in self.fileList:
            if item.get('FormType') in keys:
                filteredList.append(item)
        return filteredList

    def getCikFilteredUrls(self, keys):
        keys = keys
        filteredList = list()
        for item in self.fileList:
            if item.get('CIK') in keys:
                filteredList.append(item)
        return filteredList










