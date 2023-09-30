import os.path

import pdftotext

# get base path.
base_path = os.path.dirname(os.path.abspath(__file__))

# directory structure
input_dir = "/resources/"
output_dir = "/output/"

# file to convert
filename = "2019-coalicion-progresista.pdf"
file_path = base_path + input_dir + filename

# Load your PDF
with open(file_path, "rb") as f:
    pdf = pdftotext.PDF(f)

# Read all the text into one string
print("\n\n".join(pdf))