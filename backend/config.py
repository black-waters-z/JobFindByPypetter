import json
import os
import sys


DEFAULT_HEADERS = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://wx.mail.qq.com/",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "lang": "zh",
    "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryumi8462Cs82eah5I",
    "origin": "https://wx.mail.qq.com",
    "content-length": "0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "text/plain;charset=UTF-8",
    "Origin": "https://wx.mail.qq.com",
    "Pragma": "no-cache",
    "Referer": "https://wx.mail.qq.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

CromePath = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def _get_config_path() -> str:
    env_path = os.getenv("CONFIG_PATH")
    if env_path:
        return env_path
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "config.json")


def _load_config() -> dict:
    path = _get_config_path()
    if not os.path.exists(path):
        return {"headers": DEFAULT_HEADERS, "cookies": None}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
    except Exception:
        return {"headers": DEFAULT_HEADERS, "cookies": None}
    headers = data.get("headers") or DEFAULT_HEADERS
    cookies = data.get("cookies") or None
    return {"headers": headers, "cookies": cookies}


_CONFIG = _load_config()
headers = _CONFIG["headers"]
cookies = _CONFIG["cookies"]
