import requests

# URL do endpoint de Classificação (Standings)
# O ID da liga 71 é comumente associado à Série A do Brasil.
# Você deve sempre verificar a documentação oficial da API-Sports.
url = "https://v3.football.api-sports.io/standings"

# Parâmetros de consulta (Query Parameters)
# É crucial especificar 'league' (o ID do Brasileirão) e 'season' (o ano).
querystring = {"league":"71","season":"2023"} # Altere o ano conforme necessário

payload={}
headers = {
  'x-apisports-key': 'ec42956ece2af22d71dd387ecc06a565',
}

# A requisição agora usa os parâmetros
response = requests.request("GET", url, headers=headers, data=payload, params=querystring)

#print(response.text)

data = json.loads(response.text)
        
        # 3. Navega para os dados da Classificação
        # A estrutura costuma ser: response[0] -> league -> standings[0] -> [Lista de Posições]
        
        # Confere se há dados
#if not data['response']:
#print("Não foi encontrada classificação para os parâmetros fornecidos.")
#  exit()
            
        # Extrai a lista de classificações (que contém todos os times)
standings_list = data['response'][0]['league']['standings'][0]
        
        # 4. Processa e extrai as informações para uma lista de dicionários simples
tabela_brasileirao = []
for team_info in standings_list:
            
            # Extrai os dados principais
  posicao = team_info['rank']
  time_nome = team_info['team']['name']
  pontos = team_info['points']
  jogos_jogados = team_info['all']['played']
  vitorias = team_info['all']['win']
  empates = team_info['all']['draw']
  derrotas = team_info['all']['lose']
  gols_pro = team_info['all']['goals']['for']
  gols_contra = team_info['all']['goals']['against']
  saldo_gols = team_info['goalsDiff']
  forma_recente = team_info['form']
  status_grupo = team_info['description'] # Ex: 'Copa Libertadores', 'Relegation'

  tabela_brasileirao.append({
                'Pos': posicao,
                'Time': time_nome,
                'Pts': pontos,
                'JJ': jogos_jogados,
                'V': vitorias,
                'E': empates,
                'D': derrotas,
                'GP': gols_pro,
                'GC': gols_contra,
                'SG': saldo_gols,
                'Forma': forma_recente,
                'Status': status_grupo
            })

        # 5. Cria o DataFrame do Pandas
  df = pd.DataFrame(tabela_brasileirao)

        # 6. Exibe o resultado
print("--- Tabela do Campeonato Brasileiro Série A ---")

#print("\nColunas: Pts=Pontos, JJ=Jogos Jogados, V=Vitórias, E=Empates, D=Derrotas, GP=Gols Pro, GC=Gols Contra, SG=Saldo de Gols.")

df.to_csv('../data/tabela_serie_A')