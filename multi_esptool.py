Import ('env')
from threading import Thread
from base64 import b64decode
from platformio import util

import sys
import glob
import serial
import os
import threading

print ("Current build targets", map(str, BUILD_TARGETS))

returnCodes=[] # Contains error/return codes
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def run(port):
    env.Replace(UPLOAD_PORT=port)
    for i in range(0, 3):  # Try up to 3 times
        if(i>0):
            env.Replace(UPLOAD_SPEED="115200") # Try slowing down baud
        command = env.subst('$UPLOADCMD') +" "+ env.subst('$BUILD_DIR/$PROGNAME') + ".bin"
        errorCode=env.Execute(command)
        if (errorCode==0):
            returnCodes.append((port,errorCode))
            return

    returnCodes.append((port,errorCode))

def after_build(source, target, env):
    # Check the cinfig for multiport uploading
    defined_ports = open(b64decode(ARGUMENTS.get("PROJECT_CONFIG"))).readlines()
    simultaneous_upload_ports = ""

    for defined_port in defined_ports:
        if defined_port.strip().startswith("simultaneous_upload_ports"):
            print(defined_port)
            simultaneous_upload_ports = defined_port.split("=")[1].strip()
            break

    if (simultaneous_upload_ports!=None):
        threads = []
        ports = simultaneous_upload_ports.split(",")

        # If ports not specified flash to all of them
        if(ports[0]=="AUTO"):
            ports = serial_ports()
        
        print (("Uploading to " + str(ports)))
        for port in ports :
            port = port.strip()
            thread = Thread(target=run, args=(port,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join() # Wait for all threads to finish

        encounteredError=False
        sorted(returnCodes, key=lambda code: code[0])

        # Log flash statuses
        for code in returnCodes:
            if(code[1]==0):
                print ('\033[0;32m' + code[0] + " Uploaded Successfully" + '\033[0m')
            elif(code[1]==1):
                print ('\033[1;33m' + code[0] + " Encountered Exception, Check serial port" + '\033[0m')
                encounteredError=True
            elif(code[1]==2):
                print ('\033[0;31m' + code[0] + " Encountered Fatal Error" + '\033[0m')
                encounteredError=True
        if(encounteredError):
            Exit(1)
    Exit(0)

env.AddPreAction("upload", after_build)     # Used to flash to specified simultaneous_upload_ports
#env.AddPostAction("upload", after_build)    # First flash to upload_port then to simultaneous_upload_ports