import subprocess
import re
"""
Retrieves IP address of Aamir's Raspberry Pi on LAN
"""
# constants
cmd = "arp -a | grep aamirpi | awk -F '(' '{print $2}' | awk -F ')' '{print $1}'"
regex_match_IPv4 = "^(\d{1,3}\.){3}\d{1,3}$"
no_rpi_exception_message = "Couldn't find aamirpi on LAN"
regex_exception_message = "Couldn't get IP address of raspberry pi - {0} isn't a valid IPv4 address"

def get():
    # execute command
    task = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = task.stdout.read()
    if output == '':
        raise Exception(no_rpi_exception_message)

    # clean output
    output = output.decode('utf-8')
    output = output.replace('\n','')
    
    # verify that output is IPv4 address with regex
    match = re.search(regex_match_IPv4, output)
    if match:
        return output
    else:
        raise Exception(regex_exception_message.format(output))

print(get())
