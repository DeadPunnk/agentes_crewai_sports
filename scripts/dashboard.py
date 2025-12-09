import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
#from langchain.chat_models import AzureChatOpenAI
from langchain_openai import AzureChatOpenAI # ✅ Importação Correta
#from langchain.schema import SystemMessage, HumanMessage
from langchain_core.messages import SystemMessage, HumanMessage # ✅ Importação Correta

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Painel de Análise do campeonato brasileiro com Chat")

# --- Título principal ---
st.title("⚽ Painel de Análises Esportivas")
st.markdown("Visão consolidada do campeonato brasileiro com análises da CrewAI")
st.divider()


# --- Carrega variáveis do ambiente ---
load_dotenv()


# --- Chatbot no topo ---
st.header("💬 Converse com o Agente")

# Initialize chat_model safely
chat_model = None
try:
    chat_model = AzureChatOpenAI(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_LLM"),
        temperature=0.3,
        azure_endpoint=os.getenv("AZURE_API_BASE"),
        api_key=os.getenv("AZURE_API_KEY"),
        openai_api_version="2025-01-01-preview"
    )
except Exception as e:
    st.error(f"Erro ao inicializar o modelo de chat: {e}")
    st.warning("As funcionalidades do chatbot estarão desabilitadas.")



contexto_chat = """
Você é o "Analista Esportivo Virtual", um assistente de IA especializado em futebol e o campeonato brasileiro, com foco em fornecer insights e análises baseadas em dados.

**Seu Perfil:**
- **Especialista em:** Campeonato brasileiro, cenario do futebol brasileiro, analises dos times (contratações, lesões, composição tatica, treinadores), análises do campeonato (foco em volume e notícias relevantes) e interpretação de notícias de futebol.
- **Seu Objetivo:** Ajudar o usuário a entender o campeonato brasileiro, responder perguntas sobre determiandos times, previsões sobre os times, previsões sobre melhores taticas e melhores opções de contratação.
- **Seu Tom:** Profissional, analítico, ponderado e educativo. Seja direto, mas completo em suas respostas.

**Contexto Campeonato brasileiro atual 2025 (use como base principal para suas respostas):**
* **Mercado do futebol brasileiro:** Contratações, compra e reforma de estadios, estado economico dos times.
* **Cenário do futebol brasileiro e Notícias.
* **Previsões sobre times favoritos para os proximos anos, quais campeonatos poderam se classificar e quem será rebaixado na proxima temporada.

**Diretrizes para suas Respostas:**
1.  **Baseie-se nos Dados:** Utilize primordialmente as informações de contexto fornecidas acima. Se uma pergunta extrapolar esses dados, mencione que a informação específica não está no seu contexto atual, mas pode oferecer uma análise geral se aplicável.
2.  **Clareza e Objetividade:** Responda de forma direta e fácil de entender.
3.  **Abordagem Consultiva:** Não se limite a responder; ofereça perspectivas, explique implicações e, quando apropriado, sugira cautela ou pontos de atenção.
6.  **Interpretação de Notícias:** Ao comentar notícias, foque nos seus potenciais impactos relacionando com o prompt do usuário.
7.  **Seja Proativo:** Se uma pergunta for simples, tente agregar valor com um breve contexto adicional relevante.

Exemplo de interação desejada:
Usuário: "Qual time tem chances de classificar para a libertadores ano que vem?"
Você: "A briga pelas vagas na Copa Libertadores de 2026 está praticamente definida via Campeonato Brasileiro de 2025, que já terminou.

Sete times garantiram suas vagas através da classificação no Brasileirão, sendo 5 direto para a fase de grupos e 2 para a fase preliminar.

Confira a lista dos times classificados:
🏆 Vagas Garantidas na Fase de Grupos

    Flamengo (Campeão da Libertadores 2025 e Campeão do Brasileirão 2025) - Vaga extra pelo título da Libertadores, que abriu mais um lugar no G-7 do Brasileirão.

    Palmeiras (Vice-campeão do Campeonato Brasileiro)

    Cruzeiro (3º colocado do Campeonato Brasileiro)

    Mirassol (4º colocado do Campeonato Brasileiro)

    Fluminense (5º colocado do Campeonato Brasileiro)

⚽ Vagas Garantidas na Fase Preliminar (Pré-Libertadores)

    Botafogo (6º colocado do Campeonato Brasileiro)

    Bahia (7º colocado do Campeonato Brasileiro)

⏳ A Última Chance: Dependendo da Copa do Brasil

Ainda existe a possibilidade de uma oitava vaga via Campeonato Brasileiro, que iria para o São Paulo (8º colocado).

    Cenário para o São Paulo se classificar:

        O Cruzeiro ou o Fluminense precisa vencer a Copa do Brasil de 2025, já que ambos já estão classificados para a Libertadores pela sua colocação no Brasileirão.

        Caso um desses times vença, a vaga destinada ao campeão da Copa do Brasil é "repassada" para o Campeonato Brasileiro, e o São Paulo garantiria o 8º lugar na fase preliminar da Libertadores, junto com o Bahia.

As semifinais da Copa do Brasil (Cruzeiro x Corinthians e Vasco x Fluminense) serão disputadas nos dias 10 e 14 de dezembro."

Agora, responda à pergunta do usuário.
"""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

