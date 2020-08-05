module "jekyll-devbox" {
  source = "../../modules/jekyll-devbox-module"

  _region = "us-west-2"
  access_key = "${var._public_access_key}"
  secret_access_key = "${var._secret_access_key}"
  # path_to_ssh_keys = "${var.path_to_ssh_keys}"
  # name_of_ssh_key = "${var.name_of_ssh_key}"

}

variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
# variable "path_to_ssh_keys" { }
# variable "name_of_ssh_key" { }

##Output variables
output "security_group_id_jekyll_hosts" { value = "${module.jekyll-devbox.security_group_id_jekyll_hosts}" }
output "vpc_id_jekyll" { value = "${module.jekyll-devbox.vpc_id_jekyll}" }
output "cidr_subnet_jekyll" { value = "${module.jekyll-devbox.cidr_subnet_jekyll}" }
output "route_table_id_jekyll_host" { value = "${module.jekyll-devbox.route_table_id_jekyll_host}" }
