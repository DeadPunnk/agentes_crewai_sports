# 🎮 Agentes CrewAI para Esportes

Este projeto utiliza o framework **CrewAI** para orquestrar uma equipe de agentes de inteligência artificial autônomos, especializados na análise, pesquisa e geração de insights estratégicos para o cenário de esportes do Brasil.

## 🚀 Sobre o Projeto

O objetivo é automatizar o fluxo de trabalho de análise de dados e tendências do mercado de esportes. Através da colaboração entre diferentes agentes de IA, o sistema consegue realizar desde pesquisas profundas sobre o "tabela" atual de jogos até a redação de relatórios técnicos para times e jogadores.

## 🛠️ Tecnologias Utilizadas

* **[CrewAI](https://www.crewai.com/):** Framework principal para orquestração de agentes.
* **[LangChain](https://www.langchain.com/):** Para integração com modelos de linguagem e ferramentas de busca.
* **Python:** Linguagem base do projeto.
* **OpenAI/Anthropic/Groq:** (Dependendo da sua config) Motores de LLM para processamento de linguagem natural.

## 🤖 Agentes e Fluxo de Trabalho

O projeto conta com uma estrutura de agentes especializados:

1.  **Analista de Pesquisa (Researcher):** Responsável por varrer a web, fóruns e bancos de dados em busca de atualizações de patches, transferências de jogadores e resultados de campeonatos.
2.  **Estrategista de Esportes:** Processa as informações coletadas para identificar padrões táticos e mudanças que possam ocorrer.
3.  **Redator/Editor de Conteúdo:** Compila os insights em um formato legível, seja para redes sociais, newsletters ou relatórios técnicos de performance.

## 📂 Estrutura do Repositório

* `main.py`: Ponto de entrada para execução do Crew.
* `agents.py`: Definição dos papéis, backstories e objetivos de cada agente.
* `.env.example`: Modelo para configuração de chaves de API.

## ⚙️ Como Instalar e Rodar

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/DeadPunnk/agentes_crewai_sports.git](https://github.com/DeadPunnk/agentes_crewai_sports.git)
   cd agentes_crewai_sports

   ```
