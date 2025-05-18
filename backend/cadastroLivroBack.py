import customtkinter as ctk
from tkinter import filedialog
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

arquivo_pdf = None  # Variável para guardar o caminho do PDF selecionado

def selecionar_pdf():
    global arquivo_pdf
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho:
        arquivo_pdf = caminho
        label_pdf.configure(text=f"📄 Selecionado: {os.path.basename(caminho)}", text_color="lightblue")

def cadastrar_livro():
    titulo = campo_titulo.get()
    autor = campo_autor.get()
    editora = campo_editora.get()
    ano = campo_ano.get()
    isbn = campo_isbn.get()

    if not all([titulo, autor, editora, ano, isbn]):
        resultado.configure(text="⚠️ Preencha todos os campos!", text_color="yellow")
        return

    if not arquivo_pdf:
        resultado.configure(text="📄 Selecione um arquivo PDF antes de cadastrar!", text_color="orange")
        return

    # Aqui você pode chamar a função do backend para salvar no banco, passando o caminho do PDF
    # exemplo: salvar_livro(titulo, autor, editora, ano, isbn, arquivo_pdf)

    resultado.configure(text="📚 Livro cadastrado com sucesso!", text_color="green")

app = ctk.CTk()
app.title("📘 Cadastro de Livros")
app.geometry("500x600")

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(pady=40, padx=40, fill="both", expand=True)

titulo_label = ctk.CTkLabel(frame, text="📘 Cadastro de Livros", font=('Arial', 22, 'bold'))
titulo_label.pack(pady=(20, 10))

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

btn_upload = ctk.CTkButton(frame, text="📤 Selecionar PDF", command=selecionar_pdf)
btn_upload.pack(pady=10)

label_pdf = ctk.CTkLabel(frame, text="Nenhum arquivo selecionado", font=("Arial", 12))
label_pdf.pack(pady=5)

botao_cadastrar = ctk.CTkButton(frame, text="Cadastrar Livro", command=cadastrar_livro)
botao_cadastrar.pack(pady=15)

resultado = ctk.CTkLabel(frame, text="", font=("Arial", 12, "italic"))
resultado.pack(pady=5)

app.mainloop()
