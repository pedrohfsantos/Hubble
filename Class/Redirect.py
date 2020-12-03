from requests_html import HTMLSession
from tqdm.auto import tqdm


class Redirect:
    def __init__(self, erroRedirect):
        self.erroRedirect = erroRedirect
        self.session = HTMLSession()

    def verifica(self, urls):
        for url in tqdm(
            urls,
            unit="Projetos",
            desc="Verificando redirect da pagina 404",
            leave=False,
        ):
            try:
                try:
                    location = self.session.head(
                        self.url_https(url) + "xptoz-xptoz-xptoz"
                    ).headers["Location"]

                    if "localhost" in location or "mpitemporario" in location:
                        self.erroRedirect.append(self.dominio(url))

                except:
                    location = self.session.head(
                        self.url_http(url) + "xptoz-xptoz-xptoz"
                    ).headers["Location"]

                    if "localhost" in location or "mpitemporario" in location:
                        self.erroRedirect.append(self.dominio(url))

            except:
                self.erroRedirect.append(self.dominio(url))

    def dominio(self, url):
        url = url.split(",")
        url = url[0]
        return url

    def url_https(self, url):
        url = url.split(",")
        url = "https://" + url[0] + "/"
        return url

    def url_http(self, url):
        url = url.split(",")
        url = "http://" + url[0] + "/"
        return url