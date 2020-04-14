import subprocess
import os 

path_to_jekyll_iam_keys="C:\\projects\\Jekyll\\vars\\VarsForTerraform\\"

print("..inside pipeline jekyll network apply")

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
print("dir_path is: ")
print(dir_path)
print("cwd is: ")
print(cwd)

subprocess.run("terraform init", shell=True, check=True)

subprocess.run("terraform apply -auto-approve -var-file="+path_to_jekyll_iam_keys+"awspublickey.tfvars -var-file="+path_to_jekyll_iam_keys+"awsvpcmeta.tfvars -var-file="+path_to_jekyll_iam_keys+"awskeymeta.tfvars", shell=True, check=True)
