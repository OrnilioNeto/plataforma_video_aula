# ⚡ Início Rápido

## 1️⃣ Instalação (2 minutos)

### Windows
```bash
setup.bat
```

### Linux/Mac
```bash
chmod +x setup.sh
./setup.sh
```

---

## 2️⃣ Executar (1 minuto)

```bash
python app.py
```

Abra: **http://localhost:5000**

---

## 3️⃣ Login Padrão

```
Usuário: admin
Senha: admin123
```

---

## 4️⃣ Adicionar Vídeos

1. **Crie um vídeo de teste** (ou baixe de sample-videos.com)
2. **Coloque em**: `static/videos/video.mp4`
3. **No admin**, vá em **"Novo Vídeo"**:
   - Título: "Seu Título"
   - Arquivo: `video.mp4`
   - Duração: `600` (em segundos)
4. **Clique em Cadastrar**

---

## 5️⃣ Criar Usuários

Vá em **"Novo Usuário"**:
- Usuário: `joao`
- Senha: `senha123`
- Tipo: `user`
- **Cadastre**

---

## 6️⃣ Testar

1. **Saia** (logout)
2. **Faça login** com `joao/senha123`
3. **Veja o vídeo** - progresso é **automático!** 🎬
4. **Tente pular** - será **bloqueado!** 🔒

---

## 🎯 Funcionalidades Principais

| Feature | Tipo |
|---------|------|
| 🔐 Login seguro | ✅ |
| 🎥 Player HTML5 | ✅ |
| 🚫 Bloqueio de avanço | ✅ |
| 💾 Salva progresso | ✅ |
| 📊 Dashboard admin | ✅ |
| 👥 Multi-usuário | ✅ |
| 🎯 90% conclusão | ✅ |

---

## 📁 Estrutura

```
video_aula/
├── app.py              ← Aplicação principal
├── templates/          ← HTML (login, video, admin)
├── static/videos/      ← Coloque vídeos aqui
├── database.db         ← Banco (auto-criado)
└── requirements.txt    ← Dependências
```

---

## 🆘 Problemas?

| Problema | Solução |
|----------|---------|
| Porta em uso | Mudar em app.py (linha final) |
| Sem módulo bcrypt | `pip install bcrypt` |
| Vídeo não funciona | Verificar arquivo em `static/videos/` |
| Não salva progresso | Verificar console (F12) |

Mais: Veja **INSTALL.md** para troubleshooting completo

---

## 📚 Documentação

- **README.md** - Visão geral completa
- **INSTALL.md** - Instalação detalhada
- **API.md** - Endpoints e exemplos
- **DEVELOPMENT.md** - Para desenvolvedores
- **config.py** - Configurações customizáveis

---

## 🚀 Próximos Passos

1. ✅ Instalar e rodar
2. ✅ Criar conta de teste
3. ✅ Adicionar um vídeo
4. ✅ Testar o player
5. ✅ Explorar o admin
6. ⭐ Customizar cores/temas
7. 🚀 Deploy em produção

---

**Sucesso! 🎉**

Qualquer dúvida, consulte a documentação ou abra uma issue.
