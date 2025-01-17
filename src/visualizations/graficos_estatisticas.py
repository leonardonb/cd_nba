import os
import matplotlib
matplotlib.use('TkAgg')  # Backend interativo
import matplotlib.pyplot as plt


def visualizar_pontos_por_jogo(data):
    """
    Gera um gráfico de linha para visualizar os pontos por jogo.

    Args:
        data (pd.DataFrame): DataFrame tratado contendo as colunas 'Game_ID' e 'PTS'.
    """
    # Verificar se as colunas esperadas estão presentes
    if 'Game_ID' not in data.columns or 'PTS' not in data.columns:
        raise ValueError("As colunas 'Game_ID' e 'PTS' são necessárias no DataFrame.")

    # Criar a pasta para salvar gráficos, se não existir
    os.makedirs('./reports/graficos/', exist_ok=True)

    # Plotar os pontos por jogo
    plt.plot(data['Game_ID'], data['PTS'], marker='o', label='Pontos por Jogo')
    plt.title("Evolução dos Pontos por Jogo")
    plt.xlabel("ID do Jogo")
    plt.ylabel("Pontos")
    plt.legend()

    try:
        plt.show()  # Exibir o gráfico interativamente
        print("Gráfico exibido com sucesso.")
    except Exception as e:
        print(f"Erro ao exibir o gráfico: {e}")
        arquivo = './reports/graficos/pontos_por_jogo.png'
        plt.savefig(arquivo)
        print(f"Gráfico salvo em: {arquivo}")
    finally:
        plt.close('all')  # Fechar o gráfico após uso


def criar_grafico_linha(data, eixo_x, eixo_y, titulo, x_label, y_label, arquivo=None):
    """
    Gera um gráfico de linha e salva ou exibe o gráfico.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados.
        eixo_x (str): Nome da coluna para o eixo X.
        eixo_y (str): Nome da coluna para o eixo Y.
        titulo (str): Título do gráfico.
        x_label (str): Rótulo do eixo X.
        y_label (str): Rótulo do eixo Y.
        arquivo (str, opcional): Caminho para salvar o gráfico. Se None, exibe o gráfico.
    """
    if eixo_x not in data.columns or eixo_y not in data.columns:
        raise ValueError(f"As colunas '{eixo_x}' e '{eixo_y}' são necessárias no DataFrame.")

    plt.plot(data[eixo_x], data[eixo_y], marker='o', label=y_label)
    plt.title(titulo)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    if arquivo:
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        plt.savefig(arquivo)
        print(f"Gráfico salvo em: {arquivo}")
    else:
        plt.show()
        print("Gráfico exibido com sucesso.")
    plt.close('all')  # Fechar o gráfico após uso


def criar_grafico_barras(data, eixo_x, eixo_y, titulo, x_label, y_label, arquivo=None):
    """
    Gera um gráfico de barras e salva ou exibe o gráfico.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados.
        eixo_x (str): Nome da coluna para o eixo X.
        eixo_y (str): Nome da coluna para o eixo Y.
        titulo (str): Título do gráfico.
        x_label (str): Rótulo do eixo X.
        y_label (str): Rótulo do eixo Y.
        arquivo (str, opcional): Caminho para salvar o gráfico. Se None, exibe o gráfico.
    """
    if eixo_x not in data.columns or eixo_y not in data.columns:
        raise ValueError(f"As colunas '{eixo_x}' e '{eixo_y}' são necessárias no DataFrame.")

    plt.bar(data[eixo_x], data[eixo_y], label=y_label)
    plt.title(titulo)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    if arquivo:
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        plt.savefig(arquivo)
        print(f"Gráfico salvo em: {arquivo}")
    else:
        plt.show()
        print("Gráfico exibido com sucesso.")
    plt.close('all')  # Fechar o gráfico após uso


def criar_grafico_pontos_jogadores(data, jogadores, id_para_nome):
    """
    Cria gráficos de pontos por jogo para cada jogador.

    Args:
        data (pd.DataFrame): Dados tratados.
        jogadores (list): Lista de IDs de jogadores.
        id_para_nome (dict): Mapeamento de IDs para nomes dos jogadores.
    """
    # Criar a pasta para salvar gráficos, se não existir
    os.makedirs('./reports/graficos/', exist_ok=True)

    # Iterar sobre cada jogador e plotar seus dados
    for player_id in jogadores:
        jogador_dados = data[data['Player_ID'] == player_id]
        if not jogador_dados.empty:  # Verificar se há dados para o jogador
            nome_jogador = id_para_nome.get(player_id, f"Jogador {player_id}")
            plt.plot(
                jogador_dados['Game_ID'],
                jogador_dados['PTS'],
                marker='o',
                label=nome_jogador  # Nome do jogador na legenda
            )

    # Configuração do gráfico
    plt.title("Evolução dos Pontos por Jogo")
    plt.xlabel("ID do Jogo")
    plt.ylabel("Pontos")
    plt.legend()  # Exibir a legenda com os nomes dos jogadores
    plt.savefig('./reports/graficos/pontos_jogadores.png')  # Salvar o gráfico
    plt.show()  # Exibir o gráfico interativamente
    plt.close('all')  # Fechar o gráfico após uso

def criar_grafico_comparativo_times(media_pontos_times, nets_id):
    """
    Cria um gráfico comparativo entre o Brooklyn Nets e outros times.

    Args:
        media_pontos_times (pd.Series): Média de pontos por jogo de cada time.
        nets_id (int): ID do Brooklyn Nets.
    """
    # Criar pasta para salvar gráficos
    os.makedirs('./reports/graficos/', exist_ok=True)

    # Transformar IDs dos times em categorias
    media_pontos_times = media_pontos_times.sort_values(ascending=False)
    times = media_pontos_times.index.astype(str)  # Convertendo IDs para string para melhor visualização
    valores = media_pontos_times.values

    # Configuração do gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(times, valores, label='Média de Pontos por Time', alpha=0.7)

    # Destacar o Brooklyn Nets
    if nets_id in media_pontos_times.index:
        nets_media = media_pontos_times.loc[nets_id]
        plt.bar(str(nets_id), nets_media, color='red', label='Brooklyn Nets')

    plt.title("Comparação da Média de Pontos entre Times")
    plt.xlabel("Times (ID)")
    plt.ylabel("Média de Pontos por Jogo")
    plt.xticks(rotation=90)  # Rotacionar os rótulos do eixo x para melhor visualização
    plt.legend()

    # Salvar e exibir o gráfico
    plt.savefig('./reports/graficos/comparacao_times.png')
    plt.show()