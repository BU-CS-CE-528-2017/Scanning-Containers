from pymongo import MongoClient
from argparse import ArgumentParser
import os.path
from bs4 import BeautifulSoup
from pprint import pprint
import datetime
import uuid
import os
import json

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # return an open file handle


# Argument parser

'''
parser = ArgumentParser(description="arg parse")

parser.add_argument("-s", dest="source", required=True,
                    help="Source file of scap content (Required)", metavar="FILE",
                    type=lambda arg: is_valid_file(parser, arg))
parser.add_argument("-type", dest="type", required=True,
                    help="Type of scan (xccdf or oval) (Required)", metavar="TYPE",
                    #type=lambda arg: is_valid_type(parser,arg)
                    )
parser.add_argument("-d", dest="dest", required=False,
                    help="Destination file for JSON (Optional)", metavar="FILE")
parser.add_argument("-u", dest="user", required=False,
                    help="Username to associate results file with (Required)")
parser.add_argument("-db", dest="db", required=False,
                    help="Name of database (optional)")

args = parser.parse_args()

contentPath = ""
filePath = contentPath + args.source
user = args.user

html_string = open(filePath,'r').read()

scanid = str(uuid.uuid4())




cl = MongoClient()
coll = cl["scans"][user]
#'''


# get timestamp info
now = datetime.datetime.now()
year = int(now.year)
month = int(now.month)
day = int(now.day)
hour = int(now.hour)
minute = int(now.minute)
second = int(now.second)



i=0
# max number of lines to search (basically a failsafe against attacks)
lines = 10000

def xccdf(source, user, db="scans"):

    contentPath = ""
    filePath = contentPath + source
    user = user

    html_string = open(filePath, 'r').read()
    scanid = str(uuid.uuid4())

    cl = MongoClient()
    coll = cl[db][user]

    soup = BeautifulSoup(html_string, 'lxml')

    # store the raw html immediately

    storeHtml(coll, scanid, now, html_string,"xccdf")
    resultTable = soup.find_all("table", {"class":"treetable"})[0]

    i=0
    # find only applicable lines
    data = {}
    bulk = coll.initialize_unordered_bulk_op();

    for row in resultTable.find_all('tr', {"class": "rule-overview-leaf"}):


        rawHtml = str(row)
        rowArray = row.find_all('td')
        resName = rowArray[0].getText()
        resSeverity = rowArray[1].getText()
        resultTF = rowArray[2].getText()
        referenceLink = "none"
        bulk.insert(
            {
                "scanid": scanid,
                "timestamp": now,
                "rawHtml": str(row),
                "resName": resName,
                "resSeverity": resSeverity,
                "type": "compliance",
                "resultTF": resultTF,
                "referenceLink": referenceLink
            }
        )
        i += 1
        if i >= lines:
            break
    bulk.execute();
    return html_string,scanid

def oval(source, user, db="scans"):

    contentPath = ""
    filePath = contentPath + source
    user = user

    html_string = open(filePath, 'r').read()
    scanid = str(uuid.uuid4())

    cl = MongoClient()
    coll = cl[db][user]

    soup = BeautifulSoup(html_string, 'lxml')

    # store the raw html immediately
    storeHtml(coll, scanid, now, html_string,"oval")
    topTable = soup.find_all('table', { "border" : "1" })[3]
    resultTable = topTable.find_next_siblings('table')[0]
    i = 0
    #find only applicable lines

    bulk = coll.initialize_unordered_bulk_op();

    for row in resultTable.find_all('tr',
                {"class":
                    ["resultbadA",
                     "resultbadB",
                     "resultgoodA",
                     "resultgoodB",
                     "errorA",
                     "errorB",
                     "unknownA",
                     "unknownB",
                     "otherA",
                     "otherB"]}):
        rawHtml = str(row)
        rowArray = row.find_all('td')
        resID = rowArray[0].getText()
        resultTF = rowArray[1].getText()
        resultClass = rowArray[2].getText()
        referenceID = rowArray[3].getText()
        print(resID)
        try:
            referenceLink = rowArray[2].find('a')['href']
        except:
            referenceLink = "none"


        # format datetime

        coll.insert(
            {
                "scanid" : scanid,
                "timestamp": now,
                "rawHtml": rawHtml,
                "id": resID,
                "result": resultTF,
                "type": "vulnerability",
                "Reference ID": referenceID,
                "Reference Link": referenceLink
            }
        )

        i += 1
        if i>=lines:
            break

    bulk.execute();
    return html_string,scanid

# add the entire scan's html as just a raw string
# this is found using:
#   db.user.find({"scanid":"xxxx-xxxx-xxxx-html"})

def storeHtml(coll,scanid,now,html_string,type):
    coll.insert(
        {
            "scanid": scanid + "-html",
            "type":type,
            "timestamp":
                {
                    "time": now
                },
            "html": html_string
        }

)








