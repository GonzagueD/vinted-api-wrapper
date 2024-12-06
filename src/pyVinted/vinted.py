from urllib.parse import urlparse, parse_qsl
import requests

from pyVinted.items import Items
from pyVinted.requester import requester

class Vinted:
    """
    This class is built to connect with the pyVinted API.

    It's main goal is to be able to retrieve items from a given url search.
    """

    def __init__(self, proxies=None):
        """
        Args:
            proxies (list[str]): liste de proxies à utiliser, par ex. ["http://user:pass@host:port", "http://..."]
        """
        if proxies is not None:
            requester.set_proxies(proxies)

        self.items = Items()
