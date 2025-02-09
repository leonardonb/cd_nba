import os
import pandas as pd
import matplotlib.pyplot as plt

from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams

def apresentar_performance_defensiva():
    """
    Gera relatórios (CSV, HTML e JPG) com a performance defensiva do Brooklyn Nets para as temporadas
    2023-24 e 2024-25. Cada relatório contém uma tabela com:
      - Nome do adversário (convertido da sigla para o nome completo)
      - Data do jogo (verificando se a informação está disponível)
      - Total de roubos de bola
      - Total de rebotes defensivos
      - Total de tocos
      - Total de erros (turnovers)
      - Total de faltas

    Os arquivos serão salvos nas seguintes pastas:
      - CSV:    reports/arquivos_csv/parte1
      - HTML:   reports/html/parte1
      - JPG:    reports/imagens/parte1

    Cada arquivo terá o prefixo 'rf6_' no nome.

    Referências:
      - nba_api: https://github.com/swar/nba_api
      - Pandas: https://pandas.pydata.org/docs/
      - Matplotlib (table): https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.table.html
    """
    # Diretórios de saída
    output_dir = "reports/arquivos_csv/parte1"
    html_dir = "reports/html/parte1"
    img_dir = "reports/imagens/parte1"

    # Cria os diretórios, se não existirem
    for directory in [output_dir, html_dir, img_dir]:
        os.makedirs(directory, exist_ok=True)

    # Obtém a lista de times e cria um mapeamento de sigla para nome completo
    nba_teams = teams.get_teams()
    team_mapping = {team['abbreviation']: team['full_name'] for team in nba_teams}

    # ID do Brooklyn Nets
    brooklyn_nets_id = 1610612751  # Brooklyn Nets

    # Lista de temporadas a serem processadas
    temporadas = ["2023-24", "2024-25"]

    # Processa cada temporada
    for temporada in temporadas:
        try:
            # Obter o game log da temporada para o Brooklyn Nets
            game_log = teamgamelog.TeamGameLog(team_id=brooklyn_nets_id, season=temporada)
            df = game_log.get_data_frames()[0]
        except Exception as e:
            print(f"Erro ao obter dados para a temporada {temporada}: {e}")
            continue

        # Remove linhas sem informação na data do jogo para evitar NaN
        df = df.dropna(subset=['GAME_DATE'])

        # Função para extrair o adversário a partir da coluna 'MATCHUP'
        def extrair_oponente(matchup):
            # Exemplo de matchup: "BKN vs. BOS" ou "BKN @ TOR"
            if " vs. " in matchup:
                partes = matchup.split(" vs. ")
                oponente_sigla = partes[1].strip()
            elif " @ " in matchup:
                partes = matchup.split(" @ ")
                oponente_sigla = partes[1].strip()
            else:
                oponente_sigla = ""
            # Retorna o nome completo do time adversário, se disponível
            return team_mapping.get(oponente_sigla, oponente_sigla)

        # Aplica a extração do nome do adversário
        df['Nome do adversário'] = df['MATCHUP'].apply(extrair_oponente)

        # Cria a tabela com as informações solicitadas
        tabela = pd.DataFrame({
            "Nome do adversário": df['Nome do adversário'],
            "Data do jogo": df['GAME_DATE'],
            "Roubos de bola": df['STL'],
            "Rebotes defensivos": df['DREB'],
            "Tocos": df['BLK'],
            "Erros": df['TOV'],   # Alterado de 'TO' para 'TOV'
            "Faltas": df['PF']
        })

        # Define o nome base do arquivo com o prefixo rf6_
        nome_arquivo_base = f"rf6_Brooklyn_Nets_{temporada}_performance"

        # Salva o arquivo CSV
        caminho_csv = os.path.join(output_dir, nome_arquivo_base + ".csv")
        tabela.to_csv(caminho_csv, index=False, encoding='utf-8-sig')

        # Salva o arquivo HTML
        caminho_html = os.path.join(html_dir, nome_arquivo_base + ".html")
        tabela.to_html(caminho_html, index=False)

        # Cria uma figura com a tabela para salvar como JPG
        # Ajusta o tamanho da figura de acordo com o número de linhas e colunas
        fig, ax = plt.subplots(figsize=(len(tabela.columns)*2, len(tabela)*0.5 + 1))
        ax.axis('tight')
        ax.axis('off')
        tabela_plot = ax.table(cellText=tabela.values,
                               colLabels=tabela.columns,
                               cellLoc='center',
                               loc='center')
        fig.tight_layout()

        # Salva a figura em formato JPG
        caminho_img = os.path.join(img_dir, nome_arquivo_base + ".jpg")
        plt.savefig(caminho_img, format='jpg', bbox_inches='tight')
        plt.close(fig)

        print(f"Arquivos gerados para a temporada {temporada}:")
        print(f"  CSV:  {caminho_csv}")
        print(f"  HTML: {caminho_html}")
        print(f"  JPG:  {caminho_img}\n")