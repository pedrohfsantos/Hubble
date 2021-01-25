from requests_html import HTMLSession
from tqdm.auto import tqdm


class Sitemap:
    def __init__(self, erro_sitemap, erro_sitemap_tamanho):
        self.erro_sitemap = erro_sitemap
        self.erro_sitemap_tamanho = erro_sitemap_tamanho
        self.session = HTMLSession()

    def verifica(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando Sitemap", leave=False):
            try:
                mapa_site = self.session.get("http://" + self.dominio(url) + "/mapa-site")
                sitemap = self.session.get("http://" + self.dominio(url) + "/sitemap.xml")

                if sitemap.url.endswith("/404"):
                    self.erro_sitemap.append(url)

                else:
                    links_mapa_site = mapa_site.html.xpath('//*[@class="sitemap"]//li//a/@href')
                    links_sitemap = sitemap.html.xpath("//loc/text()")

                    if len(links_mapa_site) > len(links_sitemap):
                        self.erro_sitemap_tamanho.append(url)

            except:
                self.erro_sitemap.append(url)

    def dominio(self, url):
        url = url.split(" => ")
        url = url[0]
        return url
