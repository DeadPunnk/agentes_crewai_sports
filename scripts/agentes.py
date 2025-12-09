import os
import pandas as pd 
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import AzureChatOpenAI
from crewai_tools.tools import SerperDevTool



load_dotenv()

tool = SerperDevTool()



llm = AzureChatOpenAI(
	model='azure/'+os.getenv('AZURE_OPENAI_DEPLOYMENT_LLM'),
	azure_endpoint=os.getenv('AZURE_API_BASE'),
	api_key=os.getenv('AZURE_API_KEY'),
	api_version='2025-01-01-preview',
	temperature=0.3
	)

# === Ler os novos arquivos CSV localmente ===
try:
    df_tabela_serie_a = pd.read_csv("../data/tabela_serie_A.csv")
    df_noticias_esportes = pd.read_csv("../data/noticias_esportes.csv")
    #df_indices = pd.read_csv("data/indicadores_economicos.csv")
except FileNotFoundError as e:
    print(f"Erro: Arquivo CSV não encontrado. Verifique os nomes e caminhos dos arquivos: {e}")
    print("Certifique-se que 'tabela_serie_A.csv', 'noticias_esportes.csv' estão na raiz do projeto.")
    exit()
# === Transformar os DataFrames em texto de contexto ===
contexto_tabela_serie_a = df_tabela_serie_a.to_markdown(index=False)
#df_noticias_esportes = df_noticias_esportes.to_markdown(index=False)

# Assumindo que df_noticias_esportes '
# Ajuste se os nomes das colunas forem diferentes
contexto_noticias_esportes = "\n".join([
    f"Título: {row['titulo']}\nLink: {row['link']}"
    for _, row in df_noticias_esportes.iterrows()
]) if not df_noticias_esportes.empty else "Nenhuma notícia de esportes carregada do CSV."


# === Juntar todo o contexto BASE (dos CSVs) ===
contexto_geral_csv = f"""
=== ⚽ Tabela da serie A ===
{contexto_tabela_serie_a}

=== 📰 Notícias de Investimento Recentes (do CSV) ===
{contexto_noticias_esportes}

"""
azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_LLM")


# === Definir os agentes ===
analista_esportivo = Agent(
    role="Analista Esportivo",
    goal="Analisar o cenário do campeonato brasileiro de futebol, com foco no desempenho dos times e nos resultados das partidas, especialmente os times listadas no arquivo 'tabela_serie_A.csv'.",
    backstory="Analista esportivo com vasta experiência na análises do campeonato brasileiro, performance e desempenho dos times, jogadores e técnicos. Utiliza dados históricos e informações atualizadas para embasar suas projeções.",
    verbose=True,
    allow_delegation=False,
    tools=[tool],
    llm=llm,
    model_name=f"azure/{azure_deployment_name}"
)

especialista_em_times = Agent(
    role="Especialista em Análise dos times",
    goal="Avaliar os times do campeonato brasileiro da serie A, com ênfase na tabela do campeonato 'tabela_serie_A.csv' mas não se limitando a ela, com base na análise técnica, dados fundamentalistas (se disponíveis nos CSVs ou buscados) e notícias de futebol. Gerar previsões de vitorias, derrotas, classificações no decorrer do campeonato e previsões para os próximos anos",
    backstory="Olheiro de times focado no campeonato brasileiro da serie A, com expertise em avaliação técnica de jogadores de futebol. Busca identificar e medir o nivel técnico dos jogadores, times e técnicos, fornecendo recomendações e previsões de organização dos times nos niveis técnicos e taticos",
    verbose=True,
    allow_delegation=False, # Pode se tornar True se houver um agente de pesquisa de dados fundamentalistas dedicado
    tools=[tool],
    llm=llm,
    model_name=f"azure/{azure_deployment_name}"
)

redator_de_relatorios_esportivos= Agent(
    role="Redator de Relatórios de Esportivos",
    goal="Consolidar as análises dos times, partidas e nivel técnico em um relatório final claro, conciso e bem estruturado para amantes do esporte. O relatório deve destacar as principais indicações de taticas, situação dos jogadores, situação do time e previsões para o campeonato e futuro do time, incluindo jogadores e técnicos",
    backstory="Profissional de comunicação com foco no futebol brasileiro, especializado em transformar análises técnicas complexas em relatórios de fácil compreensão para o público amante do esporte.",
    verbose=True,
    allow_delegation=False,
    tools=[],
    llm=llm,
    model_name=f"azure/{azure_deployment_name}"
)


# === Criar as tarefas ===

tarefa_analise_cenario = Task(
    description=(
        "1. Analise os dados das partidas realizadsa no campeonato brasileiro 2025\n"
        "2. Revise as 'Notícias de esportes (do CSV)' para capturar o sentimento e os eventos atuais do mercado.\n"
        "3. Utilize a ferramenta SerPerDevTool para buscar informações atualizadas (últimos 1-3 meses) sobre: "
        "a) Perspectivas para os times do campeonato nos proximos anos. "
        "b) Principais indicações sobre o desempenho do time. "
        "c) Notícias relevantes sobre o campeonato brasileiro 2025 que possa impactar os rsultados e os times.\n"
        "4. Sintetize essas informações para construir um panorama do cenário do campeonato brasileiro atual e suas implicações para os proximos anos, indicanco quem é o favorito para ganhar a competição.\n\n"
    ),
    expected_output=(
        "Um relatório conciso sobre o cenário do campeonato brasileiro, destacando: \n"
        "- Análise da trajetória recente dos principais times da serie A de 2025.\n"
        "- Principais notícias e eventos do campeonato brasileiro 2025 (do CSV e da pesquisa online).\n"
        "- Impactos esperados desse cenário no futebol brasileiro em geral."
    ),
    agent=analista_esportivo,
    #context=[contexto_tabela_serie_a]
)

tarefa_indicacao = Task(
    description=(
        "1. Com base na análise do cenário do campeonato brasileiro (fornecido pela tarefa anterior), avalie os times listadas no arquivo 'tabela_serie_A.csv'.\n"
        "2. Para cada time na 'tabela_serie_A.csv', utilize a ferramenta SerperDevTool para buscar: "
        "a) Notícias recentes e específicas sobre o time. "
        "b) Análises e perspectivas par ao time: jogadores, técnicos, lesões, contratações, penalidades. "
        "3. Se julgar pertinente, pesquise também outros times do campeonato que possam representar chances de impactar a serie A do campeonato.\n"
        "4. Formule recomendações e previsões sobre os times (escalação, posicionamento tatico ou contratações). Cada recomendação deve ser acompanhada de uma justificativa clara, baseada na análise dos times, notícias e dados do campeonato.\n\n"
        "Contexto dos CSVs (especialmente 'Tabela da serie A'):\n"
        f"{contexto_tabela_serie_a}" # Foco principal, mas não exclusivo
    ),
    expected_output=(
        "Um relatório de indicações e previsões do campeonato brasileiro contendo:\n"
        "- Previsões de resultados, contratações, taticas, previsão para o desempenho dos times.\n"
        "- Justificativa detalhada para cada recomendação ou previsão, explicando os fatores considerados (tatica, lesões, contratações, penalizações)."
        "Priorizar as ações do 'tabela_serie_A.csv' na análise, mas incluir outras se forem identificadas oportunidades/riscos relevantes."
    ),
    agent=especialista_em_times,
    context=[tarefa_analise_cenario] # Depende da análise 
)

