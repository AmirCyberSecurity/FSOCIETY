import requests
from concurrent.futures import ThreadPoolExecutor

urls = {
    "instagram": "https://www.instagram.com/{}/",
    "facebook": "https://www.facebook.com/{}",
    "pinterest": "https://www.pinterest.com/{}/",
    "tiktok": "https://www.tiktok.com/@{}",
    "telegram": "https://t.me/{}",
    "github": "https://github.com/{}",
    "vk": "https://vk.com/{}",
    "steam": "https://steamcommunity.com/id/{}/",
    "youtube": "https://www.youtube.com/@{}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

BAD_SIGNS = {
    "instagram": ["sorry, this page isn't available", "page not found"],
    "facebook": ["this content isn't available", "content isn't available", "page isn't available"],
    "tiktok": ["couldn't find this account", "no longer available"],
    "telegram": ["if you have telegram", "view in telegram", "not found"],
    "github": ["not found", "doesn’t exist"],
    "vk": ["page not found", "deleted"],
    "steam": ["the specified profile could not be found"],
    "youtube": ["this channel doesn't exist", "not found"],
    "pinterest": ["page not found"],
}

session = requests.Session()
session.headers.update(HEADERS)


def short_path(url: str) -> str:
    url = url.replace("https://", "").replace("http://", "")
    url = url.replace("www.", "")
    return url.strip("/")


def _check_site(site: str, username: str):
    url = urls[site].format(username)

    try:
        r = session.get(url, timeout=2, allow_redirects=True)
        text = (r.text or "").lower()
        final_url = r.url

        if r.status_code != 200:
            return site, "Not Exists"

        for bad in BAD_SIGNS.get(site, []):
            if bad in text:
                return site, "Not Exists"

        if "login" in final_url and site in ["instagram", "facebook"]:
            return site, "Not Exists"

        return site, short_path(final_url)

    except:
        return site, "Not Exists"


def check(username: str) -> dict:
    result = {}

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(_check_site, site, username)
            for site in urls.keys()
        ]

        for f in futures:
            site, value = f.result()
            result[site] = value

    return result

