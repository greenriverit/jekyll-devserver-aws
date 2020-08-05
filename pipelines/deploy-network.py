## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    

import sys
import subprocess
import re
import networkdeploymentfunctions as ndep
import networkvalidation as nval
import time
import os

print("The new environment variables read into python are: ")
print(os.environ['P_K_A'])
print(os.environ['S_K_A'])

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

##Start of new _try_ block
try:
    ndep.deployHostNetwork( command_to_call_jekyll_module, path_to_call_to_jekyll_module)
    #PUT THIS BACK IN FOR REAL: nval.validateHostNetwork(ndep.cidr_subnet, ndep.cidr_subnet_list, ndep.security_group_id, ndep.vpc_id, ndep.route_table_id)
except Exception: 
    print("FAILED TO RUN THE subprocess.popen COMMAND IN networkdeploymentfunctions. ")
    pass
##End of new _try_ block

print("                                  ")
print("  **** Finished Deploying Jekyll Host Network. ****")
print("                                  ")

