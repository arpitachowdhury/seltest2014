import subprocess
import platform
import paramiko
import sys
import time
import select
    
hostname = "10.15.148.118"


def ping(hostname):
    if (platform.system() == 'Windows'):
        output = subprocess.Popen(["ping",hostname],stdout = subprocess.PIPE).communicate()[0]
    elif (platform.system() == 'Linux'):
        output = subprocess.Popen(["ping", "-c 3", hostname],stdout = subprocess.PIPE).communicate()[0]
    else:
        ret = 0
        return ret

    print(output)

    if ('unreachable' in output):    ret = 0
    elif ('timed out' in output):    ret = 0
    elif ('Reply from' in output):   ret = 1
    else :    ret = 0
    return ret



ret = ping(hostname)
print ret


i = 1

#
# Try to connect to the host.
# Retry a few times if it fails.
#
while True:
    print "Trying to connect to %s (%i/30)" % (hostname, i)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username='admin',password='admins')
        print "Connected to %s" % hostname
        break
    except paramiko.AuthenticationException:
        print "Authentication failed when connecting to %s" % hostname
        sys.exit(1)
    except:
        print "Could not SSH to %s, waiting for it to start" % hostname
        i += 1
        time.sleep(30)

    # If we could not connect within time limit
    if i == 30:
        print "Could not connect to %s. Giving up" % hostname
        sys.exit(1)
stdin, stdout, stderr = ssh.exec_command("help",get_pty=True)
print 'This is output =',stdout.readlines()
print 'This is error =',stderr.readlines()
ssh.close()

