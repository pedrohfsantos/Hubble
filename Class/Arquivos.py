from os import listdir, makedirs
import os.path
import shutil


class Arquivo:
    def __init__(self):
        pastas = ["DNS", "Analytics", "SSL", "Redirect", "Sitemap"]

        if not os.path.isdir("Resultados"):
            makedirs("Resultados")
            for pasta in pastas:
                makedirs(f"Resultados/{pasta}")

        for pasta in pastas:
            if not os.path.isdir(f"Resultados/{pasta}"):
                makedirs(f"Resultados/{pasta}")

    def arquivo_resultado(self, caminho, resultados):
        for resultado in resultados:
            if len(resultados[resultado]) > 0:
                arquivo = open(f"{caminho}/{resultado}.txt", "w", -1, "utf-8")
                for linha in resultados[resultado]:
                    arquivo.write(f"{linha}\n")

                arquivo.close()
        resultados.clear()

    def ler_arquivo(self, caminho, arquivo, extensao="txt"):
        documento = open(f"{caminho}/{arquivo}.{extensao}", "r")
        linhas = documento.readlines()
        arrayLinhas = []
        for linha in linhas:
            arrayLinhas.append(linha.strip("\n").strip(" "))

        documento.close()
        return arrayLinhas


    def clear_resultados(self):
        shutil.rmtree('Resultados')