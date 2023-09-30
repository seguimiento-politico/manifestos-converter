import json
import os.path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def convert_pdf_to_json(pdf_path):
    output = {"pages": []}
    page_num = 0
    
    for page_layout in extract_pages(pdf_path):
        page_num += 1
        page_data = {"page_number": page_num, "content": []}
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                line_content = ""
                bold_flags = []
                for char in element:
                    if isinstance(char, LTChar):
                        line_content += char.get_text()
                        bold_flags.append("Bold" in char.fontname)
                is_bold = any(bold_flags)
                page_data["content"].append({
                    "text": line_content,
                    "bold": is_bold
                })
        output["pages"].append(page_data)

    return json.dumps(output, ensure_ascii=False, indent=4)

# get base path.
base_path = os.path.dirname(os.path.abspath(__file__))

input_dir = "/resources/"
output_dir = "/output/"

filename = "2019-coalicion-progresista.pdf"
file_path = base_path + input_dir + filename

# Uso de la función
json_data = convert_pdf_to_json(file_path)

# Guardar el contenido JSON en un archivo
with open(base_path + output_dir + 'output.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print("¡Conversión completa!")
