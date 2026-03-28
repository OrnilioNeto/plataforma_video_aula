# 🎓 Sistema de Treinamento com Vídeo

Um sistema web completo de treinamento com vídeo desenvolvido em **Python Flask** e **SQLite**, com autenticação de usuários, controle avançado de progresso de vídeo e painel administrativo completo.

## 🚀 Funcionalidades Principais

### 👥 Autenticação e Controle de Acesso
- ✅ Sistema de login seguro com hash de senha (bcrypt)
- ✅ Dois tipos de usuários: **Admin** e **Usuário Comum**
- ✅ Redirecionamento automático baseado no tipo de usuário
- ✅ Proteção de rotas e validação de sessão
- ✅ Tempo de sessão configurável

### 🎥 Funcionalidade de Vídeo
- ✅ Player de vídeo HTML5 integrado
- ✅ **Retomada automática** do tempo anterior
- ✅ **Bloqueio de avanço** - não é permitido assistir além do conteúdo já visto
- ✅ Detecção de pulos grandes (máximo 30 segundos)
- ✅ Bloqueio de alteração de velocidade de reprodução
- ✅ Progresso de vídeo em tempo real
- ✅ **Conclusão automática** quando 90% do vídeo é assistido
- ✅ Barra de progresso visual
- ✅ Validação no backend (segurança)

### 📊 Painel Administrativo
- ✅ Dashboard com estatísticas gerais
- ✅ Listagem de usuários com tempo assistido
- ✅ Gerenciamento de vídeos
- ✅ Visualização de progresso detalhado por usuário
- ✅ Cadastro de novos usuários e vídeos
- ✅ Deleção de usuários (com confirmação)
- ✅ Interface moderna e responsiva

### 🔒 Segurança
- ✅ Hash de senha com bcrypt
- ✅ Validação de entrada no backend
- ✅ Proteção contra avanço indevido de vídeo
- ✅ Sessão segura com Flask
- ✅ CSRF protection nativo do Flask
- ✅ Sanitização de dados

## 📋 Requisitos

- Python 3.8+
- pip (gerenciador de pacotes)
- Navegador moderno (Chrome, Firefox, Safari, Edge)

## 🛠️ Instalação

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/seu-usuario/video-treinamento.git
cd video-treinamento
```

### 2. Crie um ambiente virtual

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

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🚀 Executar a Aplicação

```bash
python app.py
```

A aplicação será iniciada em `http://localhost:5000`

**Caso tenha erro de porta em uso**, modifique a porta no final do `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude para 5001 ou outra porta
```

## 🔑 Credenciais Padrão

| Rolle | Usuário | Senha |
|-------|---------|-------|
| Admin | `admin` | `admin123` |
| User  | (nenhum) | (crie via admin) |

## 📁 Estrutura do Projeto

```
/video_aula
├── app.py                    # Aplicação principal Flask
├── database.db               # Banco de dados SQLite (criado automaticamente)
├── requirements.txt          # Dependências do projeto
├── README.md                 # Este arquivo
│
├── /templates/               # Templates HTML
│   ├── login.html           # Página de login
│   ├── video.html           # Página de assistir vídeo
│   └── admin.html           # Painel administrativo
│
└── /static/                 # Arquivos estáticos
    ├── /css/               # Estilos CSS (opcional)
    ├── /js/                # Scripts JavaScript (opcional)
    └── /videos/            # Pasta para vídeos
        └── [Coloque seus vídeos aqui]
```

## 🎬 Como Adicionar Vídeos

### 1. Copie seu arquivo de vídeo

Coloque seu arquivo `.mp4` na pasta `static/videos/`. Por exemplo:
```
static/videos/aula_01.mp4
static/videos/aula_02.mp4
```

### 2. No Painel Admin

1. Faça login como admin
2. Vá para aba **"Novo Vídeo"**
3. Preencha os dados:
   - **Título**: Nome descritivo do vídeo
   - **Arquivo**: Nome do arquivo (ex: `aula_01.mp4`)
   - **Duração em segundos**: Calcule a duração em segundos
4. Clique em **"Cadastrar Vídeo"**

### Calcular Duração de Vídeo

**Windows (PowerShell):**
```powershell
# Instale FFmpeg primeiro: choco install ffmpeg
ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1:precision=0 "static/videos/seu_video.mp4"
```

**Linux/Mac:**
```bash
# Instale FFmpeg: sudo apt install ffmpeg (ou brew install ffmpeg)
ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1:precision=0 static/videos/seu_video.mp4
```

Ou simplesmente use uma calculadora online/programa de edição de vídeo.

## 📊 Banco de Dados

O banco SQLite é criado automaticamente com as seguintes tabelas:

### Tabela `usuarios`
```sql
- id (PK)
- username (único)
- senha (hash)
- tipo (admin ou user)
- criado_em (timestamp)
```

