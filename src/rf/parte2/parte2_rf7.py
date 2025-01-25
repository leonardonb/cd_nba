from matplotlib import pyplot as plt
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import os

def fetch_player_stats(player_id):
    """
    Busca os dados de jogos de um jogador na temporada atual e retorna pontos, rebotes e assistências.

    Args:
        player_id (int): ID do jogador na NBA API.

    Returns:
        pd.DataFrame: DataFrame com os dados dos jogos do jogador.
    """
    try:
        player_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season="2024-25",
            timeout=30
        ).get_data_frames()[0]

        player_log = player_log[player_log['MATCHUP'].str.contains("BKN")]

        player_log = player_log.rename(columns={
            'PTS': 'Pontos',
            'REB': 'Rebotes',
            'AST': 'Assistências',
            'GAME_DATE': 'Data do Jogo'
        })

        return player_log[['Data do Jogo', 'Pontos', 'Rebotes', 'Assistências']]

    except Exception as e:
        print(f"Erro ao buscar dados do jogador {player_id}: {e}")
        return pd.DataFrame()

def calcular_e_apresentar_modas(players, output_dir, html_dir, img_dir):
    """
    Calcula e apresenta a moda de pontos, rebotes e assistências dos jogadores,
    além da quantidade de vezes que a moda aparece e a porcentagem de partidas abaixo da média.

    Args:
        players (list): Lista de dicionários com nomes e IDs dos jogadores.
        output_dir (str): Diretório para salvar os resultados em CSV.
        html_dir (str): Diretório para salvar os resultados em HTML.
        img_dir (str): Diretório para salvar os resultados como imagens.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for player in players:
        player_name = player['PLAYER']
        player_id = player['PLAYER_ID']

        try:
            print(f"Buscando dados do jogador: {player_name}, ID: {player_id}")
            stats = fetch_player_stats(player_id)

            if stats.empty:
                print(f"Nenhumas estatísticas encontradas para {player_name}.")
                continue

            modas = []
            ocorrencias_moda = []

            for col in ['Pontos', 'Rebotes', 'Assistências']:
                moda = stats[col].mode()

                # Verificar se todos os valores aparecem com a mesma frequência
                freq = stats[col].value_counts()
                if freq.nunique() == 1:  # Todos os valores têm a mesma frequência
                    modas.append("Não possui")
                    ocorrencias_moda.append(0)
                elif len(moda) > 1:  # Caso multimodal
                    modas.append(", ".join(map(str, moda.values)))
                    ocorrencias_moda.append(", ".join([str((stats[col] == m).sum()) for m in moda]))
                else:  # Caso com uma única moda
                    modas.append(moda.iloc[0])
                    ocorrencias_moda.append((stats[col] == moda.iloc[0]).sum())


            # Cálculo das médias
            medias = stats[['Pontos', 'Rebotes', 'Assistências']].mean()

            # Identificar partidas abaixo da média
            abaixo_da_media = stats[['Pontos', 'Rebotes', 'Assistências']].lt(medias)

            # Calcular porcentagens de partidas abaixo da média
            porcentagens_abaixo = abaixo_da_media.mean() * 100

            # Criar DataFrame final
            final = pd.DataFrame({
                'Estatística': ['Pontos', 'Rebotes', 'Assistências'],
                'Moda': modas,
                'Ocorrências da Moda': ocorrencias_moda,
                '% Abaixo da Média': porcentagens_abaixo.round(2).values
            })

            # Salvar como CSV
            csv_path = os.path.join(output_dir, f"{player_name}_modas.csv")
            final.to_csv(csv_path, index=False)
            print(f"Tabela CSV salva em: {csv_path}")

            # Salvar como HTML
            html_path = os.path.join(html_dir, f"{player_name}_modas.html")
            final.to_html(html_path, index=False)
            print(f"Tabela HTML salva em: {html_path}")

            # Salvar como imagem
            img_path = os.path.join(img_dir, f"{player_name}_modas.jpg")
            salvar_tabela_como_imagem(final, img_path, f"Modas - {player_name}")

        except Exception as e:
            print(f"Erro ao processar dados do jogador {player_name}: {e}")

    print('Processamento do RF7 concluído.')

def salvar_tabela_como_imagem(df, img_path, title):
    """
    Salva uma tabela como imagem.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem salvos.
        img_path (str): Caminho para salvar a imagem.
        title (str): Título da tabela.
    """
    if df.empty:
        print("DataFrame vazio. Não é possível salvar como imagem.")
        return

    fig, ax = plt.subplots(figsize=(8, len(df) * 0.6))
    ax.axis("off")
    ax.axis("tight")
    ax.set_title(title, fontsize=14, weight="bold")
    table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(img_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Tabela salva como imagem em: {img_path}")
