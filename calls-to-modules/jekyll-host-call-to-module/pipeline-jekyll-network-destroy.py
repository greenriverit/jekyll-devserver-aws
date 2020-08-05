## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    

import subprocess

path_to_jekyll_iam_keys="C:\\projects\\Jekyll\\vars\\VarsForTerraform\\"

subprocess.run("terraform destroy -auto-approve -var-file="+path_to_jekyll_iam_keys+"awspublickey.tfvars -var-file="+path_to_jekyll_iam_keys+"awsvpcmeta.tfvars -var-file="+path_to_jekyll_iam_keys+"awskeymeta.tfvars", shell=True, check=True)
