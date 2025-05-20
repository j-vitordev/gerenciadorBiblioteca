# backend/cadusuario.py

from .conexao import conectar
import bcrypt

def cadastrar_usuario(nome, email, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verifica se o e-mail já está cadastrado
        cursor.execute("SELECT * FROM Usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            print("Erro: Email já cadastrado.")
            return False

        # Criptografa a senha antes de salvar
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO Usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash.decode('utf-8'))
        )

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erro ao cadastrar:", e)
        return False

def validar_usuario(email, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Busca a senha hash pelo email
        cursor.execute("SELECT senha FROM Usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()

        if resultado:
            senha_hash = resultado[0]
            return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))

        return False
    except Exception as e:
        print("Erro ao validar login:", e)
        return False
