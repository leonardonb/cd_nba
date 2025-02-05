from src.rf.parte1.parte1_rf1 import listar_times_conferencia
from src.rf.parte1.parte1_rf2 import apresentar_classificacao_atual
from src.rf.parte1.parte1_rf3 import calcular_vitorias_derrotas_por_temporada
from src.rf.parte1.parte1_rf4 import calcular_totais_do_time
from src.rf.parte1.parte1_rf5 import apresentar_dados_divididos
from src.rf.parte1.parte1_rf6 import apresentar_performance_defensiva
from src.rf.parte1.parte1_rf7 import apresentar_jogos_do_time
from src.rf.parte1.parte1_rf8 import rf_graficos_desempenho_brooklyn_nets
from src.rf.parte2.parte2_rf1 import apresentar_dados_jogadores
from src.rf.parte2.parte2_rf2 import apresentar_dados_partidas_time_por_id
from src.rf.parte2.parte2_rf3 import apresentar_dados_partidas_contra_time
from src.rf.parte2.parte2_rf4 import apresentar_dados_jogos_casa_fora
from src.rf.parte2.parte2_rf5 import calcular_e_apresentar_medias
from src.rf.parte2.parte2_rf6 import calcular_e_apresentar_medianas
from src.rf.parte2.parte2_rf7 import calcular_e_apresentar_modas
from src.rf.parte2.parte2_rf8 import calcular_e_apresentar_desvios
from src.rf.parte2.parte2_rf9 import apresentar_totais_carreira
from src.rf.parte2.parte2_rf10 import comparar_estatisticas
from src.rf.parte3.parte3_rf1 import aplicar_metodo_gumbel
from src.rf.parte3.parte3_rf2 import visualizando_metodo_gumbel
from src.data.limpeza_dados import tratar_dados_jogadores, adicionar_informacoes_placar
from src.data.coleta_dados import coletar_dados_time

import pandas as pd
import os
import pdfkit

# Configurações do projeto
team_id = 1610612751  # ID do Brooklyn Nets
team_abbr = "BRK"  # Abreviação do Brooklyn Nets
seasons = ["2023-24", "2024-25"]
output_dir = "reports/arquivos_csv"
html_dir = "reports/html"
img_dir = "reports/imagens"

# Criar diretórios de saída
os.makedirs(output_dir, exist_ok=True)
os.makedirs(html_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)

player_names = ["Cam Thomas", "Cameron Johnson", "D'Angelo Russell"]

players = [
    {'PLAYER': 'Cam Thomas', 'PLAYER_ID': 1630560},
    {'PLAYER': 'Cameron Johnson', 'PLAYER_ID': 1629661},
    {'PLAYER': 'D\'Angelo Russell', 'PLAYER_ID': 1626156}
]

# Parte 01 RF1: Listar times por conferência
print("Executando RF1: Listar times por conferência...")
listar_times_conferencia("reports/imagens/parte1/parte1", "reports/html/parte1", "reports/imagens/parte1")

# Parte 01 RF2: Apresentar classificação atual
print("Executando RF2: Apresentar classificação atual dos times...")
apresentar_classificacao_atual("reports/imagens/parte1/parte1", "reports/html/parte1", "reports/imagens/parte1")

# Parte 01 RF3: Calcular vitórias e derrotas
print("Executando RF3: Calcular vitórias e derrotas do time...")
calcular_vitorias_derrotas_por_temporada(team_id, seasons, "reports/imagens/parte1/parte1", "reports/imagens/parte1")

# Parte 01 RF4: Calcular totais do time
print("Executando RF4: Calcular totais do time por temporada...")
calcular_totais_do_time(team_id, seasons, "reports/imagens/parte1/parte1", "reports/html/parte1", "reports/imagens/parte1")

# Parte 01 RF5: Apresentar divisão de dados do time
print("Executando RF5: Divisão de dados do time...")
apresentar_dados_divididos(
    team_id=team_id,
    seasons=seasons,
    output_dir="reports/imagens/parte1/parte1",
    html_dir="reports/html/parte1",
    img_dir="reports/imagens/parte1"
)

# Parte 01 RF6: Apresentar os dados referentes a performance defensiva do time
print("Executando RF6: Performance defensiva do time...")
apresentar_performance_defensiva(
    team_id=1610612751,
    seasons=["2023-24", "2024-25"],
    output_dir="reports/imagens/parte1/parte1",
    html_dir="reports/html/parte1",
    img_dir="reports/imagens/parte1"
)

