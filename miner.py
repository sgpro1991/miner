import requests as req
import os
import sh
import signal
import subprocess
import json


uuid = '50c441ab-05a0-423f-a511-3b93a7dfa29c'
index = '3'




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
