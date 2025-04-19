import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def cadastrar_usuario():
    nome = campo_nome.get()
    email = campo_email.get()
    senha = campo_senha.get()
    confirmar = campo_confirmar_senha.get()

    if senha != confirmar:
        resultado.configure(text="❌ As senhas não coincidem!", text_color="red")
    elif nome and email and senha:
        resultado.configure(text="✅ Cadastro realizado com sucesso!", text_color="green")
    else:
        resultado.configure(text="⚠️ Preencha todos os campos.", text_color="yellow")

app = ctk.CTk()
app.title("📚 Biblioteca - Cadastro")
app.geometry("500x500")

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(pady=40, padx=40, fill="both", expand=True)

titulo = ctk.CTkLabel(frame, text="📝 Cadastro de Usuário", font=('Arial', 22, 'bold'))
titulo.pack(pady=(20, 10))

campo_nome = ctk.CTkEntry(frame, placeholder_text="Nome completo")
campo_nome.pack(padx=20, pady=5, fill="x")

campo_email = ctk.CTkEntry(frame, placeholder_text="E-mail")
campo_email.pack(padx=20, pady=5, fill="x")

campo_senha = ctk.CTkEntry(frame, placeholder_text="Senha", show="*")
campo_senha.pack(padx=20, pady=5, fill="x")

campo_confirmar_senha = ctk.CTkEntry(frame, placeholder_text="Confirmar senha", show="*")
campo_confirmar_senha.pack(padx=20, pady=5, fill="x")

botao_cadastrar = ctk.CTkButton(frame, text="Cadastrar", command=cadastrar_usuario)
botao_cadastrar.pack(pady=15)

resultado = ctk.CTkLabel(frame, text="", font=("Arial", 12, "italic"))
resultado.pack(pady=5)

app.mainloop()
