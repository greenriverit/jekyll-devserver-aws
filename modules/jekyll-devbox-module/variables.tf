## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    

# Using these data sources allows the configuration to be generic for any region.
data "aws_region" "current" {}
data "aws_availability_zones" "available" {}

variable "access_key" { }
variable "secret_access_key" { }
variable "_region" { }
variable "path_to_ssh_keys" { }
variable "name_of_ssh_key" { }

#VPC to which the security group will be attached
variable "vpc_id" {}
data "aws_vpc" "selected" { id = var.vpc_id }

# Workstation External IP. Override with variable or hardcoded value if necessary.
data "http" "admin-external-ip" { url = "http://ipv4.icanhazip.com" }
locals { admin-external-cidr = "${chomp(data.http.admin-external-ip.body)}/32" }

#############Output variables
output "security_group_id_jekyll_hosts" { value = "${aws_security_group.jekyll-hosts.id}" }
output "vpc_id_jekyll" { value = "${aws_vpc.jekyll-host.id}" }
output "cidr_subnet_jekyll" { value = "${aws_subnet.jekyll-host.cidr_block}" }
output "route_table_id_jekyll_host" { value = "${aws_route_table.jekyll-host.id}" }
