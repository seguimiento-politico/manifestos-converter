import os.path
import sys
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import yaml

# only useful to create an index. not content included in the YAML resulting file
# to include everything use pdf2text.py instead

def extract_content_from_pdf(pdf_path):
    data = {"index": []}
    current_chapters = [0, 0, 0, 0, 0]  # Asumimos hasta H5, se puede ajustar
    stack = [data["index"]]
    
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            print(element)
            if isinstance(element, LTTextContainer):
                # Estimar si es un header basado en el tamaño de fuente y el estilo
                font_sizes = [char.size for char in element if isinstance(char, LTChar)]
                avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 0

                is_bold = any("Bold" in char.fontname for char in element if isinstance(char, LTChar))
                is_header = is_bold  # Esto es solo una suposición. Ajustar según sea necesario.
                
                content = element.get_text().strip()

                if is_header:
                    level = int(avg_font_size)  # Estimación basada en el tamaño de fuente. Ajustar según sea necesario.
                    current_chapters[level-1] += 1

                    for i in range(level, len(current_chapters)):
                        current_chapters[i] = 0

                    chapter_data = {
                        "chapter": current_chapters[level-1],
                        "title": content,
                        "page": -1  # Por ahora no detectamos el número de página. Añadir si es necesario.
                    }

                    for _ in range(len(stack) - level):
                        stack.pop()

                    stack[-1].append(chapter_data)

                    if "children" not in chapter_data:
                        chapter_data["children"] = []
                    
                    stack.append(chapter_data["children"])

                else:
                    stack[-1].append({"text": content})

    return data

def convert_pdf_to_yaml(pdf_path, yaml_path):
    data = extract_content_from_pdf(pdf_path)
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

# get base path.
base_path = os.path.dirname(os.path.abspath(__file__))
input_dir = "/inputs/"
output_dir = "/outputs/"
filename = sys.argv[1]
file_path = base_path + input_dir + filename

# Convertir PDF a YAML
convert_pdf_to_yaml(file_path, base_path + output_dir + 'output.yaml')
print("¡Conversión completa!")
