import shutil
import os

def copiar_pasta(origem, destino):
    """
    Copia todos os arquivos de uma pasta para outra.

    Args:
        origem (str): Caminho da pasta de origem.
        destino (str): Caminho da pasta de destino.
    """
    if not os.path.exists(origem):
        print(f"❌ Erro: A pasta de origem '{origem}' não existe.")
        return

    if not os.path.exists(destino):
        os.makedirs(destino)

    arquivos_copiados = 0
    for arquivo in os.listdir(origem):
        caminho_origem = os.path.join(origem, arquivo)
        caminho_destino = os.path.join(destino, arquivo)

        if os.path.isfile(caminho_origem):  # Garante que só copia arquivos
            shutil.copy2(caminho_origem, caminho_destino)
            arquivos_copiados += 1

    print(f"✅ {arquivos_copiados} arquivos copiados de '{origem}' para '{destino}'.")

if __name__ == "__main__":
    # Lista de pares (origem, destino)
    caminhos = [
        ("reports/imagens/parte1/parte1-rf8", "src/visualizations/dashboard/parte1/assets"),
        ("reports/imagens/parte2/parte2-rf10", "src/visualizations/dashboard/parte2/assets")
    ]

    # Executa a cópia para cada par
    for origem, destino in caminhos:
        copiar_pasta(origem, destino)

# Rode este comando para copiar os gráficos das RFs específicas para a pasta do Dash:
# python src/utils/copiar_pasta.py
