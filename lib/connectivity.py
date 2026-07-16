import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 1.0

TARGETS = [
    ("1.1.1.1", 443),
    ("8.8.8.8", 443),       
    ("google.com", 443),
    ("cloudflare.com", 443),
    ("github.com", 443),
    ("microsoft.com", 443),
    ("amazon.com", 443),
]


def probe(host, port):
    try:
        with socket.create_connection((host, port), TIMEOUT):
            return True
    except OSError:
        return False


def check_connectivity():
    with ThreadPoolExecutor(max_workers=len(TARGETS)) as executor:
        futures = [executor.submit(probe, h, p) for h, p in TARGETS]

        for future in as_completed(futures):
            if future.result():
                return True

    return False
