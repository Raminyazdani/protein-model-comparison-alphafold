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

# Align templates and include ligands if present in PDB files
for (code, chain) in templates:
    mdl = Model(env, file=code, model_segment=('FIRST:'+chain, 'LAST:'+chain))
    aln.append_model(mdl, atom_files=code, align_codes=code+chain)

aln.salign(rms_cutoff=3.5, normalize_pp_scores=False,
           rr_file='$(LIB)/as1.sim.mat', overhang=30,
           gap_penalties_1d=(-450, -50),
           gap_penalties_3d=(0, 3), gap_gap_score=0, gap_residue_score=0,
           dendrogram_file='fm00495.tree',
           alignment_type='tree',
           improve_alignment=True, fit=True,
           output='ALIGNMENT QUALITY')

aln.write(file='res.pap', alignment_format='PAP')
aln.write(file='res.ali', alignment_format='PIR')

# Refine alignment
aln.salign(rms_cutoff=1.0, normalize_pp_scores=False,
           rr_file='$(LIB)/as1.sim.mat', overhang=30,
           gap_penalties_1d=(-450, -50), gap_penalties_3d=(0, 3),
           gap_gap_score=0, gap_residue_score=0, dendrogram_file='1is3A.tree',
           alignment_type='progressive', feature_weights=[0]*6,
           improve_alignment=False, fit=False, write_fit=True,
           write_whole_pdb=False, output='QUALITY')

# Read aligned sequences and templates
log.verbose()
env = Environ()
env.libs.topology.read(file='$(LIB)/top_heav.lib')

# Load alignment and structure-sensitive variable gap penalties
aln = Alignment(env)
aln.append(file='res.ali', align_codes='all')
aln_block = len(aln)
aln.append(file='2R9R_2.pir', align_codes='all')

aln.salign(output='', max_gap_length=20,
           gap_function=True,
           alignment_type='PAIRWISE', align_block=aln_block,
           feature_weights=(1., 0., 0., 0., 0., 0.), overhang=0,
           gap_penalties_1d=(-450, 0),
           gap_penalties_2d=(0.35, 1.2, 0.9, 1.2, 0.6, 8.6, 1.2, 0., 0.),
           similarity_flag=True)

aln.write(file='2R9R-mult.ali', alignment_format='PIR')
aln.write(file='2R9R-mult.pap', alignment_format='PAP')

# Generate models including ligand prediction
models_dir = Path("./models")
if models_dir.exists():
    print("models directory already exists")
else:
    models_dir.mkdir(parents=True)
log.verbose()
env = Environ()
env.io.output_directory = str(models_dir)
a = AutoModel(env, alnfile='2R9R-mult.ali',
              knowns=('3LUTB','8VC3B'), sequence='2R9R_2|Chains',
              assess_methods=(assess.DOPE))
a.starting_model = 1
a.ending_model = 5
a.make()

# best model is 2R9R_2|Chains.B99990004.pdb    12625.04395   -43980.13672

with open("2R9R_modeller.pdb","w") as f:
    with open("2R9R_2|Chains.B99990004.pdb") as f2:
        f.write(f2.read())


# now i want to try model with the ligand prediction
hetero_dir = Path("./with_hetero")
if not hetero_dir.exists():
    hetero_dir.mkdir(parents=True)
os.chdir(str(hetero_dir))

######

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
env.io.hetatm = True

target_sequence_fasta_path ="2R9R_2.fasta"
# Read aligned sequence(s):
a = alignment(env, file=f'{target_sequence_fasta_path}', alignment_format='FASTA')
a.write(file=f'{target_sequence_fasta_path.split(".")[0] + ".pir"}', alignment_format='PIR')



##### 4 create the multiple template alignment
log.verbose()
env = Environ()
env.io.hetatm = True

env.io.atom_files_directory = ['.', '../atom_files/']

# Template PDB files and chains
templates = [('8VC3', 'B'), ('3LUT', 'B')]
aln = Alignment(env)

# Align templates and include ligands if present in PDB files
for (code, chain) in templates:
    mdl = Model(env, file=code, model_segment=('FIRST:'+chain, 'LAST:'+chain))
    aln.append_model(mdl, atom_files=code, align_codes=code+chain)

aln.salign(rms_cutoff=3.5, normalize_pp_scores=False,
           rr_file='$(LIB)/as1.sim.mat', overhang=30,
           gap_penalties_1d=(-450, -50),
           gap_penalties_3d=(0, 3), gap_gap_score=0, gap_residue_score=0,
           dendrogram_file='fm00495.tree',
           alignment_type='tree',
           improve_alignment=True, fit=True,
           output='ALIGNMENT QUALITY')

aln.write(file='res.pap', alignment_format='PAP')
aln.write(file='res.ali', alignment_format='PIR')

# Refine alignment
aln.salign(rms_cutoff=1.0, normalize_pp_scores=False,
           rr_file='$(LIB)/as1.sim.mat', overhang=30,
           gap_penalties_1d=(-450, -50), gap_penalties_3d=(0, 3),
           gap_gap_score=0, gap_residue_score=0, dendrogram_file='1is3A.tree',
           alignment_type='progressive', feature_weights=[0]*6,
           improve_alignment=False, fit=False, write_fit=True,
           write_whole_pdb=False, output='QUALITY')

# Read aligned sequences and templates
log.verbose()
env = Environ()
env.io.hetatm = True

env.libs.topology.read(file='$(LIB)/top_heav.lib')

# Load alignment and structure-sensitive variable gap penalties
aln = Alignment(env)
aln.append(file='res.ali', align_codes='all')
aln_block = len(aln)
aln.append(file='2R9R_2.pir', align_codes='all')

aln.salign(output='', max_gap_length=20,
           gap_function=True,
           alignment_type='PAIRWISE', align_block=aln_block,
           feature_weights=(1., 0., 0., 0., 0., 0.), overhang=0,
           gap_penalties_1d=(-450, 0),
           gap_penalties_2d=(0.35, 1.2, 0.9, 1.2, 0.6, 8.6, 1.2, 0., 0.),
           similarity_flag=True)

aln.write(file='2R9R-mult.ali', alignment_format='PIR')
aln.write(file='2R9R-mult.pap', alignment_format='PAP')

# Generate models including ligand prediction
models_dir = Path("./models")
if models_dir.exists():
    print("models directory already exists")
else:
    models_dir.mkdir(parents=True)
log.verbose()
env = Environ()
env.io.output_directory = str(models_dir)
env.io.hetatm = True

a = AutoModel(env, alnfile='2R9R-mult.ali',
              knowns=('3LUTB','8VC3B'), sequence='2R9R_2|Chains',
              assess_methods=(assess.DOPE))
a.starting_model = 1
a.ending_model = 5
a.make()

# best model is 2R9R_2|Chains.B99990004.pdb    12625.04395   -43980.13672

with open("2R9R_modeller.pdb","w") as f:
    with open("2R9R_2|Chains.B99990004.pdb") as f2:
        f.write(f2.read())