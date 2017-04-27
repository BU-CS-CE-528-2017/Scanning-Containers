from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import docker
import time
import os
import subprocess
import uuid
from subprocess import PIPE, Popen

class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        print "Got event for file %s" % event.src_path 
        s_cont = event.src_path
	cont_name = s_cont[27:39]
	docker_container_pid(cont_name)
	print "Container added is %s" %cont_name

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def docker_container_pid(name):
        container_name = name
	#pid = cli.inspect_container(container_name)
        pid = str(cmdline("docker inspect --format '{{.State.Pid}}' %s" % container_name))
	root = str(os.path.join('/proc',pid))
	pid= pid.rstrip('\n')
	print(pid)
	print len(pid)
	root = str(os.path.join('/proc',pid,'root'))	
	#root1 = str('/proc')
	output = subprocess.Popen("./oscap-chroot %s oval eval /home/ubuntu/oscap_docker/com.ubuntu.xenial.cve.oval.xml --report /home/ubuntu/oscap_docker/report.xml --results /home/ubuntu/oscap_docker/results.html" % root,shell=True, executable="/bin/bash")
	#output = subprocess.Popen("[./oscap-chroot %s oval eval /home/ubuntu/oscap_docker/com.ubuntu.xenial.cve.oval.xml --report %s.html --results %s.xml" % root, uq_name, uq_name],shell=True, executable="/bin/bash")


s_cont = []
pid = str(5)
uq_name = uuid.uuid4()
cli = docker.from_env()
observer = Observer()
event_handler = ExampleHandler() # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path='/var/lib/docker/containers')
observer.start()
#print pid

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
