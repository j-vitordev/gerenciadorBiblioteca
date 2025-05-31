# backend/cadastroLivroBack.py

from backend.conexao import conectar


def cadastrar_livro(titulo, autor, editora, ano_publicacao, isbn, caminho_pdf):
    try:
        conn = conectar()
        cursor = conn.cursor()

        comando = """
        INSERT INTO dbo.livros (titulo, autor, editora, ano_publicacao, isbn, caminho_pdf)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(comando, (titulo, autor, editora, ano_publicacao, isbn, caminho_pdf))
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Erro ao cadastrar livro no banco: {e}")
        return False
