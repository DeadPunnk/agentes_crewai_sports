import requests
from bs4 import BeautifulSoup
import pandas as pd
# Script para coletar notícias de economia e investimentos
palavras_chave = [
    'futebol', 'gol', 'pontos', 'campeonato', 'campeão', 'jogos', 'pontos', 'gols', 'lesão', 'São Paulo', 'Corinthians', 
    'Flamengo', 'Palmeiras', 'Cruzeiro', 'Atletico Mineiro', 'Fluminense', 'Serie A', 'Serie B', 'Serie C', 'Base',
    'Vasco', 'Ceilandia', 'Candangão', 'Samambaia', 'Brasiliense', 'Mirasol' 
]

headers = {'User-Agent': 'Mozilla/5.0'}

sites = {
    'DF Esportes': 'https://dfesportes.com/',
    'Globo Esporte': 'https://ge.globo.com/',
    'ESPN': 'https://www.espn.com.br',
    'SBT Sportes': 'https://sports.sbt.com.br/'
}

noticias = []

def filtrar_noticias(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    encontrados = []
    for a in soup.find_all("a", href=True):
        titulo = a.get_text().strip().lower()
        link = a["href"]
        if any(p in titulo for p in palavras_chave):
            if titulo and link.startswith("http"):
                encontrados.append({"titulo": titulo.title(), "link": link})
            elif titulo and link.startswith("/"):
                encontrados.append({"titulo": titulo.title(), "link": base_url + link})
    return encontrados

for nome_site, url in sites.items():
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            base_url = "/".join(url.split("/")[:3])
            noticias += filtrar_noticias(resp.text, base_url)
        else:
            print(f"[!] Erro ao acessar {nome_site}: Status {resp.status_code}")
    except Exception as e:
        print(f"[!] Falha ao acessar {nome_site}: {e}")



# Remover duplicadas
noticias_unicas = list({n["titulo"]: n for n in noticias}.values())
# Salvar CSV
df = pd.DataFrame(noticias_unicas)

print(f"✅ CSV gerado com {len(df)} notícias: noticias_esportes.csv")

df.to_csv("../data/noticias_esportes.csv", index=False, encoding="utf-8-sig")


