from requests_html import HTMLSession
from tqdm.auto import tqdm
import re


class Sitemap:
    def __init__(self, erroSitemap, erroSitemapTamanho):
        self.erroSitemap = erroSitemap
        self.erroSitemapTamanho = erroSitemapTamanho
        self.session = HTMLSession()

    def verifica(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando Sitemap", leave=False):
            try:
                r = self.session.get(self.url_http(url) + "mapa-site")
                linksMapaSite = r.html.xpath('//*[@class="sitemap"]//li//a/@href')

                r = self.session.get(self.url_http(url) + "sitemap.xml")
                linksSitemap = r.html.xpath("//loc/text()")

                if len(linksMapaSite) > len(linksSitemap):
                    self.erroSitemapTamanho.append(self.dominio(url))

            except:
                self.erroSitemap.append(self.dominio(url))

    def dominio(self, url):
        url = url.split(",")
        url = url[0]
        return url

    def url_http(self, url):
        url = url.split(",")
        url = "http://" + url[0] + "/"
        return url