
import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import AllChem, Draw, Descriptors
import py3Dmol
from stmol import showmol
import pubchempy as pcp
import joblib
import numpy as np
import pandas as pd

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    layout="wide",
    page_title="Molecular Structure & Toxicity Predictor",
    page_icon="🔬"
)

st.title("🔬 Molecular Structure & Toxicity Predictor")

st.markdown(
    """
AI-powered molecular visualization and toxicity prediction platform using RDKit,
Streamlit, and Machine Learning.
"""
)

# ---------------- FIX JS ISSUE ---------------- #

components.html(
    """
    <script>
    if (typeof Object.hasOwn === 'undefined') {
        Object.hasOwn = function(obj, prop) {
            return Object.prototype.hasOwnProperty.call(obj, prop);
        };
    }
    </script>
    """,
    height=0,
)

# ---------------- LOAD MODEL ---------------- #

@st.cache_resource
def load_model():
    return joblib.load("tox_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading toxicity model: {e}")
    st.stop()

# ---------------- MOLECULE LOADER ---------------- #

@st.cache_data(show_spinner=False)
def get_molecule(user_input):

    # Try SMILES first
    mol = Chem.MolFromSmiles(user_input)

    # If not SMILES -> search PubChem
    if mol is None:
        try:
            compounds = pcp.get_compounds(user_input, 'name')

            if compounds:
                smiles = compounds[0].canonical_smiles
                mol = Chem.MolFromSmiles(smiles)

        except Exception:
            return None, "Search Error"

    if mol is None:
        return None, "Invalid Structure"

    # Add hydrogens
    mol = Chem.AddHs(mol)

    status = "Success"

    # Generate 3D coordinates
    try:
        params = AllChem.ETKDG()

        if AllChem.EmbedMolecule(mol, params) == -1:
            status = "2D only"

        else:
            AllChem.MMFFOptimizeMolecule(mol)

    except Exception:
        status = "2D only"

    return mol, status

# ---------------- 2D IMAGE ---------------- #

def generate_2d_image(mol):
    return Draw.MolToImage(
        mol,
        size=(350, 350)
    )

# ---------------- 3D VIEWER ---------------- #

def generate_3d_view(mol):

    mol_block = Chem.MolToMolBlock(mol)

    view = py3Dmol.view(
        width=500,
        height=450
    )

    view.addModel(mol_block, "mol")

    view.setStyle({
        "stick": {},
        "sphere": {"scale": 0.3}
    })

    view.setBackgroundColor("white")

    view.zoomTo()

    return view

# ---------------- FINGERPRINT ---------------- #

def generate_fingerprint(mol):

    fp = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius=2,
        nBits=1024
    )

    arr = np.array(list(fp))

    return arr.reshape(1, -1)

# ---------------- TOXICITY PREDICTION ---------------- #

def predict_toxicity(mol):

    fp = generate_fingerprint(mol)

    prediction = model.predict(fp)[0]

    try:
        probability = model.predict_proba(fp)[0]
        confidence = round(max(probability) * 100, 2)

    except Exception:
        confidence = "N/A"

    if prediction == 1:
        result = "⚠️ Potentially Toxic"

    else:
        result = "✅ Low Toxicity"

    return result, confidence

# ---------------- DESCRIPTORS ---------------- #

def calculate_descriptors(mol):

    descriptors = {
        "Molecular Weight": round(Descriptors.MolWt(mol), 2),
        "LogP": round(Descriptors.MolLogP(mol), 2),
        "TPSA": round(Descriptors.TPSA(mol), 2),
        "H-Bond Donors": Descriptors.NumHDonors(mol),
        "H-Bond Acceptors": Descriptors.NumHAcceptors(mol),
    }

    return descriptors

# ---------------- USER INPUT ---------------- #

user_input = st.text_input(
    "Enter Compound Name or SMILES:",
    "Caffeine"
)

# ---------------- MAIN APP ---------------- #

if user_input:

    molecule, status = get_molecule(user_input)

    if molecule is not None:

        st.success(f"Molecule Loaded Successfully: {user_input}")

        # Layout
        col1, col2 = st.columns(2)

        # 2D Structure
        with col1:

            st.subheader("2D Molecular Structure")

            image = generate_2d_image(molecule)

            st.image(image)

        # 3D Structure
        with col2:

            st.subheader("3D Interactive Viewer")

            if status == "2D only":

                st.warning(
                    "Could not generate optimized 3D coordinates."
                )

            else:

                try:
                    view = generate_3d_view(molecule)

                    showmol(
                        view,
                        height=450,
                        width=500
                    )

                except Exception:
                    st.warning("3D Viewer failed to load.")

        st.divider()

        # Toxicity Prediction
        st.subheader("🧪 Toxicity Prediction")

        toxicity, confidence = predict_toxicity(molecule)

        if "Toxic" in toxicity:
            st.error(toxicity)

        else:
            st.success(toxicity)

        st.metric(
            label="Prediction Confidence",
            value=f"{confidence}%"
            if confidence != "N/A"
            else "N/A"
        )

        st.divider()

        # Molecular Descriptors
        st.subheader("📊 Molecular Descriptors")

        descriptors = calculate_descriptors(molecule)

        desc_df = pd.DataFrame(
            descriptors.items(),
            columns=["Property", "Value"]
        )

        st.dataframe(
            desc_df,
            use_container_width=True
        )

    else:

        st.error(
            "Could not find or process the entered molecule."
        )
