from lxml import html
from lxml import etree
import xmlUtil
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

        formDBasicInfo = dict(cik_=basicInfoElement.find("cik").text,
                              entityName_=basicInfoElement.find("entityName").text,
                              jurisdictionOfInc_=basicInfoElement.find("jurisdictionOfInc").text,
                              issuerPreviousNameListValue_=basicInfoElement.find("issuerPreviousNameList").
                              find("value"),
                              previousName_=basicInfoElement.find("edgarPreviousNameList").find("previousName"),
                              overFiveYears_="" if yearOfIncorporationOverFive is None
                              else yearOfIncorporationOverFive.text,
                              withinFiveYears_="" if yearOfIncorporationWithinFive is None
                              else yearOfIncorporationWithinFive.text,
                              yetFormed_="" if yearOfIncorporationYetFormed is None
                              else yearOfIncorporationYetFormed.text,
                              entityType_=basicInfoElement.find("entityType").text,
                              yearOfIncValue_="" if yearOfIncorporationValue is None
                              else yearOfIncorporationValue.text,
                              street1_=basicInfoElement.find("issuerAddress").find("street1").text,
                              street2_=basicInfoElement.find("issuerAddress").find("street2").text,
                              city_=basicInfoElement.find("issuerAddress").find("city").text,
                              stateOrCountry_=basicInfoElement.find("issuerAddress").find("stateOrCountry").text,
                              stateOrCountryDescription_=basicInfoElement.find("issuerAddress").find("stateOrCountryDescription").text,
                              zipCode_=basicInfoElement.find("issuerAddress").find("zipCode").text,
                              issuerPhoneNumber_=basicInfoElement.find("issuerPhoneNumber").text
                              )
        return formDBasicInfo

    def setFormDRelatedPersons(self, thePage):
        tree = etree.fromstring(thePage.content)
        relatedPersonsElement = tree.find("relatedPersonsList")

        relatedPersons = list()
        for person in relatedPersonsElement.findall("relatedPersonInfo"):

            relatedPersonDict = dict(firstName_=person.find("relatedPersonName").find("firstName").text,
                                     lastName_=person.find("relatedPersonName").find("lastName").text,
                                     street1_=person.find("relatedPersonAddress").find("street1").text,
                                     city_=person.find("relatedPersonAddress").find("city").text,
                                     stateOrCountry_=person.find("relatedPersonAddress").find("stateOrCountry").text,
                                     stateOrCountryDescription_=person.find("relatedPersonAddress")
                                     .find("stateOrCountryDescription").text,
                                     zipCode_=person.find("relatedPersonAddress").find("zipCode").text,
                                     relationship_=person.find("relatedPersonRelationshipList")
                                     .find("relationship").text
                                     )
            relatedPersons.append(relatedPersonDict)
        return relatedPersons

    def setSalesCompensationList(self, theSalesCompensationListElement):
        compensationRecipients = list()
        for recipient in theSalesCompensationListElement.findall("recipient"):
            salesCompRecipientData = dict(
                recipientName_=recipient.find("recipientName").text,
                recipientCrdNumber_=recipient.find("recipientCRDNumber").text,
                associatedBDName_=recipient.find("associatedBDName").text,
                associatedBDCRDNumber_=recipient.find("associatedBDCRDNumber").text,
                recipientAddressStreet1=recipient.find("recipientAddress").find("street1").text,
                recipientAddressStreet2=recipient.find("recipientAddress").find("street2").text,
                recipientAddressCity=recipient.find("recipientAddress").find("city").text,
                recipientAddressStateOrCountry=recipient.find("recipientAddress").find("stateOrCountry").text,
                recipientAddressStateOrCountryDescription=recipient.find("recipientAddress").
                    find("stateOrCountryDescription").text,
                recipientAddressZip=recipient.find("recipientAddress").find("zipCode").text,

            )
            compensationRecipients.append(salesCompRecipientData)
        print compensationRecipients
        return compensationRecipients

    def setFormDOfferingData(self, thePage):
        tree = etree.fromstring(thePage.content)
        offeringDataElement = tree.find("offeringData")

        compensationRecipients = offeringDataElement.find("salesCompensationList")
        mySalesCompRecipients = self.setSalesCompensationList(compensationRecipients)

        formDOfferingInfo = dict(industryGroupType_=offeringDataElement.find("industryGroup").
                                 find("industryGroupType").text,
                                 revenueRange_=offeringDataElement.find("issuerSize").find("revenueRange").text,
                                 federalExemptionsExclusionsItem_=offeringDataElement.
                                 find("federalExemptionsExclusions").find("item").text,
                                 isAmendment_=offeringDataElement.find("typeOfFiling").
                                 find("newOrAmendment").find("isAmendment").text,
                                 dateOfFirstSaleValue_=offeringDataElement.find("typeOfFiling").
                                 find("dateOfFirstSale").find("value").text,
                                 moreThanOneYear_=offeringDataElement.find("durationOfOffering").
                                 find("moreThanOneYear").text,
                                 isEquityType_=offeringDataElement.find("typesOfSecuritiesOffered").
                                 find("isEquityType").text,
                                 isBusinessCombinationTransaction_=offeringDataElement.
                                 find("businessCombinationTransaction").
                                 find("isBusinessCombinationTransaction").text,
                                 minimumInvestmentAccepted_=offeringDataElement.find("minimumInvestmentAccepted").text,
                                 salesCompRecipients=mySalesCompRecipients,
                                 totalOfferingAmount_=offeringDataElement.find("offeringSalesAmounts").
                                 find("totalOfferingAmount").text,
                                 totalAmountSold_=offeringDataElement.find("offeringSalesAmounts").
                                 find("totalAmountSold").text,
                                 totalRemaining_=offeringDataElement.find("offeringSalesAmounts").
                                 find("totalRemaining").text,
                                 hasNonAccreditedInvestors_=offeringDataElement.find("investors").
                                 find("hasNonAccreditedInvestors").text,
                                 totalNumberAlreadyInvested_=offeringDataElement.find("investors").
                                 find("totalNumberAlreadyInvested").text,
                                 salesCommissionsDollaramount_=offeringDataElement.find("salesCommissionsFindersFees").
                                 find("salesCommissions").find("dollarAmount").text,
                                 isEstimate_=offeringDataElement.find("salesCommissionsFindersFees").
                                 find("salesCommissions").find("isEstimate").text,
                                 findersFeesDollaramount_=offeringDataElement.find("salesCommissionsFindersFees").
                                 find("findersFees").find("dollarAmount").text,
                                 grossProceedsUsedDollaramount_=offeringDataElement.find("useOfProceeds").
                                 find("grossProceedsUsed").find("dollarAmount").text,
                                 authorizedRepresentative_=offeringDataElement.find("signatureBlock").
                                 find("authorizedRepresentative").text,
                                 issuerName_=offeringDataElement.find("signatureBlock").
                                 find("signature").find("issuerName").text,
                                 signatureName_=offeringDataElement.find("signatureBlock").
                                 find("signature").find("signatureName").text,
                                 nameOfSigner_=offeringDataElement.find("signatureBlock").
                                 find("signature").find("nameOfSigner").text,
                                 signatureTitle_=offeringDataElement.find("signatureBlock").
                                 find("signature").find("signatureTitle").text,
                                 signatureDate_=offeringDataElement.find("signatureBlock").
                                 find("signature").find("signatureDate").text,
                                 )
        return formDOfferingInfo

    def checkFormDFullComparison(self, thePage):
        combinedTagList = ["item", "value", "dollarAmount"]
        ignoreTagList = ["clarificationOfResponse"]

        #First check for missing basic info
        tree = etree.fromstring(thePage.content)
        basicInfoElement = tree.find("primaryIssuer")
        elementTags = xmlUtil.getDeepestTagList(basicInfoElement, combinedTagList, ignoreTagList)

        theBasicInfo = self.setFormDBasicInfo(thePage)

        missingTags = False
        for item in elementTags:
            if item not in theBasicInfo.keys():
                print "Missing Item: " + item
                missingTags = True
        if not missingTags:
            print("No missing basic info tags!!!")

        #Next check for missing related persons
        missingTags = False
        relatedPersonsElement = tree.find("relatedPersonsList")
        uniqueElementTags = list(set(xmlUtil.getDeepestTagList(relatedPersonsElement, combinedTagList, ignoreTagList)))
        theRelatedPersonsInfo = self.setFormDRelatedPersons(thePage)
        for person in theRelatedPersonsInfo:
            for item in uniqueElementTags:
                if item not in person.keys():
                    print "Missing Item: " + item
                    missingTags = True
        if not missingTags:
            print("No missing related persons info")

        missingTags = False
        offeringDataElement = tree.find("offeringData")
        theTagList = list()
        uniqueElementTags = xmlUtil.getDeepestTagListManually(offeringDataElement, theTagList,
                                                              combinedTagList, ignoreTagList,
                                                              ["salesCompensationList"])
        theOfferingDataInfo = self.setFormDOfferingData(thePage)
        for item in uniqueElementTags:
            if item not in theOfferingDataInfo.keys():
                print("Missing item: " + item)
                missingTags = True
        if not missingTags:
            print("No missing offering data info!!")

        return theOfferingDataInfo


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










