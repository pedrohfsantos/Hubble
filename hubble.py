from Class import *
import threading
import schedule
import time
import datetime


email = Email("EMAIL@GMAIL.COM", "SENHA")

def verifica():
    arquivo = Arquivo()
    ip = arquivo.ler_arquivo("Config", "ips")

    resultadosDNS = {
        "Casa": [],
        "Fora da cada": [],
        "Congelado": [],
        "IP Host diferente do WWW": [],
    }

    resultadosSSL = {
        "Sites com SSL": [],
        "Sites sem SSL": [],
        "SSL expira em 7 dias": [],
        "Sites sem redirect HTTPS": []
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

    dns = DNS(
        ip,
        resultadosDNS["Casa"],
        resultadosDNS["Fora da cada"],
        resultadosDNS["Congelado"],
        resultadosDNS["IP Host diferente do WWW"],
    )

    ssl = SSL(
        resultadosSSL["Sites com SSL"],
        resultadosSSL["Sites sem SSL"],
        resultadosSSL["SSL expira em 7 dias"],
        resultadosSSL["Sites sem redirect HTTPS"],
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

    mensagem = """
    E-mail enviado pelo script python que monitora os sites no ar.
    Segue anexo dos erros encontrados
    """

    anexos = [
        "Resultados/SSL/Sites sem SSL.txt",
        "Resultados/SSL/Sites sem redirect HTTPS.txt",
        "Resultados/SSL/SSL expira em 7 dias.txt",
        "Resultados/DNS/IP Host diferente do WWW.txt",
        "Resultados/Analytics/Site com problemas no ID do analytics.txt",
        "Resultados/Redirect/Site com problemas no redirect 404.txt",
        "Resultados/Sitemap/Sitemap nao foi encontrado.txt",
        "Resultados/Sitemap/Sitemap com numeros de links abaixo do esperado.txt",
    ]

    email.send(
        destinatario="",
        assunto=f"{datetime.datetime.now().strftime('%d/%m/%Y')} - Relatorio status site (SCRIPT  PYTHON)",
        mensagem=mensagem,
        anexos=anexos,
    )

    arquivo.clear_resultados()


verifica()

schedule.every().day.at("08:00").do(verifica)


while 1:
    try:
        schedule.run_pending()
    except:
        email.send(
            destinatario="",
            assunto=f"{datetime.datetime.now().strftime('%d/%m/%Y')} - ERRO (SCRIPT  PYTHON)",
            mensagem="Erro na verificação, o script foi desligado.",
            erro=True,
        )
        break
    
    time.sleep(1)
