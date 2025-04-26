import pyodbc

# Conexão com o banco SQL Server
def conectar():
    conexao = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=SEU_SERVIDOR_SQL;"
        "Database=biblioteca_db;"
        "Trusted_Connection=yes;"
    )
    return conexao

# Função para cadastrar usuário
def cadastrar_usuario(nome, email, senha):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conexao.commit()
        return True
    except Exception as e:
        print("Erro ao cadastrar:", e)
        return False

# Função para validar login
def validar_usuario(email, senha):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        resultado = cursor.fetchone()
        return resultado is not None
    except Exception as e:
        print("Erro ao validar login:", e)
        return False