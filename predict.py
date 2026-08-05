import os
import glob
import torch
from rdkit import Chem
from torch_geometric.data import Data

from gnn_models import (
    GCN,
    GIN,
    GraphSAGE,
    GAT,
)

DEVICE = torch.device("cpu")


# ============================================================
# MODEL DICTIONARY
# ============================================================

MODEL_MAP = {
    "GCN": GCN,
    "GIN": GIN,
    "GraphSAGE": GraphSAGE,
    "GAT": GAT,
}


# ============================================================
# FIND MODEL FILE AUTOMATICALLY
# ============================================================

def find_model_file(model_name, dataset, property_name):

    pattern = f"{model_name}_{dataset}_*.pth"

    files = glob.glob(pattern)

    if len(files) == 1:
        return files[0]

    property_lower = property_name.lower()

    for file in files:

        if property_lower in file.lower():

            return file

    raise FileNotFoundError(
        f"No model found for {model_name} {dataset} {property_name}"
    )


# ============================================================
# LOAD MODEL
# ============================================================

def load_model(model_name, dataset, property_name):

    model_file = find_model_file(
        model_name,
        dataset,
        property_name
    )

    model = MODEL_MAP[model_name]()

    state_dict = torch.load(
        model_file,
        map_location=DEVICE
    )

    model.load_state_dict(state_dict)

    model.eval()

    return model


# ============================================================
# SMILES TO GRAPH
# ============================================================

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

        edge_index = torch.empty((2, 0), dtype=torch.long)

    else:

        edge_index = torch.tensor(
            edge_index,
            dtype=torch.long
        ).t().contiguous()

    graph = Data(

        x=x,

        edge_index=edge_index

    )

    graph.batch = torch.zeros(
        graph.num_nodes,
        dtype=torch.long
    )

    return graph

# ============================================================
# CLASSIFICATION PREDICTION
# ============================================================

def predict_classification(
    smiles,
    model_name,
    dataset,
    property_name
):

    graph = mol_to_graph(smiles)

    if graph is None:
        raise ValueError("Invalid SMILES")

    graph = graph.to(DEVICE)

    model = load_model(
        model_name,
        dataset,
        property_name
    )

    with torch.no_grad():

        output = model(
            graph.x,
            graph.edge_index,
            graph.batch
        )

        probability = torch.sigmoid(output).item()

    prediction = int(probability >= 0.5)

    confidence = round(
        max(probability, 1 - probability) * 100,
        2
    )

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "confidence": confidence,
    }


# ============================================================
# REGRESSION PREDICTION
# ============================================================

def predict_regression(
    smiles,
    model_name,
    dataset,
    property_name
):

    graph = mol_to_graph(smiles)

    if graph is None:
        raise ValueError("Invalid SMILES")

    graph = graph.to(DEVICE)

    model = load_model(
        model_name,
        dataset,
        property_name
    )

    with torch.no_grad():

        value = model(
            graph.x,
            graph.edge_index,
            graph.batch
        ).item()

    return {
        "value": round(value, 4)
    }


# ============================================================
# UNIVERSAL PREDICTOR
# ============================================================

def predict_property(
    smiles,
    model_name,
    dataset,
    property_name,
    task
):

    task = task.lower()

    if task == "classification":

        return predict_classification(
            smiles,
            model_name,
            dataset,
            property_name
        )

    elif task == "regression":

        return predict_regression(
            smiles,
            model_name,
            dataset,
            property_name
        )

    else:

        raise ValueError(
            f"Unknown task: {task}"
        )


# ============================================================
# LABELS
# ============================================================

def toxicity_label(prediction):

    if prediction == 1:
        return "Potentially Toxic"

    return "Low Toxicity"
