import os
import os.path
from pathlib import Path

from modeller import *
from modeller.automodel import *
import requests

##### 1 download the 2R9R.fasta file 3LUT.pdb file and 8VC3.pdb file
urls = [{"file_name":"2R9R.fasta","url":"https://www.rcsb.org/fasta/entry/2R9R"},
        {"file_name":"3LUT.pdb","url":"https://files.rcsb.org/download/3LUT.pdb"},
        {"file_name":"8VC3.pdb","url":"https://files.rcsb.org/download/8VC3.pdb"}]

for item in urls:
    if os.path.exists(item["file_name"]):
        print(f"{item['file_name']} already exists")
    else:
        print(f"Downloading {item['file_name']} from {item['url']}")
        r = requests.get(item["url"])
        with open(item["file_name"], 'wb') as f:
            f.write(r.content)

print("Templates downloaded successfully")
