## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    

import subprocess
import os 
import sys 

#path_to_jekyll_iam_keys="C:\\projects\\Jekyll\\vars\\VarsForTerraform\\"

print("..inside pipeline jekyll network apply")

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
print("dir_path is: ")
print(dir_path)
print("cwd is: ")
print(cwd)

print("The new environment variables read into python pipeline-jekyll-network-apply are: ")
print(os.environ['P_K_A'])
print(os.environ['S_K_A'])

pkvar = os.environ['P_K_A']
pkstr = f'-var=\"_public_access_key={pkvar}\"'
print("About to interpolate pkvar: ")
print(f'-var=\"_public_access_key={pkvar}\"')
print("About to print pkstr: ")
print(pkstr)

skvar = os.environ['S_K_A']
skstr = f'-var=\"_secret_access_key={skvar}\"'
print("About to interpolate skvar: ")
print(f'-var=\"_secret_access_key={skvar}\"')
print("About to print skstr: ")
print(skstr)
#argsstr = f'terraform apply -auto-approve -var=\"name_of_ssh_key=ansible-server\" {pkstr} {skstr} -var=\"aws_region=us-west-2\"'
argsstr = f'terraform plan -var=\"name_of_ssh_key=ansible-server\" {pkstr} {skstr} -var=\"aws_region=us-west-2\"'
print("About to print argsstr: ")
print(argsstr)

subprocess.run("terraform init", shell=True, check=True)

try:
    print("Inside __try__ block in __pipeline-jekyll-network-apply__.  About to run __terraform__apply command. ")
    subprocess.run(argsstr, shell=True, check=True)
    #throwanerror! 
except Exception: 
    print("FAILED TO RUN THE argsstr COMMAND. ")
    pass

#subprocess.run('terraform apply -auto-approve -var="name_of_ssh_key=ansible-server" ' + pkstr + ' ' + skstr + ' -var="aws_region=us-west-2"', shell=True, check=True)

#subprocess.run("terraform apply -auto-approve -var-file="+path_to_jekyll_iam_keys+"awspublickey.tfvars -var-file="+path_to_jekyll_iam_keys+"awsvpcmeta.tfvars -var-file="+path_to_jekyll_iam_keys+"awskeymeta.tfvars", shell=True, check=True)
