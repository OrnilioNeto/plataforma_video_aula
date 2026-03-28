#!/bin/bash
# Script de inicialização rápida para Linux/Mac

echo "=========================================="
echo "🎓 Sistema de Treinamento com Vídeo"
echo "=========================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 não está instalado!"
    echo "Instale Python 3.8+ em https://www.python.org/"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"
echo ""

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✓ Ambiente virtual criado"
else
    echo "✓ Ambiente virtual já existe"
fi

echo ""
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

echo ""
echo "📚 Instalando dependências..."
pip install -r requirements.txt --quiet

echo ""
echo "🗄️  Criando dados de teste..."
python3 create_sample_data.py

echo ""
echo "=========================================="
echo "✅ Pronto! Digite o comando abaixo:"
echo ""
echo "    python3 app.py"
echo ""
echo "Depois acesse: http://localhost:5000"
echo "=========================================="
