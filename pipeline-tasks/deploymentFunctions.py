import subprocess
import re  
import sys
from pathlib import Path
from IPy import IP
import contextlib
import platform
import os

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def runShellCommand(commandToRun):
    print("Inside runShellCommand(..., ...) function. ")
    print("commandToRun is: " +commandToRun)

    proc = subprocess.Popen( commandToRun,cwd=None, stdout=subprocess.PIPE, shell=True)
    while True:
      line = proc.stdout.readline()
      if line:
        thetext=line.decode('utf-8').rstrip('\r|\n')
        decodedline=ansi_escape.sub('', thetext)
        print(decodedline)
      else:
        break
  
def createHostsFileAnsible(ansibleHostsGroupName, remoteServerIP, remoteUser, remotePassWord): 
  groupNameLine="["+ansibleHostsGroupName+"]\n"	
  hostNameLine=remoteServerIP + " ansible_ssh_pass=" + remotePassWord + "\n"	
  hostsFileNameAndPath='/etc/ansible/hosts' 
  print("hostsFileNameAndPath is: ", hostsFileNameAndPath)	
  print("About to write lines to a file.")	
  f = open(hostsFileNameAndPath, "w")	
  f.write(groupNameLine)	
  f.write(hostNameLine)	
  f.close()	

def createVarsFileAnsible(varFileName, gitKeyOrganization, gitOrganizationName, remotePassWord, gitProjectName, gitRepoName):
  pwdLine = 'rt_pass: ' + remotePassWord + "\n"	
  print("pwdLine is: ", pwdLine)
  gitKeyLine = 'git_password: ' + gitKeyOrganization + "\n"	
  gitOrgNameLine = 'git_org_user: ' + gitOrganizationName + "\n"	
  gitProjectNameLine = 'project_name: ' + gitProjectName + "\n"
  gitRepoNameLine = 'repo_name: ' + gitRepoName + "\n"
  print("About to write lines to a file.")	
  f = open(varFileName, "w")	
  f.write(pwdLine) 
  f.write(gitKeyLine) 
  f.write(gitOrgNameLine) 
  f.write(gitProjectNameLine) 
  f.write(gitRepoNameLine) 
  f.close()	

def getIP(ipFileNameAndPath):
  remoteServerIP = ''
  lineCount=0
  ipFile = Path(ipFileNameAndPath)
  try:
    #This next line will force an exception if the file does not exist, so that we can handle the exception as seen below.  
    my_abs_path = ipFile.resolve(strict=True)
    f = open(ipFileNameAndPath,'r')
    for l in f:
      print("line is: ", l)
      try: 
        print("line a valid IP: ", IP(l))  
        remoteServerIP=l
        lineCount+=1
      except:
        print("boolean check of IP is False. ")
    if lineCount > 1:
      print("There was more than one IP address. ")
  except FileNotFoundError:
    print("Failed to populate remoteServerIP dynamically.  Giving a false static value instead. ")
    remoteServerIP="not-provided"
  with contextlib.suppress(FileNotFoundError):
    os.remove(ipFileNameAndPath)
  remoteServerIP = remoteServerIP.rstrip()
  return remoteServerIP
