from .conexao import conectar
import bcrypt

def cadastrar_usuario(nome, email, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verifica se o e-mail já está cadastrado
        cursor.execute("SELECT * FROM Usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            return False, "Email já cadastrado."

        # Define se é admin baseado no email
        is_admin = 1 if email.lower() == "admin@gmail.com" else 0

        # Criptografa a senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO Usuarios (nome, email, senha, is_admin) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash.decode('utf-8'), is_admin)
        )

        conn.commit()
        conn.close()
        return True, "Usuário admin cadastrado com sucesso!" if is_admin else "Usuário cadastrado com sucesso!"
    except Exception as e:
        print("Erro ao cadastrar:", e)
        return False, f"Erro ao cadastrar: {str(e)}"

def validar_usuario(email, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT senha, is_admin FROM Usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()

        if resultado:
            senha_hash = resultado[0]
            is_admin = bool(resultado[1])
            
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
                return {"sucesso": True, "admin": is_admin}
        
        return {"sucesso": False, "admin": False}
    except Exception as e:
        print("Erro ao validar login:", e)
        return {"sucesso": False, "admin": False}