import pandas as pd
import os
from nba_api.stats.endpoints import TeamGameLog
import matplotlib.pyplot as plt
from datetime import datetime

def apresentar_dados_divididos(team_id=1610612751, seasons=["2023-24", "2024-25"], output_dir="reports/arquivos_csv", html_dir="reports/graficos_html", img_dir="reports/imagens"):
    """
    RF5: Divisão de dados do time, contendo:
    - Total de Rebotes
    - Total de Rebotes Ofensivos
    - Total de Rebotes Defensivos
    - Total de Pontos
    - Total de Cestas de 2 Pontos
    - Total de Cestas de 3 Pontos
    - Total de Lance Livre

    Relatórios gerados em CSV, HTML e JPG.
    """
    print("Apresentando divisão de dados do Brooklyn Nets...")

    # Garantir que os diretórios existem
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    dados_divididos_por_temporada = []

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
        colunas_necessarias = ["REB", "OREB", "DREB", "PTS", "FGM", "FG3M", "FTM"]
        if not all(col in game_log.columns for col in colunas_necessarias):
            print(f"Colunas ausentes no DataFrame para a temporada {season}: {colunas_necessarias}")
            continue

        # Calcular métricas
        total_rebotes = game_log["REB"].sum()
        rebotes_ofensivos = game_log["OREB"].sum()
        rebotes_defensivos = game_log["DREB"].sum()
        total_pontos = game_log["PTS"].sum()
        cestas_2_pontos = game_log["FGM"].sum() - game_log["FG3M"].sum()  # Total de cestas - cestas de 3
        cestas_3_pontos = game_log["FG3M"].sum()
        lances_livres = game_log["FTM"].sum()

        # Adicionar dados para a temporada
        dados_divididos_por_temporada.append({
            "Temporada": season,
            "Total de Rebotes": total_rebotes,
            "Total de Rebotes Ofensivos": rebotes_ofensivos,
            "Total de Rebotes Defensivos": rebotes_defensivos,
            "Total de Pontos": total_pontos,
            "Total de Cestas de 2 Pontos": cestas_2_pontos,
            "Total de Cestas de 3 Pontos": cestas_3_pontos,
            "Total de Lances Livres": lances_livres
        })

    # Criar DataFrame consolidado
    df_dados = pd.DataFrame(dados_divididos_por_temporada)

    # Verificar se o DataFrame está vazio
    if df_dados.empty:
        print("Nenhum dado disponível para as temporadas especificadas. Relatório não gerado.")
        return None

    # Caminhos para salvar os relatórios
    output_csv_path = os.path.join(output_dir, "rf5_dados_divididos_brooklyn_nets.csv")
    output_html_path = os.path.join(html_dir, "rf5_dados_divididos_brooklyn_nets.html")
    output_img_path = os.path.join(img_dir, "rf5_dados_divididos_brooklyn_nets.jpg")

    # Salvar o relatório em CSV
    df_dados.to_csv(output_csv_path, index=False)
    print(f"Relatório salvo em CSV: {output_csv_path}")

    # Salvar o relatório em HTML
    df_dados.to_html(output_html_path, index=False)
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
    salvar_tabela_como_imagem(df_dados, output_img_path, "Divisão de Dados - Brooklyn Nets")

    print("Processamento concluído.")
    return df_dados

# Exemplo de execução para Brooklyn Nets
apresentar_dados_divididos()