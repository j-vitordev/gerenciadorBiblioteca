import customtkinter as ctk
import sys
import os
from tkinter import filedialog

# Garante que o backend seja importado corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from backend.cadastroLivroBack import cadastrar_livro as cadastrar_backend

# Configurações iniciais do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Variável global para armazenar o caminho completo do PDF
caminho_pdf_completo = ""

def selecionar_pdf():
    global caminho_pdf_completo
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if caminho:
        caminho_pdf_completo = caminho  # Salva o caminho completo para enviar ao backend
        nome_arquivo = os.path.basename(caminho)
        label_pdf.configure(text=nome_arquivo)  # Atualiza o label com o nome do arquivo

def cadastrar_livro():
    global caminho_pdf_completo
    titulo = campo_titulo.get()
    autor = campo_autor.get()
    editora = campo_editora.get()
    ano = campo_ano.get()
    isbn = campo_isbn.get()

    if titulo and autor and editora and ano and isbn and caminho_pdf_completo:
        sucesso = cadastrar_backend(titulo, autor, editora, ano, isbn, caminho_pdf_completo)
        if sucesso:
            resultado.configure(text="📚 Livro cadastrado com sucesso!", text_color="green")
        else:
            resultado.configure(text="❌ Erro ao salvar no banco de dados.", text_color="red")
    else:
        resultado.configure(text="⚠️ Preencha todos os campos e selecione um PDF!", text_color="yellow")

# Criando a janela principal
app = ctk.CTk()
app.title("📘 Cadastro de Livros")
app.geometry("500x600")

# Criando o frame principal
frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(pady=40, padx=40, fill="both", expand=True)

# Título da janela
titulo_label = ctk.CTkLabel(frame, text="📘 Cadastro de Livros", font=('Arial', 22, 'bold'))
titulo_label.pack(pady=(20, 10))

# Campos do formulário
campo_titulo = ctk.CTkEntry(frame, placeholder_text="Título do livro")
campo_titulo.pack(padx=20, pady=5, fill="x")

campo_autor = ctk.CTkEntry(frame, placeholder_text="Autor")
campo_autor.pack(padx=20, pady=5, fill="x")

campo_editora = ctk.CTkEntry(frame, placeholder_text="Editora")
campo_editora.pack(padx=20, pady=5, fill="x")

campo_ano = ctk.CTkEntry(frame, placeholder_text="Ano de publicação")
campo_ano.pack(padx=20, pady=5, fill="x")

campo_isbn = ctk.CTkEntry(frame, placeholder_text="ISBN")
campo_isbn.pack(padx=20, pady=5, fill="x")

# Label para mostrar o nome do arquivo PDF selecionado (sem permitir digitar)
label_pdf = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado", anchor="w")
label_pdf.pack(padx=20, pady=5, fill="x")

# Botões
botao_selecionar_pdf = ctk.CTkButton(frame, text="Selecionar PDF", command=selecionar_pdf)
botao_selecionar_pdf.pack(pady=5)

botao_cadastrar = ctk.CTkButton(frame, text="Cadastrar Livro", command=cadastrar_livro)
botao_cadastrar.pack(pady=15)

# Mensagem de resultado
resultado = ctk.CTkLabel(frame, text="", font=("Arial", 12, "italic"))
resultado.pack(pady=5)

# Inicia a interface
app.mainloop()
