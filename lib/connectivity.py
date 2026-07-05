import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

HOSTS = [
    ("1.1.1.1", 53),
    ("8.8.8.8", 53),
    ("9.9.9.9", 53),
]

def _check(host):
    try:
        with socket.create_connection(host, 0.6):
            return True
    except OSError:
        return False

def check_connectivity():
    with ThreadPoolExecutor(max_workers=len(HOSTS)) as pool:
        futures = [pool.submit(_check, h) for h in HOSTS]

        for future in as_completed(futures):
            if future.result():
                return True

    return False
