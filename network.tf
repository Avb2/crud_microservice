data "aws_availability_zones" "available" {
}

resource "aws_vpc" "main" {
    cidr_block = "172.17.0.0/16"
}

resource "aws_subnet" "private" {
    count = var.az_count
    cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
    availability_zone = data.aws_availability_zones.available.names[count.index]
    vpc_id = aws_vpc.main.id
}

resource "aws_subnet" "public" {
    count = var.az_count
    cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, var.az_count + count.index)
    availability_zone = data.aws_availability_zones.available.names[count.index]
    vpc_id = aws_vpc.main.id
    map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "gw" {
    vpc_id = aws_vpc.main.id
}

resource "aws_route" "internet_access" {
    route_table_id = aws_vpc.main.main_route_table_id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id

    depends_on = [aws_internet_gateway.gw]
}

resource "aws_eip" "nat" {
  count  = var.az_count
  domain = "vpc"
  depends_on = [aws_internet_gateway.gw]
}


resource "aws_nat_gateway" "gw" {
  count         = var.az_count
  subnet_id     = element(aws_subnet.public[*].id, count.index)
  allocation_id = aws_eip.nat[count.index].id
  depends_on    = [aws_internet_gateway.gw]
}



resource "aws_route_table" "private" {
  count  = var.az_count
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.gw[count.index].id
  }

  depends_on = [aws_nat_gateway.gw]
}


resource "aws_route_table_association" "private" {
    count = var.az_count
    subnet_id = element(aws_subnet.private.*.id, count.index)
    route_table_id = element(aws_route_table.private.*.id, count.index)
}