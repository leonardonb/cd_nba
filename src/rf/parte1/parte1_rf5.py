import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import teamgamelog, boxscoretraditionalv2

def apresentar_dados_divididos():
    """
    Função principal que coleta dados dos jogos dos Brooklyn Nets para as temporadas
    2023-24 e 2024-25 utilizando a API nba_api e gera, para cada temporada, um CSV, um HTML e um JPG
    contendo uma tabela com as seguintes colunas:

      - Nome do adversário (nome completo, convertido a partir da sigla)
      - Data do jogo (somente se disponível)
      - Pontos a favor (pontos dos Brooklyn Nets)
      - Pontos contra (pontos do adversário, obtidos a partir do boxscore)
      - Rebotes ofensivos
      - Rebotes defensivos
      - Cestas de 2 pontos convertidas (calculadas como: FGM - FG3M)
      - Cestas de 3 pontos convertidas (FG3M)
      - Lances livres convertidos (FTM)

    Os arquivos serão salvos com o prefixo "rf5_" nas seguintes pastas:

      - CSV:    reports/arquivos_csv/parte1
      - HTML:   reports/html/parte1
      - JPG:    reports/imagens/parte1

    Algumas esperas (time.sleep) foram adicionadas para reduzir a chance de bloqueio por excesso de requisições.
    """

    # Definindo os diretórios de saída e criando-os, se necessário
    output_dir = "reports/arquivos_csv/parte1"
    html_dir = "reports/html/parte1"
    img_dir = "reports/imagens/parte1"

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # Dicionário para mapear a sigla do time para o nome completo
    team_name_mapping = {
        "ATL": "Atlanta Hawks",
        "BOS": "Boston Celtics",
        "BKN": "Brooklyn Nets",
        "CHA": "Charlotte Hornets",
        "CHI": "Chicago Bulls",
        "CLE": "Cleveland Cavaliers",
        "DAL": "Dallas Mavericks",
        "DEN": "Denver Nuggets",
        "DET": "Detroit Pistons",
        "GSW": "Golden State Warriors",
        "HOU": "Houston Rockets",
        "IND": "Indiana Pacers",
        "LAC": "Los Angeles Clippers",
        "LAL": "Los Angeles Lakers",
        "MEM": "Memphis Grizzlies",
        "MIA": "Miami Heat",
        "MIL": "Milwaukee Bucks",
        "MIN": "Minnesota Timberwolves",
        "NOP": "New Orleans Pelicans",
        "NYK": "New York Knicks",
        "OKC": "Oklahoma City Thunder",
        "ORL": "Orlando Magic",
        "PHI": "Philadelphia 76ers",
        "PHO": "Phoenix Suns",
        "POR": "Portland Trail Blazers",
        "SAC": "Sacramento Kings",
        "SAS": "San Antonio Spurs",
        "TOR": "Toronto Raptors",
        "UTA": "Utah Jazz",
        "WAS": "Washington Wizards"
    }

    # ID do Brooklyn Nets
    team_id = 1610612751

    # Lista de temporadas a processar
    seasons = ["2023-24", "2024-25"]

    for season in seasons:
        print(f"Processando temporada {season}...")

        # Obtendo os dados dos jogos dos Brooklyn Nets para a temporada usando teamgamelog
        try:
            # Nota: season_type_all_star="Regular Season" para pegar somente jogos da temporada regular.
            gamelog = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star="Regular Season")
            df_gamelog = gamelog.get_data_frames()[0]
            # Força os nomes das colunas para caixa alta para padronizar o acesso
            df_gamelog.columns = df_gamelog.columns.str.upper()
        except Exception as e:
            print(f"Erro ao obter dados para a temporada {season}: {e}")
            continue

        # Lista para armazenar os dados processados de cada jogo
        processed_data = []

        # Iterando sobre cada jogo retornado
        for _, row in df_gamelog.iterrows():
            # Verifica se a data do jogo está disponível
            game_date = row.get('GAME_DATE')
            if pd.isna(game_date):
                continue

            # Obter o ID do jogo
            game_id = row.get('GAME_ID')
            if game_id is None:
                # Se não encontrar, pula este jogo
                print("GAME_ID não encontrado, pulando jogo.")
                continue

            # Obter o matchup para identificar o adversário.
            # Exemplo de formato: "BKN vs. LAL" ou "BKN @ LAL"
            matchup = row.get('MATCHUP', '')
            if not matchup:
                print(f"Matchup não encontrado para o jogo {game_id}, pulando jogo.")
                continue
            # Divide a string e pega a última parte que é a sigla do adversário (removendo eventuais pontuações)
            parts = matchup.split()
            opponent_abbr = ''.join(filter(str.isalpha, parts[-1]))
            opponent_full_name = team_name_mapping.get(opponent_abbr, opponent_abbr)

            # Estatísticas do Brooklyn Nets obtidas no teamgamelog
            pts_a_favor = row.get('PTS')
            oreb = row.get('OREB')
            dreb = row.get('DREB')
            fgm = row.get('FGM')
            fg3m = row.get('FG3M')
            ftm = row.get('FTM')
            # Garante que, se houver valores nulos, eles sejam interpretados como 0
            fgm = fgm if pd.notna(fgm) else 0
            fg3m = fg3m if pd.notna(fg3m) else 0
            two_pt_made = fgm - fg3m

            # Obtendo os pontos do adversário através do boxscore
            try:
                boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
                # O endpoint retorna duas tabelas: a primeira com estatísticas individuais e a segunda com estatísticas do time.
                team_stats = boxscore.get_data_frames()[1]
                # Força os nomes das colunas para caixa alta, se necessário
                team_stats.columns = team_stats.columns.str.upper()
                # Seleciona a linha do Brooklyn Nets
                row_bkn = team_stats[team_stats['TEAM_ID'] == team_id]
                if row_bkn.empty:
                    print(f"Dados do Brooklyn Nets não encontrados no jogo {game_id}.")
                    continue
                # A linha do adversário é aquela cujo TEAM_ID é diferente do Brooklyn Nets
                row_opp = team_stats[team_stats['TEAM_ID'] != team_id]
                if row_opp.empty:
                    print(f"Dados do adversário não encontrados no jogo {game_id}.")
                    opponent_pts = None
                else:
                    opponent_pts = row_opp.iloc[0]['PTS']
            except Exception as e:
                print(f"Erro ao obter dados de boxscore para o jogo {game_id}: {e}")
                opponent_pts = None

            # Adiciona os dados processados em um dicionário
            processed_data.append({
                "Nome do adversário": opponent_full_name,
                "Data do jogo": game_date,
                "Pontos a favor": pts_a_favor,
                "Pontos contra": opponent_pts,
                "Rebotes ofensivos": oreb,
                "Rebotes defensivos": dreb,
                "Cestas de 2 pontos convertidas": two_pt_made,
                "Cestas de 3 pontos convertidas": fg3m,
                "Lances livres": ftm
            })

            # Aguarda um curto período para evitar problemas com limite de requisições
            time.sleep(0.6)

        # Converte os dados processados em um DataFrame do pandas
        df_processed = pd.DataFrame(processed_data)

        # Gerando o nome dos arquivos com o prefixo rf5_ e substituindo a barra da temporada por hífen
        season_name = season.replace("/", "-")
        csv_filename = f"rf5_BrooklynNets_{season_name}.csv"
        html_filename = f"rf5_BrooklynNets_{season_name}.html"
        img_filename = f"rf5_BrooklynNets_{season_name}.jpg"

        # Salvando o CSV
        csv_path = os.path.join(output_dir, csv_filename)
        df_processed.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"Arquivo CSV salvo em: {csv_path}")

        # Salvando o HTML
        html_path = os.path.join(html_dir, html_filename)
        df_processed.to_html(html_path, index=False)
        print(f"Arquivo HTML salvo em: {html_path}")

        # Gerando e salvando a imagem (JPG) com a tabela usando matplotlib
        img_path = os.path.join(img_dir, img_filename)
        fig, ax = plt.subplots(figsize=(12, max(2, len(df_processed) * 0.5)))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df_processed.values, colLabels=df_processed.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.5)
        plt.savefig(img_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Arquivo JPG salvo em: {img_path}")