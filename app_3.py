import os
import fitz  # PyMuPDF

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

script_directory = get_script_directory()
input_folder = os.path.join(script_directory, "htmlpdf")
output_folder = os.path.join(script_directory, "html2")

os.makedirs(output_folder, exist_ok=True)

def convert_pdf_to_html(input_pdf, output_html):
    """Converts a PDF to basic HTML (text only)."""
    doc = fitz.open(input_pdf)
    html_content = "<html><body>\n"

    for page in doc:
        html_content += f"<p>{page.get_text('html')}</p>\n"

    html_content += "</body></html>"

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Converted: {input_pdf} → {output_html}")

def process_pdfs():
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".pdf"):
            input_pdf = os.path.join(input_folder, file_name)
            output_html = os.path.join(output_folder, file_name.replace(".pdf", ".html"))
            convert_pdf_to_html(input_pdf, output_html)

if __name__ == "__main__":
    process_pdfs()
    print("Conversion completed!")