# Parte 01 RF7: Apresentar jogos do Time
print("Executando RF7: Apresentar jogos do time...")

# Diretório base para saída
base_output_dir = "reports/imagens/parte1"

# Executar o RF7 e salvar os resultados
dados_nets = apresentar_jogos_do_time(team_abbr, seasons, base_output_dir)

# Parte 1 RF8: Gráficos de desempenho do Brooklyn Nets
print("Executando RF8: Gerar gráficos de desempenho do Brooklyn Nets...")

# Chamada da função para gerar gráficos usando a API
rf_graficos_desempenho_brooklyn_nets(
    team_id=1610612751,  # ID do Brooklyn Nets
    seasons=["2023-24", "2024-25"],  # Temporadas para coletar dados
    output_dir="reports/graficos/parte1"  # Diretório para salvar os gráficos gerados
)

print("RF8 concluído: Gráficos gerados com sucesso.")

# Parte 2, RF1: Apresentar os dados dos Jogadores
print("Executando P2-RF1: Apresentar dados dos jogadores...")
apresentar_dados_jogadores(
    player_names, 
    output_dir="reports/arquivos_csv/parte2/parte2-rf1",
    html_dir="reports/html/parte2/parte2-rf1",
    img_dir="reports/imagens/parte2/parte2-rf1"
)

# Parte 2, RF2: Apresentar os dados de cada jogador do time
print("Executando P2-RF2: Apresentar dados de cada jogador do time...")
apresentar_dados_partidas_time_por_id(
    team_id, 
    output_dir="reports/arquivos_csv/parte2/parte2-rf2", 
    html_dir="reports/html/parte2/parte2-rf2", 
    img_dir="reports/imagens/parte2/parte2-rf2"
)

# Parte 2, RF3: Fornecer dados da partida contra time que o usuário escolher
print("Executando P2-RF3: Apresentar dados da partida contra o time selecionado...")
apresentar_dados_partidas_contra_time(
    opponent_abbr="LAL",
    output_dir="reports/arquivos_csv/parte2/parte2-rf3",
    html_dir="reports/html/parte2/parte2-rf3",
    img_dir="reports/imagens/parte2/parte2-rf3"
)

# Parte 2, RF4: Apresentar a quantidade de jogos realizados dentro e fora de casa e a quantidade de jogos dentro e fora de casa contra um determinado time [da escolha do  usuário]. 
print("Executando P2-RF4: Apresentando jogos dentro e fora de casa dos jogadores e contra um time selecionado...")
apresentar_dados_jogos_casa_fora(
    opponent_abbr="PHI",
    output_dir="reports/arquivos_csv/parte2/parte2-rf4",
    html_dir="reports/html/parte2/parte2-rf4",
    img_dir="reports/imagens/parte2/parte2-rf4"
)

# Parte 2, RF5: Apresentar e calcular a média de pontos, rebotes e assistências dos jogadores
# Parte 2, RF5-A: Apresentar ao usuário a porcentagem de pontos, rebotes e assistências abaixo da média  
print("Executando P2-RF5: Apresentando e calculando média de pontos, rebotes e assistências dos jogadores, e também as porcentagens abaixo da média...")
calcular_e_apresentar_medias(
    players, 
    output_dir = "reports/arquivos_csv/parte2/parte2-rf5",
    html_dir="reports/html/parte2/parte2-rf5",
    img_dir="reports/imagens/parte2/parte2-rf5"
)

# Parte 2, RF6: Apresentar e calcular a mediana de pontos, rebotes e assistências dos jogadores. 
# Parte 2, RF6-A: Apresentar ao usuário a porcentagem de pontos, rebotes e assistências abaixo da mediana  
print("Executando P2-RF6: Apresentando e calculando mediana de pontos, rebotes e assistências dos jogadores, e também as porcentagens abaixo da mediana...")
calcular_e_apresentar_medianas(
    players, 
    output_dir = "reports/arquivos_csv/parte2/parte2-rf6",
    html_dir="reports/html/parte2/parte2-rf6",
    img_dir="reports/imagens/parte2/parte2-rf6"
)

# Parte2, RF7: Apresentar e calcular a moda de pontos, rebotes e assistências dos jogadores. Exibir a quantidade de vezes que a moda aparece para cada item. 
# Parte2, RF7-A: Apresentar ao usuário a porcentagem de pontos, rebotes e assistências abaixo da média.
print("Executando P2-RF7: Apresentando e calculando moda de pontos, rebotes e assistências dos jogadores, e também as porcentagens abaixo da média...")
calcular_e_apresentar_modas(
    players,
    output_dir = "reports/arquivos_csv/parte2/parte2-rf7",
    html_dir="reports/html/parte2/parte2-rf7",
    img_dir="reports/imagens/parte2/parte2-rf7"
)

