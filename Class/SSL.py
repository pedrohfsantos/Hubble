import json
from urllib.request import ssl, socket, urlopen
from datetime import datetime
from tqdm.auto import tqdm


class SSL:
    def __init__(self, ssl, erroSSL, expira, redirectHTTPS):
        self.ssl = ssl
        self.erroSSL = erroSSL
        self.expira = expira
        self.redirectHTTPS = redirectHTTPS
        
    def verifica(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando SSL e Redirect para HTTPS", leave=False,):
            url = self.dominio(url)
            port = '443'
            context = ssl.create_default_context()
            
            try:
                with socket.create_connection((url, port)) as sock:
                    with context.wrap_socket(sock, server_hostname=url) as ssock:
                        self.ssl.append(url)
                        
                        data = json.dumps(ssock.getpeercert())
                        data = json.loads(data)
                        
                        inicio = datetime.strptime(data['notAfter'], "%b %d %H:%M:%S %Y %Z")
                        termino = datetime.strptime(data['notBefore'], "%b %d %H:%M:%S %Y %Z")
                        dSSL = inicio - termino

                        if dSSL.days <= 7:
                            self.expira.append(f"{url} - SSL expira em {dSSL.days} dias")

                        with urlopen("http://" + url + "/") as sssock:
                            if "https:" not in sssock.url:
                                self.redirectHTTPS.append(url)

            except:
                self.erroSSL.append(url)

    def dominio(self, url):
        url = url.split(",")
        url = url[0]
        return url