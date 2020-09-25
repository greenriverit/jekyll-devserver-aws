## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    

import subprocess
import deploymentFunctions as depfunc 

def createHostsFileAnsible(ansibleHostsGroupName, remoteJekyllServerIP, remoteJekyllPassWord): 
  groupNameLine="["+ansibleHostsGroupName+"]\n"	
  hostNameLine=remoteJekyllServerIP + " ansible_ssh_pass=" + remoteJekyllPassWord + "\n"	
  hostsFileNameAndPath='/etc/ansible/hosts' 
  print("hostsFileNameAndPath is: ", hostsFileNameAndPath)	
  print("About to write 8 lines to a file.")	
  f = open(hostsFileNameAndPath, "w")	
  f.write(groupNameLine)	
  f.write(hostsFileNameAndPath)	
  f.close()	

###################################################################################  
### 1. Import the variables.  These will come from key vault and pipeline but for 
###       now during development only we are stating them explicitly.  
################################################################################### 
DefaultWorkingDirectory=sys.argv[1] 
remoteJekyllUserName='agile-cloud'
remoteJekyllServerIP="12.345.6.78"
remoteJekyllPassWord='z.z.z.z.c.v.3'
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

###################################################################################
### 4. Run the playbook
###################################################################################
print("About to run the Ansible Playbook.  ")
#First get the directory of the playbook
playBooksDir=DefaultWorkingDirectory+"/_jekyll-devserver-aws/drop/ansible-playbooks/"
provisionJekyllDevPlayBookNameAndPath=playBooksDir+"provisionJekyllDevServer.yaml"
playBookCommandSlice = "ansible-playbook -v "
provisionJekyllDevCommand = playBookCommandSlice + provisionJekyllDevPlayBookNameAndPath

