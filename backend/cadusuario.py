# backend/cadusuario.py

from .conexao import conectar

def cadastrar_usuario(nome, email, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
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

        cursor.execute(
            "SELECT * FROM Usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )
        return cursor.fetchone() is not None
    except Exception as e:
        print("Erro ao validar login:", e)
        return False
