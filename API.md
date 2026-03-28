# 📚 Documentação da API

## Base URL
```
http://localhost:5000
```

## Headers Padrão
```json
{
    "Content-Type": "application/json"
}
```

---

## 🔐 Autenticação

### GET / (Login)
Exibe página de login

**Método**: GET  
**Autenticação**: Não requerida  
**Response**: HTML da página de login

---

### POST / (Submeter Login)
Autentica usuário e cria sessão

**Método**: POST  
**Autenticação**: Não requerida  
**Content-Type**: application/x-www-form-urlencoded  

**Parâmetros**:
```
username=admin&password=admin123
```

**Response**:
- ✓ Sucesso: Redireciona para /admin ou /video
- ✗ Erro: Retorna login.html com mensagem de erro

**Códigos**:
- 200: OK
- 302: Redirect (após sucesso)

---

### GET /logout
Encerra sessão do usuário

**Método**: GET  
**Autenticação**: Requerida  
**Response**: Redireciona para login

**Exemplo**:
```bash
curl -X GET http://localhost:5000/logout
```

---

## 🎥 Vídeo

### GET /video
Obtém página de reprodução de vídeo

**Método**: GET  
**Autenticação**: Requerida (apenas usuários)  
**Query Parameters**:
- `id` (int, opcional): ID do vídeo a reproduzir

**Response**: HTML5 com player de vídeo

**Exemplo**:
```bash
curl -X GET http://localhost:5000/video?id=1
```

---

### POST /salvar_progresso
Salva progresso do usuário em um vídeo

**Método**: POST  
**Autenticação**: Requerida  
**Content-Type**: application/json

**Request Body**:
```json
{
    "video_id": 1,
    "tempo": 120.5
}
```

**Response**:
```json
{
    "status": "sucesso",
    "tempo": 120.5,
    "concluido": 0,
    "duracao": 600
}
```

**Validações**:
- Tempo não pode ser maior que duração
- Tempo não pode ser negativo
- Pulo máximo de 30 segundos
- vídeo deve existir no BD

**Erros**:
```json
{
    "status": "erro",
    "mensagem": "Vídeo não encontrado"
}
```

**Códigos**:
- 200: OK
- 400: Bad Request
- 404: Not Found

**Exemplo**:
```bash
curl -X POST http://localhost:5000/salvar_progresso \
  -H "Content-Type: application/json" \
  -d '{"video_id": 1, "tempo": 120.5}'
```

---

## 👨‍💼 Admin

### GET /admin
Exibe painel administrativo

**Método**: GET  
**Autenticação**: Requerida (apenas admin)  
**Response**: HTML do painel admin

---

### POST /admin/cadastrar_usuario
Cria novo usuário

**Método**: POST  
**Autenticação**: Requerida (apenas admin)  
**Content-Type**: application/json

**Request Body**:
```json
{
    "username": "joao",
    "senha": "senha123",
    "tipo": "user"
}
```

**Response (Sucesso)**:
```json
{
    "status": "sucesso",
    "mensagem": "Usuário criado com sucesso"
}
```

**Response (Erro)**:
```json
{
    "status": "erro",
    "mensagem": "Este usuário já existe"
}
```

**Validações**:
- Username mínimo 3 caracteres
- Senha mínima 6 caracteres
- Username único
- Tipo deve ser 'admin' ou 'user'
- Username apenas letras, números, underscore

**Códigos**:
- 200: OK
- 400: Bad Request
- 409: Conflict (usuário existe)
- 500: Server Error

**Exemplo**:
```bash
curl -X POST http://localhost:5000/admin/cadastrar_usuario \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "senha": "senha123", "tipo": "user"}'
```

---

### GET /admin/listar_usuarios
Lista todos os usuários

**Método**: GET  
**Autenticação**: Requerida (apenas admin)

**Response**:
```json
[
    {
        "id": 1,
        "username": "admin",
        "tipo": "admin",
        "tempo_total": 3600,
        "videos_concluidos": 2
    },
    {
        "id": 2,
        "username": "joao",
        "tipo": "user",
        "tempo_total": 1800,
        "videos_concluidos": 1
    }
]
```

**Exemplo**:
```bash
curl -X GET http://localhost:5000/admin/listar_usuarios
```

---

### POST /admin/cadastrar_video
Cria novo vídeo

**Método**: POST  
**Autenticação**: Requerida (apenas admin)  
**Content-Type**: application/json

**Request Body**:
```json
{
    "titulo": "Introdução a Python",
    "arquivo": "intro_python.mp4",
    "duracao": 3600
}
```

