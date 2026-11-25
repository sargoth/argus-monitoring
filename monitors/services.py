from ipaddress import ip_address
from urllib.parse import urlsplit
from django.core.validators import URLValidator

from monitors.validators import validate_monitoring_url, resolve_public_ips
import pycurl


def execute_http_check(url: str) -> None:
    validator = URLValidator(schemes=["http", "https"])
    validator(url)
    validate_monitoring_url(url)

    split_url = urlsplit(url)
    scheme = split_url.scheme
    hostname = split_url.hostname
    port = split_url.port

    if port is None:
        if scheme == "http":
            port = 80
        elif scheme == "https":
            port = 443

    destination_ips = resolve_public_ips(hostname)
    selected_ip = sorted(destination_ips, key=lambda x: ip_address(x).version)[0]
    resolve_collection = [f"{hostname}:{port}:{selected_ip}" \
                              if ip_address(selected_ip).version == 4 else f"{hostname}:{port}:[{selected_ip}]"]

    curl = pycurl.Curl()

    try:
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.RESOLVE, resolve_collection)
        curl.setopt(pycurl.HTTPGET, True)
        curl.setopt(pycurl.CONNECTTIMEOUT, 5)
        curl.setopt(pycurl.TIMEOUT, 10)
        curl.setopt(pycurl.FOLLOWLOCATION, False)
        curl.setopt(pycurl.SSL_VERIFYPEER, True)
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)
        curl.setopt(pycurl.PROXY, "")
        curl.setopt(pycurl.PROTOCOLS, pycurl.PROTO_HTTP | pycurl.PROTO_HTTPS)
        curl.setopt(pycurl.MAXFILESIZE_LARGE, 1048576)
        curl.setopt(pycurl.USERAGENT, "ArgusMonitoring/1.0")
        curl.setopt(pycurl.WRITEFUNCTION, len)
    finally:
        curl.close()
