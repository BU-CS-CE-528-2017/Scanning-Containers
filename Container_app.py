from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *
import subprocess
from subprocess import PIPE, Popen
import webbrowser

application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.MachineData
print ("db value:",db)
print ("Database name",client.database_names())
@application.route("/addMachine",methods=['POST'])
def addMachine():
    print("In add machine")
    try:
        json_data = request.json['info']
        print(json_data)
        cont_name = json_data['cont_name']
        cont_ip = json_data['cont_ip']
        userName = json_data['username']
        password = json_data['password']
        portNumber = json_data['port']
	#print(deviceName)

        db.Machines.insert_one({
            'cont_name':cont_name,'cont_ip':cont_ip,'username':userName,'password':password,'port':portNumber
            })
        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/')
def showMachineList():
    print("In showmachine para")	
    return render_template('list.html')

@application.route('/getMachine',methods=['POST'])
def getMachine():
    print ("In getMachine para")
    try:
        machineId = request.json['id']
	#print "machineID is",machineID
        machine = db.Machines.find_one({'_id':ObjectId(machineId)})
        machineDetail = {
                'cont_name':machine['cont_name'],
                'cont_ip':machine['cont_ip'],
                'username':machine['username'],
                'password':machine['password'],
                'port':machine['port'],
                'id':str(machine['_id'])
                }
        return json.dumps(machineDetail)
    except Exception, e:
        return str(e)

@application.route('/updateMachine',methods=['POST'])
def updateMachine():
    try:
        machineInfo = request.json['info']
        machineId = machineInfo['id']
        device = machineInfo['device']
        ip = machineInfo['ip']
        username = machineInfo['username']
        password = machineInfo['password']
        port = machineInfo['port']

        db.Machines.update_one({'_id':ObjectId(machineId)},{'$set':{'device':device,'ip':ip,'username':username,'password':password,'port':port}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getMachineList",methods=['POST'])
def getMachineList():
    print ("In machinelist para:")
    try:
        machines = db.Machines.find()
        print ("machines:",machines)
        machineList = []
        for machine in machines:
	    print ("Machine",machine)
            machineItem = {
                    'cont_name':machine['cont_name'],
                    'cont_ip':machine['cont_ip'],
                    'username':machine['username'],
                    'password':machine['password'],
                    'port':machine['port'],
                    'id': str(machine['_id'])
                    }
            machineList.append(machineItem)
    except Exception,e:
        return str(e)
    return json.dumps(machineList)

@application.route("/execute",methods=['POST'])
#def execute():
#    print("In execute para")	
#    try:
#        machineInfo = request.json['info']
#	print (machineInfo)
#        cont_ip = machineInfo['cont_ip']
#        username = machineInfo['username']
#        password = machineInfo['password']
#        command = machineInfo['command']
#	print (command)
#        isRoot = machineInfo['isRoot']
#        
#        env.host_string = username + '@' + ip
#        env.password = password
#        resp = ''
#        with settings(warn_only=True):
#            if isRoot:
#                resp = sudo(command)
#            else:
#                resp = run(command)
#
#        return jsonify(status='OK',message=resp)
#    except Exception, e:
#        print 'Error is ' + str(e)
#        return jsonify(status='ERROR',message=str(e))

def execute():
    print("In execute para")
    try:
        machineInfo = request.json['info']
        #cont_name = machineInfo['cont_name']
	#cmnd = machineInfo['command']
        #env.host_string = username + '@' + ip
        #env.password = password
	#output = webbrowser.open(/home/ubuntu/oscap_docker/img_report.html[, new=0[, autoraise=True]])
        output = subprocess.Popen("lynx /home/ubuntu/oscap_docker/img_report.html",shell=True,executable="/bin/bash")
	#print (output)
        resp = ''
        #with settings(warn_only=True):
            #if isRoot:
               # resp = sudo(command)
            #else:
                #resp = run(command)

        #return jsonify(status='OK',message=)
    except Exception, e:
        print 'Error is ' + str(e)
        return jsonify(status='ERROR',message=str(e))



@application.route("/deleteMachine",methods=['POST'])
def deleteMachine():
    try:
        machineId = request.json['id']
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    application.run(host='0.0.0.0')

