from Class import *
import threading
import schedule
import time
import datetime


def verifica():
    arquivo = Arquivo()
    ip = arquivo.ler_arquivo("Config", "ips")

    resultadosDNS = {
        "Casa": [],
        "Fora da cada": [],
        "Congelado": [],
    }

    resultadosAnalytics = {
        "Site com problemas no ID do analytics": [],
    }

    resultadosRedirect = {
        "Site com problemas no redirect 404": [],
    }

    resultadosSitemap = {
        "Sitemap nao foi encontrado": [],
        "Sitemap com numeros de links abaixo do esperado": [],
    }

    resultadosSSL = {
        "Sites com SSL": [],
        "Sites sem SSL": [],
        "Sites sem redirect HTTPS": [],
        "Site com redirect para outro url": [],
    }

    dns = DNS(
        ip,
        resultadosDNS["Casa"],
        resultadosDNS["Fora da cada"],
        resultadosDNS["Congelado"],
    )

    ssl = SSL(
        resultadosSSL["Sites com SSL"],
        resultadosSSL["Sites sem SSL"],
        resultadosSSL["Sites sem redirect HTTPS"],
        resultadosSSL["Site com redirect para outro url"],
    )

    analytics = Analytics(
        resultadosAnalytics["Site com problemas no ID do analytics"],
    )

    redirect = Redirect(
        resultadosRedirect["Site com problemas no redirect 404"],
    )

    sitemap = Sitemap(
        resultadosSitemap["Sitemap nao foi encontrado"],
        resultadosSitemap["Sitemap com numeros de links abaixo do esperado"],
    )

    email = Email("" "")  # E-mail Gmail ex:exemplo@gmail.com  # Senha

    # Verifica DNS dos projetos
    sites = arquivo.ler_arquivo("Config", "dominios")
    dns.ip(sites)
    arquivo.arquivo_resultado("Resultados/DNS", resultadosDNS)
    sitesCasa = arquivo.ler_arquivo("Resultados/DNS", "Casa")

    # Verifica SSL dos projetos
    threadSSL = threading.Thread(target=ssl.verifica, args=(sitesCasa,))
    threadSSL.start()

    # Verifica Analytics
    threadAnalytics = threading.Thread(target=analytics.verifica, args=(sitesCasa,))
    threadAnalytics.start()

    # Verifica redirect para 404
    threadRedirect = threading.Thread(target=redirect.verifica, args=(sitesCasa,))
    threadRedirect.start()

    # Verifica sitemap.xml
    threadSitemap = threading.Thread(target=sitemap.verifica, args=(sitesCasa,))
    threadSitemap.start()

    # Assim que a thread finalizar o script cria os arquivos txt
    threadSSL.join()
    arquivo.arquivo_resultado("Resultados/SSL", resultadosSSL)

    threadAnalytics.join()
    arquivo.arquivo_resultado("Resultados/Analytics", resultadosAnalytics)

    threadRedirect.join()
    arquivo.arquivo_resultado("Resultados/Redirect", resultadosRedirect)

    threadSitemap.join()
    arquivo.arquivo_resultado("Resultados/Sitemap", resultadosSitemap)

    mensagem = """
    E-mail enviado pelo script python que monitora os sites no ar.
    Segue anexo dos erros encontrados
    """

    anexos = [
        "Resultados/SSL/Sites sem SSL.txt",
        "Resultados/SSL/Sites sem redirect HTTPS.txt",
        "Resultados/SSL/Site com redirect para outro url.txt",
        "Resultados/Analytics/Site com problemas no ID do analytics.txt",
        "Resultados/Redirect/Site com problemas no redirect 404.txt",
        "Resultados/Sitemap/Sitemap nao foi encontrado.txt",
        "Resultados/Sitemap/Sitemap com numeros de links abaixo do esperado.txt",
    ]

    email.send(
        destinatario="",
        assunto="Relatorio status site (SCRIPT  PYTHON)",
        mensagem=mensagem,
        anexos=anexos,
    )


schedule.every().day.at("08:00").do(verifica)
schedule.every().day.at("12:00").do(verifica)
schedule.every().day.at("16:00").do(verifica)


while 1:
    try:
        schedule.run_pending()
    except:
        print(f"Erro {datetime.datetime.now()}")

    time.sleep(1)
