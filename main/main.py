# main.py

import os

print("📋 Tabela da serie A...")
os.system("python scripts/tabela_serie_A.py")

print("📰 Executando coleta de notícias sobre esportes...")
os.system("python scripts/noticias.py")

print("🧠 Executando análise dos agentes econômicos (CrewAI)...")
os.system("python scripts/agentes.py")

print("🚀 Iniciando dashboard Streamlit...")
os.system("streamlit run streamlit/dashboard.py")