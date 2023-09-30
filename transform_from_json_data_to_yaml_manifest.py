import json
import yaml
import os.path
import uuid

# get base path.

def letters_only(string):
    text = ""
    for char in string:
        if char.isalpha() or char.isspace():
            if char.isspace() and text == "":
                continue
            text = text + char
    return text
#
def convert_json_to_yaml_manifest(file):
    filename = file.split('.')
    out_file = filename[0] + '.yaml'

    base_path = os.path.dirname(os.path.abspath(__file__))
    intermediate_dir = base_path + "/intermediate/"
    output_dir = base_path + "/outputs/"

    res = {}
    #element_types = {['header': 'H', 'toc': 'TOC', 'paragraph': 'P', 'list': 'L', 'list_item': 'LI', 'list_body': ' 'span': 'Span']}

    with open(intermediate_dir + file, 'r') as input_file, open(output_dir + out_file, "w") as output_file:
        data = json.load(input_file)
        data = data['elements']

        res['id'] = str(uuid.uuid4())
        res['title'] = filename[0].replace("_", " ").replace("-", " ").upper()
        res['index'] = []
        res['index2'] = []

        count = -1
        index = 0
        for element in data:
            count += 1
            try:
                path = element['Path'].replace("//Document/", "")
                #print(str(count) , end= ' ')
                #print(path)

                sub_paths = path.split('/')
                levels = len(sub_paths)
                
                # try to build index from TOC
                ## problems detected: 
                ## - not able to identify hierarchy (children)
                if(sub_paths[0] == 'TOC'):
                    if element['Text']:
                        text = ""
                        # remove any characters that ARE NOT letters
                        text = letters_only(element['Text'])
                        if text != "":
                            index += 1
                            res['index'].append({'chapter': index, 'title': text.strip().capitalize()})

                # try to build index from content
                if(sub_paths[0] != 'TOC' and sub_paths[0] != 'Figure'): 
                    if "H1" in sub_paths[0]:
                        if element['Kids']:
                            print('kids')
                            text = ""
                            for kid in element['Kids']:
                                text = text.join(letters_only(kid['Text']))
                                if text != "":
                                    index += 1
                                    res['index2'].append({'chapter': index, 'title': text.strip().capitalize()})
            except:
                continue
            
        yaml.dump(res, output_file, allow_unicode=True)

