import scapToMongo
from pymongo import MongoClient
import datetime
import subprocess

cl = MongoClient()
collUsers = cl["scans"]["users"]

def scan(user,container,type,db="scans"):
    coll = cl[db][user]

    if type != "xccdf" or type == "oval":
        raise ValueError

    if user not in collUsers.find({"username":user}, {"_id" : 1}):
        print("Creating new user: ",user)
        createUser(user)

    if coll.count() > 10000:
        print("Too many entries for user. Attemping to cleanup...")
        cleanupUser(user)
        if coll.count() > 10000:
            print("User has too many entries")
            raise "poop"

    '''
    TODO:

        We need to check for the os / version of the container



    '''


    # Create report filename
    destination = "report-" + str(user) + str(container) + str(datetime.datetime.timestamp())


    #

    destination = "report.html"

    '''
    TODO:

    Fix everything here...


    '''

    if type == "xccdf":
        subprocess.call(
            "oscap xccdf eval " +
            "--profile xccdf_org.ssgproject.content_profile_common "+
            "--report " + destination +
            "ssg-ubuntu1604-ds.xml")

        html = scapToMongo.xccdf(destination,user)
    elif type == "oval":
        subprocess.call(
            "oscap oval eval " +
            "--profile xccdf_org.ssgproject.content_profile_common "+
            "--report " + destination +
            "ssg-ubuntu1604-ds.xml")

        html = scapToMongo.oval(destination,user)

    '''
    To here
    '''

    else:
        raise ValueError

    return html


def createUser(user,db="scans"):
    coll = cl[db][user]
    coll.insert({"init":"init"})

    collUsers.insert({"username": user, "attributes": "None"})
    if user not in collUsers.find({"username":user}, {"_id" : 1}):
        print("ERROR: User not created: ", user)

def removeUser(user,db="scans"):
    coll = cl[db][user]
    coll.drop()

    collUsers.remove({"username":user})

    print("User: ", user, " is dead")

def cleanupUser(user,db="scans",age=24):

    coll = cl[db][user]
    print(coll)
    timeCutoff = datetime.datetime.now() - datetime.timedelta(hours=age)
    print(timeCutoff)

    print(coll.remove({
        "timestamp": {"$lt": timeCutoff}}))

    print("done")


'''
scapToMongo.xccdf("report1.html","ben")

scapToMongo.oval("report.html","ben")

'''