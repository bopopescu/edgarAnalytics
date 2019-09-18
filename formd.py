from lxml import html
from lxml import etree
import requests
import edgarDb

class formD():

    def __init__(self, url=""):
        self.url = url
        self.page = None

    def getUrlFromMaster(self, theFormDMasterRecord):
        self.url = "https://www.sec.gov/Archives/" + theFormDMasterRecord['FileName']

    def getFormD(self):
        print("Getting the page...")
        return requests.get(self.url)

    def setFormDBasicInfo(self, thePage):
        tree = etree.fromstring(thePage.content)
        basicInfoElement = tree.find("primaryIssuer")

        yearOfIncorporationOverFive = basicInfoElement.find("yearOfInc").find("overFiveYears")
        yearOfIncorporationWithinFive = basicInfoElement.find("yearOfInc").find("withinFiveYears")
        yearOfIncorporationYetFormed = basicInfoElement.find("yearOfInc").find("yetFormed")
        yearOfIncorporationValue = basicInfoElement.find("yearOfInc").find("value")

        formDBasicInfo = dict(issuerName_=basicInfoElement.find("entityName").text,
                              jurisdiction_=basicInfoElement.find("jurisdictionOfInc").text,
                              yearOfIncorporationOverFive_="" if yearOfIncorporationOverFive is None
                              else yearOfIncorporationOverFive.text,
                              yearOfIncorporationWithinFive="" if yearOfIncorporationWithinFive is None
                              else yearOfIncorporationWithinFive.text,
                              yearOfIncorporationYetFormed="" if yearOfIncorporationYetFormed is None
                              else yearOfIncorporationYetFormed.text,
                              yearOfIncorporationValue="" if yearOfIncorporationValue is None
                              else yearOfIncorporationValue.text,
                              ppbStreetAddress1=basicInfoElement.find("issuerAddress").find("street1").text,
                              ppbStreetAddress2=basicInfoElement.find("issuerAddress").find("street2").text,
                              ppbCity=basicInfoElement.find("issuerAddress").find("city").text,
                              ppbStateOrCountry=basicInfoElement.find("issuerAddress").find("stateOrCountry").text,
                              ppbStateOrCountryDesc=basicInfoElement.find("issuerAddress").find("stateOrCountryDescription").text,
                              ppbZip=basicInfoElement.find("issuerAddress").find("zipCode").text,
                              ppbPhone=basicInfoElement.find("issuerPhoneNumber").text
                              )
        return formDBasicInfo

    def setFormDRelatedPersons(self, thePage):
        tree = etree.fromstring(thePage.content)
        relatedPersonsElement = tree.find("relatedPersonsList")

        relatedPersons = list()
        for person in relatedPersonsElement.findall("relatedPersonInfo"):

            relatedPersonDict = dict(firstName_=person.find("relatedPersonName").find("firstName").text,
                                     lastName_=person.find("relatedPersonName").find("lastName").text,
                                     addressStreet_=person.find("relatedPersonAddress").find("street1").text,
                                     addressCity_=person.find("relatedPersonAddress").find("city").text,
                                     addressStateOrCountry_=person.find("relatedPersonAddress").find("stateOrCountry").text,
                                     addressStateOrCountryDescription_=person.find("relatedPersonAddress")
                                     .find("stateOrCountryDescription").text,
                                     addressZip_=person.find("relatedPersonAddress").find("zipCode").text,
                                     relatedPersonRelationship_=person.find("relatedPersonRelationshipList")
                                     .find("relationship").text
                                     )
            relatedPersons.append(relatedPersonDict)
        return relatedPersons


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










