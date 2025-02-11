## Dependências do Projeto

Para executar este projeto, é necessário instalar as seguintes bibliotecas Python. Certifique-se de que todas estão instaladas antes de rodar o código.

### Instalação
Você pode instalar todas as dependências de uma vez usando o seguinte comando:

```bash
pip install pandas matplotlib seaborn plotly numpy scipy mpld3 requests beautifulsoup4 scikit-learn pygam nba_api pdfkit dash python-dotenv
```

---

### Bibliotecas Principais

| Biblioteca       | Descrição                                                                 |
|------------------|---------------------------------------------------------------------------|
| **pandas**       | Manipulação e análise de dados em formato tabular.                        |
| **numpy**        | Computação numérica e operações com arrays.                               |
| **matplotlib**   | Criação de gráficos e visualizações estáticas.                           |
| **seaborn**      | Visualização de dados estatísticos com gráficos mais atraentes.           |
| **plotly**       | Criação de gráficos interativos.                                         |
| **scipy**        | Funções matemáticas avançadas e estatísticas.                            |
| **scikit-learn** | Ferramentas para machine learning, como regressão e classificação.       |
| **pygam**        | Modelos aditivos generalizados (GAM) para análise estatística.           |

---

### Bibliotecas de Web Scraping e Requisições HTTP

| Biblioteca       | Descrição                                                                 |
|------------------|---------------------------------------------------------------------------|
| **requests**     | Realização de requisições HTTP para coleta de dados da web.               |
| **beautifulsoup4** | Parsing de HTML e XML para extração de dados.                           |

---

### Bibliotecas Específicas para NBA

| Biblioteca       | Descrição                                                                 |
|------------------|---------------------------------------------------------------------------|
| **nba_api**      | Acesso a dados e estatísticas da NBA diretamente da API oficial.         |

---

### Bibliotecas de Geração de PDF e Visualização Web

| Biblioteca       | Descrição                                                                 |
|------------------|---------------------------------------------------------------------------|
| **pdfkit**       | Geração de arquivos PDF a partir de HTML (requer `wkhtmltopdf` instalado).|
| **dash**         | Criação de aplicações web interativas com gráficos.                       |

---

### Outras Bibliotecas

| Biblioteca       | Descrição                                                                 |
|------------------|---------------------------------------------------------------------------|
| **python-dotenv**| Carregamento de variáveis de ambiente a partir de um arquivo `.env`.      |
| **mpld3**        | Conversão de gráficos Matplotlib para HTML interativo.                    |

---

### Configuração do Arquivo `.env`

Para garantir o funcionamento correto do projeto, siga as instruções abaixo para criar e configurar o arquivo `.env`:

1. **Crie um arquivo `.env` na raiz do projeto**:
   - Na raiz do seu projeto, crie um arquivo chamado `.env`.

2. **Adicione a variável `ENGINE_IMAGE`**:
   - Dentro do arquivo `.env`, adicione uma das seguintes linhas, dependendo da engine que você está utilizando:
     ```plaintext
     ENGINE_IMAGE="kaleido"
     ```
     ou
     ```plaintext
     ENGINE_IMAGE="orca"
     ```

   - Escolha `"kaleido"` ou `"orca"` com base na engine que você está usando para gerar visualizações.

---

### Observações
- Certifique-se de que todas as bibliotecas estão atualizadas para evitar conflitos de versão.
- O projeto depende de uma conexão com a internet para acessar dados da NBA via `nba_api`.
- Certifique-se de que o arquivo .env tenha sido criado corretamente.

---

### Executar
- Para executar o código, use o comando:

```bash
python main.py
```