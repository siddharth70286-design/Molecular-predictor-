
#Molecular Structure Predictor

-Live Demo
https://huggingface.co/spaces/ShiddharthTiwari11/molecular-structure-predictor

-Overview

1.Molecular Structure Predictor is an interactive web application that generates 2D and 3D molecular structures from compound names using PubChem API and RDKit.

2.The application allows users to visualize chemical structures instantly and interact with 3D molecular models directly in the browser.

-Features

1.Compound name search via PubChem

2.Automatic SMILES retrieval

3.2D molecular structure visualization

4.Interactive 3D molecular model rendering

5.Clean Streamlit interface

6.Deployed using Docker on Hugging Face Spaces

-Tech Stack

1.Python

2.RDKit

3.Streamlit

4.PubChemPy

5.stmol / py3Dmol

6.Docker

7.Hugging Face Spaces

-How It Works

1.User enters a compound name.

2.PubChem API fetches molecular data.

3.RDKit generates the 2D structure.

4.3D coordinates are generated and rendered interactively.

5.Deployment

6.The application is containerized using Docker and deployed on Hugging Face Spaces.

7.Installation (Local Setup)

8.Clone the repository:

git clone https://github.com/your-username/your-repository-name.git

-Install dependencies:

-pip install -r requirements.txt

-Run the app:

streamlit run streamlit_app.py

-License

This project is licensed under the MIT License.

-Author

Shiddharth Tiwari


