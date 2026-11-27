import re
from ipaddress import ip_address
from urllib.parse import urlsplit, urlunsplit

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from monitors.validators import validate_monitoring_url, resolve_public_ips
import pycurl

def normalize_hostname(hostname: str) -> str:
    if not hostname:
        raise ValidationError("Hostname cannot be empty.")
    if "%" in hostname or not hostname.isascii():
        raise ValidationError("Invalid hostname.")

    hostname = hostname.lower()

    try:
        canonical_ip = ip_address(hostname)
        return str(canonical_ip)
    except ValueError:
        if len(hostname) > 253:
            raise ValidationError("Invalid hostname.")

        label_pattern = re.compile(r"[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?")
        labels = hostname.split(".")

        if not labels[-1].isalpha() or len(labels) < 2:
            raise ValidationError("Invalid hostname.")

        if all(label_pattern.fullmatch(l) for l in labels):
            return hostname
        raise ValidationError("Invalid hostname.")


def execute_http_check(url: str) -> None:
    if any(ch.isspace() or not ch.isprintable() or ch == "\\" for ch in url):
        raise ValidationError("Invalid URL.")

    validator = URLValidator(schemes=["http", "https"])
    validator(url)
    validate_monitoring_url(url)

    split_url = urlsplit(url)
    if not split_url.netloc.isascii():
        raise ValidationError("URL contains non-ASCII characters.")
    scheme = split_url.scheme
    hostname = normalize_hostname(split_url.hostname)
    port = split_url.port
    path = split_url.path
    query_params = split_url.query

    if port is None:
        if scheme == "http":
            port = 80
        elif scheme == "https":
            port = 443

    is_literal_ip = False
    resolve_collection = []
    destination_ips = resolve_public_ips(hostname)
    selected_ip = ""

    try:
        ip_addr_obj = ip_address(hostname)
        is_literal_ip = True
        if ip_addr_obj in {ip_address(ip) for ip in destination_ips}:
            selected_ip = hostname
        else:
            raise ValidationError("Provided hostname IP does not match destination IP.")
    except ValueError:
        selected_ip = sorted(destination_ips, key=lambda x: ip_address(x).version)[0]
        resolve_collection = [f"{hostname}:{port}:{selected_ip}" \
                                  if ip_address(selected_ip).version == 4 else f"{hostname}:{port}:[{selected_ip}]"]

    netloc = f"{hostname}:{port}" if ':' not in hostname else f"[{hostname}]:{port}"
    components = (
        scheme,
        netloc,
        path,
        query_params,
        ""
    )
    final_url = urlunsplit(components)

    curl = pycurl.Curl()

    try:
        curl.setopt(pycurl.URL, final_url)
        if not is_literal_ip:
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

execute_http_check("http://[2001:4860:4860::8888]")
