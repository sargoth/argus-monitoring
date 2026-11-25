import socket
from ipaddress import ip_address
from urllib.parse import urlsplit

from django.core.exceptions import ValidationError


def validate_monitoring_url(url: str) -> None:
    try:
        split_url = urlsplit(url)
        port = split_url.port
    except ValueError:
        raise ValidationError("Invalid URL or port. Please provide a valid URL.")

    if split_url.scheme not in ["http", "https"]:
        raise ValidationError("Invalid protocol. Please provide a valid URL.")
    if not split_url.hostname:
        raise ValidationError("No domain provided. Please provide a valid URL.")
    if split_url.username is not None or split_url.password is not None:
        raise ValidationError("URLs containing embedded credentials are not allowed.")
    if port == 0:
        raise ValidationError("Invalid URL or port. Please provide a valid URL.")


def resolve_public_ips(hostname: str) -> set[str]:
    resolved_ips = set()

    try:
        for dns_result in socket.getaddrinfo(
            host=hostname,
            port=None,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM
        ):
            resolved_ips.add(dns_result[4][0])
    except socket.gaierror:
        raise ValidationError("Unable to resolve hostname.")

    if not resolved_ips:
        raise ValidationError("Unable to resolve domain.")

    for ip in resolved_ips:
        ip_obj = ip_address(ip)
        if ip_obj.is_multicast:
            raise ValidationError("Domain resolves to a multicast address. Please provide a valid URL.")
        if ip_obj.is_reserved:
            raise ValidationError("Domain resolves to a reserved IP address.")
        if not ip_obj.is_global:
            raise ValidationError("Monitoring is only permitted for public IP addresses.")

    return resolved_ips
