import os
import os.path
from pathlib import Path

from modeller import *
from modeller.automodel import *
from modeller.scripts import complete_pdb
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

##### 2 extract the chain B from 2R9R.fasta and save it in 2R9R_2.fasta
with open("2R9R.fasta") as f:
    data = f.read()
    data = [str(">"+x).strip() for x in data.split(">") if x.strip()!=""]
    print(*data,sep="\n")
with open("2R9R_2.fasta","w") as f:
    f.write(data[1])

##### 3 create the pir file for sequence
log.verbose()
env = Environ()
target_sequence_fasta_path ="2R9R_2.fasta"
# Read aligned sequence(s):
a = alignment(env, file=f'{target_sequence_fasta_path}', alignment_format='FASTA')
a.write(file=f'{target_sequence_fasta_path.split(".")[0] + ".pir"}', alignment_format='PIR')



##### 4 create the multiple template alignment
log.verbose()
env = Environ()
env.io.atom_files_directory = ['.', '../atom_files/']

# Template PDB files and chains
templates = [('8VC3', 'B'), ('3LUT', 'B')]
aln = Alignment(env)

for pdb, chain in templates:
    mdl = Model(env, file=pdb, model_segment=('FIRST:'+chain, 'LAST:'+chain))
    aln.append_model(mdl, align_codes=pdb, atom_files=pdb)

# Read the target sequence
aln.append(file='2R9R_2.pir', align_codes='2R9R')

# Perform alignment
aln.align2d(max_gap_length=50)

# Save alignment
aln.write(file='2R9R-mult.ali', alignment_format='PIR')
aln.write(file='2R9R-mult.pap', alignment_format='PAP')

# Now write separate template alignments
for pdb, chain in templates:
    aln_single = Alignment(env)
    mdl = Model(env, file=pdb, model_segment=('FIRST:'+chain, 'LAST:'+chain))
    aln_single.append_model(mdl, align_codes=pdb, atom_files=pdb)
    aln_single.append(file='2R9R_2.pir', align_codes='2R9R')
    aln_single.align2d()
    aln_single.write(file='res.ali', alignment_format='PIR')
    aln_single.write(file='res.pap', alignment_format='PAP')

##### 5 build models using MODELLER
# FIXED: Create the models directory before using it
models_dir = Path("./models")
if models_dir.exists():
    print("models directory already exists")
else:
    models_dir.mkdir(parents=True)
log.verbose()
env = Environ()
env.io.output_directory = str(models_dir)

a = AutoModel(env, alnfile='2R9R-mult.ali',
              knowns=('8VC3', '3LUT'), sequence='2R9R',
              assess_methods=(assess.DOPE,))
a.starting_model = 1
a.ending_model = 5
a.make()

print("Models built successfully")
