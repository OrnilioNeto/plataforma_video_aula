import sqlite3
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
from datetime import timedelta
import bcrypt
import re

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-muito-segura-2024'
app.permanent_session_lifetime = timedelta(hours=24)

# Caminho do banco de dados
DB_PATH = 'database.db'

# ==================== FUNCÕES DO BANCO DE DADOS ====================

def get_db_connection():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT,
            username TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT DEFAULT 'user' CHECK(tipo IN ('admin', 'user')),
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de vídeos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            arquivo TEXT,
            url TEXT,
            tipo TEXT,
            duracao INTEGER NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de progresso
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            video_id INTEGER NOT NULL,
            tempo REAL DEFAULT 0,
            concluido BOOLEAN DEFAULT 0,
            UNIQUE(usuario_id, video_id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY(video_id) REFERENCES videos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela de acesso a vídeos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario_videos_acesso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            video_id INTEGER NOT NULL,
            UNIQUE(usuario_id, video_id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY(video_id) REFERENCES videos(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    
    # Verificar se já existe o usuário admin
    cursor.execute('SELECT * FROM usuarios WHERE username = ?', ('admin',))
    if cursor.fetchone() is None:
        # Criar usuário admin padrão
        senha_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt())
        cursor.execute(
            'INSERT INTO usuarios (nome_completo, username, senha, tipo) VALUES (?, ?, ?, ?)',
            ('Administrador do Sistema', 'admin', senha_hash, 'admin')
        )
        conn.commit()
    
    conn.close()

def hash_password(password):
    """Faz hash da senha com bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, password_hash):
    """Verifica se a senha está correta"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash)

# ==================== DECORADORES ====================

def login_required(f):
    """Verifica se o usuário está autenticado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Verifica se o usuário é admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT tipo FROM usuarios WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        conn.close()
        
        if user is None or user['tipo'] != 'admin':
            return redirect(url_for('video_page'))
        
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return render_template('login.html', error='Usuário e senha são obrigatórios')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and verify_password(password, user['senha']):
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['tipo'] = user['tipo']
            
            # Redirecionar baseado no tipo de usuário
            if user['tipo'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('video_page'))
        else:
            return render_template('login.html', error='Usuário ou senha incorretos')
    
    if 'user_id' in session:
        if session['tipo'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('video_page'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Encerrar sessão"""
    session.clear()
    return redirect(url_for('login'))

# ==================== ROTAS DE VÍDEO ====================

@app.route('/video')
@login_required
def video_page():
    """Página de assistir vídeo"""
    if session['tipo'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obter lista de vídeos permitidos para o usuário
    cursor.execute('''
        SELECT v.* FROM videos v
        JOIN usuario_videos_acesso uva ON uva.video_id = v.id
        WHERE uva.usuario_id = ?
        ORDER BY v.id
    ''', (session['user_id'],))
    videos = cursor.fetchall()
    
    if not videos:
        conn.close()
        return render_template('video.html', video=None, videos=[], progresso={'tempo': 0, 'concluido': 0}, error="Você não possui vídeos vinculados à sua conta. Contate o administrador.")
        
    # Verificar vídeo solicitado
    video_id_req = request.args.get('id', type=int)
    video = None
    
    if video_id_req:
        video = next((v for v in videos if v['id'] == video_id_req), None)
        
    if video is None:
        video = videos[0]
    
    # Obter progresso do usuário
    cursor.execute(
        'SELECT * FROM progresso WHERE usuario_id = ? AND video_id = ?',
        (session['user_id'], video['id'])
    )
    progresso = cursor.fetchone()
    
    if progresso is None:
        # Criar registro de progresso se não existir
        cursor.execute(
            'INSERT INTO progresso (usuario_id, video_id) VALUES (?, ?)',
            (session['user_id'], video['id'])
        )
        conn.commit()
        progresso = {'tempo': 0, 'concluido': 0}
    
    conn.close()
    
    return render_template('video.html', video=video, videos=videos, progresso=progresso)

@app.route('/salvar_progresso', methods=['POST'])
@login_required
def salvar_progresso():
    """API para salvar o progresso do vídeo"""
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'erro', 'mensagem': 'Dados inválidos'}), 400
    
    video_id = data.get('video_id')
    tempo = data.get('tempo')
    
    if video_id is None or tempo is None:
        return jsonify({'status': 'erro', 'mensagem': 'Dados incompletos'}), 400
    
    try:
        tempo = float(tempo)
    except (ValueError, TypeError):
        return jsonify({'status': 'erro', 'mensagem': 'Tempo inválido'}), 400
    
    # Validações de segurança
    if tempo < 0:
        return jsonify({'status': 'erro', 'mensagem': 'Tempo não pode ser negativo'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar se o vídeo existe e obter sua duração
    cursor.execute('SELECT duracao FROM videos WHERE id = ?', (video_id,))
    video = cursor.fetchone()
    
    if video is None:
        conn.close()
        return jsonify({'status': 'erro', 'mensagem': 'Vídeo não encontrado'}), 404
    
    duracao = video['duracao']
    
    # Validar se o tempo não excede a duração do vídeo
    if tempo > duracao:
        tempo = duracao
    
    # Verificar saltos grandes (proteção contra avanço indevido)
    cursor.execute(
        'SELECT tempo FROM progresso WHERE usuario_id = ? AND video_id = ?',
        (session['user_id'], video_id)
    )
    progresso_atual = cursor.fetchone()
    
    if progresso_atual:
        tempo_anterior = progresso_atual['tempo']
        # Permitir pulo máximo de 30 segundos ou se for menor (rebobinamento)
        if tempo - tempo_anterior > 10:
            tempo = tempo_anterior + 10
    
    # Verificar se vídeo foi concluído (90% da duração)
    concluido = 1 if tempo >= (duracao * 0.9) else 0
    
    # Salvar ou atualizar progresso
    cursor.execute(
        '''UPDATE progresso 
           SET tempo = ?, concluido = ?
           WHERE usuario_id = ? AND video_id = ?''',
        (tempo, concluido, session['user_id'], video_id)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'sucesso',
        'tempo': tempo,
        'concluido': concluido,
        'duracao': duracao
    })



def converter_youtube(url):
    if "watch?v=" in url:
        video_id = url.split("watch?v=")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return url
# ==================== ROTAS DO PAINEL ADMIN ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Painel administrativo - Dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obter todos os usuários com seus dados de progresso
    cursor.execute('''
        SELECT 
            u.id,
            u.nome_completo,
            u.username,
            u.tipo,
            u.criado_em,
            COALESCE(SUM(p.tempo), 0) as tempo_total,
            COALESCE(SUM(CASE WHEN p.concluido = 1 THEN 1 ELSE 0 END), 0) as videos_concluidos,
            COUNT(DISTINCT p.video_id) as videos_assistindo
        FROM usuarios u
        LEFT JOIN progresso p ON u.id = p.usuario_id
        WHERE u.tipo = 'user'
        GROUP BY u.id
        ORDER BY u.criado_em DESC
    ''')
    usuarios = cursor.fetchall()
    
    # Obter estatísticas gerais
    cursor.execute('SELECT COUNT(*) as total FROM usuarios WHERE tipo = "user"')
    total_usuarios = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM videos')
    total_videos = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('admin.html', 
                         usuarios=usuarios, 
                         total_usuarios=total_usuarios,
                         total_videos=total_videos)

@app.route('/admin/cadastrar_usuario', methods=['POST'])
@admin_required
def cadastrar_usuario():
    """API para cadastrar novo usuário"""
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'erro', 'mensagem': 'Dados inválidos'}), 400
    
    nome_completo = data.get('nome_completo', '').strip()
    cpf = data.get('cpf', '').strip()
    tipo = data.get('tipo', 'user')
    
    # Validações
    if not nome_completo or not cpf:
        return jsonify({'status': 'erro', 'mensagem': 'Nome completo e CPF são obrigatórios'}), 400
    
    if len(cpf) < 11:
        return jsonify({'status': 'erro', 'mensagem': 'CPF inválido (deve conter pelo menos 11 dígitos)'}), 400
    
    if tipo not in ['admin', 'user']:
        tipo = 'user'
    
    # Validar CPF (apenas números)
    if not re.match(r'^[0-9]+$', cpf):
        return jsonify({'status': 'erro', 'mensagem': 'O CPF deve conter apenas números'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar se usuário já existe
    cursor.execute('SELECT id FROM usuarios WHERE username = ?', (cpf,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'status': 'erro', 'mensagem': 'Este CPF/Usuário já está cadastrado'}), 409
    
    try:
        senha_hash = hash_password(cpf)
        cursor.execute(
            'INSERT INTO usuarios (nome_completo, username, senha, tipo) VALUES (?, ?, ?, ?)',
            (nome_completo, cpf, senha_hash, tipo)
        )
        conn.commit()
        conn.close()
        return jsonify({'status': 'sucesso', 'mensagem': 'Usuário criado com sucesso'})
    except Exception as e:
        conn.close()
        return jsonify({'status': 'erro', 'mensagem': f'Erro ao criar usuário: {str(e)}'}), 500

@app.route('/admin/listar_usuarios')
@admin_required
def listar_usuarios():
    """API para listar usuários"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            u.id,
            u.nome_completo,
            u.username,
            u.tipo,
            COALESCE(SUM(p.tempo), 0) as tempo_total,
            COALESCE(SUM(CASE WHEN p.concluido = 1 THEN 1 ELSE 0 END), 0) as videos_concluidos
        FROM usuarios u
        LEFT JOIN progresso p ON u.id = p.usuario_id
        WHERE u.tipo = 'user'
        GROUP BY u.id
        ORDER BY u.nome_completo
    ''')
    usuarios = cursor.fetchall()
    conn.close()
    
    usuarios_list = [{
        'id': u['id'],
        'nome_completo': u['nome_completo'] or u['username'],
        'username': u['username'],
        'tipo': u['tipo'],
        'tempo_total': u['tempo_total'],
        'videos_concluidos': u['videos_concluidos']
    } for u in usuarios]
    
    return jsonify(usuarios_list)

@app.route('/admin/cadastrar_video', methods=['POST'])
@admin_required
def cadastrar_video():
    """API para cadastrar novo vídeo"""
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'erro', 'mensagem': 'Dados inválidos'}), 400
    
    titulo = data.get('titulo', '').strip()
    url = data.get('url', '').strip()
    duracao = data.get('duracao')

    tipo = 'arquivo'
    arquivo = data.get('arquivo', '').strip()

    if url:
        tipo = 'youtube'
        url = converter_youtube(url)
    
    # Validações
    # Validação básica
    if not titulo or duracao is None or not tipo:
        return jsonify({'status': 'erro', 'mensagem': 'Campos obrigatórios faltando'}), 400

    # Validação por tipo
    if tipo == 'arquivo' and not arquivo:
        return jsonify({'status': 'erro', 'mensagem': 'Arquivo é obrigatório'}), 400

    if tipo == 'youtube':
        if not url:
            return jsonify({'status': 'erro', 'mensagem': 'URL é obrigatória'}), 400
        url = converter_youtube(url)

    # Validação da duração
    try:
        duracao = int(duracao)
        if duracao <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({'status': 'erro', 'mensagem': 'Duração deve ser um número válido'}), 400

    # Validação do título
    if len(titulo) < 3:
        return jsonify({'status': 'erro', 'mensagem': 'Título deve ter pelo menos 3 caracteres'}), 400
    

    conn = get_db_connection()
    cursor = conn.cursor()
        
    try:
        cursor.execute(
            'INSERT INTO videos (titulo, arquivo, url, duracao, tipo) VALUES (?, ?, ?, ?, ?)',
            (titulo, arquivo, url, duracao, tipo)
        )
        conn.commit()
        video_id = cursor.lastrowid
        conn.close()
        return jsonify({
            'status': 'sucesso',
            'mensagem': 'Vídeo criado com sucesso',
            'video_id': video_id
        })
    except Exception as e:
        conn.close()
        return jsonify({'status': 'erro', 'mensagem': f'Erro ao criar vídeo: {str(e)}'}), 500

@app.route('/admin/listar_videos')
@admin_required
def listar_videos():
    """API para listar vídeos"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            v.id,
            v.titulo,
            v.arquivo,
            v.duracao,
            COUNT(DISTINCT p.usuario_id) as usuarios_assistindo,
            COALESCE(SUM(CASE WHEN p.concluido = 1 THEN 1 ELSE 0 END), 0) as usuarios_concluidos
        FROM videos v
        LEFT JOIN progresso p ON v.id = p.video_id
        GROUP BY v.id
        ORDER BY v.id
    ''')
    videos = cursor.fetchall()
    conn.close()
    
    videos_list = [{
        'id': v['id'],
        'titulo': v['titulo'],
        'arquivo': v['arquivo'],
        'duracao': v['duracao'],
        'usuarios_assistindo': v['usuarios_assistindo'],
        'usuarios_concluidos': v['usuarios_concluidos']
    } for v in videos]
    
    return jsonify(videos_list)

@app.route('/admin/deletar_usuario/<int:usuario_id>', methods=['POST'])
@admin_required
def deletar_usuario(usuario_id):
    """API para deletar usuário"""
    if usuario_id == session['user_id']:
        return jsonify({'status': 'erro', 'mensagem': 'Você não pode deletar sua própria conta'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar se usuário existe
    cursor.execute('SELECT id FROM usuarios WHERE id = ? AND tipo = "user"', (usuario_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'status': 'erro', 'mensagem': 'Usuário não encontrado'}), 404
    
    try:
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'sucesso', 'mensagem': 'Usuário deletado com sucesso'})
    except Exception as e:
        conn.close()
        return jsonify({'status': 'erro', 'mensagem': f'Erro ao deletar usuário: {str(e)}'}), 500

@app.route('/progresso_usuario/<int:usuario_id>')
@admin_required
def progresso_usuario(usuario_id):
    """API para obter progresso detalhado de um usuário"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            v.id,
            v.titulo,
            v.duracao,
            p.tempo,
            p.concluido,
            ROUND((p.tempo / v.duracao) * 100, 1) as percentual
        FROM progresso p
        JOIN videos v ON p.video_id = v.id
        WHERE p.usuario_id = ?
        ORDER BY v.id
    ''', (usuario_id,))
    
    progresso = cursor.fetchall()
    conn.close()
    
    progresso_list = [{
        'titulo': p['titulo'],
        'duracao': p['duracao'],
        'tempo': p['tempo'],
        'concluido': p['concluido'],
        'percentual': p['percentual']
    } for p in progresso]
    
    return jsonify(progresso_list)

@app.route('/admin/listar_acessos_usuario/<int:usuario_id>')
@admin_required
def listar_acessos_usuario(usuario_id):
    """API para listar os vídeos que um usuário tem acesso"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT video_id FROM usuario_videos_acesso WHERE usuario_id = ?', (usuario_id,))
    acessos = [row['video_id'] for row in cursor.fetchall()]
    conn.close()
    return jsonify({'acessos': acessos})

@app.route('/admin/salvar_acessos_usuario', methods=['POST'])
@admin_required
def salvar_acessos_usuario():
    """API para salvar os vídeos vinculados a um usuário"""
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    video_ids = data.get('video_ids', [])
    
    if not usuario_id:
        return jsonify({'status': 'erro', 'mensagem': 'ID do usuário não fornecido'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Remover acessos antigos
        cursor.execute('DELETE FROM usuario_videos_acesso WHERE usuario_id = ?', (usuario_id,))
        # Inserir novos acessos
        for video_id in video_ids:
            cursor.execute(
                'INSERT INTO usuario_videos_acesso (usuario_id, video_id) VALUES (?, ?)',
                (usuario_id, video_id)
            )
        conn.commit()
        conn.close()
        return jsonify({'status': 'sucesso', 'mensagem': 'Acessos atualizados com sucesso'})
    except Exception as e:
        conn.close()
        return jsonify({'status': 'erro', 'mensagem': f'Erro ao salvar acessos: {str(e)}'}), 500

@app.route('/admin/relatorios_kpi')
@admin_required
def relatorios_kpi():
    """API para retornar o relatório completo de KPI"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            u.nome_completo,
            u.username as cpf,
            v.titulo as video_titulo,
            v.duracao as video_duracao,
            COALESCE(p.tempo, 0) as tempo_assistido,
            CASE WHEN p.concluido = 1 THEN 'Sim' ELSE 'Não' END as concluido,
            ROUND((COALESCE(p.tempo, 0) / v.duracao) * 100, 1) as percentual
        FROM usuarios u
        JOIN usuario_videos_acesso uva ON u.id = uva.usuario_id
        JOIN videos v ON uva.video_id = v.id
        LEFT JOIN progresso p ON p.usuario_id = u.id AND p.video_id = v.id
        WHERE u.tipo = 'user'
        ORDER BY u.nome_completo, v.titulo
    ''')
    relatorio = cursor.fetchall()
    conn.close()
    
    relatorio_list = [{
        'nome_completo': r['nome_completo'] or r['cpf'],
        'cpf': r['cpf'],
        'video_titulo': r['video_titulo'],
        'video_duracao': r['video_duracao'],
        'tempo_assistido': r['tempo_assistido'],
        'concluido': r['concluido'],
        'percentual': r['percentual']
    } for r in relatorio]
    
    return jsonify(relatorio_list)

# ==================== MANIPULADOR DE ERROS ====================

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    """Página 404"""
    return render_template('login.html', error='Página não encontrada'), 404

@app.errorhandler(500)
def erro_interno(e):
    """Página 500"""
    return render_template('login.html', error='Erro interno do servidor'), 500

# ==================== INICIALIZAR APLICAÇÃO ====================

if __name__ == '__main__':
    # Inicializar banco de dados
    init_db()
    
    print("=" * 60)
    print("🚀 Sistema de Treinamento com Vídeo")
    print("=" * 60)
    print("📍 Acesse: http://localhost:5000")
    print("👤 Admin padrão: admin / admin123")
    print("=" * 60)
    
    # Executar aplicação
    app.run(debug=True, host='0.0.0.0', port=5000)
