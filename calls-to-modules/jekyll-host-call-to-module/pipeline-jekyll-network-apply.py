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

print("The imported variables resolve to: ")
print(sys.argv[0])
print(sys.argv[1])
print(sys.argv[2])


subprocess.run("terraform init", shell=True, check=True)

subprocess.run('terraform apply -auto-approve -var="name_of_ssh_key=ansible-server" -var="_public_access_key=$(-public-access-key)" -var="_secret_access_key=$(-secret-access-key)" -var="aws_region=us-west-2"', shell=True, check=True)

#subprocess.run("terraform apply -auto-approve -var-file="+path_to_jekyll_iam_keys+"awspublickey.tfvars -var-file="+path_to_jekyll_iam_keys+"awsvpcmeta.tfvars -var-file="+path_to_jekyll_iam_keys+"awskeymeta.tfvars", shell=True, check=True)
