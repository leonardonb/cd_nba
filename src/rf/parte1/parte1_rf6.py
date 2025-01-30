import pandas as pd
import os
from nba_api.stats.endpoints import TeamGameLog
import matplotlib.pyplot as plt
from datetime import datetime

def apresentar_performance_defensiva(team_id=1610612751, seasons=["2023-24", "2024-25"], output_dir="reports/arquivos_csv/parte1", html_dir="reports/html/parte1", img_dir="reports/imagens/parte1"):
    """
    RF6: Apresentar a performance defensiva do time, contendo:
    - Total de Roubos de Bola
    - Total de Rebotes Defensivos
    - Total de Tocos por Jogo
    - Total de Erros por Jogo
    - Total de Faltas por Jogo

    Relatórios gerados em CSV, HTML e JPG.
    """
    print("Apresentando performance defensiva do Brooklyn Nets...")

    # Garantir que os diretórios existem
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    dados_defensivos_por_temporada = []

    for season in seasons:
        print(f"Processando dados para a temporada {season}...")

        # Tentar acessar a API
        try:
            game_log = TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
        except Exception as e:
            print(f"Erro ao acessar a API para a temporada {season}: {e}")
            continue

        # Verificar se há dados
        if game_log.empty:
            print(f"Nenhum dado encontrado para a temporada {season}.")
            continue

        # Validar colunas necessárias
        colunas_necessarias = ["STL", "DREB", "BLK", "TOV", "PF"]
        if not all(col in game_log.columns for col in colunas_necessarias):
            print(f"Colunas ausentes no DataFrame para a temporada {season}: {colunas_necessarias}")
            continue

        # Calcular métricas defensivas
        total_roubos_bola = game_log["STL"].sum()
        total_rebotes_defensivos = game_log["DREB"].sum()
        media_tocos = game_log["BLK"].mean()
        media_erros = game_log["TOV"].mean()
        media_faltas = game_log["PF"].mean()

        # Adicionar dados para a temporada
        dados_defensivos_por_temporada.append({
            "Temporada": season,
            "Total de Roubos de Bola": total_roubos_bola,
            "Total de Rebotes Defensivos": total_rebotes_defensivos,
            "Média de Tocos por Jogo": round(media_tocos, 2),
            "Média de Erros por Jogo": round(media_erros, 2),
            "Média de Faltas por Jogo": round(media_faltas, 2)
        })

    # Criar DataFrame consolidado
    df_defensivo = pd.DataFrame(dados_defensivos_por_temporada)

    # Verificar se o DataFrame está vazio
    if df_defensivo.empty:
        print("Nenhum dado disponível para as temporadas especificadas. Relatório não gerado.")
        return None

    # Caminhos para salvar os relatórios
    output_csv_path = os.path.join("reports/arquivos_csv/parte1", "rf6_performance_defensiva_brooklyn_nets.csv")
    output_html_path = os.path.join("reports/html/parte1", "rf6_performance_defensiva_brooklyn_nets.html")
    output_img_path = os.path.join("reports/imagens/parte1", "rf6_performance_defensiva_brooklyn_nets.jpg")

    # Salvar o relatório em CSV
    df_defensivo.to_csv(output_csv_path, index=False)
    print(f"Relatório salvo em CSV: {output_csv_path}")

    # Salvar o relatório em HTML
    df_defensivo.to_html(output_html_path, index=False)
    print(f"Relatório salvo em HTML: {output_html_path}")

    # Função auxiliar para salvar tabela como imagem
    def salvar_tabela_como_imagem(df, img_path, title):
        fig, ax = plt.subplots(figsize=(10, len(df) * 0.5))  # Ajustar tamanho baseado no número de linhas
        ax.axis("off")
        ax.axis("tight")
        ax.set_title(title, fontsize=16, weight="bold")
        table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(df.columns))))
        plt.savefig(img_path, bbox_inches="tight", dpi=300)
        plt.close()
        print(f"Tabela salva como imagem em: {img_path}")

    # Salvar o relatório como imagem
    salvar_tabela_como_imagem(df_defensivo, output_img_path, "Performance Defensiva - Brooklyn Nets")

    print("Processamento concluído.")
    return df_defensivo

# Exemplo de execução para Brooklyn Nets
apresentar_performance_defensiva()