### Tabela `videos`
```sql
- id (PK)
- titulo
- arquivo (caminho)
- duracao (segundos)
- criado_em (timestamp)
```

### Tabela `progresso`
```sql
- id (PK)
- usuario_id (FK)
- video_id (FK)
- tempo (float, segundos)
- concluido (boolean)
- UNIQUE(usuario_id, video_id)
```

## 🔗 Rotas da API

### Autenticação
- `GET /` - Página de login
- `POST /` - Submeter login
- `GET /logout` - Encerrar sessão

### Usuário
- `GET /video` - Página de assistir vídeo
- `POST /salvar_progresso` - Salvar progresso do vídeo

### Admin
- `GET /admin` - Dashboard administrativo
- `POST /admin/cadastrar_usuario` - Criar novo usuário
- `GET /admin/listar_usuarios` - Listar usuários (API)
- `POST /admin/cadastrar_video` - Criar novo vídeo
- `GET /admin/listar_videos` - Listar vídeos (API)
- `GET /progresso_usuario/<id>` - Progresso de um usuário
- `POST /admin/deletar_usuario/<id>` - Deletar usuário

## 🎨 Interface

### Página de Login
- Design moderno com gradiente
- Validação de entrada
- Mensagens de erro claras

### Página de Vídeo
- Player HTML5 com controles
- Barra de progresso visual
- Lista de vídeos na lateral
- Status de conclusão
- Notificações de ações

### Painel Admin
- Dashboard com estatísticas
- Abas para diferentes seções
- Tabelas responsivas
- Modais para ver progresso
- Formulários de cadastro

## 🔐 Segurança

### Medidas Implementadas
1. **Hash de Senha**: Bcrypt com salt
2. **Bloqueio de Avanço de Vídeo**:
   - Máximo de 30 segundos de avanço permitido
   - Validação no backend do tempo
   - Impossibilidade de pular para o final
3. **Validação de Sessão**: Verificação em cada rota protegida
4. **Validação de Entrada**: Verificação de tipos e valores
5. **Proteção de Rotas**: Decoradores para admin e login obrigatório
6. **CSRF Protection**: Nativa do Flask

## 🐛 Troubleshooting

### Erro: "Address already in use"
```bash
# Mude a porta no app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Erro: "ModuleNotFoundError: No module named 'bcrypt'"
```bash
pip install bcrypt
```

### Vídeos não aparecem
- Verifique se estão na pasta `static/videos/`
- Confirme que o caminho está exato no BD

### Progresso não salva
- Verifique o console do navegador (F12)
- Verifique se `database.db` tem permissões de escrita

## 📈 Diferenciais Implementados

- ✅ Barra de progresso em tempo real visualmente atualizada
- ✅ Bloqueio de mudança de velocidade de reprodução
- ✅ Criptografia de senha com bcrypt (além de hash)
- ✅ Interface moderna e responsiva
- ✅ Notificações em tempo real
- ✅ Dashboard com estatísticas
- ✅ Validações robustas no frontend e backend
- ✅ Suporte a múltiplos usuários simultâneos

## 📝 Exemplo de Uso

### 1. Admin cria nova conta de usuário
```
Login: admin / admin123
Vai à aba "Novo Usuário"
Cria usuario "joao" com senha "senha123"
```

### 2. Admin cadastra um vídeo
```
Na aba "Novo Vídeo"
Título: "Introdução a Python"
Arquivo: "intro_python.mp4" (deve estar em static/videos/)
Duração: 3600 (em segundos)
```

### 3. Usuário assiste vídeo
```
Login: joao / senha123
Vê o vídeo na página principal
Player bloqueia avanço além do assistido
Progresso é salvo automaticamente
```

### 4. Admin acompanha progresso
```
Vai ao painel admin
Clica em "Ver Progresso" de um usuário
Vê percentual e tempo assistido de cada vídeo
```

## 🚀 Deploy

Para colocar em produção:

1. **Desative debug mode**: `debug=False` no app.py
2. **Use um servidor WSGI**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```
3. **Use HTTPS**: Configure com Nginx/Apache
4. **Banco de dados**: Considere migrar para PostgreSQL
5. **Variáveis de ambiente**: Coloque a `secret_key` em env

## 📞 Suporte

Caso enfrente problemas:

1. Verifique o console do navegador (F12)
2. Verifique os logs da aplicação Python
3. Confirme que todas as dependências estão instaladas
4. Verifique permissões de arquivo

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente.

## 🎯 Roadmap Futuro

- [ ] Sistema de certificados
- [ ] Quiz após vídeos
- [ ] Comentários nos vídeos
- [ ] Taxa de engajamento
- [ ] Integração com YouTube
- [ ] App mobile
- [ ] Notificações por email
- [ ] Análise avançada de dados

---

**Versão**: 1.0  
**Última atualização**: Março 2024  
**Desenvolvido com** ❤️ **em Python**
