import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

_TIMEOUT = 0.08

_TARGETS = (
    ("127.0.0.1", 9050),      
    ("127.0.0.1", 9150),      

    ("1.1.1.1", 53),          
    ("8.8.8.8", 53),          
    ("9.9.9.9", 53),          
    ("208.67.222.222", 53)
)


def _probe(target):
    try:
        with socket.create_connection(target, _TIMEOUT):
            return True
    except OSError:
        return False


def check_connectivity() -> bool:
    executor = ThreadPoolExecutor(max_workers=len(_TARGETS))

    try:
        futures = [executor.submit(_probe, target) for target in _TARGETS]

        for future in as_completed(futures):
            if future.result():
                executor.shutdown(wait=False, cancel_futures=True)
                return True

        return False

    finally:
        executor.shutdown(wait=False, cancel_futures=True)
