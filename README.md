# Protein Structure Prediction Comparison: MODELLER vs. AlphaFold2 vs. RoseTTAFold

Comparative analysis of protein structure prediction methods using MODELLER, AlphaFold2, and RoseTTAFold on the 2R9R protein

## Overview

This project performs comparative modeling of protein structures using MODELLER with multiple templates and benchmarks the predictions against modern deep learning methods (AlphaFold2 and RoseTTAFold). The analysis focuses on protein 2R9R (chain B), evaluating prediction quality against the experimental reference structure.

## Problem & Approach

**Problem:**  
Evaluating and comparing different protein structure prediction methodologies to understand their relative strengths, accuracy, and applicability in structural bioinformatics research.

**Approach:**  
1. **Template-based modeling** with MODELLER using multiple protein templates (3LUT, 8VC3)
2. **Comparative analysis** against deep learning predictions (AlphaFold2, RoseTTAFold)
3. **Quality assessment** using standard structural metrics (RMSD, TM-score, DOPE score)
4. **Benchmarking** against experimental reference structure (2R9R.pdb from RCSB PDB)

## Tech Stack

- **Python 3.x** - Primary programming language
- **BioPython** - Sequence and structure manipulation
- **MODELLER** - Comparative protein structure modeling (requires separate installation)
- **Requests** - Automated retrieval of PDB structures and sequences

## Repository Structure

```
protein-model-comparison-alphafold/
├── model_comparison.py          # Main comparison script (MODELLER workflow)
├── 2R9R.fasta                   # Target sequence (chain B)
├── 2R9R.pdb                     # Experimental reference structure
├── 2R9R_alphafold2.pdb          # AlphaFold2 prediction
├── 2R9R_modeller.pdb            # MODELLER prediction (output)
├── 2R9R_rosettafold.pdb         # RoseTTAFold prediction
├── requirements.txt             # Python dependencies
├── .gitignore                   # Excludes generated files
└── README.md                    # This file
```

## Setup

### Prerequisites

1. **Python 3.7+** with pip
2. **MODELLER** - Requires special installation:
   - Visit [Sali Lab MODELLER](https://salilab.org/modeller/)
   - Free for academic use (requires registration and license key)
   - Follow installation instructions for your platform
   - Configure license key after installation

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Raminyazdani/protein-model-comparison-alphafold.git
cd protein-model-comparison-alphafold
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Verify MODELLER installation:
```bash
python -c "from modeller import *; print('MODELLER installed successfully')"
```

## How to Run

### Running the MODELLER Workflow

From the repository root directory:

```bash
python model_comparison.py
```

**What the script does:**
1. Downloads required template structures (3LUT.pdb, 8VC3.pdb) from RCSB PDB
2. Extracts chain B from 2R9R.fasta
3. Creates sequence alignments in PIR format
4. Performs multiple template alignment
5. Generates 5 protein structure models
6. Selects best model based on DOPE score
7. Runs both with and without heteroatom (ligand) prediction

**Expected runtime:** 5-15 minutes depending on system (MODELLER optimization is compute-intensive)

### Structure Visualization (Optional)

To visualize and compare structures, use molecular visualization software:

**PyMOL:**
```bash
pymol 2R9R.pdb 2R9R_alphafold2.pdb 2R9R_modeller.pdb 2R9R_rosettafold.pdb
```

**ChimeraX:**
```bash
chimerax 2R9R.pdb 2R9R_alphafold2.pdb 2R9R_modeller.pdb 2R9R_rosettafold.pdb
```

## Data & Inputs

### Required Inputs (Included in Repository)

- `2R9R.fasta` - FASTA sequence file for protein 2R9R (chain B)
- `2R9R.pdb` - Experimental reference structure from RCSB PDB
- `2R9R_alphafold2.pdb` - AlphaFold2 predicted structure
- `2R9R_rosettafold.pdb` - RoseTTAFold predicted structure

### Automatically Downloaded

The script automatically downloads template structures:
- `3LUT.pdb` - Template 1 (RCSB PDB)
- `8VC3.pdb` - Template 2 (RCSB PDB)

**Note:** Internet connection required for initial run to download templates.

## Outputs

### Primary Outputs

- `2R9R_modeller.pdb` - Best MODELLER prediction (root directory)
- `models/` - Directory containing all 5 generated models with DOPE scores
- `with_hetero/` - Directory containing models with ligand predictions

### Intermediate Files

- `2R9R_2.fasta` - Extracted chain B sequence
- `2R9R_2.pir` - Sequence in PIR format
- `res.ali`, `res.pap` - Template alignments
- `2R9R-mult.ali`, `2R9R-mult.pap` - Multiple sequence alignments
- `*.tree` - Phylogenetic trees for alignment
- `*.log` - MODELLER execution logs

**Note:** Intermediate files are excluded from version control via `.gitignore`.

## Reproducibility Notes

### Environment
- Python 3.7+ recommended
- MODELLER version 10.x (academic license required)
- BioPython 1.79+
- Tested on Linux and macOS

### Determinism
- MODELLER optimization includes stochastic elements
- Results may vary slightly between runs
- For reproducibility, MODELLER uses consistent starting conditions
- DOPE scores and model rankings should be consistent

### System Requirements
- **CPU:** Multi-core recommended (MODELLER can utilize parallel processing)
- **RAM:** 2GB minimum, 4GB+ recommended
- **Disk:** ~50MB for intermediate files
- **Network:** Required for initial template download

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'modeller'"**
- MODELLER is not installed or not in Python path
- Solution: Install MODELLER from Sali Lab and configure license key
- Verify: `python -c "from modeller import *"`

**"License key error"**
- MODELLER requires a valid license key
- Solution: Register at https://salilab.org/modeller/ and configure key
- Place key in: `~/.modeller/config.py` (Linux/Mac) or MODELLER installation directory (Windows)

**"Import errors for biopython or numpy"**
- Missing dependencies
- Solution: `pip install -r requirements.txt`

**"PDB file format errors"**
- Corrupted PDB file downloads
- Solution: Delete downloaded templates (3LUT.pdb, 8VC3.pdb) and re-run

**"Models directory already exists"**
- Previous run artifacts present
- Solution: Remove `models/` and `with_hetero/` directories or let script skip existing

**Script fails during alignment**
- Template structures may have issues
- Solution: Check template PDB files are valid and complete

### Performance Tips

- First run takes longer (downloads templates, ~5-15 min total)
- Subsequent runs skip downloads (<5 min)
- MODELLER log verbosity can be reduced by commenting `log.verbose()` lines
- For faster testing, reduce `a.ending_model` from 5 to 2 (generates fewer models)

## Contributing

This is a research project demonstrating comparative protein structure prediction methods. Contributions for improvements, additional analysis methods, or extended comparisons are welcome.

## License

This project code is provided for educational and research purposes. 

**External Dependencies:**
- MODELLER: Free for academic use with registration ([License](https://salilab.org/modeller/registration.html))
- BioPython: BSD-3-Clause License
- PDB structures: RCSB PDB (free for research use)

## Citation

If you use this code or methodology in your research, please cite:

**AlphaFold2:**
- Jumper, J. et al. Highly accurate protein structure prediction with AlphaFold. Nature (2021)

**RoseTTAFold:**
- Baek, M. et al. Accurate prediction of protein structures and interactions using a three-track neural network. Science (2021)

**MODELLER:**
- Webb, B. & Sali, A. Comparative Protein Structure Modeling Using MODELLER. Current Protocols in Bioinformatics (2016)

## Contact

For questions or issues, please open an issue on the GitHub repository.
