from src.visualizations.graficos_estatisticas import (
    visualizar_pontos_por_jogo,
    criar_grafico_pontos_jogadores
)
from src.data.coleta_dados import coletar_dados_jogadores
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
        f"Este relatório analisa o desempenho de três jogadores durante a temporada:\n"
    )
    for jogador in jogadores.values():
        texto += f"- {jogador}\n"
    texto += (
        "\nOs dados coletados incluem informações sobre pontuação (PTS), rebotes (REB), assistências (AST) "
        "e impacto no placar (PLUS_MINUS). Além disso, foram feitas predições baseadas nesses dados para entender "
        "o desempenho futuro dos jogadores e as chances de vitória ou derrota do time.\n\n"
    )
    return texto

def main():
    # IDs dos jogadores e da temporada
    jogadores_ids = [1629680, 201609, 1627742]  # Cam Thomas, Dennis Schroder, Cameron Johnson
    id_para_nome = {
        1629680: "Cam Thomas",
        201609: "Dennis Schroder",
        1627742: "Cameron Johnson"
    }
    season = '2020-25'
    # season = '2024-25'

    # Inicializar o relatório
    relatorio = []
    relatorio.append(gerar_intro_relatorio(id_para_nome, season))

    # Coleta e limpeza de dados
    print("Coletando dados dos jogadores...")
    relatorio.append("**Coletando dados dos jogadores...**\n")
    dados_brutos = coletar_dados_jogadores(player_ids=jogadores_ids, season=season)
    relatorio.append("Os dados brutos coletados contêm informações sobre o desempenho de cada jogador em diversos jogos.\n")

    print("Limpando dados...")
    relatorio.append("\n**Limpando dados...**\n")
    dados_tratados = tratar_dados_jogadores(dados_brutos)
    relatorio.append(
        "Após a limpeza, os dados foram organizados para incluir apenas as informações mais importantes: "
        "pontuação (PTS), rebotes (REB), assistências (AST) e impacto no placar (PLUS_MINUS).\n"
    )

    # Dados tratados por jogador
    print("Dados tratados por jogador:")
    relatorio.append("\n**Estatísticas por jogador:**\n")
    for player_id in jogadores_ids:
        nome_jogador = id_para_nome[player_id]
        dados_jogador = dados_tratados[dados_tratados['Player_ID'] == player_id]
        relatorio.append(
            f"\nJogador: {nome_jogador}\n"
            f"  - Pontos máximos em um jogo: {dados_jogador['PTS'].max()}\n"
            f"  - Média de rebotes por jogo: {dados_jogador['REB'].mean():.2f}\n"
            f"  - Assistências máximas em um jogo: {dados_jogador['AST'].max()}\n"
            f"  - Maior impacto no placar (PLUS_MINUS): {dados_jogador['PLUS_MINUS'].max()}\n"
        )

    # Criar gráfico consolidado de pontos por jogador
    print("Criando gráfico de pontos por jogador...")
    relatorio.append(
        "\n**Gráficos de Pontuação:**\n"
        "Um gráfico foi gerado para mostrar como cada jogador pontuou em diferentes jogos. "
        "Isso ajuda a visualizar a consistência e o impacto de cada jogador na temporada.\n"
    )
    criar_grafico_pontos_jogadores(dados_tratados, jogadores_ids, id_para_nome)

    # Executar regressão linear
    print("\nExecutando regressão linear nos dados dos jogadores...")
    relatorio.append("\n**Predição de Pontuação (Regressão Linear):**\n")
    relatorio.append(
        regressao_linear(dados_tratados) +
        "Essa análise ajuda a prever a pontuação futura de um jogador com base em suas estatísticas de rebotes, assistências e impacto no jogo.\n"
    )

    # Adicionar uma coluna fictícia 'WL' (Win = 1, Loss = 0) para regressão logística
    print("\nAdicionando coluna 'WL' fictícia...")
    dados_tratados['WL'] = np.random.choice([0, 1], size=len(dados_tratados), p=[0.5, 0.5])
    relatorio.append("\n**Predição de Vitória ou Derrota (Regressão Logística):**\n")
    relatorio.append(
        "Uma análise foi realizada para prever a probabilidade de vitória ou derrota do time com base nas estatísticas de jogo (pontos, rebotes e assistências).\n"
    )
    relatorio.append(regressao_logistica(dados_tratados))

    # Salvar relatório em arquivo
    salvar_relatorio('\n'.join(relatorio), './reports/analises.txt')

if __name__ == "__main__":
    main()