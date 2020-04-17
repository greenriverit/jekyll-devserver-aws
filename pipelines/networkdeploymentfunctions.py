import subprocess
import re
import ipaddress
import os
from os.path import exists
#import requests
import sys
import time
import glob

# NOTE:  Need to harden all the string processing code below.  This will include:
# --- startIndex calculated programatically for each split of a string
# Consolidate the functions to become more polymorphic.

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

cidr_subnet = ''
cidr_subnet_list = []
security_group_id = ''
vpc_id = ''
route_table_id = ''

def checkForErrors(myDecodedLine):
    foundAnExceptionWorthStoppingScript="no"
    if "connectex: No connection could be made because the target machine actively refused it." in myDecodedLine:
        foundAnExceptionWorthStoppingScript="yes"
    if foundAnExceptionWorthStoppingScript=="yes":
        print("                                           ")
        print("---- Stopping script due to error. ----")
        print("                                           ")
        exit(1)

def deployHostNetwork( scriptName, workingDir ):
    print("scriptName is: " +scriptName)
    print("workingDir is: " +workingDir)

    ##Start of new _try_ block
    try:
        proc = subprocess.Popen( scriptName,cwd=workingDir,stdout=subprocess.PIPE, shell=True)
    except Exception: 
        print("FAILED TO RUN THE subprocess.popen COMMAND IN networkdeploymentfunctions. ")
        pass
    ##End of new _try_ blodk

    inCidrBlock='false'
    while True:
      line = proc.stdout.readline()
      if line:
        thetext=line.decode('utf-8').rstrip('\r|\n')
        decodedline=ansi_escape.sub('', thetext)
        checkForErrors(decodedline)
        print(decodedline)
        if "Outputs:" in decodedline:  
          print("JENGA")
        global cidr_subnet_list
        if "cidr_subnet_" in decodedline:  
            if not "[" in decodedline:  
                global cidr_subnet
                cidr_subnet = decodedline[22:]
                ##Test the following:  
                cidr_subnet_line_test = re.findall("(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?",decodedline)
                print("cidr_subnet_line_test is: " +cidr_subnet_line_test[0])
                ##End of test
                cidr_subnet_list.append(cidr_subnet_line_test[0])
            if "[" in decodedline:  
                inCidrBlock='true'
        elif inCidrBlock=='true':
            if "]" in decodedline:
                inCidrBlock='false'
            if inCidrBlock=='true':
                decodedline=decodedline.strip()
                decodedline=decodedline.replace(",","")
                ##Test the following:  
                cidr_subnet_line_test = re.findall("(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?",decodedline)
                if len(cidr_subnet_line_test) == 0:
                    print("cidr_subnet_line_test is EMPTY. ")
                elif len(cidr_subnet_line_test) == 1:
                    print("cidr_subnet_line_test is: " +cidr_subnet_line_test[0])
                    cidr_subnet_list.append(cidr_subnet_line_test[0])
                else:
                    print("UNHANDLED EXCEPTION: cidr_subnet_line_test has multiple entries.")
                ##End of test
        if "security_group_id" in decodedline:  
          global security_group_id
          security_group_id = decodedline[34:]
        if "vpc_id" in decodedline:  
          global vpc_id
          vpc_id = decodedline[17:]
        if "route_table_id" in decodedline:  
          print("                                            ")
          print("decodedline is: " +decodedline)
          startIndex = int(decodedline.find('rtb-'))
          print("startIndex is: " +str(startIndex))
          print("                                            ")
          global route_table_id
          route_table_id = decodedline[startIndex:]
      else:
        break

def removeHostNetwork( scriptName, workingDir ): 
    proc = subprocess.Popen( scriptName,cwd=workingDir,stdout=subprocess.PIPE, shell=True)
    while True:
      line = proc.stdout.readline()
      if line:
        thetext=line.decode('utf-8').rstrip('\r|\n')
        decodedline=ansi_escape.sub('', thetext)
        print(decodedline)
        if "Outputs:" in decodedline:  
          print("Outputs are: ")
      else:
        break
