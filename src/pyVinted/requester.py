import requests
import random
from requests.exceptions import HTTPError

class Requester:
    def __init__(self, proxies=None, max_retries=250):
        self.HEADER = {
            "User-Agent": "PostmanRuntime/7.28.4",
            "Host": "www.vinted.fr",
        }
        self.VINTED_AUTH_URL = "https://www.vinted.fr/"
        self.MAX_RETRIES = max_retries
        self.session = requests.Session()
        self.session.headers.update(self.HEADER)

        self.all_proxies = proxies if proxies else []
        self.available_proxies = self.all_proxies.copy()
        self.banned_proxies = set()
        self.current_proxy = None
        self.rotate_proxy()

    def set_proxies(self, proxies):
        self.all_proxies = proxies if proxies else []
        self.available_proxies = self.all_proxies.copy()
        self.banned_proxies.clear()
        self.current_proxy = None
        self.rotate_proxy()

    def rotate_proxy(self):
        if not self.available_proxies and self.all_proxies:
            self.available_proxies = self.all_proxies.copy()
            self.banned_proxies.clear()

        if self.available_proxies:
            self.current_proxy = random.choice(self.available_proxies)
            self.session.proxies = {
                "http": self.current_proxy,
                "https": self.current_proxy,
            }
        else:
            self.session.proxies.clear()
            self.current_proxy = None

    def ban_current_proxy(self):
        if self.current_proxy in self.available_proxies:
            self.available_proxies.remove(self.current_proxy)
        self.banned_proxies.add(self.current_proxy)
        self.rotate_proxy()

    def setLocale(self, locale):
        self.VINTED_AUTH_URL = f"https://{locale}/"
        self.session.headers.update({
            "User-Agent": "PostmanRuntime/7.28.4",
            "Host": f"{locale}",
        })

    def get(self, url, params=None):
        tried = 0
        while tried < self.MAX_RETRIES:
            tried += 1
            try:
                response = self.session.get(url, params=params, timeout=20)
                if response.status_code == 200:
                    return response
                else:
                    print(response.status_code)
                    self.ban_current_proxy()
            except Exception:
                self.ban_current_proxy()
        raise HTTPError(f"Impossible de récupérer l'URL : {url}")

    def post(self, url, params=None):
        tried = 0
        while tried < self.MAX_RETRIES:
            tried += 1
            try:
                response = self.session.post(url, params=params, timeout=20)
                response.raise_for_status()
                return response
            except Exception:
                self.ban_current_proxy()
        raise HTTPError(f"Impossible de poster sur l'URL : {url}")

    def setCookies(self):
        self.session.cookies.clear_session_cookies()
        try:
            self.session.head(self.VINTED_AUTH_URL)
        except Exception:
            pass


requester = Requester()
