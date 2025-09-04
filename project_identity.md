# Project Identity: Protein Model Comparison AlphaFold

## Professional Identity (Portfolio-Ready)

### Display Title
**Protein Structure Prediction Comparison: MODELLER vs. AlphaFold2 vs. RoseTTAFold**

### Repo Slug (Suggested)
`protein-model-comparison-alphafold`

### Tagline
Comparative analysis of protein structure prediction methods using MODELLER, AlphaFold2, and RoseTTAFold on the 2R9R protein

### GitHub Description
A structural bioinformatics project that performs comparative modeling with MODELLER using multiple templates and benchmarks predictions against AlphaFold2 and RoseTTAFold results for protein 2R9R.

### Primary Stack
- Python 3.x
- BioPython
- MODELLER (comparative protein structure modeling)
- Structural analysis tools

### Topics/Keywords
- structural-bioinformatics
- protein-structure-prediction
- alphafold2
- modeller
- rosettafold
- comparative-modeling
- protein-modeling
- structure-comparison
- biopython
- computational-biology

### Problem & Approach

**Problem:**  
Evaluating and comparing different protein structure prediction methodologies to understand their relative strengths and accuracy against experimental structures.

**Approach:**  
1. Use MODELLER for template-based comparative modeling (templates: 3LUT, 8VC3)
2. Compare generated models with deep learning predictions (AlphaFold2, RoseTTAFold)
3. Assess model quality using standard structural metrics (RMSD, TM-score)
4. Benchmark against experimental reference structure (2R9R.pdb)

### Inputs Overview
- **Target sequence:** 2R9R (chain B) from RCSB PDB
- **Template structures:** 3LUT.pdb, 8VC3.pdb (automatically downloaded)
- **Reference predictions:** 2R9R_alphafold2.pdb, 2R9R_modeller.pdb, 2R9R_rosettafold.pdb

### Outputs Overview
- MODELLER-generated protein structure models (5 models, best selected by DOPE score)
- Alignment files (PIR, PAP formats)
- Model quality assessment metrics
- Intermediate files for structure analysis
