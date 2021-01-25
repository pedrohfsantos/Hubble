# Hubble

Script criado para monitorar projetos no ar.

Pontos validados:

* IP do site
* SSL
* Analysts
* Redirect
* Sitemap

## Configuração e preparação do ambiente

* Instale o Python >= 3.6 na sua máquina. [importante]
* Siga o passo-passo abaixo, e instale todas as bibliotecas utilizando o comando "pip install" no cmd.


## Pacotes para instalar

```bash
pip install tqdm
pip install schedule
pip install requests-html
```

## Como usar o Script
Para executar o script é preciso informar em Config/dominios.txt a lista de domínios que serão validados, também é preciso informar a lista de IP dos servidores no arquivo Config/ip.txt, essa lista sera usada para comparar se o projeto está dentro desses servidores.