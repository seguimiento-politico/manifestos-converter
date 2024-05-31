import json
import logging
import os.path
import sys
import asyncio
from zipfile import ZipFile

# only useful to cerate an index.
# if all the content of the pdf is needed use pdf2text instead.

from extract_txt_with_styling_info_from_pdf import extract_pdf_to_json
from transform_from_json_data_to_yaml_manifest import convert_json_to_yaml_manifest

# get base path.
base_path = os.path.dirname(os.path.abspath(__file__))
input_dir = base_path + "/inputs/"
intermediate_dir = base_path + "/intermediate/"
output_dir = base_path + "/outputs/"

#transform PDF to a structured JSON
async def parse_files():
    # Opening JSON file
    f = open('pdfservices-api-credentials.json')

    # returns JSON object as a dictionary
    data = json.load(f)

    # Set enviroment variables
    os.environ["PDF_SERVICES_CLIENT_ID"] = data['client_credentials']['client_id']
    os.environ["PDF_SERVICES_CLIENT_SECRET"] = data['client_credentials']['client_secret']

    # Iterate resources directory
    for file_path in os.listdir(input_dir):
        print("FILE TO PARSE: " + file_path)
        await extract_pdf_to_json(file_path)
        os.remove(input_dir + file_path)

#asyncio.run(parse_files())

#extract the JSON files from ZIP files
def extract_files():
    # Iterate output directory
    for file_path in os.listdir(intermediate_dir):
        # check if the file is a zip
        file_name = file_path.split(".")
        file_type = file_name[len(file_name)-1]
        if file_type == "zip":
            print("FILE TO EXTRACT: " + file_path)
            # loading the temp.zip and creating a zip object
            with ZipFile(intermediate_dir + file_path, 'r') as zObject:
                # rename the destination file
                zObject.getinfo("structuredData.json").filename = file_name[0] + ".json"
                # Extracting all content of the zip into a specific location.
                zObject.extract("structuredData.json", path=intermediate_dir)
                #os.remove(intermediate_dir + file_path)

#extract_files()

#transform the JSON data into a cutmom structured YAML file
def convert_files():
    # Iterate output directory
    for file_path in os.listdir(intermediate_dir):
        # check if the file is a json
        file_name = file_path.split(".")
        file_type = file_name[len(file_name)-1]
        if file_type == "json":
            print("FILE TO CONVERT: " + file_path)
            convert_json_to_yaml_manifest(file_path)

convert_files()