import subprocess

path_to_jekyll_iam_keys="C:\\projects\\Jekyll\\vars\\VarsForTerraform\\"

subprocess.run("terraform destroy -auto-approve -var-file="+path_to_jekyll_iam_keys+"awspublickey.tfvars -var-file="+path_to_jekyll_iam_keys+"awsvpcmeta.tfvars -var-file="+path_to_jekyll_iam_keys+"awskeymeta.tfvars", shell=True, check=True)
