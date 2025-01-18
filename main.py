# Importar funções de outros RFs
from src.rf.rf1 import listar_times_conferencia
from src.rf.rf2 import apresentar_classificacao_atual
from src.rf.rf3 import calcular_vitorias_derrotas_por_temporada
from src.rf.rf4 import calcular_totais_do_time
from src.rf.rf5 import apresentar_dados_divididos
from src.rf.rf6 import apresentar_performance_defensiva


import pandas as pd
import os

# Configurações do projeto
team_id = 1610612751  # ID do Brooklyn Nets
seasons = ["2023-24", "2024-25"]
output_dir = "reports/arquivos_csv"
html_dir = "reports/graficos_html"
img_dir = "reports/imagens"

# Criar diretórios de saída
os.makedirs(output_dir, exist_ok=True)
os.makedirs(html_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)

# RF1: Listar times por conferência
print("Executando RF1: Listar times por conferência...")
listar_times_conferencia(output_dir, html_dir, img_dir)

# RF2: Apresentar classificação atual
print("Executando RF2: Apresentar classificação atual dos times...")
apresentar_classificacao_atual(output_dir, html_dir, img_dir)

# RF3: Calcular vitórias e derrotas
print("Executando RF3: Calcular vitórias e derrotas do time...")
calcular_vitorias_derrotas_por_temporada(team_id, seasons, output_dir, img_dir)

# RF4: Calcular totais do time
print("Executando RF4: Calcular totais do time por temporada...")
calcular_totais_do_time(team_id, seasons, output_dir, html_dir, img_dir)

# RF5: Apresentar divisão de dados do time
print("Executando RF5: Divisão de dados do time...")
apresentar_dados_divididos(
    team_id=team_id,
    seasons=seasons,
    output_dir=output_dir,
    html_dir=html_dir,
    img_dir=img_dir
)

# RF6: Apresentar os dados referentes a performance defensiva do time
print("Executando RF6: Performance defensiva do time...")
apresentar_performance_defensiva(
    team_id=1610612751,
    seasons=["2023-24", "2024-25"],
    output_dir="reports/arquivos_csv",
    html_dir="reports/graficos_html",
    img_dir="reports/imagens"
)

print("Processamento concluído.")