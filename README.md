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

### Observações
- Certifique-se de que todas as bibliotecas estão atualizadas para evitar conflitos de versão.
- O projeto depende de uma conexão com a internet para acessar dados da NBA via `nba_api`.

---

### Executar
- Para executar o código, use o comando:

```bash
python main.py
```