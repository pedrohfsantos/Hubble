from requests_html import HTMLSession
from tqdm.auto import tqdm
import re


class Analytics:
    def __init__(self, erroidAnalytics):
        self.erroidAnalytics = erroidAnalytics
        self.session = HTMLSession()

    def verifica(self, urls):
        for url in tqdm(
            urls, unit="Projetos", desc="Verificando ID do Analytics", leave=False
        ):
            try:
                r = self.session.get(self.url_http(url))
                body = r.html.find("body", first=True)
                idAnalytics = re.search(
                    "(gtag|ga)\(['\"]create['\"].*?['\"]([a-zA-Z]*-\d*-\d*)['\"].*?\)",
                    body.text,
                ).group(2)

            except:
                self.erroidAnalytics.append(self.dominio(url))

    def dominio(self, url):
        url = url.split(",")
        url = url[0]
        return url

    def url_http(self, url):
        url = url.split(",")
        url = "http://www." + url[0] + "/"
        return url