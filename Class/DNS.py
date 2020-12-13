import socket
from tqdm.auto import tqdm


class DNS:
    def __init__(self, ips, casa, foraCasa, congelado, HostdiferenteWWW):
        self.ips = ips
        self.casa = casa
        self.foraCasa = foraCasa
        self.congelado = congelado
        self.HostdiferenteWWW = HostdiferenteWWW


    def ip(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando IP dos projetos", leave=False,):
            try:
                ipSite = socket.gethostbyname(url)
                try:
                    ipSiteWWW = socket.gethostbyname("www." + url)
                except:
                    ipSiteWWW = "NULL"


                if ipSite in self.ips or ipSiteWWW in self.ips:
                    self.casa.append(f"{url},Host: {ipSite},WWW: {ipSiteWWW}")

                    if ipSite != ipSiteWWW:
                        self.HostdiferenteWWW.append(f"{url}")

                else:
                    self.foraCasa.append(f"{url},{ipSite}")
                    
            except:
                self.congelado.append(url)
