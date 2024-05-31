import os.path
import os
import sys
import pdftotext
import yaml
import re
import uuid

# get base path.
base_path = os.path.dirname(os.path.abspath(__file__))

# directory structure
input_dir = "/inputs/"
output_dir = "/outputs/"

# file to convert
filename = sys.argv[1]
file_path = base_path + input_dir + filename
filename = filename.split(".") 
output_filename = filename[0] + ".yaml"

text = ''

# instead of open both files I decided to dump the whole text so that I can avoid looping every page 
# and dumping each one which caused the inclussion of very anoying extra -''
# to be noted: there is a risk of memory errors if the file is huge

# Load your PDF
with open(file_path, "rb") as i:
    pdf = pdftotext.PDF(i)
    text = ''.join(pdf)

# write another text file
with open(base_path + output_dir + output_filename, "w", encoding="utf-8") as o:   
    # eliminar numeradcion de paginas
    # por el momento no las elimino para facilitar la identifiación de la página
    #text = re.sub(r"\n\d+\n", "", text) 
    #text = re.sub(r"\n\d+\n", "- page: ", text) 

    # elimino los fin de página
    text = re.sub(r"\f", "", text)    

    text = text.replace("•","")

    # eliminar espacios antes y despues de saltos de linea
    text = re.sub(r" \n", "\n", text)
    text = re.sub(r"\n ", "\n", text)
        
    # eliminar multiples saltos de linea
    text = re.sub(r"\n+", r"\n", text)      

    # sustituyo \n por espacio en caso de frases sin terminar (saltos de linea entre palabras con letras minusculas)
    for match in re.finditer(r"[a-z|,]\n[a-z|ú]", text):
        index = match.start()
        text = text[:index + 1] + " " + text[index + 2:] 

    # transformación final
    text = text.split("\n")
    
    res = {}
    res['id'] = str(uuid.uuid4())
    res['version'] = 2

    res['type'] = ""
    res['parties'] = ""
    res['election_type'] = ""
    res['election_date'] = ""
    res['publication_date'] = ""
    res['url'] = ""
    res['web_history'] = ""
    res['title'] = ""
    res['description'] = ""

    res['content'] = []
    for string in text:
        dict = {'declaration': {'id': str(uuid.uuid4()), 'page': "", 'text': string}}
        res['content'].append(dict)

    yaml.safe_dump(res, o, allow_unicode=True, width=float("inf"), sort_keys=False)
    
    