import subprocess
import re
import networkdeploymentfunctions as ndf

#path_to_jekyll_module='C:\\projects\\terraform\\portable-kubernetes-example\\modules\\ansible-and-aws-hostnetwork-module\\'
path_to_call_to_jekyll_module = "C:\\projects\\terraform\\jekyll-devbox-aws\\calls-to-modules\\jekyll-host-call-to-module"

###############################################################################
### Remove the Host Network
###############################################################################
ndf.removeHostNetwork( 'pipeline-jekyll-network-destroy.py', path_to_call_to_jekyll_module)
print("                                  ")
print("  **** Finished Removing Jekyll Host Network. ****")
print("                                  ")
