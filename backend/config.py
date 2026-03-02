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

DEFAULT_COOKIES = [
    {"name": "RK", "value": "rBNB6yZOaT", "domain": "wx.mail.qq.com"},
    {"name": "ptcz", "value": "a833f812b16b1d44f1d7d387ce3500f9a660a48f08eb84fdc5e9e093188edd8a", "domain": "wx.mail.qq.com"},
    {"name": "yyb_muid", "value": "35FC33F86FDC641322ED25DD6E8665CE", "domain": "wx.mail.qq.com"},
    {"name": "pgv_pvid", "value": "1006830016", "domain": "wx.mail.qq.com"},
    {"name": "qm_device_id", "value": "Jqkm6bFh2Tqq3PbP1yxQ5Mb6LTgN2cOnrApy22JU9563ATuWep4NuM7OWu7SPh8A", "domain": "wx.mail.qq.com"},
    {"name": "lang", "value": "zh-CN", "domain": "wx.mail.qq.com"},
    {"name": "qm_logintype", "value": "qq", "domain": "wx.mail.qq.com"},
    {"name": "_qpsvr_localtk", "value": "0.06342973214490677", "domain": "wx.mail.qq.com"},
    {"name": "xm_envid", "value": "456_R9BVJ0+Mj/CmzNxFOKHpXhlex5ZjJWalyl97NmUAR9hDYSQUFwUxslSe7OQtFcrherxGWZJEI0QnyTuzP+nEcRHQ5l02zbdHNuq4gbdsP+Cp+DgIGOW8+oAtuSWUGDoNqVkuRECA5JTdc7TkNVLGDxsptxqsdELsmpCMTw==", "domain": "wx.mail.qq.com"},
    {"name": "sid", "value": "1060827621&", "domain": "wx.mail.qq.com"},
    {"name": "xm_pcache", "value": "13102662085702117&V2@pN6HIhPKRDGeet4AJPjTEwAA@0", "domain": "wx.mail.qq.com"},
    {"name": "xm_device_id", "value": "c5c73fcb", "domain": "wx.mail.qq.com"},
    {"name": "xm_uin", "value": "13102662085702117", "domain": "wx.mail.qq.com"},
    {"name": "xm_sid", "value": "zeV0S4zxQlguOmswAD9HYQAA", "domain": "wx.mail.qq.com"},
    {"name": "xm_muti_sid", "value": "13102662085702117&zeV0S4zxQlguOmswAD9HYQAA", "domain": "wx.mail.qq.com"},
    {"name": "xm_skey", "value": "13102662085702117&e382c67e2d3bdc04895f8bd8e7aa6af7", "domain": "wx.mail.qq.com"},
    {"name": "xm_ws", "value": "13102662085702117&0b94b13658a65f6c79acc94970d95a96", "domain": "wx.mail.qq.com"},
    {"name": "xm_data_ticket", "value": "13102662085702117&CAESIGmWqjYALozNPzrx5TETgnyghkwSeTwOcYHotcjJ2_nX", "domain": "wx.mail.qq.com"}
]

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
        return {"headers": DEFAULT_HEADERS, "cookies": DEFAULT_COOKIES}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
    except Exception:
        return {"headers": DEFAULT_HEADERS, "cookies": DEFAULT_COOKIES}
    headers = data.get("headers") or DEFAULT_HEADERS
    cookies = data.get("cookies") or DEFAULT_COOKIES
    return {"headers": headers, "cookies": cookies}


_CONFIG = _load_config()
headers = _CONFIG["headers"]
cookies = _CONFIG["cookies"]
