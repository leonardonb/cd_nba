import pandas as pd
import os
from nba_api.stats.endpoints import TeamGameLog
import matplotlib.pyplot as plt
from datetime import datetime

def calcular_totais_do_time(team_id=1610612751, seasons=["2023-24", "2024-25"], output_dir="reports/arquivos_csv/parte1", html_dir="reports/html/parte1", img_dir="reports/imagens/parte1"):
    """
    RF4: Apresentar os totais do time Brooklyn Nets, contendo:
    - Total de Pontos por Jogo
    - Total de Assistências por Jogo
    - Total de Rebotes por Jogo
    - Total de Cestas de 3 Pontos Convertidas
    - Total de Derrotas em Casa
    - Total de Derrotas Fora de Casa

    Relatórios gerados em CSV, HTML e JPG.
    """
    print("Calculando totais do time Brooklyn Nets...")

    # Garantir que os diretórios existem
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    totais_por_temporada = []

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

        # Adicionar coluna indicando se o jogo foi em casa ou fora
        game_log["Local"] = game_log["MATCHUP"].apply(lambda x: "Casa" if "vs." in x else "Fora")

        # Calcular métricas
        total_pontos = game_log["PTS"].sum()
        total_assistencias = game_log["AST"].sum()
        total_rebotes = game_log["REB"].sum()
        total_cestas_3 = game_log["FG3M"].sum()  # Field Goals Made - 3 Pointers
        derrotas_casa = len(game_log[(game_log["WL"] == "L") & (game_log["Local"] == "Casa")])
        derrotas_fora = len(game_log[(game_log["WL"] == "L") & (game_log["Local"] == "Fora")])

        # Adicionar dados para a temporada
        totais_por_temporada.append({
            "Temporada": season,
            "Total de Pontos por Jogo": total_pontos,
            "Total de Assistências por Jogo": total_assistencias,
            "Total de Rebotes por Jogo": total_rebotes,
            "Total de Cestas de 3 Pontos Convertidas": total_cestas_3,
            "Total de Derrotas em Casa": derrotas_casa,
            "Total de Derrotas Fora de Casa": derrotas_fora
        })

    # Criar DataFrame consolidado
    df_totais = pd.DataFrame(totais_por_temporada)

    # Verificar se o DataFrame está vazio
    if df_totais.empty:
        print("Nenhum dado disponível para as temporadas especificadas. Relatório não gerado.")
        return None

    # Caminhos para salvar os relatórios
    output_csv_path = os.path.join("reports/arquivos_csv/parte1", "rf4_totais_do_time_brooklyn_nets.csv")
    output_html_path = os.path.join("reports/html/parte1", "rf4_totais_do_time_brooklyn_nets.html")
    output_img_path = os.path.join("reports/imagens/parte1", "rf4_totais_do_time_brooklyn_nets.jpg")

    # Salvar o relatório em CSV
    df_totais.to_csv(output_csv_path, index=False)
    print(f"Relatório salvo em CSV: {output_csv_path}")

    # Salvar o relatório em HTML
    df_totais.to_html(output_html_path, index=False)
    print(f"Relatório salvo em HTML: {output_html_path}")

    # Função auxiliar para salvar tabela como imagem
    def salvar_tabela_como_imagem(df, img_path, title):
        fig, ax = plt.subplots(figsize=(10, len(df) * 0.8))  # Ajustar tamanho baseado no número de linhas
        ax.axis("off")
        ax.axis("tight")
        ax.set_title(title, fontsize=16, weight="bold")
        table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(df.columns))))
        plt.savefig(img_path, bbox_inches="tight", dpi=300)
        plt.close()
        print(f"Relatório salvo em JPG: {img_path}")

    # Salvar o relatório como imagem
    salvar_tabela_como_imagem(df_totais, output_img_path, "Totais do Brooklyn Nets")

    print("Processamento concluído para todas as temporadas.")
    return df_totais

# Exemplo de execução para Brooklyn Nets
calcular_totais_do_time()