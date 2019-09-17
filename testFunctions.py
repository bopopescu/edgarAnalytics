import edgarDb
import formd

def testInsertFormD():
    dailyIndex = formd.dailyIndex("QTR2", "20190401")
    filteredUrls = dailyIndex.getCikFilteredUrls(['1771428'])[0]
    formD = formd.formD("dkljflkdj")
    formD.insertFormDRecord(filteredUrls)
