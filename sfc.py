import scapToMongo
from pymongo import MongoClient
import datetime
import subprocess
import time
import pprint
import sys
import smtplib
from email.mime.text import MIMEText


cl = MongoClient()
collUsers = cl["scans"]["users"]



def scan(user,container,type="oval",db="scans",destination="",note=False):
    '''
    Main function for performing a scan
    :param user: username
    :param container: name of container
    :param type: oval or xccdf
    :param db: name of database (optional)
    :param destination: name of report file to save to
    :return: html (string) the raw html of the report
    '''

    db = str(db)
    coll = cl[db][user]

    type = type.lower()
    if type not in ["xccdf","oval"]:
        print("invalid param: type")
        sys.exit(1)

    if collUsers.find({"username":user}).count() < 1:

        createUser(user)

    #'''


    #'''
    '''
    TODO:

        We need to check for the os / version of the container



    '''


    # Create report filename
    #
    if destination == "":
        if type == "oval":
            destination = "report.html"
        elif type == "xccdf":
            destination = "report1.html"
    else:
        destination = "report-" + str(user) + str(container) + str(time.time())

    '''
    TODO:
    Fix everything here...
    '''

    if type == "xccdf":
        if len(coll.distinct("scanid",{"type":"compliance"})) > 20:
            cleanupUser(user)
            if len(coll.distinct("scanid")) > 20:
                print("User quota exceeded: no more XCCDF scans allowed")
                print("User cleanupUser(user,age=?) to clear entries")
                sys.exit(1)

        '''
        subprocess.call(
            "oscap-docker xccdf eval " +
            "--profile xccdf_org.ssgproject.content_profile_common "+
            "--report " + destination +
            "ssg-ubuntu1604-ds.xml")
        #'''
        html,scanid = scapToMongo.xccdf(destination,user)

    elif type == "oval":
        # Record
        if len(coll.distinct("scanid",{"type":"vulnerability"})) > 5:
            cleanupUser(user)
            if len(coll.distinct("scanid")) > 5:
                print("User quota exceeded: no more OVAL scans allowed")
                print("User cleanupUser(user,age=?) to clear entries")

        '''
        subprocess.call(
            "oscap-docker oval eval " +
            "--profile xccdf_org.ssgproject.content_profile_common "+
            "--report " + destination +
            "ssg-ubuntu1604-ds.xml")
        #'''
        html,scanid = scapToMongo.oval(destination,user)
    else:
        print("ERROR")
        sys.exit(1)
    '''
    To here
    '''
    # associate the scanid with the user in

    collUsers.update({"username":user},
                     {"$push":{"scans":scanid}}
                     )

    #pprint.pprint(html)
    sendNotification(user,html)
    print("Done")
    return html


def createUser(user,db="scans"):
    '''

    :param user: username
    :param db: name of database (optional)
    :return:
    '''
    print("Creating new user: ", user)
    coll = cl[db][user]
    coll.insert({"init":"init"})

    collUsers.insert(
        {"username": user,
        "scans":[],
        "email":"bsowens@bu.edu"}
        )

def removeUser(user,db="scans"):
    '''

    :param user: username
    :param db: name of database (optional)
    :return:
    '''
    coll = cl[db][user]
    coll.drop()

    collUsers.remove(
        {"username":user}
    )

    print("User: ", user, " is dead")

def cleanupUser(user,db="scans",age=24,type=["xccdf","oval"],all=False):
    '''
    :param user: username
    :param db: name of database (optional)
    :param age: deletes entries older than this number (hours) (optional)
    :param all: override to delete all entries
    :return:
    '''
    coll = cl[db][user]

    if all == True:
        coll.remove({})
    print("Attemping autocleaup")
    timeCutoff = datetime.datetime.now() - datetime.timedelta(hours=age)


    coll.remove({
        "timestamp": {"$lt": timeCutoff}}
    )

def getVersion(user,container)

def sendNotification(user,html,email=""):

    sender = 'no-reply@email.com'
    receivers = ['bsowens@bu.edu']
    subject = "Report"

    message = "From: " + sender +\
    "To: " + receivers[0] +\
    "Subject: " + subject + "\n\n"

    "Here is your report \n" + html

    message.encode('utf-8').strip()
    pprint.pprint(message)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")



'''
scapToMongo.xccdf("report1.html","ben")

scapToMongo.oval("report.html","ben")

'''