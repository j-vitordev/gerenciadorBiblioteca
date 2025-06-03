from backend.conexao import conectar
import bcrypt

def buscar_usuarios_nao_admin():
    conexao = conectar()
    cursor = conexao.cursor()
    
    query = """
    SELECT [id], [nome], [email], [senha], [is_admin]
    FROM [Biblioteca].[dbo].[Usuarios]
    WHERE [is_admin] = 0
    """
    
    cursor.execute(query)
    usuarios = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return usuarios

def excluir_usuario(user_id):
    conexao = conectar()
    cursor = conexao.cursor()

    query = "DELETE FROM [Biblioteca].[dbo].[Usuarios] WHERE [id] = ?"
    cursor.execute(query, user_id)
    
    conexao.commit()
    cursor.close()
    conexao.close()

def atualizar_senha(user_id, nova_senha):
    # Gerar hash da nova senha
    hashed = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        query = "UPDATE [Biblioteca].[dbo].[Usuarios] SET [senha] = ? WHERE [id] = ?"
        cursor.execute(query, (hashed.decode('utf-8'), user_id))  # armazenar como string
        conexao.commit()
    except Exception as e:
        print(f"Erro ao atualizar senha: {e}")
    finally:
        cursor.close()
        conexao.close()
