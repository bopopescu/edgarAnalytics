import mysql.connector

def getEdgarDbConnector():
    mydb = mysql.connector.connect(
        host="db-edgar.cso8bj6tym7m.us-east-2.rds.amazonaws.com",
        user="root",
        passwd="integra)",
        database="db-form-d"
    )
    return mydb

def insertFilingMasterInfo(theDbConnection, theFilingInfo):
    myCursor = theDbConnection.cursor()
    sql = ("INSERT INTO filingMasterInfo_ (accessionNumber_, cik_, formType_, dateFiled_, filePath_) "
           "VALUES ('%s', %s, '%s', %s, '%s')" %(theFilingInfo['accessionNumber'], theFilingInfo['CIK'],
                                                 theFilingInfo['FormType'], theFilingInfo['DateFiled'],
                                                 theFilingInfo['FileName']))
    print(sql)
    myCursor.execute(sql)
    theDbConnection.commit()
    print(myCursor.rowcount, " record inserted")
    return myCursor.rowcount


