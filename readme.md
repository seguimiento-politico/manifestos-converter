## Requirements
This script uses the Adobe pdfservices API to extract the PDF text into a structured JSON file.
1. Before using "pdfservices-sdk" must be installed by typing in terminal "pip install requirements.txt"
2. You also need to get the API credentials and copy the resulting file "pdfservices-api-credentials.json" into the root folder 

## How to use it
1. Copy to the "Inputs" folder all the PDF to be converted
2. Execute "python main.py"
3. The resulting YAML files will be generated into "Output" folder. The "Intermediate" folder locates the JSON files created via Adobe pdfservices_sdk

## Troubleshouting
If after executing you get an error like this one: "OSError: [Errno 18] Invalid cross-device link: ..." you may fixe it by following theese steps:
1. open /usr/local/lib/python3.9/dist-packages/pdfservices_sdk-2.3.0-py3.9.egg/adobe/pdfservices/operation/internal/io/file_ref_impl.py
2. look for "os.rename(self._file_path, abs_path)"
3. replace it "shutil.copy(self._file_path, abs_path)" and "os.remove(self._file_path, abs_path)"
4. at the line #15 add "import shutil"