pergunta_cliente = st.text_input("Digite sua pergunta sobre o campeonato brasileiro")

if pergunta_cliente and chat_model:
    mensagens = [SystemMessage(content=contexto_chat)]
    for troca in st.session_state.chat_history:
        mensagens.append(HumanMessage(content=troca["pergunta"]))
        # Langchain typically expects AIMessage for bot responses in history for some models,
        # but SystemMessage can work depending on the model and library version.
        # If issues arise, consider changing this to AIMessage for 'resposta'.
        mensagens.append(SystemMessage(content=troca["resposta"]))
    mensagens.append(HumanMessage(content=pergunta_cliente))

    try:
        resposta = chat_model.invoke(mensagens).content
        st.session_state.chat_history.append({"pergunta": pergunta_cliente, "resposta": resposta})

        st.markdown("### 🧠 Resposta do Agente:")
        st.write(resposta)
    except Exception as e:
        st.error(f"Erro ao obter resposta do agente: {e}")

elif pergunta_cliente and not chat_model:
    st.warning("O modelo de chat não está configurado. Não é possível processar a pergunta.")

if chat_model:
    with st.expander("📜 Histórico da conversa", expanded=False):
        for i, troca in enumerate(st.session_state.chat_history):
            st.markdown(f"**Você:** {troca['pergunta']}")
            st.markdown(f"**Agente:** {troca['resposta']}")
            if i < len(st.session_state.chat_history) - 1:
                 st.markdown("---")
st.divider()


# --- Funções de carregamento ---
@st.cache_data
def carregar_relatorio_md(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return f.read()
    return "Relatório não encontrado. Execute a CrewAI primeiro."

@st.cache_data
def carregar_csv(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return f"Arquivo {os.path.basename(caminho_arquivo)} não encontrado."
    try:
        df = pd.read_csv(caminho_arquivo)
        if df.empty:
            return f"Arquivo {os.path.basename(caminho_arquivo)} está vazio."
        return df
    except pd.errors.EmptyDataError: # Specific error for empty CSV
        return f"Arquivo {os.path.basename(caminho_arquivo)} não contém dados para parsear."
    except Exception as e:
        return f"Erro ao carregar {os.path.basename(caminho_arquivo)}: {e}"


# --- Caminhos dos arquivos ---
ARQUIVO_RELATORIO_ESPORTIVO= "../data/relatorio_esportivo.md"
TABELA_SERIE_A = "../data/tabela_serie_A.csv" 
ARQUIVO_NOTICIAS = "../data/noticias_esportes.csv"

# --- Painel principal ---
st.header("📊 Análises Detalhadas")
st.divider()

# --- Relatório dos agentes ---
st.subheader("🤖 Relatório da Análise dos Agentes (CrewAI)")
relatorio_agentes = carregar_relatorio_md(ARQUIVO_RELATORIO_ESPORTIVO)
with st.expander("Clique para ver o relatório completo", expanded=False):
    st.markdown(relatorio_agentes, unsafe_allow_html=True)
st.divider()

# --- Ações e Índices Econômicos em colunas ---


st.subheader("📋 Tabela do Campeonato)")
df = carregar_csv(TABELA_SERIE_A)
if isinstance(df, pd.DataFrame):

    # Display the DataFrame
   	st.subheader("Tabela do campeonato brasileiro 2025")
   	st.dataframe(df, height=300, hide_index=True) # Set height for better viewing
        


# --- Notícias Recentes ---
st.subheader("📰 Top 10 Notícias")
df_noticias = carregar_csv(ARQUIVO_NOTICIAS)
if isinstance(df_noticias, pd.DataFrame):
    if 'titulo' in df_noticias.columns and 'link' in df_noticias.columns:
        for _, row in df_noticias.head(min(10, len(df_noticias))).iterrows():
            st.markdown(f"### {row['titulo']}")
            if pd.notna(row['link']) and str(row['link']).strip() and str(row['link']).lower() not in ['nan', 'na', 'n/a']:
                st.markdown(f"[Ler notícia completa]({row['link']})")
                st.caption(f"Link: {row['link']}")
            else:
                st.caption("Link não disponível.")
            st.markdown("---")
    else:
        st.warning(f"Colunas 'titulo' e 'link' não encontradas no arquivo {os.path.basename(ARQUIVO_NOTICIAS)}. Exibindo primeiras 10 linhas se disponíveis.")
        st.dataframe(df_noticias.head(10))
elif isinstance(df_noticias, str):
    st.error(df_noticias)

# --- Rodapé ---
st.sidebar.info(f"Painel atualizado em: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}")