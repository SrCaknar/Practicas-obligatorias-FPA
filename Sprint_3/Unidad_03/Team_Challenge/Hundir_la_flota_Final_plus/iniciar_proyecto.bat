@echo off
echo Iniciando proyecto cEDH...

if not exist .venv (
    echo Creando entorno virtual...
    python -m venv .venv
)

call .venv\Scripts\activate

echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo Ejecutando app con Streamlit...
streamlit run main.py

pause
