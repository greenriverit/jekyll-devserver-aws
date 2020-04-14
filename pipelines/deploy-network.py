# For info on how to refer to variables between scripts, see: https://stackoverflow.com/questions/16048237/pass-variable-between-python-scripts
import subprocess
import re
import networkdeploymentfunctions as ndep
import networkvalidation as nval
import time

#################################################################################
#################################################################################
#### Variable definition for function calls
#################################################################################
#################################################################################

#path_to_jekyll_module='C:\\projects\\terraform\\portable-kubernetes-example\\modules\\ansible-and-aws-hostnetwork-module\\'
#path_to_call_to_jekyll_module = "C:\\projects\\terraform\\jekyll-devbox-aws\\calls-to-modules\\jekyll-host-call-to-module"
path_to_call_to_jekyll_module = "../calls-to-modules/jekyll-host-call-to-module"
command_to_call_jekyll_module = 'python3 pipeline-jekyll-network-apply.py'

myRegion="us-west-2"

################################################################################  
### 1. NOW DEPLOY THE JEKYLL HOST NETWORK
################################################################################  
ndep.deployHostNetwork( command_to_call_jekyll_module, path_to_call_to_jekyll_module)
nval.validateHostNetwork(ndep.cidr_subnet, ndep.cidr_subnet_list, ndep.security_group_id, ndep.vpc_id, ndep.route_table_id)
print("                                  ")
print("  **** Finished Deploying Jekyll Host Network. ****")
print("                                  ")

