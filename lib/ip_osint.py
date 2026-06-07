import requests
import ipaddress

_cache = {}


def _get_data(target_ip):
    if target_ip not in _cache:
        response = requests.get(
            f"http://ip-api.com/json/{target_ip}"
            "?fields=status,message,country,countryCode,"
            "region,regionName,city,zip,lat,lon,"
            "timezone,isp,org,as,asname,mobile,"
            "proxy,hosting,query"
        )

        _cache[target_ip] = response.json()

    return _cache[target_ip]


def _none(value):
    if value in ("", None, False):
        return "None"

    return str(value)


def checking(target_ip) -> bool:
    data = _get_data(target_ip)

    if data["status"] == "success":
        return True

    return False


def get_ip(target_ip) -> str:
    return f"IP: {_none(_get_data(target_ip).get('query'))}"


def get_country(target_ip) -> str:
    return f"COUNTRY: {_none(_get_data(target_ip).get('country'))}"


def get_city(target_ip) -> str:
    return f"CITY: {_none(_get_data(target_ip).get('city'))}"


def get_isp(target_ip) -> str:
    return f"ISP: {_none(_get_data(target_ip).get('isp'))}"


def get_org(target_ip) -> str:
    return f"ORG: {_none(_get_data(target_ip).get('org'))}"


def get_cords(target_ip) -> str:
    data = _get_data(target_ip)

    if data.get("lat") is None or data.get("lon") is None:
        return "COORDS: None"

    return f"COORDS: {data['lat']}, {data['lon']}"


def get_ip_type(target_ip):
    ip = ipaddress.ip_address(target_ip)

    if ip.is_private:
        ip_type = "PRIVATE"
    elif ip.is_loopback:
        ip_type = "LOOPBACK"
    elif ip.is_reserved:
        ip_type = "RESERVED"
    elif ip.is_multicast:
        ip_type = "MULTICAST"
    elif ip.is_link_local:
        ip_type = "LINK_LOCAL"
    else:
        ip_type = "PUBLIC"

    return f"IP TYPE: {ip_type}"


def get_asname(target_ip):
    return f"ASNAME: {_none(_get_data(target_ip).get('asname'))}"


def get_mobile(target_ip):
    data = _get_data(target_ip)

    if data.get("mobile") is True:
        return "MOBILE: Yes"

    return "MOBILE: None"


def get_proxy(target_ip):
    data = _get_data(target_ip)

    if data.get("proxy") is True:
        org = data.get("org")

        if org:
            return f"PROXY/VPN: {org}"

        return "PROXY/VPN: Detected"

    return "PROXY/VPN: None"


def get_hosting(target_ip):
    data = _get_data(target_ip)

    if data.get("hosting") is True:
        org = data.get("org")

        if org:
            return f"HOSTING: {org}"

        isp = data.get("isp")

        if isp:
            return f"HOSTING: {isp}"

        return "HOSTING: Detected"

    return "HOSTING: None"
