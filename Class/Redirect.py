from urllib.request import urlopen
from tqdm.auto import tqdm

class Redirect:
    def __init__(self, erroRedirect):
        self.erroRedirect = erroRedirect

    def verifica(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando redirect da pagina 404", leave=False,):
            url = self.dominio(url)
            try:
                location = urlopen("http://" + url + "/xptoz-xptoz-xptoz").url
                if "localhost" in location or "mpitemporario" in location or "/404" not in location:
                    self.erroRedirect.append(url)

            except:
                self.erroRedirect.append(url)

    def dominio(self, url):
        url = url.split(",")
        url = url[0]
        return url
