import edgarDb
import formd

def testInsertFormD():
    dailyIndex = formd.dailyIndex("QTR2", "20190401")
    filteredUrls = dailyIndex.getCikFilteredUrls(['1771428'])[0]
    formD = formd.formD()
    formD.getUrlFromMaster(filteredUrls)
    print("URL is: " + formD.url)
    assert formD.url == "https://www.sec.gov/Archives/edgar/data/1771428/000161577419005115/primary_doc.xml", (
        "Should be 'https://www.sec.gov/Archives/edgar/data/1771428/000161577419005115/primary_doc.xml'")
    formD.insertFormDRecord(filteredUrls)

def testGetFormDPage():
    dailyIndex = formd.dailyIndex("QTR2", "20190401")
    filteredUrls = dailyIndex.getCikFilteredUrls(['1771428'])[0]
    formD = formd.formD()
    formD.getUrlFromMaster(filteredUrls)
    print("URL: " + formD.url)
    thePage = formD.getFormD()
    assert thePage.status_code == 200, "Should be 200"
    return formD.setFormDBasicInfo(thePage)

def testGetFormDPageRelatedPersons():
    dailyIndex = formd.dailyIndex("QTR2", "20190401")
    filteredUrls = dailyIndex.getCikFilteredUrls(['1771428'])[0]
    formD = formd.formD()
    formD.getUrlFromMaster(filteredUrls)
    print("URL: " + formD.url)
    thePage = formD.getFormD()
    assert thePage.status_code == 200, "Should be 200"
    return formD.setFormDRelatedPersons(thePage)
