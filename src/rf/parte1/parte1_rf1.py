import pandas as pd
import os
import matplotlib.pyplot as plt

def listar_times_conferencia(output_dir="reports/arquivos_csv/parte1", html_dir="reports/html/parte1", img_dir="reports/imagens/parte1"):
    """
    RF1: Listar todos os times da NBA agrupados por conferência e unificados,
    gerando relatórios em CSV, HTML e JPG.

    Args:
        output_dir (str): Diretório para salvar os relatórios em CSV.
        html_dir (str): Diretório para salvar os relatórios em HTML.
        img_dir (str): Diretório para salvar os relatórios como imagens.
    """
    from nba_api.stats.static import teams

    # Obter todos os times
    all_teams = pd.DataFrame(teams.get_teams())

    # Mapeamento manual de conferências
    leste_teams = [
        "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
        "Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers",
        "Miami Heat", "Milwaukee Bucks", "New York Knicks", "Orlando Magic",
        "Philadelphia 76ers", "Toronto Raptors", "Washington Wizards"
    ]

    oeste_teams = [
        "Dallas Mavericks", "Denver Nuggets", "Golden State Warriors", "Houston Rockets",
        "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Minnesota Timberwolves",
        "New Orleans Pelicans", "Oklahoma City Thunder", "Phoenix Suns", "Portland Trail Blazers",
        "Sacramento Kings", "San Antonio Spurs", "Utah Jazz"
    ]

    # Adicionar coluna de conferência
    all_teams["conference"] = all_teams["full_name"].apply(
        lambda x: "East" if x in leste_teams else "West" if x in oeste_teams else "Unknown"
    )

    # Dividir por conferência
    leste = all_teams[all_teams["conference"] == "East"]
    oeste = all_teams[all_teams["conference"] == "West"]

    # Criar tabela unificada
    unificada = all_teams.sort_values(by=["conference", "full_name"]).reset_index(drop=True)

    # Criar diretórios para salvar os resultados
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # Caminhos para salvar arquivos
    leste_csv_path = os.path.join("reports/arquivos_csv/parte1", "rf1_times_conferencia_leste.csv")
    oeste_csv_path = os.path.join("reports/arquivos_csv/parte1", "rf1_times_conferencia_oeste.csv")
    unificada_csv_path = os.path.join("reports/arquivos_csv/parte1", "rf1_times_unificados.csv")
    leste_html_path = os.path.join("reports/html/parte1", "rf1_tabela_times_leste.html")
    oeste_html_path = os.path.join("reports/html/parte1", "rf1_tabela_times_oeste.html")
    unificada_html_path = os.path.join("reports/html/parte1", "rf1_tabela_times_unificados.html")
    leste_img_path = os.path.join("reports/imagens/parte1", "rf1_times_conferencia_leste.jpg")
    oeste_img_path = os.path.join("reports/imagens/parte1", "rf1_times_conferencia_oeste.jpg")
    unificada_img_path = os.path.join("reports/imagens/parte1", "rf1_times_unificados.jpg")

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
    salvar_tabela_como_imagem(leste, leste_img_path, "Times da Conferência Leste")
    salvar_tabela_como_imagem(oeste, oeste_img_path, "Times da Conferência Oeste")
    salvar_tabela_como_imagem(unificada, unificada_img_path, "Times Unificados")

    print("Processamento do RF1 concluído.")
    return leste, oeste, unificada
