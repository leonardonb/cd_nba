import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
from nba_api.stats.endpoints import TeamGameLog

# Função para salvar a tabela como imagem
def salvar_tabela_como_imagem(df, img_path, title):
    fig, ax = plt.subplots(figsize=(8, len(df) * 0.8))
    ax.axis("off")
    ax.axis("tight")
    ax.set_title(title, fontsize=14, weight="bold")
    table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(img_path, bbox_inches="tight", dpi=300)
    plt.close()

# Função principal para processar as temporadas
def processar_temporadas(team_id=1610612751, seasons=["2023-24", "2024-25"], output_dir="reports/arquivos_csv/parte1", img_dir="reports/imagens/parte1", html_dir="reports/html/parte1"):
    # Garantir que os diretórios existem
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)

    # Processar cada temporada
    for season in seasons:
        print(f"Processando a temporada {season}...")

        try:
            game_log = TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
        except Exception as e:
            print(f"Erro ao acessar a API para a temporada {season}: {e}")
            continue

        if game_log.empty:
            print(f"Nenhum dado encontrado para a temporada {season}.")
            continue

        # Adicionar colunas de resultado e local do jogo
        game_log["Resultado"] = game_log["WL"].apply(lambda x: "Vitória" if x == "W" else "Derrota")
        game_log["Local"] = game_log["MATCHUP"].apply(lambda x: "Casa" if "vs." in x else "Fora")

        # Calcular totais
        total_vitorias = len(game_log[game_log["Resultado"] == "Vitória"])
        total_derrotas = len(game_log[game_log["Resultado"] == "Derrota"])
        vitorias_casa = len(game_log[(game_log["Resultado"] == "Vitória") & (game_log["Local"] == "Casa")])
        derrotas_casa = len(game_log[(game_log["Resultado"] == "Derrota") & (game_log["Local"] == "Casa")])
        vitorias_fora = len(game_log[(game_log["Resultado"] == "Vitória") & (game_log["Local"] == "Fora")])
        derrotas_fora = len(game_log[(game_log["Resultado"] == "Derrota") & (game_log["Local"] == "Fora")])

        # Criar DataFrame do relatório de resumo
        df_resumo = pd.DataFrame({
            "Métrica": [
                "Total de Vitórias", "Total de Vitórias em Casa", "Total de Vitórias Fora de Casa",
                "Total de Derrotas", "Total de Derrotas em Casa", "Total de Derrotas Fora de Casa"
            ],
            "Quantidade": [total_vitorias, vitorias_casa, vitorias_fora, total_derrotas, derrotas_casa, derrotas_fora],
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Salvar relatório resumo em CSV, HTML e JPG
        resumo_csv_path = os.path.join(output_dir, f"rf3_resumo_brooklyn_nets_{season}.csv")
        resumo_html_path = os.path.join(html_dir, f"rf3_resumo_brooklyn_nets_{season}.html")
        resumo_img_path = os.path.join(img_dir, f"rf3_resumo_brooklyn_nets_{season}.jpg")

        df_resumo.to_csv(resumo_csv_path, index=False, encoding="utf-8-sig")
        df_resumo.to_html(resumo_html_path, index=False)
        salvar_tabela_como_imagem(df_resumo, resumo_img_path, f"Vitórias e Derrotas - Brooklyn Nets ({season})")

        # Criar DataFrame do relatório detalhado por adversário
        df_detalhado = pd.DataFrame({
            "Adversário": game_log["MATCHUP"].str.split(" ").str[-1],
            "Data": game_log["GAME_DATE"],
            "Casa": game_log.apply(lambda x: 1 if (x["Local"] == "Casa" and x["Resultado"] == "Vitória") else (-1 if (x["Local"] == "Casa" and x["Resultado"] == "Derrota") else 0), axis=1),
            "Fora": game_log.apply(lambda x: 1 if (x["Local"] == "Fora" and x["Resultado"] == "Vitória") else (-1 if (x["Local"] == "Fora" and x["Resultado"] == "Derrota") else 0), axis=1)
        })

        # Salvar relatório detalhado em CSV, HTML e JPG
        detalhado_csv_path = os.path.join(output_dir, f"rf3_detalhado_brooklyn_nets_{season}.csv")
        detalhado_html_path = os.path.join(html_dir, f"rf3_detalhado_brooklyn_nets_{season}.html")
        detalhado_img_path = os.path.join(img_dir, f"rf3_detalhado_brooklyn_nets_{season}.jpg")

        df_detalhado.to_csv(detalhado_csv_path, index=False, encoding="utf-8-sig")
        df_detalhado.to_html(detalhado_html_path, index=False)
        salvar_tabela_como_imagem(df_detalhado, detalhado_img_path, f"Resultados por Adversário - Brooklyn Nets ({season})")

        print(f"Temporada {season} processada com sucesso.")

# Chamar a função principal
processar_temporadas()
