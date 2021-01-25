from Class import *
import threading
import schedule
import time
import datetime


email = Email("EMAIL@GMAIL.COM", "SENHA")


def verifica():
    arquivo = Arquivo()

    ip = arquivo.ler_arquivo("Config", "ips")
    resultadosDNS = {"Casa": [], "Fora da cada": [], "Congelado": [], "IP Host diferente do WWW": []}
    resultadosSitemap = {"Sitemap nao foi encontrado": [], "Sitemap com numeros de links abaixo do esperado": []}
    resultadosSSL = {"Sites com SSL": [], "Sites sem SSL": []}
    resultadosAnalytics = {"Site com problemas no ID do analytics": []}
    resultadosRedirect = {"Site com problemas no redirect 404": [], "Site com problemas no redirect HTTPS": []}

    dns = DNS(
        ip,
        resultadosDNS["Casa"],
        resultadosDNS["Fora da cada"],
        resultadosDNS["Congelado"],
        resultadosDNS["IP Host diferente do WWW"],
    )

    sitemap = Sitemap(
        resultadosSitemap["Sitemap nao foi encontrado"],
        resultadosSitemap["Sitemap com numeros de links abaixo do esperado"],
    )

    ssl = SSL(resultadosSSL["Sites com SSL"], resultadosSSL["Sites sem SSL"])
    analytics = Analytics(resultadosAnalytics["Site com problemas no ID do analytics"])
    redirect = Redirect(
        resultadosRedirect["Site com problemas no redirect 404"],
        resultadosRedirect["Site com problemas no redirect HTTPS"],
    )

    data_arquivo = datetime.datetime.now().strftime("%d-%m-%Y")
    data_email = datetime.datetime.now().strftime("%d/%m/%Y")

    # Verifica DNS dos projetos
    sites = arquivo.ler_arquivo("Config", "dominios")
    dns.ip(sites)
    arquivo.arquivo_resultado(f"Resultados/{data_arquivo}/DNS", resultadosDNS)
    sites_casa = arquivo.ler_arquivo(f"Resultados/{data_arquivo}/DNS", "Casa")

    ssl.verifica(sites_casa)
    arquivo.arquivo_resultado(f"Resultados/{data_arquivo}/SSL", resultadosSSL)
    sites_ssl = arquivo.ler_arquivo(f"Resultados/{data_arquivo}/SSL", "Sites com SSL")

    thread_analytics = threading.Thread(target=analytics.verifica, args=(sites_casa,))
    thread_sitemap = threading.Thread(target=sitemap.verifica, args=(sites_casa,))
    thread_redirect_404 = threading.Thread(target=redirect.redirect_404, args=(sites_casa,))
    thread_redirect_ssl = threading.Thread(target=redirect.redirect_ssl, args=(sites_ssl,))

    thread_analytics.start()
    thread_sitemap.start()
    thread_redirect_404.start()
    thread_redirect_ssl.start()

    # Assim que a thread finalizar o script cria os arquivos txt
    thread_analytics.join()
    arquivo.arquivo_resultado(f"Resultados/{data_arquivo}/Analytics", resultadosAnalytics)

    thread_sitemap.join()
    arquivo.arquivo_resultado(f"Resultados/{data_arquivo}/Sitemap", resultadosSitemap)

    thread_redirect_404.join() and thread_redirect_ssl.join()
    arquivo.arquivo_resultado(f"Resultados/{data_arquivo}/Redirect", resultadosRedirect)

    mensagem = """
    E-mail enviado pelo script python que monitora os sites no ar.
    Segue anexo dos erros encontrados
    """

    anexos = [
        f"Resultados/{data_arquivo}/SSL/Sites sem SSL.txt",
        f"Resultados/{data_arquivo}/SSL/Sites sem redirect HTTPS.txt",
        f"Resultados/{data_arquivo}/SSL/SSL expira em 7 dias.txt",
        f"Resultados/{data_arquivo}/DNS/IP Host diferente do WWW.txt",
        f"Resultados/{data_arquivo}/Analytics/Site com problemas no ID do analytics.txt",
        f"Resultados/{data_arquivo}/Redirect/Site com problemas no redirect 404.txt",
        f"Resultados/{data_arquivo}/Redirect/Site com problemas no redirect HTTPS.txt",
        f"Resultados/{data_arquivo}/Sitemap/Sitemap nao foi encontrado.txt",
        f"Resultados/{data_arquivo}/Sitemap/Sitemap com numeros de links abaixo do esperado.txt",
    ]

    email.send(
        destinatario="",
        assunto=f"{data_email} - Relatorio status site (SCRIPT  PYTHON)",
        mensagem=mensagem,
        anexos=anexos,
    )


schedule.every().day.at("08:00").do(verifica)


while 1:
    try:
        schedule.run_pending()
    except:
        email.send(
            destinatario="",
            assunto=f"{data_email} - ERRO (SCRIPT  PYTHON)",
            mensagem="Erro na verificação, o script foi desligado.",
            erro=True,
        )
        break

    time.sleep(1)
