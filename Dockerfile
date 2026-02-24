FROM python:3.10-slim

# 1) install needed system libraries for RDKit drawing + widgets
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libxext6 \
    libxrender1 \
    libsm6 \
    && rm -rf /var/lib/apt/lists/*

# 2) install Python dependencies
RUN pip install --no-cache-dir \
    streamlit \
    rdkit-pypi \
    pubchempy \
    stmol \
    py3Dmol \
    pillow \
    ipywidgets \
    ipython-genutils

# 3) set working dir and copy files
WORKDIR /app
COPY . .

# 4) expose port and run Streamlit
EXPOSE 7860
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0"]