tarefa_compilacao_relatorio_final = Task(
    description=(
        "**Sua responsabilidade é GERAR e ESCREVER O CONTEÚDO COMPLETO do relatório ddo campeonato final em formato markdown. NÃO descreva o que você faria ou o que o relatório conteria; em vez disso, PRODUZA o relatório AGORA.**\n\n"
        "Para fazer isso, você DEVE:\n"
        "1. Unificar a 'análise do cenário do campeonato brasileiro' (fornecida pelo Analista Esportivoso) e as 'indicações e previsões' (fornecidas pelo Especialista em Times) em um relatório final coeso, detalhado e bem formatado.\n"
        "2. Escrever o relatório em linguagem clara, profissional e acessível para amantes do esporte, utilizando a sintaxe markdown para uma excelente estrutura (títulos H2 e H3, subtítulos, listas com marcadores ou numeradas, negrito para destaques).\n"
        "3. Detalhar as principais conclusões da análise do campeonato brasileiro e explicar explicitamente como elas fundamentam as estratégias de investimento e as recomendações de ações específicas.\n"
        "4. Apresentar de forma proeminente e individualizada cada indicação de ação (mudança tetica, contratação, previsão~, escalação).\n"
        "**Utilize as informações das análises das tarefas anteriores, que estão disponíveis no contexto, como base fundamental para escrever este relatório.**"
    ),
    expected_output=(
        "O TEXTO COMPLETO e FINAL de um Relatório do campeonato brasileiro em formato markdown na língua portuguesa do brasil. O relatório DEVE ser abrangente e conter as seguintes seções PREENCHIDAS com análises, dados e texto gerado:\n"
        "### Sumário\n"
        "   - (Texto do sumário com as principais conclusões e recomendações ou previsões.)\n"
        "### Análise do Cenário do campeonato\n"
        "   - (Texto da análise detalhada dos indicadores economicos, notícias relevantes e seus impactos esperados no mercado de ações.)\n"
        "### Indicações de Ações Detalhadas para os times\n"
        "   - (Para cada ação recomendada: mudança tatica, escalação, contratação, previsão de desempenho, e Justificativa completa e bem fundamentada.)\n"
        "### Breves Considerações sobre Riscos e Oportunidades\n"
        "   - (Texto com uma visão geral dos riscos e oportunidades identificados no cenário atual.)\n"
        "### Apêndice: Fontes de Dados\n"
        "   - (Texto mencionando as fontes de dados utilizadas.)"
    ),
    agent=redator_de_relatorios_esportivos,
    context=[tarefa_analise_cenario, tarefa_indicacao],
)


# === Criar o time (Crew) ===
crew_recomendacoes_esportivas = Crew(
    agents=[analista_esportivo, especialista_em_times, redator_de_relatorios_esportivos],
    tasks=[tarefa_analise_cenario, tarefa_indicacao, tarefa_compilacao_relatorio_final],
    verbose=True, # verbose=True para ver os pensamentos dos agentes
    manager_llm=llm,
    #process=Process.hierarchical, # Habilita o "gerente" para orquestrar com mais "raciocínio"
)


# === Executar o Crew ===
print("Iniciando a análise da Crew para recomendação de ações...")
resultado_crew = crew_recomendacoes_esportivas.kickoff() # Mudei o nome da variável para clareza

print("\n\n=== OBJETO CrewOutput COMPLETO (para depuração) ===\n")
print(resultado_crew) # Isso vai mostrar a estrutura do objeto CrewOutput


# Tente acessar o resultado textual. A forma exata pode variar um pouco
# dependendo da versão do CrewAI e do que a sua Crew retorna.
# Tentativa 1: Acessar um atributo 'result' ou 'raw' se o objeto for um Pydantic model
# ou tiver um atributo específico para o output textual.
# Vamos testar com str() primeiro, que é mais genérico.
if hasattr(resultado_crew, 'raw') and isinstance(resultado_crew.raw, str):
    texto_para_salvar = resultado_crew.raw
elif hasattr(resultado_crew, 'result') and isinstance(resultado_crew.result, str): # Comum em versões mais antigas ou específicas
    texto_para_salvar = resultado_crew.result
else:
    # Se não houver um atributo óbvio, converter o objeto todo para string
    # pode funcionar se o __str__ do CrewOutput for o relatório final.
    texto_para_salvar = str(resultado_crew)

print("\n\n=== RELATÓRIO FINAL DE INVESTIMENTO GERADO PELA CREW (TEXTO) ===\n")
print(texto_para_salvar)


# Salvar o resultado em um arquivo .md ===
nome_arquivo_saida = "../data/relatorio_esportivo.md"
with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
    f.write(texto_para_salvar) # Agora estamos passando uma string
print(f"\n\nRelatório salvo em '{nome_arquivo_saida}'")