# Parte2, RF8: Apresentar o Desvio Padrão de pontos, rebotes e assistências dos jogadores.  Quanto mais próximo de zero, mais agrupado em torno da média os dados estão. 
print("Executando P2-RF8: Apresentar o Desvio Padrão de pontos, rebotes e assistências dos jogadores...")
calcular_e_apresentar_desvios(
    players,
    output_dir = "reports/arquivos_csv/parte2/parte2-rf8",
    html_dir="reports/html/parte2/parte2-rf8",
    img_dir="reports/imagens/parte2/parte2-rf8"
)

# Parte2, RF9: O sistema deve apresentar a quantidade de pontos, assistências e rebotes de toda a  carreira do jogador. 
print("Executando P2-RF9: Apresentando a quantidade de pontos, assistências e rebotes de toda a carreira dos jogadores... ")
apresentar_totais_carreira(
    players,
    output_dir = "reports/arquivos_csv/parte2/parte2-rf9",
    html_dir="reports/html/parte2/parte2-rf9",
    img_dir="reports/imagens/parte2/parte2-rf9"
)

# Parte 2, RF10: O sistema deve apresentar a quantidade de pontos, assistências e rebotes de toda a carreira do jogador e comparada com a atual temporada.
# Parte 2, RF10-A: Apresentar gráficos de desempenho dos seus jogadores [temporada atual] para compor o Dashboard do projeto.
print("Executando P2-RF10: Apresentando a quantidade de pontos, assistências e rebotes de toda a carreira dos jogadores e comparando com a atual, e gerando os gráficos para o Dashboard... ")
comparar_estatisticas(
    players,
    output_dir="reports/arquivos_csv/parte2/parte2-rf10",
    html_dir="reports/html/parte2/parte2-rf10",
    img_dir="reports/imagens/parte2/parte2-rf10"
)

# Parte 3, RF1: Precisamos modelar e prever eventos extremos, assim precisamos verificar em cima dos dados que possuímos as probabilidades de ocorrência de pontuação, assistências e rebotes máximos e mínimos.
print("Executando P3-RF1: Modelagem de eventos extremos usando Gumbel...")
csv_paths = {
    "Cam Thomas": "./reports/arquivos_csv/parte2/parte2-rf2/Cam Thomas_dados_partidas.csv",
    "Cameron Johnson": "./reports/arquivos_csv/parte2/parte2-rf2/Cameron Johnson_dados_partidas.csv",
    "D'Angelo Russell": "./reports/arquivos_csv/parte2/parte2-rf2/D'Angelo Russell_dados_partidas.csv"
}

df_cam_thomas = pd.read_csv(csv_paths["Cam Thomas"])
df_cameron_johnson = pd.read_csv(csv_paths["Cameron Johnson"])
df_dangelo_russell = pd.read_csv(csv_paths["D'Angelo Russell"])
    
valores_x = {
    'PTS': 20,
    'REB': 15,
    'AST': 10
}
valores_y = {
    'PTS': 15,
    'REB': 10,
    'AST': 5
}
valores_z = {
    'PTS': 25,
    'REB': 20,
    'AST': 15
}

cam = aplicar_metodo_gumbel(df_cam_thomas, valores_x)
camerom = aplicar_metodo_gumbel(df_cameron_johnson, valores_y)
dangelo = aplicar_metodo_gumbel(df_dangelo_russell, valores_z)

# Parte 3 RF2: Apresente gráficos que facilitem a visualização dos extremos e das  respostas as perguntas realizadas no RF1. Use gráficos do seu interesse. 
print("Executando P3-RF2: Apresentando os gráficos referentes aos resultados obitidos da Parte3-RF1...")
visualizando_metodo_gumbel(
    cam,
    "Cam Thomas",
    output_dir="./reports/graficos/parte3/parte3-rf2"
)
visualizando_metodo_gumbel(
    camerom,
    "Cameron Johnson",
    output_dir="./reports/graficos/parte3/parte3-rf2"
)
visualizando_metodo_gumbel(
    dangelo,
    "D'Angelo Russell",
    output_dir="./reports/graficos/parte3/parte3-rf2"
)


print("Processamento concluído.")