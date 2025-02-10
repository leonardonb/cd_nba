import os
import plotly.graph_objects as go
import pandas as pd
from nba_api.stats.endpoints import teamgamelog
from dotenv import load_dotenv

load_dotenv()
engine_image = os.getenv('ENGINE_IMAGE')

def rf_graficos_desempenho_brooklyn_nets(
        team_id=1610612751,
        seasons=["2023-24", "2024-25"],
        html_output_dir="reports/html/parte1/parte1-rf8",
        csv_output_dir="reports/arquivos_csv/parte1/parte1-rf8",
        img_output_dir="reports/imagens/parte1/parte1-rf8"
):
    os.makedirs(html_output_dir, exist_ok=True)
    os.makedirs(csv_output_dir, exist_ok=True)
    os.makedirs(img_output_dir, exist_ok=True)

    def coletar_dados_temporada(team_id, season):
        print(f"Coletando dados para a temporada {season}...")
        game_log = teamgamelog.TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
        game_log["SEASON"] = season
        return game_log

    all_seasons_data = pd.concat([coletar_dados_temporada(team_id, season) for season in seasons], ignore_index=True)

    # Ordena os dados por temporada e Game_ID
    all_seasons_data = all_seasons_data.sort_values(by=["SEASON", "Game_ID"], ascending=[True, False])

    # Calcula a coluna de pontos permitidos (PTS_PA) utilizando o deslocamento dos pontos do jogo seguinte e preenchendo os NaN
    all_seasons_data["PTS_PA"] = all_seasons_data["PTS"].shift(-1)
    all_seasons_data["PTS_PA"] = all_seasons_data["PTS_PA"].fillna(all_seasons_data["PTS"].mean())

    # Cria colunas para vitórias e derrotas (utilizadas em outros gráficos)
    all_seasons_data["WINS"] = all_seasons_data["WL"].apply(lambda x: 1 if x == "W" else 0)
    all_seasons_data["LOSSES"] = all_seasons_data["WL"].apply(lambda x: 1 if x == "L" else 0)
    # Identifica se o jogo foi em casa (presença de "vs" no campo MATCHUP)
    all_seasons_data["HOME_GAME"] = all_seasons_data["MATCHUP"].apply(lambda x: "vs" in x)

    # -------------------------------------------------------------------------
    # Tabela Agregada de Totais (por Temporada e Local)
    dados_por_local = all_seasons_data.groupby(["SEASON", "HOME_GAME"]).agg(
        total_pontos_marcados=("PTS", "sum"),
        total_pontos_sofridos=("PTS_PA", "sum"),
        total_rebotes=("REB", "sum")
    ).reset_index()

    dados_por_local["Local"] = dados_por_local["HOME_GAME"].map({True: "Casa", False: "Fora"})
    tabela_final = dados_por_local[["SEASON", "Local", "total_pontos_marcados", "total_pontos_sofridos", "total_rebotes"]]

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Tabela de Médias de Pontos Marcados, Pontos Sofridos e Rebotes (por Temporada e Local)
    tabela_media = all_seasons_data.groupby(["SEASON", "HOME_GAME"]).agg(
        media_pontos_marcados=("PTS", "mean"),
        media_pontos_sofridos=("PTS_PA", "mean"),
        media_rebotes=("REB", "mean")
    ).reset_index()

    tabela_media["Local"] = tabela_media["HOME_GAME"].map({True: "Casa", False: "Fora"})
    tabela_media = tabela_media[["SEASON", "Local", "media_pontos_marcados", "media_pontos_sofridos", "media_rebotes"]]

    # -------------------------------------------------------------------------

    # 1. Gráfico de Barras Empilhado (utilizando dados totais)
    print("Gerando Gráfico de Barras Empilhado...")
    wins_losses = all_seasons_data.groupby("SEASON").agg(
        total_wins=("WINS", "sum"),
        total_losses=("LOSSES", "sum"),
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=wins_losses["SEASON"], y=wins_losses["total_wins"], name="Vitórias", marker_color="green"))
    fig.add_trace(go.Bar(x=wins_losses["SEASON"], y=wins_losses["total_losses"], name="Derrotas", marker_color="red"))

    fig.update_layout(title="Vitórias e Derrotas (Empilhado)",
                      xaxis_title="Temporada", yaxis_title="Número de Jogos", barmode="stack")

    barras_html_path = os.path.join(html_output_dir, "rf8_barras_empilhado_vitorias_derrotas.html")
    barras_img_path = os.path.join(img_output_dir, "rf8_barras_empilhado_vitorias_derrotas.jpg")
    barras_csv_path = os.path.join(csv_output_dir, "rf8_barras_empilhado_vitorias_derrotas.csv")

    fig.write_html(barras_html_path)
    fig.write_image(barras_img_path, format="jpg", engine=engine_image)
    wins_losses.to_csv(barras_csv_path, index=False)

    print(f"Gráficos salvos em {barras_html_path} e {barras_img_path}")
    print(f"CSV salvo em {barras_csv_path}")

    # 2. Gráficos de Pizza (utilizando dados totais)
    print("Gerando Gráficos de Pizza...")
    for season in seasons:
        season_data = all_seasons_data[all_seasons_data["SEASON"] == season]
        total_home_wins = season_data.loc[season_data["HOME_GAME"], "WINS"].sum()
        total_away_wins = season_data.loc[~season_data["HOME_GAME"], "WINS"].sum()
        total_home_losses = season_data.loc[season_data["HOME_GAME"], "LOSSES"].sum()
        total_away_losses = season_data.loc[~season_data["HOME_GAME"], "LOSSES"].sum()

        labels = ["Vitórias em Casa", "Vitórias Fora", "Derrotas em Casa", "Derrotas Fora"]
        values = [total_home_wins, total_away_wins, total_home_losses, total_away_losses]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
        fig.update_layout(title=f"rf8_Percentual de Vitórias e Derrotas ({season})")

        pizza_html_path = os.path.join(html_output_dir, f"rf8_pizza_vitorias_derrotas_{season}.html")
        pizza_img_path = os.path.join(img_output_dir, f"rf8_pizza_vitorias_derrotas_{season}.jpg")
        pizza_csv_path = os.path.join(csv_output_dir, f"rf8_grafico_pizza_{season}.csv")

        fig.write_html(pizza_html_path)
        fig.write_image(pizza_img_path, format="jpg", engine=engine_image)
        pd.DataFrame({"Categoria": labels, "Frequência": values}).to_csv(pizza_csv_path, index=False)

        print(f"Gráficos salvos para {season} em {pizza_html_path} e {pizza_img_path}")
        print(f"CSV salvo em {pizza_csv_path}")

    # 3. Gráficos de Radar baseados na Tabela de Médias (com 3 métricas)
    #    Separadamente para Jogos FORA de casa e Jogos EM CASA
    #
    # As métricas utilizadas são:
    # - Média Pontos Marcados
    # - Média Pontos Sofridos
    # - Média Rebotes

    # Radar para Jogos Fora de Casa
    away_media = tabela_media[tabela_media["Local"] == "Fora"]

    if not away_media.empty:
        fig_radar_away = go.Figure()
        categories = ["Média Pontos Marcados", "Média Pontos Sofridos", "Média Rebotes"]
        for _, row in away_media.iterrows():
            season = row["SEASON"]
            values = [
                row["media_pontos_marcados"],
                row["media_pontos_sofridos"],
                row["media_rebotes"]
            ]
            # Fecha o polígono repetindo o primeiro valor
            values.append(values[0])
            fig_radar_away.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=season
            ))
        # Define o range radial com base no maior valor entre as três métricas para jogos fora
        max_val_away = away_media[["media_pontos_marcados", "media_pontos_sofridos", "media_rebotes"]].max().max()
        fig_radar_away.update_layout(title="Médias Fora de Casa (por Temporada)",
                                     polar=dict(radialaxis=dict(visible=True, range=[0, max_val_away])))

        radar_away_html_path = os.path.join(html_output_dir, "rf8_radar_fora_media.html")
        radar_away_img_path = os.path.join(img_output_dir, "rf8_radar_fora_media.jpg")
        radar_away_csv_path = os.path.join(csv_output_dir, "rf8_radar_fora_media.csv")

        fig_radar_away.write_html(radar_away_html_path)
        fig_radar_away.write_image(radar_away_img_path, format="jpg", engine=engine_image)
        away_media.to_csv(radar_away_csv_path, index=False)

        print(f"Radar (Fora - Média) salvo em {radar_away_html_path} e {radar_away_img_path}")

    # Radar para Jogos em Casa
    home_media = tabela_media[tabela_media["Local"] == "Casa"]

    if not home_media.empty:
        fig_radar_home = go.Figure()
        categories = ["Média Pontos Marcados", "Média Pontos Sofridos", "Média Rebotes"]
        for _, row in home_media.iterrows():
            season = row["SEASON"]
            values = [
                row["media_pontos_marcados"],
                row["media_pontos_sofridos"],
                row["media_rebotes"]
            ]
            values.append(values[0])
            fig_radar_home.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=season
            ))
        max_val_home = home_media[["media_pontos_marcados", "media_pontos_sofridos", "media_rebotes"]].max().max()
        fig_radar_home.update_layout(title="Médias em Casa (por Temporada)",
                                     polar=dict(radialaxis=dict(visible=True, range=[0, max_val_home])))

        radar_home_html_path = os.path.join(html_output_dir, "rf8_radar_casa_media.html")
        radar_home_img_path = os.path.join(img_output_dir, "rf8_radar_casa_media.jpg")
        radar_home_csv_path = os.path.join(csv_output_dir, "rf8_radar_casa_media.csv")

        fig_radar_home.write_html(radar_home_html_path)
        fig_radar_home.write_image(radar_home_img_path, format="jpg", engine=engine_image)
        home_media.to_csv(radar_home_csv_path, index=False)

        print(f"Radar (Casa - Média) salvo em {radar_home_html_path} e {radar_home_img_path}")

    # 4. Gráfico de Linhas - Sequência de Vitórias e Derrotas por Temporada
    #
    # Para cada temporada, o gráfico exibirá a sequência dos jogos (em ordem cronológica)
    # com o eixo x representando o número do jogo e o eixo y representando o resultado:
    # 1 para vitória e 0 para derrota. Os marcadores serão coloridos (verde para vitória, vermelho para derrota),
    # e a coluna "WL" será exibida como texto ao pairar o mouse.
    for season in seasons:
        season_data = all_seasons_data[all_seasons_data["SEASON"] == season].copy()
        # Se existir a coluna "GAME_DATE", converte para datetime usando o formato "%b %d, %Y" e ordena; senão, ordena por "Game_ID"
        if "GAME_DATE" in season_data.columns:
            season_data["GAME_DATE"] = pd.to_datetime(season_data["GAME_DATE"], format="%b %d, %Y")
            season_data = season_data.sort_values("GAME_DATE", ascending=True)
        else:
            season_data = season_data.sort_values("Game_ID", ascending=True)
        season_data = season_data.reset_index(drop=True)
        season_data["Game_Number"] = season_data.index + 1

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x = season_data["Game_Number"],
            y = season_data["WINS"],
            mode = "lines+markers",
            line = dict(color="green"),
            marker = dict(
                color = season_data["WINS"].map({1:"green", 0:"red"}),
                size = 10
            ),
            text = season_data["WL"],  # Exibe W ou L no hover
            name = season
        ))
        fig_line.update_layout(
            title = f"Sequência de Vitórias e Derrotas - Temporada {season}",
            xaxis_title = "Número do Jogo",
            yaxis_title = "Resultado (1 = Vitória, 0 = Derrota)",
            yaxis = dict(tickvals=[0, 1], ticktext=["Derrota", "Vitória"])
        )

        line_html_path = os.path.join(html_output_dir, f"rf8_linha_seq_{season}.html")
        line_img_path = os.path.join(img_output_dir, f"rf8_linha_seq_{season}.jpg")
        line_csv_path = os.path.join(csv_output_dir, f"rf8_linha_seq_{season}.csv")

        fig_line.write_html(line_html_path)
        fig_line.write_image(line_img_path, format="jpg", engine=engine_image)
        season_data.to_csv(line_csv_path, index=False)
        print(f"Gráfico de Linha para {season} salvo em {line_html_path} e {line_img_path}")

    # 5. Gráfico de Dispersão - Média de Pontos Marcados vs Média de Pontos Sofridos por Temporada
    #
    # Para cada temporada (considerando todas as partidas, independentemente de casa ou fora),
    # calculamos a média de pontos marcados e a média de pontos sofridos. Cada ponto no gráfico
    # representa uma temporada e é rotulado com o nome da equipe e a temporada.
    scatter_data = all_seasons_data.groupby("SEASON").agg(
        media_pontos=("PTS", "mean"),
        media_pontos_sofridos=("PTS_PA", "mean")
    ).reset_index()

    # Tenta obter o nome da equipe a partir dos dados; se não existir, utiliza um rótulo fixo
    if "TEAM_NAME" in all_seasons_data.columns:
        scatter_data["Equipe"] = all_seasons_data["TEAM_NAME"].iloc[0]
    else:
        scatter_data["Equipe"] = "Brooklyn Nets"

    fig_scatter = go.Figure()
    for _, row in scatter_data.iterrows():
        season = row["SEASON"]
        x = row["media_pontos"]
        y = row["media_pontos_sofridos"]
        team = row["Equipe"]
        fig_scatter.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            name=f"{team} {season}",   # Define o nome do trace para a legenda
            text=[f"{team} {season}"],
            textposition="top center",
            marker=dict(size=12)
        ))
    fig_scatter.update_layout(
        title="Média de Pontos Marcados vs Média de Pontos Sofridos por Temporada",
        xaxis_title="Média de Pontos Marcados",
        yaxis_title="Média de Pontos Sofridos"
    )
    scatter_html_path = os.path.join(html_output_dir, "rf8_scatter_media_pontos.html")
    scatter_img_path = os.path.join(img_output_dir, "rf8_scatter_media_pontos.jpg")
    scatter_csv_path = os.path.join(csv_output_dir, "rf8_scatter_media_pontos.csv")

    fig_scatter.write_html(scatter_html_path)
    fig_scatter.write_image(scatter_img_path, format="jpg", engine=engine_image)
    scatter_data.to_csv(scatter_csv_path, index=False)
    print(f"Gráfico de Dispersão salvo em {scatter_html_path} e {scatter_img_path}")

    # 6. Gráfico de Barras para Estatísticas Específicas do RF06
    print("Gerando Gráfico de Barras para Estatísticas Específicas (Roubos, Rebotes Defensivos, Tocos, Erros e Faltas)...")

    # Agrega os dados por temporada
    stats_aggregated = all_seasons_data.groupby("SEASON").agg(
        total_roubos=("STL", "sum"),
        total_reb_defensivos=("DREB", "sum"),
        media_tocos=("BLK", "mean"),
        media_erros=("TOV", "mean"),  # Utiliza "TOV" em vez de "TO"
        media_faltas=("PF", "mean")
    ).reset_index()

    # Cria o gráfico de barras agrupado
    fig_stats = go.Figure(data=[
        go.Bar(name="Total de Roubos de Bola",
               x=stats_aggregated["SEASON"],
               y=stats_aggregated["total_roubos"]),
        go.Bar(name="Total de Rebotes Defensivos",
               x=stats_aggregated["SEASON"],
               y=stats_aggregated["total_reb_defensivos"]),
        go.Bar(name="Média de Tocos por Jogo",
               x=stats_aggregated["SEASON"],
               y=stats_aggregated["media_tocos"]),
        go.Bar(name="Média de Erros por Jogo",
               x=stats_aggregated["SEASON"],
               y=stats_aggregated["media_erros"]),
        go.Bar(name="Média de Faltas por Jogo",
               x=stats_aggregated["SEASON"],
               y=stats_aggregated["media_faltas"])
    ])

    # Atualiza o layout do gráfico para exibição em barras agrupadas
    fig_stats.update_layout(
        title="Estatísticas Específicas por Temporada",
        xaxis_title="Temporada",
        yaxis_title="Valor",
        barmode="group"
    )

    # Define os caminhos para salvar os arquivos gerados
    stats_html_path = os.path.join(html_output_dir, "rf8_bar_stats_especificas RF06.html")
    stats_img_path = os.path.join(img_output_dir, "rf8_bar_stats_especificas RF06.jpg")
    stats_csv_path = os.path.join(csv_output_dir, "rf8_bar_stats_especificas RF06.csv")

    # Salva o gráfico e os dados
    fig_stats.write_html(stats_html_path)
    fig_stats.write_image(stats_img_path, format="jpg", engine=engine_image)
    stats_aggregated.to_csv(stats_csv_path, index=False)

    print(f"Gráfico de Barras para Estatísticas Específicas salvo em {stats_html_path} e {stats_img_path}")
    print(f"CSV salvo em {stats_csv_path}")

    # 7. Gráfico de Dispersão Interativo para Detalhes dos Jogos com Legenda Personalizada
    print("Gerando Gráfico de Dispersão Interativo para Detalhes dos Jogos...")
    # Cria colunas adicionais para extrair o adversário e identificar se o jogo foi em casa ou fora
    all_seasons_data["OPPONENT"] = all_seasons_data["MATCHUP"].apply(lambda x: x.split(" ")[-1])
    all_seasons_data["Local_Str"] = all_seasons_data["HOME_GAME"].map({True: "Casa", False: "Fora"})

    # Converte a coluna de data para datetime (assumindo o formato '%b %d, %Y')
    if "GAME_DATE" in all_seasons_data.columns:
        all_seasons_data["GAME_DATE_DT"] = pd.to_datetime(all_seasons_data["GAME_DATE"], format="%b %d, %Y")
    else:
        # Caso não exista a coluna GAME_DATE, tenta outro método (ajuste conforme necessário)
        all_seasons_data["GAME_DATE_DT"] = pd.to_datetime(all_seasons_data["Game_ID"], errors='coerce')

    # Calcula a margem de vitória/derrota (diferença de pontos)
    all_seasons_data["MARGIN"] = all_seasons_data["PTS"] - all_seasons_data["PTS_PA"]

    # Cria traces agrupados para cada grupo: (resultado, home, label, cor, símbolo)
    grupos = [
        ("W", True, "Vitória em Casa", "green", "circle"),
        ("W", False, "Vitória Fora", "green", "triangle-up"),
        ("L", True, "Derrota em Casa", "red", "circle"),
        ("L", False, "Derrota Fora", "red", "triangle-up")
    ]

    fig_details = go.Figure()
    for resultado, home, label, cor, simbolo in grupos:
        df_grupo = all_seasons_data[(all_seasons_data["WL"] == resultado) & (all_seasons_data["HOME_GAME"] == home)]
        if not df_grupo.empty:
            fig_details.add_trace(go.Scatter(
                x=df_grupo["GAME_DATE_DT"],
                y=df_grupo["MARGIN"],
                mode="markers",
                marker=dict(
                    color=cor,
                    symbol=simbolo,
                    size=10,
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                text=df_grupo.apply(lambda row: f"Data: {row['GAME_DATE']}<br>"
                                                f"Adversário: {row['OPPONENT']}<br>"
                                                f"Resultado: {row['WL']}<br>"
                                                f"Local: {row['Local_Str']}<br>"
                                                f"Placar: {row['PTS']} - {row['PTS_PA']}", axis=1),
                hoverinfo="text",
                showlegend=False  # Esses traces não aparecerão na legenda
            ))

    # Adiciona traces "dummy" para criar uma legenda personalizada
    dummy_home = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(symbol="circle", color="black", size=10),
        legendgroup="Local",
        showlegend=True,
        name="Jogo em Casa (círculo)"
    )
    dummy_away = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(symbol="triangle-up", color="black", size=10),
        legendgroup="Local",
        showlegend=True,
        name="Jogo Fora (triângulo)"
    )
    dummy_win = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(symbol="circle", color="green", size=10),
        legendgroup="Resultado",
        showlegend=True,
        name="Vitória (verde)"
    )
    dummy_loss = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(symbol="circle", color="red", size=10),
        legendgroup="Resultado",
        showlegend=True,
        name="Derrota (vermelho)"
    )

    fig_details.add_trace(dummy_home)
    fig_details.add_trace(dummy_away)
    fig_details.add_trace(dummy_win)
    fig_details.add_trace(dummy_loss)

    fig_details.update_layout(
        title="Detalhes dos Jogos dos Brooklyn Nets",
        xaxis_title="Data do Jogo",
        yaxis_title="Margem de Pontos (Placar: Nets - Adversário)",
        xaxis=dict(type="date"),
        legend_title="Legenda"
    )

    details_html_path = os.path.join(html_output_dir, "rf8_scatter_detalhes_jogos RF07.html")
    details_img_path = os.path.join(img_output_dir, "rf8_scatter_detalhes_jogos RF07.jpg")
    details_csv_path = os.path.join(csv_output_dir, "rf8_scatter_detalhes_jogos RF07.csv")

    fig_details.write_html(details_html_path)
    fig_details.write_image(details_img_path, format="jpg", engine=engine_image)
    all_seasons_data.to_csv(details_csv_path, index=False)

    print(f"Gráfico de Dispersão dos Jogos salvo em {details_html_path} e {details_img_path}")

    print("✅ Todos os gráficos e arquivos CSV foram gerados com sucesso!")
