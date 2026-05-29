# Molecular Structure and Toxicity Predictor (MSTP) — V2

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Hugging%20Face-orange)](https://huggingface.co/spaces/ShiddharthTiwari11/molecular-structure-predictor)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io)

A cheminformatics web application for molecular structure visualization and machine learning-based toxicity prediction. Built entirely on a mobile phone using RDKit, Streamlit, and scikit-learn.

## Live Demo

[Launch MSTP V2](https://huggingface.co/spaces/ShiddharthTiwari11/molecular-structure-predictor)

---

## Features — V2

- 2D Structure Visualization — renders molecular structures from SMILES strings
- 3D Interactive Viewer — rotatable 3D molecular viewer
- ML Toxicity Prediction — Random Forest classifier with confidence scoring
- Molecular Descriptors — full descriptor table for each compound
- PubChem Search — compound lookup by name via PubChem API
- SMILES Input — direct SMILES string entry supported

---

## Toxicity Prediction Pipeline

- Algorithm: Random Forest Classifier
- Fingerprints: Morgan Fingerprints (radius 2, 2048 bits)
- Training Data: DeepChem toxicity dataset sourced from AWS S3
- Model File: tox_model.pkl (included in repository)
- Validation: 99% confidence score on Caffeine benchmark

---

## Repository Structure

- streamlit_app.py — Main application, V2
- tox_model.pkl — Trained Random Forest toxicity model
- Dockerfile — Container configuration
- README.md
- LICENSE — MIT License
- .gitignore

---

## Installation and Local Setup

git clone https://github.com/siddharth70286-design/Molecular-predictor-.git
cd Molecular-predictor-

pip install streamlit rdkit scikit-learn py3Dmol stmol pubchempy joblib

streamlit run streamlit_app.py

Or with Docker:

docker build -t mstp .
docker run -p 8501:8501 mstp

---

## Tech Stack

- Frontend: Streamlit
- Cheminformatics: RDKit
- 3D Visualization: py3Dmol / stmol
- Machine Learning: scikit-learn (Random Forest)
- Fingerprinting: Morgan Fingerprints
- Data Source: DeepChem / AWS S3
- Deployment: Hugging Face Spaces

---

## Preprint and Citation

A V1 preprint is published on ChemRxiv. A V2 preprint is forthcoming on ChemRxiv — covering the ML toxicity pipeline, 3D visualization module, and updated molecular descriptor framework.

Citation details will be added here once the V2 preprint is published.

Author: Shiddharth Tiwari
ORCID: https://orcid.org/0009-0002-7308-3495
Affiliation: FY BSc Chemistry, K.J. Somaiya College of Science and Commerce, Mumbai

---

## Roadmap

- V1 — 2D structure visualization, SMILES and PubChem input (completed)
- V2 — 3D viewer, ML toxicity prediction, molecular descriptors, confidence scoring (completed)
- V3 — Graph Neural Network (GNN) integration for toxicity prediction (planned)

---

## Notable

This application was designed and built entirely on a mobile phone. No laptop or desktop was used at any stage of development. The ML pipeline was first written by hand in a physical notebook before being coded.

---

## License

MIT License. See LICENSE for details.
