import ipaddress


def is_valid_subnet(cidr: str):
    try:
        ipaddress.ip_network(cidr, strict=True)
    except ValueError as _e:
        return False
    return True


def is_private_subnet(cidr: str):
    private_ranges = [
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
    ]

    try:

        subnet = ipaddress.ip_network(cidr, strict=True)
    except ValueError as _e:
        return False

    return any(subnet.overlaps(private_range) for private_range in private_ranges)


def is_in_cidr(child_cidr: str, parent_cidr: str):
    if not is_valid_subnet(child_cidr):
        return False

    if not is_valid_subnet(parent_cidr):
        return False

    child = ipaddress.ip_network(child_cidr, strict=True)
    parent = ipaddress.ip_network(parent_cidr, strict=True)

    return child.subnet_of(parent)
