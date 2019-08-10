import subprocess
from subprocess import PIPE
import shlex

def get():
    # get command
    f = open('get_rpi_ip_addr_cmd.txt')
    full_cmd = f.readline()
    divided_cmd = full_cmd.split("|")

    # execute command
    task = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE)
    output = task.stdout.read()

    # clean output
    output = output.decode('utf-8')
    output = output.replace('\n','')

    return output
print(get())
