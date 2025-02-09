import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import teamgamelog, boxscoretraditionalv2
from nba_api.stats.static import teams

def calcular_detalhes_jogos():
    """
    Coleta informações dos jogos do Brooklyn Nets para as temporadas 2023-24 e 2024-25,
    retornando um dicionário de DataFrames, onde cada chave é a temporada.

    Cada DataFrame conterá as colunas:
      - Adversário (nome completo)
      - Data do Jogo (garantindo que não haja NaN)
      - Pontos a Favor (pontos do Brooklyn Nets)
      - Pontos Contra (pontos do adversário)
      - Assistências
      - Rebotes
      - 3PT Convertidos
      - Jogo em Casa (se o jogo foi em casa: 1 se venceu, -1 se perdeu; se não, 0)
      - Jogo Fora (se o jogo foi fora: 1 se venceu, -1 se perdeu; se não, 0)
    """
    temporadas = ['2023-24', '2024-25']
    nets_team_id = 1610612751

    # Cria um mapeamento de sigla para nome completo das equipes
    lista_times = teams.get_teams()
    mapa_times = {time_info['abbreviation'].upper(): time_info['full_name'] for time_info in lista_times}

    resultados_por_temporada = {}

    for temporada in temporadas:
        detalhes_jogos = []
        try:
            # Obtém o game log do Brooklyn Nets para a temporada
            game_log = teamgamelog.TeamGameLog(team_id=nets_team_id, season=temporada)
            df_game_log = game_log.get_data_frames()[0]
            # Normaliza os nomes das colunas para maiúsculas
            df_game_log.columns = [col.upper() for col in df_game_log.columns]
        except Exception as e:
            print(f"Erro ao obter game log para a temporada {temporada}: {e}")
            continue

        # Processa cada jogo da temporada
        for _, row in df_game_log.iterrows():
            if 'GAME_ID' not in row:
                print("Coluna GAME_ID não encontrada para um jogo, pulando...")
                continue

            game_id   = row['GAME_ID']
            game_date = row['GAME_DATE']
            matchup   = row['MATCHUP']
            pts_for   = row['PTS']
            assists   = row['AST']
            rebounds  = row['REB']
            three_pm  = row['FG3M']

            # Verifica se a data do jogo é válida
            if pd.isna(game_date):
                continue

            # Identifica se o jogo é em casa ou fora
            # Se o caractere '@' estiver presente, o jogo é fora; caso contrário, se contiver "vs.", é em casa.
            if '@' in matchup:
                jogo_em_casa = False
                adversario_sigla = matchup.split('@')[-1].strip().upper()
            elif 'vs.' in matchup.lower():
                jogo_em_casa = True
                adversario_sigla = matchup.split('vs.')[-1].strip().upper()
            else:
                # Caso não seja possível identificar, pula o jogo
                continue

            adversario_nome = mapa_times.get(adversario_sigla, adversario_sigla)

            # Obtém os pontos do adversário através do boxscore
            pts_against = None
            try:
                boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
                df_team_stats = boxscore.get_data_frames()[1]  # DataFrame com estatísticas dos times
                opp_stats  = df_team_stats[df_team_stats['TEAM_ID'] != nets_team_id]
                if not opp_stats.empty:
                    pts_against = opp_stats.iloc[0]['PTS']
                else:
                    pts_against = None
            except Exception as e:
                print(f"Erro ao obter boxscore para o jogo {game_id}: {e}")
                pts_against = None

            # Se não foi possível obter os pontos do adversário, pula o jogo
            if pts_against is None:
                continue

            # Calcula a diferença para determinar vitória ou derrota
            diferenca = pts_for - pts_against
            if jogo_em_casa:
                jogo_em_casa_valor = 1 if diferenca > 0 else -1
                jogo_fora_valor   = 0
            else:
                jogo_fora_valor   = 1 if diferenca > 0 else -1
                jogo_em_casa_valor = 0

            detalhes_jogos.append({
                'Adversário':      adversario_nome,
                'Data do Jogo':    game_date,
                'Pontos a Favor':  pts_for,
                'Pontos Contra':   pts_against,
                'Assistências':    assists,
                'Rebotes':         rebounds,
                '3PT Convertidos': three_pm,
                'Jogo em Casa':    jogo_em_casa_valor,
                'Jogo Fora':       jogo_fora_valor
            })

            # Delay para respeitar os limites de requisições da API
            time.sleep(0.6)

        resultados_por_temporada[temporada] = pd.DataFrame(detalhes_jogos)

    return resultados_por_temporada

def salvar_resultados_rf4(df, temporada):
    """
    Salva o DataFrame gerado nos formatos CSV, HTML e JPG nas pastas solicitadas,
    utilizando o prefixo rf4_ e incluindo a temporada no nome dos arquivos.
    """
    # Diretórios de saída
    output_dir = "reports/arquivos_csv/parte1"
    html_dir   = "reports/html/parte1"
    img_dir    = "reports/imagens/parte1"

    # Cria os diretórios, se não existirem
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # Define os nomes completos dos arquivos com o prefixo rf4_ e a temporada
    csv_file  = os.path.join(output_dir, f"rf4_detalhes_jogos_{temporada}.csv")
    html_file = os.path.join(html_dir, f"rf4_detalhes_jogos_{temporada}.html")
    img_file  = os.path.join(img_dir, f"rf4_detalhes_jogos_{temporada}.jpg")

    # Salva em CSV
    try:
        df.to_csv(csv_file, index=False)
        print(f"Arquivo CSV salvo em: {csv_file}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

    # Salva em HTML
    try:
        df.to_html(html_file, index=False)
        print(f"Arquivo HTML salvo em: {html_file}")
    except Exception as e:
        print(f"Erro ao salvar HTML: {e}")

    # Salva em JPG: Cria uma imagem do DataFrame utilizando matplotlib
    try:
        # Define o tamanho da figura de acordo com o número de linhas
        fig, ax = plt.subplots(figsize=(12, max(4, len(df) * 0.5)))
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        plt.tight_layout()
        plt.savefig(img_file, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Arquivo JPG salvo em: {img_file}")
    except Exception as e:
        print(f"Erro ao salvar JPG: {e}")
