# Salvar PDFs
def converter_html_para_pdf(html_dir, pdf_dir):
    """
    Converte todos os arquivos HTML em um diretório para PDFs e os salva em outro diretório.

    Args:
        html_dir (str): Diretório contendo os arquivos HTML.
        pdf_dir (str): Diretório onde os PDFs serão salvos.
    """
    # Caminho manual para o executável wkhtmltopdf (ajuste conforme necessário)
    config = pdfkit.configuration(wkhtmltopdf=r'C:\caminho\para\wkhtmltopdf.exe')

    os.makedirs(pdf_dir, exist_ok=True)
    for file_name in os.listdir(html_dir):
        if file_name.endswith(".html"):
            html_path = os.path.join(html_dir, file_name)
            pdf_path = os.path.join(pdf_dir, file_name.replace(".html", ".pdf"))
            pdfkit.from_file(html_path, pdf_path, configuration=config)
            print(f"Arquivo convertido para PDF: {pdf_path}")