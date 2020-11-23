import socket
from tqdm.auto import tqdm


class DNS:
    def __init__(self, ips, casa, foraCasa, congelado):
        self.ips = ips
        self.casa = casa
        self.foraCasa = foraCasa
        self.congelado = congelado

    def ip(self, urls):
        for url in tqdm(
            urls, unit="Projetos", desc="Verificando IP dos projetos", leave=False
        ):
            try:
                ipSite = socket.gethostbyname(url)

                if ipSite in self.ips:
                    self.casa.append(f"{url},{ipSite}")
                else:
                    self.foraCasa.append(f"{url},{ipSite}")
            except:
                self.congelado.append(url)
