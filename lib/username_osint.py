import requests

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

HEADERS = {"User-Agent": "Mozilla/5.0"}


def short_path(url: str) -> str:
    url = url.replace("https://", "").replace("http://", "")
    url = url.replace("www.", "")
    return url.strip("/")


def check(username: str) -> dict:
    result = {}

    for site, url in urls.items():
        try:
            r = requests.get(
                url.format(username),
                headers=HEADERS,
                timeout=1,
                allow_redirects=True
            )

            if r.status_code == 200:
                result[site] = short_path(r.url)
            else:
                result[site] = "Not Exists"

        except:
            result[site] = "Not Exists"

    return result

