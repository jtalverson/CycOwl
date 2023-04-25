import pexpect
import sys

def getb():
    response = ''
    p = pexpect.spawn('bluetoothctl',encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect('#')
    p.sendline("info")
    response = p.after
    print(response)
    p.sendline("quit")
    p.close()


getb()
