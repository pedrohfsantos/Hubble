from Class import *
import threading
import schedule
import time


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
        "Sites  sem redirect HTTPS": [],
        "Site com redirect para outra url": [],
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
        resultadosSSL["Sites  sem redirect HTTPS"],
        resultadosSSL["Site com redirect para outra url"],
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


schedule.every().day.at("08:00").do(verifica)
schedule.every().day.at("12:00").do(verifica)
schedule.every().day.at("16:00").do(verifica)


while 1:
    schedule.run_pending()
    time.sleep(1)