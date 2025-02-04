import pandas as pd
import os
from nba_api.stats.endpoints import TeamGameLog
import matplotlib.pyplot as plt
from datetime import datetime

def calcular_vitorias_derrotas_por_temporada(team_id=1610612751, seasons=["2023-24", "2024-25"], output_dir="reports/arquivos_csv/parte1", img_dir="reports/imagens/parte1", html_dir="reports/html/parte1"):
    """
    RF3: Apresentar o total de vitórias e derrotas do time Brooklyn Nets,
    separados por partidas jogadas em casa (mandante) e fora de casa (visitante),
    com relatórios gerados para cada temporada fornecida.

    Args:
        team_id (int): ID do Brooklyn Nets na NBA (padrão: 1610612751).
        seasons (list): Lista de temporadas no formato "AAAA-AA".
        output_dir (str): Diretório para salvar os relatórios em CSV.
        img_dir (str): Diretório para salvar os relatórios como JPG.
        html_dir (str): Diretório para salvar os relatórios como HTML.
    """
    # Garantir que os diretórios existem
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)

    # Processar cada temporada
    for season in seasons:
        print(f"Calculando vitórias e derrotas para o Brooklyn Nets na temporada {season}...")

        # Tentar acessar a API
        try:
            game_log = TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
        except Exception as e:
            print(f"Erro ao acessar a API para a temporada {season}: {e}")
            continue

        # Verificar se o DataFrame retornou dados
        if game_log.empty:
            print(f"Nenhum dado retornado para a temporada {season}.")
            continue

        # Adicionar coluna indicando vitória ou derrota
        game_log["Resultado"] = game_log["WL"].apply(lambda x: "Vitória" if x == "W" else "Derrota")

        # Adicionar coluna indicando se o jogo foi em casa ou fora
        game_log["Local"] = game_log["MATCHUP"].apply(lambda x: "Casa" if "vs." in x else "Fora")

        # Calcular totais
        total_vitorias = len(game_log[game_log["Resultado"] == "Vitória"])
        total_derrotas = len(game_log[game_log["Resultado"] == "Derrota"])

        # Vitórias e derrotas em casa
        vitorias_casa = len(game_log[(game_log["Resultado"] == "Vitória") & (game_log["Local"] == "Casa")])
        derrotas_casa = len(game_log[(game_log["Resultado"] == "Derrota") & (game_log["Local"] == "Casa")])

        # Vitórias e derrotas fora de casa
        vitorias_fora = len(game_log[(game_log["Resultado"] == "Vitória") & (game_log["Local"] == "Fora")])
        derrotas_fora = len(game_log[(game_log["Resultado"] == "Derrota") & (game_log["Local"] == "Fora")])

        # Criar DataFrame para relatório
        data = {
            "Métrica": [
                "Total de Vitórias", "Total de Vitórias em Casa", "Total de Vitórias Fora de Casa",
                "Total de Derrotas", "Total de Derrotas em Casa", "Total de Derrotas Fora de Casa"
            ],
            "Quantidade": [
                total_vitorias, vitorias_casa, vitorias_fora,
                total_derrotas, derrotas_casa, derrotas_fora
            ]
        }
        df_relatorio = pd.DataFrame(data)

        # Adicionar data de criação ao relatório
        df_relatorio["Data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Caminhos para salvar os relatórios
        output_csv_path = os.path.join("reports/arquivos_csv/parte1", f"rf3_relatorio_vitorias_derrotas_brooklyn_nets_{season}.csv")
        output_img_path = os.path.join("reports/imagens/parte1", f"rf3_relatorio_vitorias_derrotas_brooklyn_nets_{season}.jpg")
        output_html_path = os.path.join("reports/html/parte1", f"rf3_relatorio_vitorias_derrotas_brooklyn_nets_{season}.html")

        # Salvar o relatório em CSV
        df_relatorio.to_csv(output_csv_path, index=False)
        print(f"Relatório salvo em CSV: {output_csv_path}")

        # Salvar o relatório em HTML
        df_relatorio.to_html(output_html_path, index=False)
        print(f"Relatório salvo em HTML: {output_html_path}")

        # Função auxiliar para salvar tabela como imagem
        def salvar_tabela_como_imagem(df, img_path, title):
            fig, ax = plt.subplots(figsize=(8, len(df) * 0.8))  # Ajustar tamanho baseado no número de linhas
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
        salvar_tabela_como_imagem(df_relatorio, output_img_path, f"Vitórias e Derrotas - Brooklyn Nets ({season})")

    print("Processamento concluído para todas as temporadas.")

