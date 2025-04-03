#!/bin/bash

echo "🔧 Iniciando proyecto cEDH..."

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "⚙️  Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

# Ejecutar con Streamlit
echo "🚀 Ejecutando app con Streamlit..."
streamlit run main.py

# Pausa al final
echo ""
read -p "Presiona Enter para cerrar..."
