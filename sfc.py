import scapToMongo
from pymongo import MongoClient
import datetime
import subprocess
import time
import pprint
import sys


cl = MongoClient()
collUsers = cl["scans"]["users"]

def scan(user,container,type="oval",db="scans",destination=""):
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


    if type not in ["xccdf","oval"]:
        raise ValueError

    if collUsers.find({"username":user}).count() < 1:
        print("Creating new user: ",user)
        createUser(user)

    #'''

    print("User entries: ",coll.count())
    if coll.count() > 20000:
        print("Too many entries for user. Attemping to cleanup...")
        cleanupUser(user)
        for i in range(24,0,-1):
            print("User entries: ", coll.count())
            print("Too many entries for user. Deleting entries older than ", i," hours")
            cleanupUser(user,age=i)

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
        '''
        subprocess.call(
            "oscap-docker xccdf eval " +
            "--profile xccdf_org.ssgproject.content_profile_common "+
            "--report " + destination +
            "ssg-ubuntu1604-ds.xml")
        #'''
        html = scapToMongo.xccdf(destination,user)

    elif type == "oval":
        # Record
        if len(coll.distinct("scanid")) > 5:
            cleanupUser(user)
            if len(coll.distinct("scanid")) > 5:
                print("User quota exceeded: no more OVAL scans allowed")


        '''
        subprocess.call(
            "oscap-docker oval eval " +
            "--profile xccdf_org.ssgproject.content_profile_common "+
            "--report " + destination +
            "ssg-ubuntu1604-ds.xml")
        #'''
        html = scapToMongo.oval(destination,user)
    else:
        print("ERROR")
        sys.exit(1)
    '''
    To here
    '''
    #pprint.pprint(html)
    print("Done")
    return html


def createUser(user,db="scans"):
    '''

    :param user: username
    :param db: name of database (optional)
    :return:
    '''
    coll = cl[db][user]
    coll.insert({"init":"init"})

    collUsers.update(
        {"username": user},
        {"username": user, "attributes": "None"}
        #,
        # TODO:
        #{"$upsert":"True"}
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

def cleanupUser(user,db="scans",age=24,all=False):
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

    timeCutoff = datetime.datetime.now() - datetime.timedelta(hours=age)
    print(timeCutoff)

    print(coll.remove({
        "timestamp": {"$lt": timeCutoff}}
    )
    )




'''
scapToMongo.xccdf("report1.html","ben")

scapToMongo.oval("report.html","ben")

'''