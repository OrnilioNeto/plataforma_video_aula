# 📦 Guia de Instalação

## Pré-requisitos

- **Python 3.8 ou superior**
- **pip** (gerenciador de pacotes - geralmente vem com Python)
- Navegador moderno (Chrome, Firefox, Safari, Edge)

## Verificar Instalação do Python

### Windows
```bash
python --version
```

### Linux/Mac
```bash
python3 --version
```

Se o comando não for reconhecido, [baixe Python aqui](https://www.python.org/downloads/)

---

## 🚀 Instalação Rápida

### Opção 1: Script Automático (Recomendado)

#### Windows
```bash
setup.bat
```

#### Linux/Mac
```bash
chmod +x setup.sh
./setup.sh
```

Depois execute:
```bash
python app.py
```

---

### Opção 2: Instalação Manual

#### Passo 1: Clonar ou Baixar o Projeto
```bash
git clone <url-do-repositorio>
cd video-treinamento
```

#### Passo 2: Criar Ambiente Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

#### Passo 4: Criar Dados de Teste (Opcional)
```bash
python create_sample_data.py
```

#### Passo 5: Executar Aplicação
```bash
python app.py
```

---

## ✅ Verificar Instalação

Após executar, você deve ver algo como:

```
============================================================
🚀 Sistema de Treinamento com Vídeo
============================================================
📍 Acesse: http://localhost:5000
👤 Admin padrão: admin / admin123
============================================================
```

Abra seu navegador e acesse: **http://localhost:5000**

---

## 🎬 Adicionar Vídeos de Teste

### 1. Crie um Arquivo de Vídeo Teste

Para teste, você pode usar um vídeo de teste gratuito:
- Baixe de: https://sample-videos.com/

**OU** crie um vídeo teste simples com FFmpeg:

```bash
# Instale FFmpeg primeiro
# Windows: choco install ffmpeg
# Linux: sudo apt install ffmpeg
# Mac: brew install ffmpeg

# Criar vídeo de teste 10 segundos
ffmpeg -f lavfi -i color=c=blue:s=640x480:d=10 -f lavfi -i sine=f=1000:d=10 test.mp4
```

### 2. Copie para a Pasta Correta
```
static/videos/test_video.mp4
```

### 3. Adicione via Painel Admin

1. Login com admin (admin / admin123)
2. Vá para "Novo Vídeo"
3. Preencha:
   - Título: "Vídeo de Teste"
   - Arquivo: "test_video.mp4"
   - Duração: 10 (segundos)
4. Clique em "Cadastrar Vídeo"

---

## 🐛 Problemas Comuns

### Erro: "python: command not found"
**Solução**: Python não está na variável PATH
- Reinstale Python marcando "Add Python to PATH"
- Ou use `python3` em vez de `python`

### Erro: "No module named 'flask'"
**Solução**: Dependências não instaladas
```bash
pip install -r requirements.txt
```

### Erro: "Address already in use"
**Solução**: Porta 5000 já está em uso

Opção 1 - Mude a porta:
```python
# No final de app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

Opção 2 - Feche a aplicação anterior:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Vídeos não aparecem
**Solução**: 
1. Confirme arquivo em `static/videos/`
2. Verifique nome do arquivo no banco
3. Tente outro formato de vídeo (.webm, .ogv)

### Progresso não salva
**Solução**:
1. Abra console (F12) - veja erros
2. Confirme que `database.db` existe
3. Verifique permissões de arquivo
4. Tente limpar cache do navegador (Ctrl+Shift+Del)

---

## 📋 Testar Funcionalidades

### 1. Teste de Login
- [ ] Admin: admin / admin123 → Vai para /admin
- [ ] User: user1 / senha123 → Vai para /video
- [ ] Credenciais inválidas → Erro exibido

### 2. Teste de Vídeo
- [ ] Vídeo começa do tempo anterior
- [ ] Não consegue pular para frente
- [ ] Progresso salva automaticamente
- [ ] Conclusão marca em 90%

### 3. Teste de Admin
- [ ] Dashboard mostra usuários e vídeos
- [ ] Pode criar novo usuário
- [ ] Pode criar novo vídeo
- [ ] Pode ver progresso de usuários
- [ ] Pode deletar usuários

---

## 🔧 Variáveis de Ambiente (Opcional)

Crie arquivo `.env`:
```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=sua-chave-secreta
```

---

## 📦 Atualizar Dependências

Periodicamente, atualize:
```bash
pip install --upgrade -r requirements.txt
```

---

## 🗑️ Desinstalar / Limpar

### Remover Ambiente Virtual
```bash
# Windows
rmdir /s venv

# Linux/Mac
rm -rf venv
```

### Deletar Banco de Dados (Recomeçar do Zero)
```bash
# Windows
del database.db

# Linux/Mac
rm database.db
```

---

## 📚 Documentação Adicional

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Bcrypt Documentation](https://github.com/pyca/bcrypt)
- [HTML5 Video](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video)

---

## ✨ Próximos Passos

1. Explore o painel admin
2. Crie usuários de teste
3. Adicione seus próprios vídeos
4. Customize cores e temas em `templates/`
5. Ajuste configurações em `config.py`

---

**Sucesso na instalação!** 🚀

Para dúvidas ou problemas, consulte o README.md ou crie uma issue no repositório.
