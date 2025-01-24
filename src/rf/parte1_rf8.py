import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import teamgamelog

def rf_graficos_desempenho_brooklyn_nets(team_id=1610612751, seasons=["2023-24", "2024-25"], output_dir="reports/graficos/parte1", csv_output_dir="reports/arquivos_csv/parte1/graficos_csv"):
    """
    Gera gráficos de desempenho do Brooklyn Nets para as temporadas especificadas e salva os dados correspondentes em CSV.

    Args:
        team_id (int): ID do Brooklyn Nets na NBA API.
        seasons (list): Lista de temporadas (formato "YYYY-YY") para coletar dados.
        output_dir (str): Diretório para salvar os gráficos gerados.
        csv_output_dir (str): Diretório para salvar os arquivos CSV dos gráficos.
    """
    # Criar diretórios para os gráficos e CSVs
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(csv_output_dir, exist_ok=True)

    # Função para coletar dados da API
    def coletar_dados_temporada(team_id, season):
        print(f"Coletando dados para a temporada {season}...")
        game_log = teamgamelog.TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
        game_log["SEASON"] = season  # Adicionar a coluna da temporada
        return game_log

    # Coletar dados para todas as temporadas especificadas
    all_seasons_data = pd.concat([coletar_dados_temporada(team_id, season) for season in seasons], ignore_index=True)

    # Adicionar colunas calculadas
    all_seasons_data["PTS_PA"] = all_seasons_data["PTS"].shift(-1)
    all_seasons_data["WINS"] = all_seasons_data["WL"].apply(lambda x: 1 if x == "W" else 0)
    all_seasons_data["LOSSES"] = all_seasons_data["WL"].apply(lambda x: 1 if x == "L" else 0)
    all_seasons_data["HOME_GAME"] = all_seasons_data["MATCHUP"].apply(lambda x: "vs" in x)

    # 1. Gráfico de Barras Empilhado
    print("Gerando Gráfico de Barras Empilhado...")
    wins_losses = all_seasons_data.groupby("SEASON").agg(
        total_wins=("WINS", "sum"),
        total_losses=("LOSSES", "sum"),
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(wins_losses["SEASON"]))
    ax.bar(x, wins_losses["total_wins"], label="Vitórias", color="green")
    ax.bar(x, wins_losses["total_losses"], bottom=wins_losses["total_wins"], label="Derrotas", color="red")

    ax.set_xlabel("Temporada")
    ax.set_ylabel("Número de Jogos")
    ax.set_title("Vitórias e Derrotas (Empilhado)")
    ax.set_xticks(x)
    ax.set_xticklabels(wins_losses["SEASON"])
    ax.legend()

    barras_empilhado_path = os.path.join(output_dir, "barras_empilhado_vitorias_derrotas.png")
    plt.tight_layout()
    plt.savefig(barras_empilhado_path)
    plt.close()
    print(f"Gráfico de Barras Empilhado salvo em {barras_empilhado_path}")

    # Salvar CSV do Gráfico de Barras Empilhado
    barras_empilhado_csv_path = os.path.join(csv_output_dir, "barras_empilhado_vitorias_derrotas.csv")
    wins_losses.to_csv(barras_empilhado_csv_path, index=False)
    print(f"CSV do Gráfico de Barras Empilhado salvo em {barras_empilhado_csv_path}")

    # 2. Gráfico de Pizza
    print("Gerando Gráficos de Pizza...")
    for season in seasons:
        season_data = all_seasons_data[all_seasons_data["SEASON"] == season]
        total_home_wins = season_data.loc[season_data["HOME_GAME"], "WINS"].sum()
        total_away_wins = season_data.loc[~season_data["HOME_GAME"], "WINS"].sum()
        total_home_losses = season_data.loc[season_data["HOME_GAME"], "LOSSES"].sum()
        total_away_losses = season_data.loc[~season_data["HOME_GAME"], "LOSSES"].sum()

        labels = ["Vitórias em Casa", "Vitórias Fora", "Derrotas em Casa", "Derrotas Fora"]
        values = [total_home_wins, total_away_wins, total_home_losses, total_away_losses]
        colors = ["green", "blue", "red", "brown"]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
        ax.set_title(f"Percentual de Vitórias e Derrotas ({season})")

        pizza_path = os.path.join(output_dir, f"pizza_vitorias_derrotas_{season}.png")
        plt.savefig(pizza_path)
        plt.close()
        print(f"Gráfico de Pizza salvo para a temporada {season} em {pizza_path}")

        # Salvar CSV do Gráfico de Pizza
        pizza_csv_data = pd.DataFrame({
            "Categoria": labels,
            "Frequência": values
        })
        pizza_csv_path = os.path.join(csv_output_dir, f"grafico_pizza_{season}.csv")
        pizza_csv_data.to_csv(pizza_csv_path, index=False)
        print(f"CSV do Gráfico de Pizza ({season}) salvo em {pizza_csv_path}")

    # 3. Gráfico de Radar
    print("Gerando Gráfico de Radar...")
    radar_data = all_seasons_data.groupby("HOME_GAME").agg(
        avg_points=("PTS", "mean"),
        avg_points_allowed=("PTS_PA", "mean"),
    ).reset_index()

    # Depuração: Verificar os dados calculados
    print("Dados calculados para o gráfico de radar:")
    print(radar_data)

    # Garantir que os valores sejam válidos
    if radar_data.empty or radar_data.isnull().values.any():
        print("Erro: Dados insuficientes ou inconsistentes para criar o gráfico de radar.")
        return

    categories = ["Pontos Marcados", "Pontos Sofridos"]
    try:
        values_home = (
            radar_data.loc[radar_data["HOME_GAME"] == True, "avg_points"].values[0],
            radar_data.loc[radar_data["HOME_GAME"] == True, "avg_points_allowed"].values[0],
        )
        values_away = (
            radar_data.loc[radar_data["HOME_GAME"] == False, "avg_points"].values[0],
            radar_data.loc[radar_data["HOME_GAME"] == False, "avg_points_allowed"].values[0],
        )
    except IndexError:
        print("Erro: Não foi possível acessar os valores para o gráfico de radar.")
        values_home = [0, 0]
        values_away = [0, 0]

    values_home += values_home[:1]
    values_away += values_away[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, values_home, label="Casa", color="green", linewidth=2)
    ax.fill(angles, values_home, color="green", alpha=0.25)
    ax.plot(angles, values_away, label="Fora", color="blue", linewidth=2)
    ax.fill(angles, values_away, color="blue", alpha=0.25)

    ax.set_title("Média de Pontos Marcados e Sofridos (Casa e Fora)", size=15, weight="bold", pad=20)
    ax.set_yticks([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

    radar_path = os.path.join(output_dir, "grafico_radar_pontos.png")
    plt.savefig(radar_path)
    plt.close()
    print(f"Gráfico de Radar salvo em {radar_path}")

    # Salvar CSV do Gráfico de Radar
    radar_csv_path = os.path.join(csv_output_dir, "grafico_radar_pontos.csv")
    radar_data.to_csv(radar_csv_path, index=False)
    print(f"CSV do Gráfico de Radar salvo em {radar_csv_path}")

    print("Todos os gráficos e arquivos CSV foram gerados com sucesso!")