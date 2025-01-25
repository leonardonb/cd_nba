# Importar funções de outros RFs
# import relatorio

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
listar_times_conferencia(output_dir, "reports/html/parte1", img_dir)

# Parte 01 RF2: Apresentar classificação atual
print("Executando RF2: Apresentar classificação atual dos times...")
apresentar_classificacao_atual(output_dir, "reports/html/parte1", img_dir)

# Parte 01 RF3: Calcular vitórias e derrotas
print("Executando RF3: Calcular vitórias e derrotas do time...")
calcular_vitorias_derrotas_por_temporada(team_id, seasons, output_dir, img_dir)

# Parte 01 RF4: Calcular totais do time
print("Executando RF4: Calcular totais do time por temporada...")
calcular_totais_do_time(team_id, seasons, output_dir, "reports/html/parte1", img_dir)

# Parte 01 RF5: Apresentar divisão de dados do time
print("Executando RF5: Divisão de dados do time...")
apresentar_dados_divididos(
    team_id=team_id,
    seasons=seasons,
    output_dir=output_dir,
    html_dir="reports/html/parte1",
    img_dir=img_dir
)

# Parte 01 RF6: Apresentar os dados referentes a performance defensiva do time
print("Executando RF6: Performance defensiva do time...")
apresentar_performance_defensiva(
    team_id=1610612751,
    seasons=["2023-24", "2024-25"],
    output_dir="reports/arquivos_csv",
    html_dir="reports/html/parte1",
    img_dir="reports/imagens"
)

# Parte 01 RF7: Apresentar jogos do Time
print("Executando RF7: Apresentar jogos do time...")

# Diretório base para saída
base_output_dir = "reports"

# Executar o RF7 e salvar os resultados
dados_nets = apresentar_jogos_do_time(team_abbr, seasons, base_output_dir)

# Exibir as primeiras linhas do DataFrame processado
print("Dados do RF7 processados:")
print(dados_nets.head())

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

print("Processamento concluído.")