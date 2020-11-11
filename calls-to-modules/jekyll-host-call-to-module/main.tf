## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/GreenRiverIT    

module "jekyll-devbox" {
  source = "../../modules/jekyll-devbox-module"

  _region = "${var.aws_region}"
  access_key = "${var._public_access_key}"
  secret_access_key = "${var._secret_access_key}"
  vpc_id = "${var.vpc_id}"  

}

variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
variable "vpc_id" { }
