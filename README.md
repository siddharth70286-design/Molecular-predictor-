# 🧪 Molecular Structure & Toxicity Predictor (MSTP) V3

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![RDKit](https://img.shields.io/badge/RDKit-Cheminformatics-green.svg)]()
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red.svg)]()
[![PyTorch Geometric](https://img.shields.io/badge/PyTorch-Geometric-orange.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20Application-ff4b4b.svg)]()

An AI-powered cheminformatics platform integrating **Machine Learning**, **Graph Neural Networks**, and **Computational Chemistry** for molecular visualization, descriptor generation, and toxicity prediction.

Developed as an academic research project to demonstrate modern AI applications in molecular science, cheminformatics, and drug discovery.

---
PROJECT AT A GLANCE:

| 🚀 Models              | 🤖 AI Architectures      | 🧬 Molecular Records | 🧪 Unique Molecules | 📊 Datasets |
| ---------------------- | ------------------------ | -------------------: | ------------------: | ----------: |
| Random Forest + 4 GNNs | GCN, GIN, GraphSAGE, GAT |        **2,669,958** |          **67,271** |      **10** |


# 🌐 Live Application

**Hugging Face Deployment**

https://huggingface.co/spaces/ShiddharthTiwari11/molecular-structure-predictor/tree/main

---

# 📖 Overview

Molecular Structure & Toxicity Predictor (MSTP) V3 is a browser-based cheminformatics application capable of accepting either a **compound name** or a **SMILES string** and automatically performing molecular analysis.

The platform combines **RDKit**, **Random Forest**, and multiple **Graph Neural Network (GNN)** architectures to generate molecular structures, calculate molecular descriptors, and predict toxicity-related properties.

Unlike traditional molecular visualization tools, MSTP integrates **multiple AI models** into a unified workflow, enabling researchers and students to perform computational molecular analysis without requiring local software installation.

---

# 🚀 Key Features

✅ Compound Name → SMILES Conversion

✅ SMILES Input Support

✅ Interactive 2D Molecular Visualization

✅ Interactive 3D Molecular Visualization

✅ Molecular Descriptor Calculation

✅ Toxicity Prediction

✅ Multi-Model AI Comparison

✅ Browser-Based Interface

✅ Hugging Face Deployment

---

# 🤖 Artificial Intelligence Models

## Classical Machine Learning

- Random Forest Classifier

## Graph Neural Networks

- Graph Convolutional Network (GCN)
- Graph Isomorphism Network (GIN)
- GraphSAGE
- Graph Attention Network (GAT)

These models collectively provide robust molecular property prediction and comparative AI analysis.

---

# 📊 Dataset Engineering

A unified master molecular dataset was developed by integrating benchmark datasets from the **MoleculeNet ecosystem** and other publicly available cheminformatics resources.

The data engineering workflow included:

- Dataset Integration
- Molecular Standardization
- Descriptor Generation (RDKit)
- Label Harmonization
- Duplicate Removal
- Quality Control
- Multi-task Dataset Construction

---

## 📈 Dataset Statistics

| Metric | Value |
|---------|-------|
| Total Molecular Records | **2,669,958** |
| Unique Molecular Structures | **67,271** |
| Benchmark Datasets Integrated | **10** |
| Molecular Features | **20** |
| Duplicate Records | **0** |
| Learning Tasks | **Classification & Regression** |

---

## Integrated Benchmark Datasets

| Dataset | Records |
|----------|--------:|
| ToxCast | 1,535,080 |
| BACE | 898,722 |
| Tox21 | 85,777 |
| HIV | 82,254 |
| SIDER | 38,529 |
| ESOL | 10,152 |
| Lipophilicity | 8,400 |
| BBBP | 6,150 |
| ClinTox | 2,968 |
| FreeSolv | 1,926 |

---

# 🧬 Molecular Descriptors

The application automatically computes molecular descriptors using **RDKit**, including:

- Molecular Weight
- Exact Molecular Weight
- LogP
- Topological Polar Surface Area (TPSA)
- Hydrogen Bond Donors
- Hydrogen Bond Acceptors
- Heavy Atom Count
- Rotatable Bonds
- Ring Count
- Aromatic Ring Count
- Fraction Csp³
- Formal Charge
- Molar Refractivity
- Hetero Atom Count
- Valence Electrons

---

# 💻 Technology Stack

### Programming

- Python

### Cheminformatics

- RDKit

### Machine Learning

- Scikit-learn
- Random Forest

### Deep Learning

- PyTorch
- PyTorch Geometric

### Graph Neural Networks

- GCN
- GIN
- GraphSAGE
- GAT

### Deployment

- Streamlit
- Hugging Face Spaces

### Molecular Data

- PubChem REST API
- MoleculeNet Benchmark Datasets

---

# 📂 Repository Structure

```
Molecular-Structure-Toxicity-Predictor/

│── streamlit_app.py
│── predict.py
│── requirements.txt
│── Dockerfile
│── README.md

├── models/
│      Random Forest
│      GCN
│      GIN
│      GraphSAGE
│      GAT

├── dataset/

├── assets/
```

---

# 🔬 Scientific Applications

This platform can be applied to:

- Cheminformatics
- Molecular Property Prediction
- Toxicity Prediction
- Drug Discovery
- Molecular Visualization
- AI-assisted Chemical Analysis
- Computational Chemistry Education
- Machine Learning Research

---

# 📚 Publications

## ChemRxiv

**Molecular Structure & Toxicity Predictor (MSTP)**

---

## Authorea

**Framework for Low-Temperature Upgrading of Biodiesel-Derived Crude Glycerol: A Theoretical Techno-Economic Assessment**

---

# 🔮 Future Development (Version 4)

The next version aims to introduce:

- Novel Molecular Property Prediction
- Reduced Dependence on External Databases
- Advanced Graph Neural Networks
- Confidence Calibration
- Explainable Artificial Intelligence (XAI)
- Hybrid Molecular Intelligence Pipeline

---

# 👨‍🔬 Developer

**Shiddharth Tiwari**

B.Sc. Chemistry

KJ Somaiya College of Science and Commerce

### Research Interests

- Cheminformatics
- Computational Chemistry
- Molecular Artificial Intelligence
- Graph Neural Networks
- Drug Discovery
- Scientific Software Development

LinkedIn:
www.linkedin.com/in/shiddharthcheminformatics30

---

# ⭐ Support

If you found this project useful, please consider giving the repository a ⭐.

Feedback, suggestions, and research collaborations are always welcome.

---

# 📄 License

This project is released under the **MIT License**.
