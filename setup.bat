@echo off
REM Script de inicialização rápida para Windows

echo ==========================================
echo 🎓 Sistema de Treinamento com Vídeo
echo ==========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não está instalado!
    echo Instale Python 3.8+ em https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python encontrado: %PYTHON_VERSION%
echo.

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    echo ✓ Ambiente virtual criado
) else (
    echo ✓ Ambiente virtual já existe
)

echo.
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 📚 Instalando dependências...
pip install -r requirements.txt --quiet

echo.
echo 🗄️  Criando dados de teste...
python create_sample_data.py

echo.
echo ==========================================
echo ✅ Pronto! Digite o comando abaixo:
echo.
echo     python app.py
echo.
echo Depois acesse: http://localhost:5000
echo ==========================================
echo.
pause
