import subprocess
import time

while True:
    subprocess.call("ls", shell=True)
    subprocess.call("./openscap_update.sh", shell=True)
    time.sleep(5)