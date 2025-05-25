import customtkinter as ctk
from PIL import Image
import sys
import os
from dotenv import load_dotenv

load_dotenv('credenciais.env')

# Configuração de caminhos
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

# Importações
from backend.cadusuario import validar_usuario, cadastrar_usuario as cadastrar_no_banco

# Tema
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# Janela principal
app = ctk.CTk()
app.title('📚 Biblioteca - Acesso')
app.geometry('500x500')
app.resizable(True, True)

frame = ctk.CTkFrame(master=app, corner_radius=15)
frame.pack(pady=40, padx=40, fill='both', expand=True)

# Funções
def mostrar_tela_login(janela=None):
    janela = janela or app
    
    for widget in frame.winfo_children():
        widget.destroy()

    try:
        imagem = ctk.CTkImage(Image.open(os.getenv("LOGO_UNI")), size=(80, 80))
        logo = ctk.CTkLabel(master=frame, image=imagem, text="")
        logo.pack(pady=(10, 5))
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        logo = ctk.CTkLabel(master=frame, text="📚", font=("Arial", 30))
        logo.pack(pady=(10, 5))

    titulo = ctk.CTkLabel(master=frame, text='🔒 Acesso à Biblioteca', font=('Arial', 22, 'bold'))
    titulo.pack(pady=(5, 10))

    label_usuario = ctk.CTkLabel(master=frame, text='Usuário:', anchor='w')
    label_usuario.pack(padx=20, pady=(10, 0), fill='x')

    campo_usuario = ctk.CTkEntry(master=frame, placeholder_text="Digite o seu usuário")
    campo_usuario.pack(padx=20, pady=5, fill='x')

    label_senha = ctk.CTkLabel(master=frame, text='Senha:', anchor='w')
    label_senha.pack(padx=20, pady=(10, 0), fill='x')

    campo_senha = ctk.CTkEntry(master=frame, placeholder_text="Digite sua senha", show='*')
    campo_senha.pack(padx=20, pady=5, fill='x')

    botao_login = ctk.CTkButton(master=frame, text='Entrar na Biblioteca',
                               command=lambda: validar_login(campo_usuario, campo_senha))
    botao_login.pack(pady=(10, 5))

    ctk.CTkButton(master=frame, text='Esqueceu a senha?', fg_color='transparent',
                 hover_color='#444', text_color='lightblue', command=mostrar_tela_recuperar_senha).pack(pady=(0, 10))

    ctk.CTkButton(master=frame, text="Criar conta", fg_color='transparent',
                 hover_color='#444', text_color='lightblue', command=mostrar_tela_cadastro).pack(pady=(0, 10))

    global resultado_login
    resultado_login = ctk.CTkLabel(master=frame, text='', font=('Arial', 12, 'italic'))
    resultado_login.pack(pady=5)

def mostrar_tela_cadastro():
    for widget in frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame, text="📝 Cadastro de Usuário", font=('Arial', 22, 'bold')).pack(pady=(20, 10))

    global campo_nome, campo_email, campo_senha, campo_confirmar_senha

    campo_nome = ctk.CTkEntry(frame, placeholder_text="Nome completo")
    campo_nome.pack(padx=20, pady=5, fill="x")

    campo_email = ctk.CTkEntry(frame, placeholder_text="E-mail")
    campo_email.pack(padx=20, pady=5, fill="x")

    campo_senha = ctk.CTkEntry(frame, placeholder_text="Senha", show="*")
    campo_senha.pack(padx=20, pady=5, fill="x")

    campo_confirmar_senha = ctk.CTkEntry(frame, placeholder_text="Confirmar senha", show="*")
    campo_confirmar_senha.pack(padx=20, pady=5, fill="x")

    ctk.CTkButton(frame, text="Cadastrar", command=cadastrar_usuario).pack(pady=15)

    ctk.CTkButton(frame, text="🔙 Voltar para o Login", fg_color='transparent',
                 hover_color='#444', text_color='lightblue', command=mostrar_tela_login).pack(pady=(0, 10))

    global resultado
    resultado = ctk.CTkLabel(frame, text="", font=("Arial", 12, "italic"))
    resultado.pack(pady=5)

def mostrar_tela_recuperar_senha():
    for widget in frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame, text="🔐 Recuperar Senha", font=('Arial', 22, 'bold')).pack(pady=(20, 10))

    campo_email = ctk.CTkEntry(frame, placeholder_text="Digite seu e-mail")
    campo_email.pack(padx=20, pady=10, fill="x")

    def recuperar_senha():
        email = campo_email.get()
        if email:
            resultado.configure(text=f"📧 Enviamos instruções para {email}", text_color="green")
        else:
            resultado.configure(text="❗ Digite seu e-mail!", text_color="red")

    ctk.CTkButton(frame, text="Enviar Instruções", command=recuperar_senha).pack(pady=10)
    ctk.CTkButton(frame, text="🔙 Voltar para o Login", fg_color='transparent',
                 hover_color='#444', text_color='lightblue', command=mostrar_tela_login).pack(pady=(0, 10))

    global resultado
    resultado = ctk.CTkLabel(frame, text="", font=("Arial", 12, "italic"))
    resultado.pack(pady=5)

def validar_login(campo_usuario, campo_senha):
    email = campo_usuario.get()
    senha = campo_senha.get()

    resultado_validacao = validar_usuario(email, senha)

    if resultado_validacao["sucesso"]:
        resultado_login.configure(text='Login feito com sucesso ✅', text_color='green')
        if resultado_validacao["admin"]:
            frame.after(500, abrir_tela_home_admin)
        else:
            frame.after(500, abrir_tela_home)
    else:
        resultado_login.configure(text='Usuário ou senha incorretos ❌', text_color='red')

def abrir_tela_home():
    for widget in app.winfo_children():
        widget.destroy()
    from tela_home import mostrar_tela_home
    mostrar_tela_home(app)

def abrir_tela_home_admin():
    for widget in app.winfo_children():
        widget.destroy()
    from tela_home_adm import TelaHomeAdmin
    TelaHomeAdmin(app)  # Passa a janela principal como parâmetro

def cadastrar_usuario():
    nome = campo_nome.get()
    email = campo_email.get()
    senha = campo_senha.get()
    confirmar = campo_confirmar_senha.get()

    if senha != confirmar:
        resultado.configure(text="❌ As senhas não coincidem!", text_color="red")
    elif nome and email and senha:
        sucesso, mensagem = cadastrar_no_banco(nome, email, senha)
        if sucesso:
            resultado.configure(text=f"✅ {mensagem}", text_color="green")
            campo_nome.delete(0, "end")
            campo_email.delete(0, "end")
            campo_senha.delete(0, "end")
            campo_confirmar_senha.delete(0, "end")
        else:
            resultado.configure(text=f"❌ {mensagem}", text_color="red")
    else:
        resultado.configure(text="⚠️ Preencha todos os campos.", text_color="yellow")

mostrar_tela_login()
app.mainloop()