**Response (Sucesso)**:
```json
{
    "status": "sucesso",
    "mensagem": "Vídeo criado com sucesso",
    "video_id": 1
}
```

**Validações**:
- Título mínimo 3 caracteres
- Duração maior que 0
- Todos os campos obrigatórios

**Códigos**:
- 200: OK
- 400: Bad Request
- 500: Server Error

**Exemplo**:
```bash
curl -X POST http://localhost:5000/admin/cadastrar_video \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Intro Python", "arquivo": "intro.mp4", "duracao": 3600}'
```

---

### GET /admin/listar_videos
Lista todos os vídeos

**Método**: GET  
**Autenticação**: Requerida (apenas admin)

**Response**:
```json
[
    {
        "id": 1,
        "titulo": "Introdução a Python",
        "arquivo": "intro_python.mp4",
        "duracao": 3600,
        "usuarios_assistindo": 5,
        "usuarios_concluidos": 2
    }
]
```

---

### POST /admin/deletar_usuario/:id
Deleta um usuário

**Método**: POST  
**Autenticação**: Requerida (apenas admin)  
**URL Parameter**: `id` (int) - ID do usuário

**Response (Sucesso)**:
```json
{
    "status": "sucesso",
    "mensagem": "Usuário deletado com sucesso"
}
```

**Validações**:
- Não pode deletar própria conta
- Usuário deve existir
- Deve ser do tipo 'user' (não admin)

**Códigos**:
- 200: OK
- 400: Bad Request
- 404: Not Found
- 500: Server Error

**Exemplo**:
```bash
curl -X POST http://localhost:5000/admin/deletar_usuario/2
```

---

### GET /progresso_usuario/:id
Obtém progresso detalhado de um usuário

**Método**: GET  
**Autenticação**: Requerida (apenas admin)  
**URL Parameter**: `id` (int) - ID do usuário

**Response**:
```json
[
    {
        "titulo": "Introdução a Python",
        "duracao": 3600,
        "tempo": 1800,
        "concluido": 0,
        "percentual": 50.0
    },
    {
        "titulo": "Funções em Python",
        "duracao": 1800,
        "tempo": 1800,
        "concluido": 1,
        "percentual": 100.0
    }
]
```

**Exemplo**:
```bash
curl -X GET http://localhost:5000/progresso_usuario/2
```

---

## 📊 Formatos de Resposta

### Sucesso
```json
{
    "status": "sucesso",
    "mensagem": "Operação realizada",
    "dados": { }
}
```

### Erro
```json
{
    "status": "erro",
    "mensagem": "Descrição do erro"
}
```

---

## 🔒 Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Requisição bem sucedida |
| 302 | Redirect - Redirecionamento |
| 400 | Bad Request - Dados inválidos |
| 404 | Not Found - Recurso não encontrado |
| 409 | Conflict - Recurso duplicado |
| 500 | Server Error - Erro no servidor |

---

## 📝 Exemplos de Requisição

### JavaScript (Fetch)
```javascript
// Salvar progresso
fetch('/salvar_progresso', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        video_id: 1,
        tempo: 120.5
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Erro:', error));
```

### cURL
```bash
# Listar usuários
curl -X GET http://localhost:5000/admin/listar_usuarios

# Criar usuário
curl -X POST http://localhost:5000/admin/cadastrar_usuario \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","senha":"pass123","tipo":"user"}'

# Salvar progresso
curl -X POST http://localhost:5000/salvar_progresso \
  -H "Content-Type: application/json" \
  -d '{"video_id":1,"tempo":120.5}'
```

### Python (requests)
```python
import requests

# Login
response = requests.post('http://localhost:5000/', data={
    'username': 'admin',
    'password': 'admin123'
})

# Salvar progresso
response = requests.post('http://localhost:5000/salvar_progresso', json={
    'video_id': 1,
    'tempo': 120.5
})

print(response.json())
```

---

## 🚫 Erros Comuns

### 401 Unauthorized
```json
{
    "status": "erro",
    "mensagem": "Você não está autenticado"
}
```
**Solução**: Fazer login primeiro

### 403 Forbidden
```json
{
    "status": "erro",
    "mensagem": "Você não tem permissão"
}
```
**Solução**: Ser admin para acessar /admin

### 404 Not Found
```json
{
    "status": "erro",
    "mensagem": "Recurso não encontrado"
}
```
**Solução**: Verificar ID ou rota

---

## 📞 Rate Limiting

Atualmente **não há** rate limiting implementado.

Para produção, recomenda-se usar:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

**Versão da API**: 1.0  
**Última atualização**: Março 2024
