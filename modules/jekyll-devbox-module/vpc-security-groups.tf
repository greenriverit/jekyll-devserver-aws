# Security groups and rules to allow the nodes to communicate with each other and the outside world.  
# Here we are putting all nodes in the same security group and subnet.  
# This is a simple example.

resource "aws_security_group" "jekyll-hosts" {
  name        = "jekyll nodes"
  description = "Security group for all nodes in the cluster"
  vpc_id      = aws_vpc.jekyll-host.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "jekyll-admin-ssh" {
  type = "ingress"
  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks       = ["${local.admin-external-cidr}"]
  security_group_id        = aws_security_group.jekyll-hosts.id
}

resource "aws_security_group_rule" "jekyll-preview-http" {
  type = "ingress"
  from_port = 4000
  to_port = 4000
  protocol = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id        = aws_security_group.jekyll-hosts.id
}
