## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    

import subprocess
import sys
import deploymentFunctions as depfunc 

def createHostsFileAnsible(ansibleHostsGroupName, remoteJekyllServerIP, remoteJekyllPassWord): 
  groupNameLine="["+ansibleHostsGroupName+"]\n"	
  hostNameLine=remoteJekyllServerIP + " ansible_ssh_pass=" + remoteJekyllPassWord + "\n"	
  hostsFileNameAndPath='/etc/ansible/hosts' 
  print("hostsFileNameAndPath is: ", hostsFileNameAndPath)	
  print("About to write 2 lines to a file.")	
  f = open(hostsFileNameAndPath, "w")	
  f.write(groupNameLine)	
  f.write(hostNameLine)	
  f.close()	

def createVarsFileAnsible(varFileName, remoteJekyllPassWord):
  pwdLine = 'root_pass_jekyll: ' + remoteJekyllPassWord
  print("pwdLine is: ", pwdLine)
  print("About to write 1 line to a file.")	
  f = open(varFileName, "w")	
  f.write(pwdLine)
  f.close()	


###################################################################################  
### 1. Import the variables.  These will come from key vault and pipeline but for 
###       now during development only we are stating them explicitly.  
################################################################################### 
DefaultWorkingDirectory=sys.argv[1] 
remoteJekyllUserName='agile-cloud'
remoteJekyllServerIP=""
remoteJekyllPassWord=''
ansibleHostsGroupName='demoservers'

print("DefaultWorkingDirectory is:", DefaultWorkingDirectory)
print("remoteJekyllUserName is:", remoteJekyllUserName)
print("remoteJekyllServerIP is:", remoteJekyllServerIP)
print("remoteJekyllPassWord is:", remoteJekyllPassWord)
print("ansibleHostsGroupName is:", ansibleHostsGroupName)

###################################################################################
### 2. Add remote ip to known_hosts file using BatchMode:
###################################################################################
print("About to add remote IP to known_hosts so that Ansible can ssh without an interactive prompt.  ")
knownHostsCommand='ssh -o BatchMode=yes -o StrictHostKeyChecking=no ' + remoteJekyllUserName + '@' + remoteJekyllServerIP + " \"uptime\""
depfunc.runShellCommand(knownHostsCommand)

###################################################################################
### 3. Overwrite /etc/ansible/hosts file with ips from preceding create vms task, 
###       and with password from key vault.  
###################################################################################
print("About to create the Ansible Hosts file that Ansible will use to determine which IPs to associate with each group name.  ")
createHostsFileAnsible(ansibleHostsGroupName, remoteJekyllServerIP, remoteJekyllPassWord)

hostsFileNameAndPath='/etc/ansible/hosts' 
print("About to read the /etc/ansible/hosts file we just wrote.")	
#open and read the file after the appending:	
f = open(hostsFileNameAndPath, "r")	
print(f.read()) 	

###################################################################################
### 4. Run the playbook
###################################################################################
print("About to run the Ansible Playbook.  ")
#First get the directory of the playbook
playBooksDir=DefaultWorkingDirectory+"/_jekyll-devserver-aws/drop/ansible-playbooks/"
#Then create the var file which will hold the sudo password and maybe other things
varFileName=playBooksDir+'myVars.yaml'
print("varFileName is: ", varFileName)
createVarsFileAnsible(varFileName, remoteJekyllPassWord)  

provisionJekyllDevPlayBookNameAndPath=playBooksDir+"provisionJekyllDevServer.yaml"
print("About to read the Playbook we will subsequently run. ")
print("provisionJekyllDevPlayBookNameAndPath is: ", provisionJekyllDevPlayBookNameAndPath)
f = open(provisionJekyllDevPlayBookNameAndPath, "r")	
print(f.read())
  
playBookCommandSlice = "ansible-playbook -vvv "
provisionJekyllDevCommand = playBookCommandSlice + provisionJekyllDevPlayBookNameAndPath
print("provisionJekyllDevCommand is: ", provisionJekyllDevCommand)
depfunc.runShellCommand(provisionJekyllDevCommand)
