#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar dados de teste no banco de dados
Execute: python create_sample_data.py
"""

import sqlite3
import bcrypt
from app import init_db, hash_password, DB_PATH

def criar_dados_teste():
    """Cria dados de teste no banco de dados"""
    
    print("=" * 60)
    print("🎬 Criando Dados de Teste")
    print("=" * 60)
    
    # Inicializar banco de dados
    init_db()
    print("✓ Banco de dados inicializado")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Criar usuários de teste
    usuarios_teste = [
        ('joao', 'senha123', 'user'),
        ('maria', 'senha123', 'user'),
        ('pedro', 'senha123', 'user'),
    ]
    
    for username, senha, tipo in usuarios_teste:
        try:
            cursor.execute('SELECT id FROM usuarios WHERE username = ?', (username,))
            if cursor.fetchone() is None:
                senha_hash = hash_password(senha)
                cursor.execute(
                    'INSERT INTO usuarios (username, senha, tipo) VALUES (?, ?, ?)',
                    (username, senha_hash, tipo)
                )
                print(f"✓ Usuário '{username}' criado com sucesso")
            else:
                print(f"⚠ Usuário '{username}' já existe")
        except Exception as e:
            print(f"✗ Erro ao criar usuário '{username}': {e}")
    
    conn.commit()
    
    # Criar vídeos de teste
    videos_teste = [
        ('Introdução a Python', 'intro_python.mp4', 600),
        ('Estruturas de Dados', 'estruturas_dados.mp4', 900),
        ('Funções em Python', 'funcoes_python.mp4', 720),
        ('Orientação a Objetos', 'oop_python.mp4', 1200),
    ]
    
    for titulo, arquivo, duracao in videos_teste:
        try:
            cursor.execute('SELECT id FROM videos WHERE titulo = ?', (titulo,))
            if cursor.fetchone() is None:
                cursor.execute(
                    'INSERT INTO videos (titulo, arquivo, duracao) VALUES (?, ?, ?)',
                    (titulo, arquivo, duracao)
                )
                print(f"✓ Vídeo '{titulo}' criado com sucesso")
            else:
                print(f"⚠ Vídeo '{titulo}' já existe")
        except Exception as e:
            print(f"✗ Erro ao criar vídeo '{titulo}': {e}")
    
    conn.commit()
    
    # Criar progresso de teste para alguns usuários
    cursor.execute('SELECT id FROM usuarios WHERE username IN (?, ?)', ('joao', 'maria'))
    usuarios = cursor.fetchall()
    
    cursor.execute('SELECT id FROM videos')
    videos = cursor.fetchall()
    
    for usuario in usuarios:
        for video in videos[:2]:  # Apenas primeiros 2 vídeos
            try:
                cursor.execute(
                    'SELECT id FROM progresso WHERE usuario_id = ? AND video_id = ?',
                    (usuario['id'], video['id'])
                )
                if cursor.fetchone() is None:
                    # Simular progresso aleatório
                    tempo = video[3] * 0.5  # 50% do vídeo assistido
                    cursor.execute(
                        'INSERT INTO progresso (usuario_id, video_id, tempo, concluido) VALUES (?, ?, ?, ?)',
                        (usuario['id'], video['id'], tempo, 0)
                    )
            except Exception as e:
                print(f"✗ Erro ao criar progresso: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Dados de Teste Criados com Sucesso!")
    print("=" * 60)
    print("\n📋 CREDENCIAIS DE TESTE:\n")
    print("Admin:")
    print("  Usuário: admin")
    print("  Senha: admin123\n")
    print("Usuários Comuns:")
    for username, senha, _ in usuarios_teste:
        print(f"  Usuário: {username}")
        print(f"  Senha: {senha}\n")

if __name__ == '__main__':
    criar_dados_teste()
