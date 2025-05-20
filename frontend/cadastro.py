# frontend/cadastro_usuario.py

import customtkinter as ctk
import sys
import os

# Garante que o backend seja importado corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from backend.cadusuario import cadastrar_usuario as cadastrar_backend

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
        sucesso = cadastrar_backend(nome, email, senha)
        if sucesso:
            resultado.configure(text="✅ Cadastro realizado com sucesso!", text_color="green")
            limpar_campos()
        else:
            resultado.configure(text="❌ Erro ao cadastrar. Verifique se o e-mail já foi usado.", text_color="red")
    else:
        resultado.configure(text="⚠️ Preencha todos os campos.", text_color="yellow")

def limpar_campos():
    campo_nome.delete(0, "end")
    campo_email.delete(0, "end")
    campo_senha.delete(0, "end")
    campo_confirmar_senha.delete(0, "end")

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
