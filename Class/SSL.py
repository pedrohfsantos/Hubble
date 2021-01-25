from requests_html import HTMLSession
from tqdm.auto import tqdm


class SSL:
    def __init__(self, ssl, erro_ssl):
        self.ssl = ssl
        self.erro_ssl = erro_ssl
        self.session = HTMLSession()

    def verifica(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando SSL e Redirect para HTTPS", leave=False):
            try:
                r = self.session.get("https://" + self.dominio(url) + "/")
                self.ssl.append(url)

            except:
                self.erro_ssl.append(url)

    def dominio(self, url):
        url = url.split(" => ")
        url = url[0]
        return url
