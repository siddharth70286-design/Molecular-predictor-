import streamlit as st
import streamlit.components.v1 as components

import torch
import joblib
import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.Chem import AllChem, Draw, Descriptors

import py3Dmol
import requests

from torch_geometric.data import Data

from gnn_models import (
    GCN,
    GIN,
    GraphSAGE,
    GAT
)

st.set_page_config(
    page_title="Molecular Structure & Toxicity Predictor V3",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Molecular Structure & Toxicity Predictor V3")

st.markdown(
"""
Random Forest + Graph Neural Networks
Supported Models
• Random Forest
• GCN
• GIN
• GraphSAGE
• GAT
"""
)

device = torch.device("cpu")


# ==========================================================
# Load Random Forest
# ==========================================================

@st.cache_resource
def load_rf():

    return joblib.load("tox_model.pkl")


rf_model = load_rf()


# ==========================================================
# Load GNN Models
# ==========================================================

@st.cache_resource
def load_models():

    models = {}

    try:

        model = GCN()
        model.load_state_dict(
            torch.load(
                "gcn_tox21_nr_ar.pth",
                map_location=device
            )
        )
        model.eval()

        models["GCN"] = model

    except:

        pass


    try:

        model = GIN()
        model.load_state_dict(
            torch.load(
                "GIN_Tox21_NR-AR.pth",
                map_location=device
            )
        )
        model.eval()

        models["GIN"] = model

    except:

        pass


    try:

        model = GraphSAGE()
        model.load_state_dict(
            torch.load(
                "GraphSAGE_Tox21_NR-AR.pth",
                map_location=device
            )
        )
        model.eval()

        models["GraphSAGE"] = model

    except:

        pass


    try:

        model = GAT()
        model.load_state_dict(
            torch.load(
                "GAT_Tox21_NR-AR.pth",
                map_location=device
            )
        )
        model.eval()

        models["GAT"] = model

    except:

        pass

    return models


gnn_models = load_models()

# ==========================================================
# Convert SMILES to Graph
# ==========================================================

def mol_to_graph(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    x = []

    for atom in mol.GetAtoms():

        x.append([
            atom.GetAtomicNum(),
            atom.GetDegree(),
            atom.GetFormalCharge(),
            atom.GetHybridization().real,
            int(atom.GetIsAromatic())
        ])

    edge_index = []

    for bond in mol.GetBonds():

        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()

        edge_index.append([i, j])
        edge_index.append([j, i])

    x = torch.tensor(x, dtype=torch.float)

    if len(edge_index) == 0:

        edge_index = torch.empty((2,0), dtype=torch.long)

    else:

        edge_index = torch.tensor(
            edge_index,
            dtype=torch.long
        ).t().contiguous()

    data = Data(
        x=x,
        edge_index=edge_index
    )

    data.batch = torch.zeros(
        data.num_nodes,
        dtype=torch.long
    )

    return data


# ==========================================================
# Predict with one GNN
# ==========================================================

def predict_gnn(model, smiles):

    graph = mol_to_graph(smiles)

    if graph is None:

        return None

    graph = graph.to(device)

    with torch.no_grad():

        output = model(
            graph.x,
            graph.edge_index,
            graph.batch
        )

        probability = torch.sigmoid(output).item()

    return probability


# ==========================================================
# Predict with all available GNNs
# ==========================================================

def predict_all_models(smiles):

    results = {}

    for name, model in gnn_models.items():

        try:

            prob = predict_gnn(model, smiles)

            if prob is not None:

                results[name] = prob

        except Exception:

            continue

    return results

# ==========================================================
# Random Forest Prediction
# ==========================================================

def get_rf_features(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    fp = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius=2,
        nBits=2048
    )

    arr = np.zeros((2048,), dtype=np.int8)

    Chem.DataStructs.ConvertToNumpyArray(fp, arr)

    return arr.reshape(1, -1)


def predict_random_forest(smiles):

    features = get_rf_features(smiles)

    if features is None:
        return None

    probability = rf_model.predict_proba(features)[0][1]

    return probability


# ==========================================================
# Molecular Information
# ==========================================================

def molecular_information(mol):

    info = {}

    info["Molecular Weight"] = round(
        Descriptors.MolWt(mol),
        2
    )

    info["LogP"] = round(
        Descriptors.MolLogP(mol),
        2
    )

    info["TPSA"] = round(
        Descriptors.TPSA(mol),
        2
    )

    info["H Bond Donors"] = Descriptors.NumHDonors(mol)

    info["H Bond Acceptors"] = Descriptors.NumHAcceptors(mol)

    info["Rotatable Bonds"] = Descriptors.NumRotatableBonds(mol)

    return info


# ==========================================================
# Convert Name to SMILES
# ==========================================================
def name_to_smiles(name):

    try:

        url = (
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
            + requests.utils.quote(name.strip())
            + "/property/CanonicalSMILES/JSON"
        )

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        if response.status_code != 200:
            return None

        data = response.json()

        properties = data["PropertyTable"]["Properties"][0]

        if "CanonicalSMILES" in properties:
            return properties["CanonicalSMILES"]

        return properties["ConnectivitySMILES"]

    except Exception as e:

        st.error(e)

        return None
# ==========================================================
# Generate 2D Image
# ==========================================================

def generate_2d_image(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    return Draw.MolToImage(
        mol,
        size=(450,450)
    )


# ==========================================================
# Generate 3D Viewer (WITHOUT STMOL)
# ==========================================================

def generate_3d_html(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    mol = Chem.AddHs(mol)

    AllChem.EmbedMolecule(
        mol,
        AllChem.ETKDG()
    )

    AllChem.MMFFOptimizeMolecule(mol)

    block = Chem.MolToMolBlock(mol)

    viewer = py3Dmol.view(
        width=700,
        height=500
    )

    viewer.addModel(
        block,
        "mol"
    )

    viewer.setStyle(
        {
            "stick": {}
        }
    )

    viewer.setBackgroundColor("white")

    viewer.zoomTo()

    return viewer._make_html()


# ==========================================================
# Prediction Label
# ==========================================================

def prediction_label(probability):

    if probability >= 0.5:
        return "Potentially Toxic"

    return "Low Toxicity"


# ==========================================================
# Confidence
# ==========================================================

def confidence(probability):

    return round(
        max(
            probability,
            1-probability
        )*100,
        2
    )

# ==========================================================
# USER INPUT
# ==========================================================

user_input = st.text_input(
    "Enter Compound Name or SMILES",
    "Caffeine"
)

if user_input:

    smiles = user_input

    if Chem.MolFromSmiles(smiles) is None:

        smiles = name_to_smiles(user_input)

    if smiles is None:

        st.error("Compound not found.")

        st.stop()

    mol = Chem.MolFromSmiles(smiles)

    st.success(f"SMILES : {smiles}")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("2D Structure")

        img = generate_2d_image(smiles)

        st.image(img)

    with col2:

        st.subheader("Interactive 3D Structure")

        html = generate_3d_html(smiles)

        components.html(
            html,
            height=500,
            scrolling=False
        )

    st.divider()

    st.header("Random Forest Prediction")

    rf_probability = predict_random_forest(smiles)

    st.metric(
        "Prediction",
        prediction_label(rf_probability)
    )

    st.metric(
        "Confidence",
        f"{confidence(rf_probability)} %"
    )

    st.progress(float(rf_probability))

    st.divider()

    st.header("Graph Neural Network Predictions")

    gnn_results = predict_all_models(smiles)

    if len(gnn_results) == 0:

        st.warning("No GNN models loaded.")

    else:

        table = []

        for model_name, probability in gnn_results.items():

            table.append({

                "Model": model_name,

                "Prediction": prediction_label(probability),

                "Probability": round(probability,4),

                "Confidence (%)": confidence(probability)

            })

        st.dataframe(
            pd.DataFrame(table),
            use_container_width=True
        )

    st.divider()

    st.header("Molecular Properties")

    properties = molecular_information(mol)

    st.dataframe(

        pd.DataFrame(

            properties.items(),

            columns=[
                "Property",
                "Value"
            ]

        ),

        use_container_width=True

    )

    st.divider()

    st.info(
        "Version 3 • Random Forest + GCN + GIN + GraphSAGE + GAT"
    )
