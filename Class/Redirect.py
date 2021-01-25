from requests_html import HTMLSession
from tqdm.auto import tqdm


class Redirect:
    def __init__(self, erro_redirect_404, erro_redirect_ssl):
        self.erro_redirect_404 = erro_redirect_404
        self.erro_redirect_ssl = erro_redirect_ssl
        self.session = HTMLSession()

    def redirect_404(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando redirect da pagina 404", leave=False):
            try:
                link = self.session.get("http://" + self.dominio(url) + "/xptoz-xptoz-xptoz").url

                if "localhost" in link or "mpitemporario" in link or not link.endswith("/404"):
                    self.erro_redirect_404.append(url)

            except:
                self.erro_redirect_404.append(url)

    def redirect_ssl(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando redirect SSL", leave=False):
            try:
                link = self.session.get("http://" + self.dominio(url) + "/").url

                if not link.startswith("https"):
                    self.erro_redirect_ssl.append(url)

            except:
                self.erro_redirect_ssl.append(url)

    def dominio(self, url):
        url = url.split(" => ")
        url = url[0]
        return url
