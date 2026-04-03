import sqlite3
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

# Usar DB_PATH do ambiente, ou fallback local se não houver
DB_PATH = os.environ.get('DB_PATH', 'database.db')

# Conectar ao banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Definir credenciais do admin lendo das variáveis de ambiente (com falback temporário caso não exista env)
username = os.environ.get('DEFAULT_ADMIN_USER', 'admin').strip()
senha_plana = os.environ.get('DEFAULT_ADMIN_PASS', '@Machado2025').strip()
senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
tipo = "admin"
nome_completo = os.environ.get('DEFAULT_ADMIN_NOME', 'Ornilio Neto').strip()

# Verificar se já existe
cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
existe = cursor.fetchone()

if existe:
    # Atualiza senha, tipo e nome completo
    cursor.execute(
        "UPDATE usuarios SET senha = ?, tipo = ?, nome_completo = ? WHERE username = ?",
        (senha_hash, tipo, nome_completo, username)
    )
    print("Usuário admin atualizado.")
else:
    # Cria novo admin
    cursor.execute(
        "INSERT INTO usuarios (nome_completo, username, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome_completo, username, senha_hash, tipo)
    )
    print("Usuário admin criado.")

conn.commit()
conn.close()
