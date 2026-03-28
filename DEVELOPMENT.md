# 🔧 Guia de Desenvolvimento

## Estrutura do Projeto

```
video-treinamento/
├── app.py                      # Aplicação principal Flask
├── config.py                   # Configurações
├── create_sample_data.py        # Script para criar dados de teste
├── requirements.txt             # Dependências Python
├── database.db                  # Banco de dados SQLite (criado automaticamente)
│
├── templates/                   # Templates HTML
│   ├── login.html              # Página de login
│   ├── video.html              # Player de vídeo
│   └── admin.html              # Painel administrativo
│
└── static/                      # Arquivos estáticos
    ├── css/                    # Estilos customizados (opcional)
    ├── js/                     # Scripts customizados (opcional)
    └── videos/                 # Pasta de vídeos
```

## Arquitetura

### Backend (Flask)
- **Autenticação**: Sessão com Flask + Bcrypt
- **Banco de Dados**: SQLite com sqlite3
- **APIs REST**: JSON endpoints para frontend
- **Validação**: Proteção no servidor

### Frontend
- **Login**: HTML puro com CSS
- **Vídeo**: HTML5 Video + JavaScript
- **Admin**: Tabelas dinâmicas com AJAX
- **Notificações**: Sistema de toast/notificação

## Fluxo de Autenticação

```
1. Usuário submete login
2. App.py verifica credenciais
3. Se correto, criar sessão
4. Redirecionar baseado em tipo
5. Admin → /admin | User → /video
```

## Fluxo de Progresso de Vídeo

```
1. Usuário carrega /video
2. Backend obtém tempo anterior
3. Video.html carrega com currentTime
4. A cada 5s, envia tempo via POST
5. Backend valida e salva no BD
6. Se 90%+, marca como concluído
```

## Como Adicionar Novas Funcionalidades

### 1. Adicionar Nova Rota

**Em app.py:**
```python
@app.route('/nova-rota')
@login_required  # Usar decoradores apropriados
def nova_funcao():
    return render_template('nova.html')
```

### 2. Adicionar Nova Página

**Em templates/nova.html:**
```html
{% extends "base.html" %}  <!-- Se usar herança -->

{% block content %}
<h1>Meu Conteúdo</h1>
{% endblock %}
```

### 3. Adicionar Novo Endpoint API

```python
@app.route('/api/nova', methods=['POST', 'GET'])
@login_required
def api_nova():
    data = request.get_json()
    
    # Validar
    if not data.get('campo'):
        return jsonify({'error': 'Campo obrigatório'}), 400
    
    # Processar
    resultado = fazer_algo(data)
    
    # Retornar
    return jsonify({'status': 'sucesso', 'dados': resultado})
```

### 4. Chamar API do Frontend

```javascript
fetch('/api/nova', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ campo: 'valor' })
})
.then(r => r.json())
.then(data => {
    if (data.status === 'sucesso') {
        console.log('Sucesso!', data.dados);
    }
})
.catch(e => console.error('Erro:', e));
```

## Banco de Dados

### Executar Query SQL Diretamente

```python
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('SELECT * FROM usuarios')
usuarios = cursor.fetchall()
conn.close()
```

### Adicionar Nova Tabela

1. Edite `init_db()` em app.py
2. Adicione `CREATE TABLE` se não existir
3. Recrie banco: `rm database.db` e execute app novamente

## Testes

### Teste Manual
1. Login com diferentes usuários
2. Testar bloqueio de avanço
3. Verificar cálculos de progresso
4. Testar Admin CRUD

### Teste de Segurança
1. Tentar acessar /admin sem ser admin
2. Tentar SQL injection em login
3. Tentar modificar tempo via DevTools
4. Tentar pular para 1h de um vídeo de 10min

## Debugging

### Print/Log
```python
print('Debug:', valor)  # Console
print('Debug:', valor, file=sys.stderr)  # Stderr
```

### DevTools (navegador)
- F12 → Console (erros JS)
- F12 → Network (requisições)
- F12 → Storage → Cookies (sessão)

### Flask Debug Mode
```python
app.run(debug=True)  # Auto-reload, error page
```

## Performance

### Otimizações Implementadas
- ✓ Banco de dados indexado (PK, FK)
- ✓ Consultas eficientes (JOINs optimizados)
- ✓ Frontend leve (sem frameworks pesados)
- ✓ CSS e JS inline (menos requisições)

### Possíveis Melhorias
- Adicionar cache com Redis
- Compressão de vídeos
- CDN para vídeos
- Lazy loading de tabelas
- Paginação no admin

## Segurança

### Já Implementado
- ✓ Hash bcrypt de senhas
- ✓ Validação de sessão
- ✓ Proteção de rotas
- ✓ Validação backend
- ✓ Bloqueio de avanço indevido

### Recomendações Futuras
- HTTPS obrigatório
- Rate limiting de login
- 2FA (autenticação dupla)
- Log de atividades
- Backup automático

## Estilo de Código

### Convenções
- Variáveis: `snake_case`
- Classes: `PascalCase`
- Constantes: `UPPER_CASE`
- Comentários em português
- Docstrings em funções importantes

### Exemplo
```python
def calcular_progresso_usuario(usuario_id, video_id):
    """
    Calcula o percentual de progresso de um usuário em um vídeo.
    
    Args:
        usuario_id (int): ID do usuário
        video_id (int): ID do vídeo
    
    Returns:
        float: Percentual (0-100)
    """
    # Implementação...
    return percentual
```

## Versionamento

### Versões Semânticas
- Major: Mudanças incompatíveis
- Minor: Novas features compatíveis
- Patch: Correções de bugs

Atualmente: **v1.0.0**

## Contribuindo

1. Fork o repositório
2. Crie branch para nova feature: `git checkout -b feature/nova-feature`
3. Commit mudanças: `git commit -m 'Add: nova feature'`
4. Push: `git push origin feature/nova-feature`
5. Abra Pull Request

## Deploy

### Desenvolvimento
```bash
python app.py  # DEBUG=True
```

### Produção
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Com Nginx:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

## Troubleshooting Dev

### Banco corrompido?
```bash
rm database.db
python app.py  # Recria automaticamente
```

### Ambiente virtual corrompido?
```bash
rm -rf venv/
python -m venv venv
pip install -r requirements.txt
```

### Porta em uso?
```bash
# Mude em app.py ou use:
PORT=5001 python app.py
```

---

**Bom código! 💻**
