## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    

# For info on how to refer to variables between scripts, see: https://stackoverflow.com/questions/16048237/pass-variable-between-python-scripts
import subprocess
import re
import networkdeploymentfunctions as ndep
import time

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def validateHostNetwork(cidr_sub_, cidr_sub_list_, sg_id_, vpcid_, route_tbl_id_):
    success='true'
    print('                                          ')
    print('----------------------------------------- ')
    print('---- Validating Host Network ---- ')
    print('cidr_subnet_ is: ' +cidr_sub_)
    print('cidr_subnet_list_ is: ')
    print(cidr_sub_list_)
    print('security_group_id_ is: ' +sg_id_)
    print('vpc_id_ is: ' +vpcid_)
    print('route_table_id_ is: ' +route_tbl_id_)

    if cidr_sub_ == '':
        print('Exiting because cidr_subnet_ is empty.')
        success='false'
    if not cidr_sub_list_:  
        print('Exiting because cidr_subnet_list_ is empty.')
        success='false'
    if sg_id_ == '':
        print('exiting because security_group_id_ is empty.')
        success='false'
    if vpcid_ == '':
        print('Exiting because vpc_id_ is empty.')
        success='false'
    if route_tbl_id_ == '':
        print("Exiting because route_table_ is empty.")
        success='false'
    if success=='false':
        print('About to exit 1 from validateHostNetwork.')
        exit(1)
    else:  
        print('SUCCESS validateHostNetwork.')

