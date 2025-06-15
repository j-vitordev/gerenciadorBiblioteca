from .conexao import conectar
import bcrypt

def cadastrar_usuario(nome, email, senha):
    """
    Cadastra um novo usuário no sistema
    Retorna: (sucesso: bool, mensagem: str)
    """
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

        # Insere o novo usuário
        cursor.execute(
            "INSERT INTO Usuarios (nome, email, senha, is_admin) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash.decode('utf-8'), is_admin)
        )

        conn.commit()
        return True, "Usuário admin cadastrado com sucesso!" if is_admin else "Usuário cadastrado com sucesso!"
    
    except Exception as e:
        print("Erro ao cadastrar:", e)
        return False, f"Erro ao cadastrar: {str(e)}"
    
    finally:
        if 'conn' in locals():
            conn.close()

def validar_usuario(email, senha):
    """
    Valida as credenciais do usuário
    Retorna: {
        "sucesso": bool,
        "admin": bool,
        "usuario_id": int | None
    }
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Busca usuário incluindo o ID
        cursor.execute("""
            SELECT id, senha, is_admin 
            FROM Usuarios 
            WHERE email = ?
        """, (email,))
        
        resultado = cursor.fetchone()

        if resultado:
            usuario_id = resultado[0]
            senha_hash = resultado[1]
            is_admin = bool(resultado[2])
            
            # Verifica a senha
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
                return {
                    "sucesso": True,
                    "admin": is_admin,
                    "usuario_id": usuario_id  # ID do usuário autenticado
                }
        
        return {
            "sucesso": False,
            "admin": False,
            "usuario_id": None
        }
    
    except Exception as e:
        print("Erro ao validar login:", e)
        return {
            "sucesso": False,
            "admin": False,
            "usuario_id": None
        }
    
    finally:
        if 'conn' in locals():
            conn.close()



def buscar_dados_usuario(usuario_id):
    """
    Retorna os dados do usuário (nome e categoria) dado o ID
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT nome, is_admin FROM Usuarios WHERE id = ?", (usuario_id,))
        resultado = cursor.fetchone()

        if resultado:
            nome = resultado[0]
            is_admin = resultado[1]
            categoria = "Administrador" if is_admin else "Leitor"
            return {
                "nome": nome,
                "categoria": categoria
            }
        else:
            return {
                "nome": "Desconhecido",
                "categoria": "Indefinido"
            }

    except Exception as e:
        print("Erro ao buscar dados do usuário:", e)
        return {
            "nome": "Erro",
            "categoria": "Erro"
        }
    
    finally:
        if 'conn' in locals():
            conn.close()


def atualizar_senha(usuario_id, nova_senha):
    """
    Atualiza a senha de um usuário específico.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("UPDATE Usuarios SET senha = ? WHERE id = ?", (senha_hash.decode('utf-8'), usuario_id))
        conn.commit()
        return True, "Senha atualizada com sucesso!"
    
    except Exception as e:
        print("Erro ao atualizar senha:", e)
        return False, f"Erro ao atualizar senha: {str(e)}"
    
    finally:
        if 'conn' in locals():
            conn.close()
