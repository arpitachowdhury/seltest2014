from psutil import process_iter
from signal import SIGTERM
from time import sleep
import os
import subprocess

hubport = 4444
nodeport = 5555
seleniumjar = 'selenium-server-standalone-2.44.0.jar'

#java -jar D:\eclipse\workspace\mytest\src\selenium-server-standalone-2.44.0.jar -role hub -port 4444 -timeout 0
#java -jar D:\eclipse\workspace\mytest\src\selenium-server-standalone-2.44.0.jar -role node -port 5555 -hub http://localhost:4444/grid/register -browser browserName=firefox,maxInstances=1 -browser browserName=chrome,maxInstances=1 



def startjar(typeof, jarpath):
    if (typeof == 'hub'):
        cmd1 = 'java -jar ' + jarpath + ' -role hub -port '+ str(hubport)+ ' -timeout 0'
        print cmd1
        subprocess.Popen(cmd1, shell=True).pid
    elif (typeof == 'node'):
        cmd2 = 'java -jar ' + jarpath + ' -role node -port '+ str(nodeport)+ ' -hub http://localhost:' + str(hubport) + '/grid/register -browser browserName=firefox,maxInstances=1 -browser browserName=chrome,maxInstances=1 -maxSession 1'
        print cmd2
        subprocess.Popen(cmd2, shell=True).pid
        
currentdir =  os.path.abspath(os.path.dirname(__file__))
selpath =   os.path.join(currentdir, seleniumjar)

for proc in process_iter():
    for conns in proc.get_connections(kind='inet'):
        if ((conns.laddr[1] == hubport) or (conns.laddr[1] == nodeport)) and (conns.laddr[1] >0):
            try:
                proc.send_signal(SIGTERM)
            finally:
                print ("No such process exists..")    
sleep(5)         

#restart the jars
#start the hub
startjar('hub',selpath)
sleep(10)
startjar('node', selpath)