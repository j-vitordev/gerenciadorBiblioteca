import customtkinter as ctk
import os
from tkinter import filedialog
from backend.cadastroLivroBack import cadastrar_livro as cadastrar_backend

def TelaCadastroLivro(parent, callback_voltar):
    caminho_pdf_completo = {"caminho": ""}  # Usar dicionário mutável para atualizar internamente

    def selecionar_pdf():
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if caminho:
            caminho_pdf_completo["caminho"] = caminho
            nome_arquivo = os.path.basename(caminho)
            label_pdf.configure(text=nome_arquivo)
        # Botões
        botao_cadastrar = ctk.CTkButton(parent, text="Cadastrar Livro", command=cadastrar_livro)
        botao_cadastrar.pack(pady=15)

        resultado = ctk.CTkLabel(parent, text="", font=("Arial", 12, "italic"))
        resultado.pack(pady=5)


    def cadastrar_livro():
        titulo = campo_titulo.get()
        autor = campo_autor.get()
        editora = campo_editora.get()
        ano = campo_ano.get()
        isbn = campo_isbn.get()
        caminho_pdf_absoluto = caminho_pdf_completo["caminho"]

        if titulo and autor and editora and ano and isbn and caminho_pdf_absoluto:
            caminho_relativo = os.path.relpath(caminho_pdf_absoluto, os.getcwd())
            sucesso = cadastrar_backend(titulo, autor, editora, ano, isbn, caminho_relativo)
            if sucesso:
                resultado.configure(text="📚 Livro cadastrado com sucesso!", text_color="green")
            else:
                resultado.configure(text="❌ Erro ao salvar no banco de dados.", text_color="red")
        else:
            resultado.configure(text="⚠️ Preencha todos os campos e selecione um PDF!", text_color="yellow")

    # Título
    titulo_label = ctk.CTkLabel(parent, text="📘 Cadastro de Livros", font=('Arial', 22, 'bold'))
    titulo_label.pack(pady=(20, 10))

    # Campos
    campo_titulo = ctk.CTkEntry(parent, placeholder_text="Título do livro")
    campo_titulo.pack(padx=20, pady=5, fill="x")

    campo_autor = ctk.CTkEntry(parent, placeholder_text="Autor")
    campo_autor.pack(padx=20, pady=5, fill="x")

    campo_editora = ctk.CTkEntry(parent, placeholder_text="Editora")
    campo_editora.pack(padx=20, pady=5, fill="x")

    campo_ano = ctk.CTkEntry(parent, placeholder_text="Ano de publicação")
    campo_ano.pack(padx=20, pady=5, fill="x")

    campo_isbn = ctk.CTkEntry(parent, placeholder_text="ISBN")
    campo_isbn.pack(padx=20, pady=5, fill="x")

    # PDF
    label_pdf = ctk.CTkLabel(parent, text="Nenhum arquivo selecionado", anchor="w")
    label_pdf.pack(padx=20, pady=5, fill="x")

    botao_selecionar_pdf = ctk.CTkButton(parent, text="Selecionar PDF", command=selecionar_pdf)
    botao_selecionar_pdf.pack(pady=5)

    # Botões
    botao_cadastrar = ctk.CTkButton(parent, text="Cadastrar Livro", command=cadastrar_livro)
    botao_cadastrar.pack(pady=15)

    resultado = ctk.CTkLabel(parent, text="", font=("Arial", 12, "italic"))
    resultado.pack(pady=5)
