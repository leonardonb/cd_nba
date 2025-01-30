import pandas as pd
import os
from nba_api.stats.endpoints import LeagueStandingsV3
import matplotlib.pyplot as plt

def apresentar_classificacao_atual(output_dir="reports/arquivos_csv/parte1", html_dir="reports/html/parte1", img_dir="reports/imagens/parte1"):
    """
    RF2: Apresentar a classificação atual dos times agrupados por conferência,
    incluindo uma classificação unificada, salvando relatórios em CSV, HTML e JPG.

    Args:
        output_dir (str): Diretório para salvar os relatórios em CSV.
        graph_dir (str): Diretório para salvar os relatórios em HTML.
        img_dir (str): Diretório para salvar as tabelas como imagens.
    """
    print("Obtendo classificação atual...")

    # Obter classificação atual usando LeagueStandingsV3
    standings = LeagueStandingsV3()
    data = standings.get_data_frames()[0]

    # Ajustar colunas relevantes
    cols_interessantes = [
        "TeamName", "Conference", "PlayoffRank", "WINS", "LOSSES", "WinPCT"
    ]
    if not all(col in data.columns for col in cols_interessantes):
        raise ValueError(f"As colunas necessárias não estão disponíveis no DataFrame: {cols_interessantes}")

    # Selecionar e renomear colunas relevantes
    df_classificacao = data[cols_interessantes]
    df_classificacao.columns = ["Time", "Conferência", "Ranking", "Vitórias", "Derrotas", "Porcentagem de Vitórias"]

    # Separar por conferência
    leste = df_classificacao[df_classificacao["Conferência"] == "East"].sort_values("Ranking")
    oeste = df_classificacao[df_classificacao["Conferência"] == "West"].sort_values("Ranking")

    # Criar classificação unificada
    unificada = df_classificacao.sort_values(by=["Porcentagem de Vitórias", "Vitórias"], ascending=[False, False]).reset_index(drop=True)
    unificada.index += 1  # Ajustar o índice para começar em 1
    unificada.insert(0, "Posição", unificada.index)

    # Criar diretórios para salvar os resultados
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # Caminhos para salvar arquivos
    leste_csv_path = os.path.join("reports/arquivos_csv/parte1", "rf2_classificacao_leste.csv")
    oeste_csv_path = os.path.join("reports/arquivos_csv/parte1", "rf2_classificacao_oeste.csv")
    unificada_csv_path = os.path.join("reports/arquivos_csv/parte1", "rf2_classificacao_unificada.csv")
    leste_html_path = os.path.join("reports/html/parte1", "rf2_classificacao_leste.html")
    oeste_html_path = os.path.join("reports/html/parte1", "rf2_classificacao_oeste.html")
    unificada_html_path = os.path.join("reports/html/parte1", "rf2_classificacao_unificada.html")
    leste_img_path = os.path.join("reports/imagens/parte1", "rf2_classificacao_leste.jpg")
    oeste_img_path = os.path.join("reports/imagens/parte1", "rf2_classificacao_oeste.jpg")
    unificada_img_path = os.path.join("reports/imagens/parte1", "rf2_classificacao_unificada.jpg")

    # Salvar tabelas em CSV
    leste.to_csv(leste_csv_path, index=False)
    oeste.to_csv(oeste_csv_path, index=False)
    unificada.to_csv(unificada_csv_path, index=False)
    print(f"Tabelas CSV salvas em: {leste_csv_path}, {oeste_csv_path} e {unificada_csv_path}")

    # Salvar tabelas em HTML
    leste.to_html(leste_html_path, index=False)
    oeste.to_html(oeste_html_path, index=False)
    unificada.to_html(unificada_html_path, index=False)
    print(f"Tabelas HTML salvas em: {leste_html_path}, {oeste_html_path} e {unificada_html_path}")

    # Função para salvar como imagem
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

    # Salvar tabelas como imagens
    salvar_tabela_como_imagem(leste, leste_img_path, "Classificação Atual - Conferência Leste")
    salvar_tabela_como_imagem(oeste, oeste_img_path, "Classificação Atual - Conferência Oeste")
    salvar_tabela_como_imagem(unificada, unificada_img_path, "Classificação Atual - Unificada")

    print("Processamento do RF2 concluído.")
    return leste, oeste, unificada
