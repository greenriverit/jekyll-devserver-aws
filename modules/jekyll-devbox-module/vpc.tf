# VPC Resources ( VPC, Subnets, Internet Gateway, Route Table )

resource "aws_vpc" "jekyll-host" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = "1"
  tags = { Name = "jekyll-host" }
}

resource "aws_subnet" "jekyll-host" {
  depends_on = [aws_vpc.jekyll-host]
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block        = "10.0.0.0/24"
  vpc_id            = aws_vpc.jekyll-host.id
}

resource "aws_internet_gateway" "jekyll-host" {
  depends_on = [aws_vpc.jekyll-host]
  vpc_id = aws_vpc.jekyll-host.id
}

resource "aws_route_table" "jekyll-host" {
  depends_on = [aws_vpc.jekyll-host]
  vpc_id = aws_vpc.jekyll-host.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.jekyll-host.id
  }
}

resource "aws_route_table_association" "jekyll-host" {
  depends_on = [aws_subnet.jekyll-host, aws_route_table.jekyll-host]
  subnet_id      = aws_subnet.jekyll-host.id
  route_table_id = aws_route_table.jekyll-host.id
}
