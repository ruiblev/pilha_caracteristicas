#!/bin/bash

echo "🚀 A preparar o simulador AL 2.1..."

# --------------------------------------------------------------------------
# 1. Verificar se python3 está instalado
# --------------------------------------------------------------------------
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 não encontrado. Por favor, instale o Python 3."
    exit 1
fi

# --------------------------------------------------------------------------
# 2. Criar/validar ambiente virtual
#    Verifica se venv/bin/activate existe (não apenas a pasta venv/)
#    Caso a pasta exista mas esteja corrompida, elimina e recria.
# --------------------------------------------------------------------------
if [ -d "venv" ] && [ ! -f "venv/bin/activate" ]; then
    echo "⚠️  Ambiente virtual corrompido detectado. A recriar..."
    rm -rf venv
fi

if [ ! -d "venv" ]; then
    echo "📦 A criar ambiente virtual..."
    if ! python3 -m venv venv; then
        echo "❌ Falha ao criar o ambiente virtual."
        echo "   Execute: sudo apt install python3-venv python3-full"
        exit 1
    fi
fi

# Activar o venv
# shellcheck disable=SC1091
source venv/bin/activate

# --------------------------------------------------------------------------
# 3. Instalar dependências dentro do venv
# --------------------------------------------------------------------------
echo "📥 A instalar/verificar dependências..."
pip install --upgrade pip --quiet 2>/dev/null || true
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Falha ao instalar dependências."
    exit 1
fi

# --------------------------------------------------------------------------
# 4. Correr o simulador
# --------------------------------------------------------------------------
echo "✅ Ambiente pronto. A iniciar o simulador..."
echo "   Aceda ao link 'Local URL' que aparecerá abaixo no seu browser."
echo ""

streamlit run app.py
