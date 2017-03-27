from pymongo import MongoClient
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
import os.path
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from pprint import pprint

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

args = parser.parse_args()


contentPath = ""
filePath = contentPath + args.source
user = args.user
scanid = np.random.randint(0, 500000000)

html_string = open(filePath, 'r').read()


cl = MongoClient()
coll = cl["ovalScans"][user]

soup = BeautifulSoup(html_string, 'lxml')
topTable = soup.find_all('table', { "border" : "1" })[3]
resultTable = topTable.find_next_siblings('table')[0]
#print(topTable)
#print(resultTable)

i=0
#number of lines to search
lines = 100




#find only applicable lines
for row in resultTable.find_all('tr',{"class":["resultbadA","resultbadB"]}):

    rawHtml = str(row)
    #print(rawHtml)

    #print(row.find_all('td'))
    rowArray = row.find_all('td')
    #print(rowArray)

    resID = rowArray[0].getText()
    resultTF = rowArray[1].getText()
    resultClass = rowArray[2].getText()
    referenceID = rowArray[3].getText()
    referenceLink = rowArray[3].find('a')['href']

    coll.update(
        {"username": user},
        {'$set':
                {"username": user,
                 "scans":
                     {
                         "_id": ObjectId(),
                         "timestamp": "12:00:00",
                         "rawHtml": "<html>blah blah</html>",
                         "results":
                             {
                                 "id": resID,
                                 "result": resultTF,
                                 "Class": resultClass,
                                 "Reference ID": referenceID,
                                 "Reference Link": referenceLink
                             }
                     }
                 }


    }
    )


    #'''
    i += 1
    print()
    if i>=lines:
        break
    #'''


cursor = coll.find({})
for document in cursor:
    pprint(document)

'''
Here's the basic schema for data in the db

{
     "username": "user123",
     "attributes": "one,two,three",
     "scans":
     {
         "scanid":"id123",
         "timestamp": "12:00:00",
         "rawHtml": "<html>blah blah</html>",
         "results":
         {
            "id" : "oval:com.ubuntu.xenial:def:20176952000",
            "result" : "true",
            "Class":"vulnerability",
            "Reference ID": "[CVE-2017-6952]"
            "Reference Link": "http://efefwguehf2.com/fuef"
            "Title" : "CVE-2017-6952 on Ubuntu 16.04 LTS (xenial) - medium."
        },
        {
            "id" : "oval:com.ubuntu.xenial:def:20176952000",
            "result" : "true",
            "Class":"vulnerability",
            "Reference ID": "[CVE-2017-6952]",
            "Reference Link": "http://efefwguehf2.com/fuef",
            "Title" : "CVE-2017-6952 on Ubuntu 16.04 LTS (xenial) - medium."
        }
     },
     {
         "scanid":"id123",
         "timestamp": "12:00:00",
         "rawHtml": "<html>blah blah</html>,
         "results":
         {
            "id" : "oval:com.ubuntu.xenial:def:20176952000",
            "result" : "true",
            "Class":"vulnerability",
            "Reference ID": "[CVE-2017-6952]"
            "Reference Link": "http://efefwguehf2.com/fuef"
            "Title" : "CVE-2017-6952 on Ubuntu 16.04 LTS (xenial) - medium."
        },
        {
            "id" : "oval:com.ubuntu.xenial:def:20176952000",
            "result" : "true",
            "Class":"vulnerability",
            "Reference ID": "[CVE-2017-6952]"
            "Reference Link": "http://efefwguehf2.com/fuef"
            "Title" : "CVE-2017-6952 on Ubuntu 16.04 LTS (xenial) - medium."
        }
     }
}






'''





