FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libxext6 \
    libxrender1 \
    libsm6 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python packages
RUN pip install streamlit
RUN pip install rdkit
RUN pip install pubchempy
RUN pip install stmol
RUN pip install py3Dmol
RUN pip install pillow
RUN pip install ipywidgets
RUN pip install ipython-genutils
RUN pip install scikit-learn
RUN pip install pandas
RUN pip install numpy
RUN pip install joblib

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Expose Streamlit port
EXPOSE 7860

# Run app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0"]
