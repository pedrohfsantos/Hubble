import socket
from tqdm.auto import tqdm


class DNS:
    def __init__(self, ips, casa, fora_casa, congelado, host_diferente_www):
        self.ips = ips
        self.casa = casa
        self.fora_casa = fora_casa
        self.congelado = congelado
        self.host_diferente_www = host_diferente_www

    def ip(self, urls):
        for url in tqdm(urls, unit="Projetos", desc="Verificando IP dos projetos", leave=False):
            try:
                ip_site = socket.gethostbyname(url)
                try:
                    ip_site_www = socket.gethostbyname("www." + url)
                except:
                    ip_site_www = "NULL"

                if ip_site in self.ips or ip_site_www in self.ips:
                    # ip_site_www != "NULL" condição para subdomínio ex: subdominio.site.com.br
                    if ip_site != ip_site_www and ip_site_www != "NULL":
                        self.host_diferente_www.append(f"{url} => {ip_site} | www.{url} => {ip_site_www}")

                    else:
                        self.casa.append(f"{url} => {ip_site}")

                else:
                    self.fora_casa.append(f"{url} => {ip_site}")

            except:
                self.congelado.append(url)
