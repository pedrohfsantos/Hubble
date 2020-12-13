from urllib.request import urlopen
from lxml import etree
from tqdm.auto import tqdm

class Sitemap:
    def __init__(self, erroSitemap, erroSitemapTamanho):
        self.erroSitemap = erroSitemap
        self.erroSitemapTamanho = erroSitemapTamanho

    def verifica(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando Sitemap", leave=False):
            url = self.dominio(url)

            try:
                ms = urlopen("http://" + url + "/mapa-site")
                msXML = urlopen("http://" + url + "/sitemap.xml")

                if "/404" in msXML.url:
                    self.erroSitemap.append(url)

                html = etree.HTML(ms.read())
                linksMapaSite = html.xpath('//*[@class="sitemap"]//li//a/@href')

                html = etree.HTML(msXML.read())
                linksSitemap = html.xpath("//loc/text()")

                if len(linksMapaSite) > len(linksSitemap):
                    self.erroSitemapTamanho.append(url)

                ms.close()
                msXML.close()
            
            except:
                self.erroSitemap.append(url)

    def dominio(self, url):
        url = url.split(",")
        url = url[0]
        return url

