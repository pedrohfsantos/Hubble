from urllib.request import urlopen
from tqdm.auto import tqdm
import re

class Analytics:
    def __init__(self, erroidAnalytics):
        self.erroidAnalytics = erroidAnalytics

    def verifica(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando ID do Analytics", leave=False,):
            url = self.dominio(url)
            try:
                home = urlopen("http://" + url + "/")
                idAnalytics = re.search("(gtag|ga)\(\\\['\"](create|config)\\\['\"].*?\\\['\"](.*?-.*?)\\\['\"].*?\)", str(home.read()),).group(2)
                            
            except:
                self.erroidAnalytics.append(url)

    def dominio(self, url):
        url = url.split(",")
        url = url[0]
        return url