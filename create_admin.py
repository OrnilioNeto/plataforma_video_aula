import sqlite3
from werkzeug.security import generate_password_hash

# Conectar ao banco
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Definir credenciais do admin
username = "admin"
senha_plana = "10178415430"   # escolha a senha que quiser
senha_hash = generate_password_hash(senha_plana)
tipo = "admin"

# Verificar se já existe
cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
existe = cursor.fetchone()

if existe:
    # Atualiza senha e tipo
    cursor.execute(
        "UPDATE usuarios SET senha = ?, tipo = ? WHERE username = ?",
        (senha_hash, tipo, username)
    )
    print("Usuário admin atualizado.")
else:
    # Cria novo admin
    cursor.execute(
        "INSERT INTO usuarios (username, senha, tipo) VALUES (?, ?, ?)",
        (username, senha_hash, tipo)
    )
    print("Usuário admin criado.")

conn.commit()
conn.close()
