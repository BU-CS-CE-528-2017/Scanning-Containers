from pymongo import MongoClient
from argparse import ArgumentParser
import os.path
from bs4 import BeautifulSoup
import numpy as np
from pprint import pprint
import datetime
import uuid


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # return an open file handle


# Argument parser to specify SCAP result file path

parser = ArgumentParser(description="arg parse")

parser.add_argument("-s", dest="source", required=True,
                    help="Source file of scap content (Required)", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))

parser.add_argument("-d", dest="dest", required=False,
                    help="Destination file for JSON (Optional)", metavar="FILE")

parser.add_argument("-u", dest="user", required=False,
                    help="Username to associate results file with (Required)")

parser.add_argument("-db", dest="db", required=False,
                    help="Name of database (optional)")

parser.add_argument("-type", dest="type", required=False,
                    help="Type of scan (xccdf or oval) (optional)")
args = parser.parse_args()


contentPath = ""
filePath = contentPath + args.source
user = args.user
scanid = np.random.randint(0, 500000000)

html_string = open(filePath, 'r').read()


cl = MongoClient()
# CL
coll = cl["scans"][user]
# CL <-| users <-| user

# CL <-| users <-| user


soup = BeautifulSoup(html_string, 'lxml')
topTable = soup.find_all('table', { "border" : "1" })[3]
resultTable = topTable.find_next_siblings('table')[0]
#print(topTable)
#print(resultTable)

i=0
#number of lines to search
lines = 10

# add a unique identifier for each scan

scanid = str(uuid.uuid4())

#find only applicable lines
for row in resultTable.find_all('tr',{"class":
        ["resultbadA","resultbadB","resultgoodA",
         "resultgoodB","errorA","errorB","unknownA",
         "unknownB","otherA","otherB"]}):
    rawHtml = str(row)
    rowArray = row.find_all('td')
    resID = rowArray[0].getText()
    resultTF = rowArray[1].getText()
    resultClass = rowArray[2].getText()
    referenceID = rowArray[3].getText()
    referenceLink = rowArray[3].find('a')['href']
    now = datetime.datetime.now()
    year  =int(now.year)
    month  =int(now.month)
    day  =int(now.day)
    hour  =int(now.hour)
    minute  =int(now.minute)
    second  =int(now.second)

    # format datetime
    
    coll.insert(
        {
            "scanid" : scanid,
            "timestamp":
                {
                    "year": year ,
                    "month": month ,
                    "day": day ,
                    "hour": hour ,
                    "minute": minute ,
                    "second": second
                },

             "rawHtml": rawHtml,
             "id": resID,
             "result": resultTF,
             "Class": resultClass,
             "Reference ID": referenceID,
             "Reference Link": referenceLink
        }


    )

    i += 1
    if i>=lines:
        break



cursor = coll.find({})


'''
Here's the basic schema for data in the db

{ "_id" : ObjectId("58d98c8e0218239a229b35d8"),
 "Class" : "vulnerability",
 "rawHtml" : "<tr class=\"resultbadB\">
    \n<td align=\"center\" class=\"Text\">
    oval:com.ubuntu.xenial:def:20176831000</td>
    \n<td align=\"center\" class=\"Text\">
    true</td>
    \n<td align=\"center\" class=\"Text\">
    vulnerability</td>
    \n<td align=\"center\" class=\"Text\">
    [<a class=\"Hover\" href=\"https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-6831\" target=\"_blank\">
    CVE-2017-6831</a>
    ]</td>
    \n<td class=\"Text\">
    CVE-2017-6831 on Ubuntu 16.04 LTS (xenial) - medium.</td>
    \n</tr>",
 "Reference Link" : "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-6831",
 "Reference ID" : "[CVE-2017-6831]",
 "id" : "oval:com.ubuntu.xenial:def:20176831000",
 "result" : "true",
 "timestamp" : { "month" : 3,
 "hour" : 18,
 "second" : 2,
 "day" : 27,
 "minute" : 5,
 "year" : 2017 },
 "scanid" : "e68f226e-b56a-45f7-8b3b-24c75f6146fc" }






'''





