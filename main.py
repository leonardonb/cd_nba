from src.visualizations.graficos_estatisticas import (
    visualizar_pontos_por_jogo,
    criar_grafico_pontos_jogadores,
    criar_grafico_comparativo_times
)
from src.data.coleta_dados import (
    coletar_dados_jogadores,
    coletar_dados_time,
    coletar_dados_todos_os_times
)
from src.data.limpeza_dados import tratar_dados_jogadores
from src.analytics.regressoes import regressao_linear, regressao_logistica
import numpy as np
import pandas as pd
import os

def salvar_relatorio(texto, caminho):
    """
    Salva um relatório de texto no caminho especificado.

    Args:
        texto (str): Conteúdo do relatório.
        caminho (str): Caminho para salvar o arquivo.
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w') as arquivo:
        arquivo.write(texto)
    print(f"Relatório salvo em: {caminho}")

def gerar_intro_relatorio(jogadores, temporada):
    """
    Gera a introdução para o relatório.

    Args:
        jogadores (dict): Mapeamento de IDs para nomes dos jogadores.
        temporada (str): Temporada analisada.

    Returns:
        str: Introdução do relatório.
    """
    texto = (
        f"Relatório de Análise de Desempenho - Temporada {temporada}\n\n"
        f"Este relatório analisa o desempenho do time Brooklyn Nets e de três jogadores específicos:\n"
    )
    for jogador in jogadores.values():
        texto += f"- {jogador}\n"
    texto += (
        "\nOs dados coletados incluem informações sobre pontuação (PTS), rebotes (REB), assistências (AST) "
        "e impacto no placar (PLUS_MINUS). Além disso, foram feitas comparações com outros times da NBA e predições "
        "para entender o desempenho futuro dos jogadores e do time.\n\n"
    )
    return texto

def main():
    # IDs dos jogadores e do time Brooklyn Nets
    jogadores_ids = [1629680, 201609, 1627742]  # Cam Thomas, Dennis Schroder, Cameron Johnson
    id_para_nome = {
        1629680: "Cam Thomas",
        201609: "Dennis Schroder",
        1627742: "Cameron Johnson"
    }
    nets_id = 1610612751  # ID do Brooklyn Nets
    season = '2024-25'

    # Inicializar o relatório
    relatorio = []
    relatorio.append(gerar_intro_relatorio(id_para_nome, season))

    # Coleta e limpeza de dados dos jogadores
    print("Coletando dados dos jogadores...")
    relatorio.append("**Coletando dados dos jogadores...**\n")
    dados_brutos_jogadores = coletar_dados_jogadores(player_ids=jogadores_ids, season=season)
    dados_tratados_jogadores = tratar_dados_jogadores(dados_brutos_jogadores)

    # Coleta e limpeza de dados do time Brooklyn Nets
    print("Coletando dados do time Brooklyn Nets...")
    relatorio.append("\n**Coletando dados do time Brooklyn Nets...**\n")
    dados_nets = coletar_dados_time(nets_id, season)
    media_pontos_nets = dados_nets['PTS'].mean()
    relatorio.append(
        f"O Brooklyn Nets teve uma média de pontos de {media_pontos_nets:.2f} por jogo nesta temporada.\n"
    )

    # Comparação com outros times
    print("Coletando dados de todos os times da NBA...")
    relatorio.append("\n**Comparação com outros times da NBA...**\n")
    dados_todos_os_times = coletar_dados_todos_os_times(season)

    # Verificar colunas disponíveis e ajustar agrupamento
    print("Colunas disponíveis nos dados de todos os times:")
    print(dados_todos_os_times.columns)

    # Ajustar para a coluna correta de ID do time
    if 'TEAM_ID' in dados_todos_os_times.columns:
        media_pontos_times = dados_todos_os_times.groupby('TEAM_ID')['PTS'].mean()
    elif 'Team_ID' in dados_todos_os_times.columns:
        media_pontos_times = dados_todos_os_times.groupby('Team_ID')['PTS'].mean()
    else:
        raise KeyError("A coluna correspondente ao ID do time não foi encontrada nos dados.")

    rank_nets = media_pontos_times.rank(ascending=False).loc[nets_id]
    relatorio.append(
        f"O Brooklyn Nets está na posição {int(rank_nets)} entre os times em média de pontos por jogo.\n"
    )

    # Adicionar gráfico comparativo dos times
    print("Criando gráfico comparativo entre o Nets e outros times...")
    criar_grafico_comparativo_times(media_pontos_times, nets_id)
    relatorio.append(
        "Um gráfico foi gerado para comparar a média de pontos do Brooklyn Nets com os outros times da NBA.\n"
    )

    # Estatísticas e predições dos jogadores
    print("\n**Estatísticas e Predições dos Jogadores:**")
    relatorio.append("\n**Estatísticas e Predições dos Jogadores:**\n")
    for player_id in jogadores_ids:
        nome_jogador = id_para_nome[player_id]
        dados_jogador = dados_tratados_jogadores[dados_tratados_jogadores['Player_ID'] == player_id]
        relatorio.append(
            f"\nJogador: {nome_jogador}\n"
            f"  - Pontos máximos em um jogo: {dados_jogador['PTS'].max()}\n"
            f"  - Média de rebotes por jogo: {dados_jogador['REB'].mean():.2f}\n"
            f"  - Assistências máximas em um jogo: {dados_jogador['AST'].max()}\n"
        )

    # Salvar relatório em arquivo
    salvar_relatorio('\n'.join(relatorio), './reports/analises.txt')

if __name__ == "__main__":
    main()