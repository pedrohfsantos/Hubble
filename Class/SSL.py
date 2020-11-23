from requests_html import HTMLSession
from tqdm.auto import tqdm


class SSL:
    def __init__(self, ssl, erroSSL, sslSemRedirect, redirectSite):
        self.ssl = ssl
        self.erroSSL = erroSSL
        self.sslSemRedirect = sslSemRedirect
        self.redirectSite = redirectSite
        self.session = HTMLSession()

    def verifica(self, urls):
        for url in tqdm(
            urls,
            unit="Projetos",
            desc="Verificando SSL e Redirect para HTTPS",
            leave=False,
        ):
            try:
                r = self.session.get(self.url_https(url))
                self.ssl.append(self.dominio(url))
                try:
                    location = self.session.head(self.url_http(url)).headers["Location"]
                    if self.dominio(url) not in location:
                        self.redirectSite.append(self.dominio(url))
                except:
                    self.sslSemRedirect.append(self.dominio(url))

            except:
                self.erroSSL.append(self.dominio(url))

    def dominio(self, url):
        url = url.split(",")
        url = url[0]
        return url

    def url_https(self, url):
        url = url.split(",")
        url = "https://www." + url[0] + "/"
        return url

    def url_http(self, url):
        url = url.split(",")
        url = "http://www." + url[0] + "/"
        return url