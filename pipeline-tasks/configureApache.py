## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    
  
import subprocess
import sys
import platform
import deploymentFunctions as depfunc 

###################################################################################  
### 1. Import the variables.  These will come from key vault and pipeline but for 
###       now during development only we are stating them explicitly.  
################################################################################### 
dynamicVarsPath = "" 
if platform.system() == 'Windows':
  dynamicVarsPath = config_SecretsPath + "\\dynamicvars\\"
else:
  dynamicVarsPath = "/home/azureuser/" + "/dynamicvars/"
#Check to ensure that input file for dynamic IP variables exists.  If so, then iterate file and validate each IP.  There should only be one IP now.  If you need to support more IPs later, add a work item to support multiple IPs.
ipFileNameAndPath=dynamicVarsPath+"/vmip.txt" 

remoteServerIP = depfunc.getIP(ipFileNameAndPath)

print("remoteServerIP is: ", remoteServerIP)

DefaultWorkingDirectory=sys.argv[1] 
gitKeyOrganization=sys.argv[2]
gitOrganizationName=sys.argv[3]
#$(System.DefaultWorkingDirectory)  $(git-key-organization)  $(org_name)  $(project_name_site)  $(repo_name_static)  
#New 2:  
gitProjectName=sys.argv[4]
gitRepoName=sys.argv[5]

remoteUserName='agile-cloud'
remotePassWord='just-for-demo123'
ansibleHostsGroupName='demoservers'

print("DefaultWorkingDirectory is:", DefaultWorkingDirectory)
print("remoteUserName is:", remoteUserName)
print("remoteServerIP is:", remoteServerIP)
print("remotePassWord is:", remotePassWord)
print("ansibleHostsGroupName is:", ansibleHostsGroupName)

###################################################################################
### 2. Add remote ip to known_hosts file using BatchMode:
###################################################################################
print("About to add remote IP to known_hosts so that Ansible can ssh without an interactive prompt.  ")
knownHostsCommand='ssh -o BatchMode=yes -o StrictHostKeyChecking=no ' + remoteUserName + '@' + remoteServerIP + " \"uptime\""
depfunc.runShellCommand(knownHostsCommand)

###################################################################################
### 3. Overwrite /etc/ansible/hosts file with ips from preceding create vms task, 
###       and with password from key vault.  
###################################################################################
print("About to create the Ansible Hosts file that Ansible will use to determine which IPs to associate with each group name.  ")
depfunc.createHostsFileAnsible(ansibleHostsGroupName, remoteServerIP, remoteUserName, remotePassWord)

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
depfunc.createVarsFileAnsible(varFileName, gitKeyOrganization, gitOrganizationName, remotePassWord, gitProjectName, gitRepoName)  

provisionPlayBookNameAndPath=playBooksDir+"provisionApacheServer.yaml"
print("About to read the Playbook we will subsequently run. ")
print("provisionPlayBookNameAndPath is: ", provisionPlayBookNameAndPath)
f = open(provisionPlayBookNameAndPath, "r")	
print(f.read())
  
playBookCommandSlice = "ansible-playbook -vvvv "
provisionCommand = playBookCommandSlice + provisionPlayBookNameAndPath
print("provisionCommand is: ", provisionCommand)
depfunc.runShellCommand(provisionCommand)
