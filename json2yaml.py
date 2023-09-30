import json
import yaml
import sys

in_file = sys.argv[1]
out_file = in_file.split('.')[0] + ".yaml"

with open(in_file, 'r') as input_file, open(out_file, "w") as output_file:
    data = json.load(input_file)
    #yaml.dump(data, output_file, sort_keys=False)
    yaml.safe_dump(data, output_file, encoding='utf-8', allow_unicode=True, sort_keys=False)


    if element['Text'] or element['Kids']: