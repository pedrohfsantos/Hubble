from requests_html import HTMLSession
from tqdm.auto import tqdm
import re


class Analytics:
    def __init__(self, erro_id_analytics):
        self.erro_id_analytics = erro_id_analytics
        self.session = HTMLSession()

    def verifica(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando ID do Analytics", leave=False):
            try:
                r = self.session.get("https://" + self.dominio(url) + "/")
                idAnalytics = re.search(
                    "(gtag|ga)\(['\"](create|config)['\"].*?['\"](.*?-.*?)['\"].*?\)", r.html.text
                ).group(3)

            except:
                self.erro_id_analytics.append(url)

    def dominio(self, url):
        url = url.split(" => ")
        url = url[0]
        return url
