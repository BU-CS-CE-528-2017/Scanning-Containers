# 3/15: added to webserver/app/views.py

import subprocess

subprocess.call("ls", shell=True)
subprocess.call("sudo ./run_docker.sh", shell=True)
    
