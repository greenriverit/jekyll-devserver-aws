import sys
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

print("The two imported variabled resolve to: ")
print(sys.argv[0])
print(sys.argv[1])
print(sys.argv[2])

myRegion="us-west-2"

################################################################################  
### 1. NOW DEPLOY THE JEKYLL HOST NETWORK
################################################################################  
#PUT THIS BACK IN FOR REAL: ndep.deployHostNetwork( command_to_call_jekyll_module, path_to_call_to_jekyll_module)
#PUT THIS BACK IN FOR REAL: nval.validateHostNetwork(ndep.cidr_subnet, ndep.cidr_subnet_list, ndep.security_group_id, ndep.vpc_id, ndep.route_table_id)
print("                                  ")
print("  **** Finished Deploying Jekyll Host Network. ****")
print("                                  ")

