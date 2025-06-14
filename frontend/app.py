import customtkinter as ctk
from PIL import Image
import sys
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv('credenciais.env')

# Configuração de caminhos para imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

# Importações específicas
from backend.cadusuario import validar_usuario, cadastrar_usuario as cadastrar_no_banco

# Configuração de tema
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# Variável global para armazenar o ID do usuário logado
USUARIO_LOGADO_ID = None

# Janela principal
app = ctk.CTk()
app.title('📚 Biblioteca - Acesso')
app.geometry('500x500')
app.resizable(True, True)

# Frame principal
frame = ctk.CTkFrame(master=app, corner_radius=15)
frame.pack(pady=40, padx=40, fill='both', expand=True)

# ==============================================
# FUNÇÕES PRINCIPAIS
# ==============================================

def mostrar_tela_login(janela=None):
    """Exibe a tela de login com campos para email e senha"""
    global resultado_login
    
    janela = janela or app
    
    # Limpa o frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Logo da aplicação
    try:
        imagem = ctk.CTkImage(Image.open(os.getenv("LOGO_UNI")), size=(80, 80))
        logo = ctk.CTkLabel(master=frame, image=imagem, text="")
        logo.pack(pady=(10, 5))
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        logo = ctk.CTkLabel(master=frame, text="📚", font=("Arial", 30))
        logo.pack(pady=(10, 5))

    # Título
    titulo = ctk.CTkLabel(
        master=frame, 
        text='🔒 Acesso à Biblioteca', 
        font=('Arial', 22, 'bold')
    )
    titulo.pack(pady=(5, 10))

    # Campo de usuário (email)
    label_usuario = ctk.CTkLabel(
        master=frame, 
        text='Usuário (E-mail):', 
        anchor='w'
    )
    label_usuario.pack(padx=20, pady=(10, 0), fill='x')

    campo_usuario = ctk.CTkEntry(
        master=frame, 
        placeholder_text="Digite seu e-mail"
    )
    campo_usuario.pack(padx=20, pady=5, fill='x')

    # Campo de senha
    label_senha = ctk.CTkLabel(
        master=frame, 
        text='Senha:', 
        anchor='w'
    )
    label_senha.pack(padx=20, pady=(10, 0), fill='x')

    campo_senha = ctk.CTkEntry(
        master=frame, 
        placeholder_text="Digite sua senha", 
        show='*'
    )
    campo_senha.pack(padx=20, pady=5, fill='x')

    # Botão de login
    botao_login = ctk.CTkButton(
        master=frame, 
        text='Entrar na Biblioteca',
        command=lambda: validar_login(campo_usuario, campo_senha)
    )
    botao_login.pack(pady=(10, 5))

    # Links adicionais
    ctk.CTkButton(
        master=frame, 
        text='Esqueceu a senha?', 
        fg_color='transparent',
        hover_color='#444', 
        text_color='lightblue', 
        command=mostrar_tela_recuperar_senha
    ).pack(pady=(0, 10))

    ctk.CTkButton(
        master=frame, 
        text="Criar conta", 
        fg_color='transparent',
        hover_color='#444', 
        text_color='lightblue', 
        command=mostrar_tela_cadastro
    ).pack(pady=(0, 10))

    # Label para feedback
    resultado_login = ctk.CTkLabel(
        master=frame, 
        text='', 
        font=('Arial', 12, 'italic')
    )
    resultado_login.pack(pady=5)

def mostrar_tela_cadastro():
    """Exibe o formulário de cadastro de novo usuário"""
    global campo_nome, campo_email, campo_senha, campo_confirmar_senha, resultado
    
    # Limpa o frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Título
    ctk.CTkLabel(
        frame, 
        text="📝 Cadastro de Usuário", 
        font=('Arial', 22, 'bold')
    ).pack(pady=(20, 10))

    # Campos do formulário
    campo_nome = ctk.CTkEntry(
        frame, 
        placeholder_text="Nome completo"
    )
    campo_nome.pack(padx=20, pady=5, fill="x")

    campo_email = ctk.CTkEntry(
        frame, 
        placeholder_text="E-mail válido"
    )
    campo_email.pack(padx=20, pady=5, fill="x")

    campo_senha = ctk.CTkEntry(
        frame, 
        placeholder_text="Senha (mínimo 6 caracteres)", 
        show="*"
    )
    campo_senha.pack(padx=20, pady=5, fill="x")

    campo_confirmar_senha = ctk.CTkEntry(
        frame, 
        placeholder_text="Confirmar senha", 
        show="*"
    )
    campo_confirmar_senha.pack(padx=20, pady=5, fill="x")

    # Botão de cadastro
    ctk.CTkButton(
        frame, 
        text="Cadastrar", 
        command=cadastrar_usuario
    ).pack(pady=15)

    # Botão de voltar
    ctk.CTkButton(
        frame, 
        text="🔙 Voltar para o Login", 
        fg_color='transparent',
        hover_color='#444', 
        text_color='lightblue', 
        command=mostrar_tela_login
    ).pack(pady=(0, 10))

    # Label para feedback
    resultado = ctk.CTkLabel(
        frame, 
        text="", 
        font=("Arial", 12, "italic")
    )
    resultado.pack(pady=5)

def mostrar_tela_recuperar_senha():
    """Exibe a tela de recuperação de senha"""
    global resultado
    
    # Limpa o frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Título
    ctk.CTkLabel(
        frame, 
        text="🔐 Recuperar Senha", 
        font=('Arial', 22, 'bold')
    ).pack(pady=(20, 10))

    # Campo de e-mail
    campo_email = ctk.CTkEntry(
        frame, 
        placeholder_text="Digite seu e-mail cadastrado"
    )
    campo_email.pack(padx=20, pady=10, fill="x")

    # Função de recuperação
    def recuperar_senha():
        email = campo_email.get()
        if email:
            resultado.configure(
                text=f"📧 Enviamos instruções para {email}", 
                text_color="green"
            )
        else:
            resultado.configure(
                text="❗ Digite seu e-mail!", 
                text_color="red"
            )

    # Botão de envio
    ctk.CTkButton(
        frame, 
        text="Enviar Instruções", 
        command=recuperar_senha
    ).pack(pady=10)

    # Botão de voltar
    ctk.CTkButton(
        frame, 
        text="🔙 Voltar para o Login", 
        fg_color='transparent',
        hover_color='#444', 
        text_color='lightblue', 
        command=mostrar_tela_login
    ).pack(pady=(0, 10))

    # Label para feedback
    resultado = ctk.CTkLabel(
        frame, 
        text="", 
        font=("Arial", 12, "italic")
    )
    resultado.pack(pady=5)

def validar_login(campo_usuario, campo_senha):
    """Valida as credenciais do usuário"""
    global USUARIO_LOGADO_ID
    
    email = campo_usuario.get()
    senha = campo_senha.get()

    # Verifica no banco de dados
    resultado_validacao = validar_usuario(email, senha)

    if resultado_validacao["sucesso"]:
        # Armazena o ID do usuário logado
        USUARIO_LOGADO_ID = resultado_validacao["usuario_id"]
        
        resultado_login.configure(
            text='Login feito com sucesso ✅', 
            text_color='green'
        )
        
        # Redireciona conforme o tipo de usuário
        if resultado_validacao["admin"]:
            frame.after(500, lambda: abrir_tela_home_admin(USUARIO_LOGADO_ID))
        else:
            frame.after(500, lambda: abrir_tela_home(USUARIO_LOGADO_ID))
    else:
        resultado_login.configure(
            text='Usuário ou senha incorretos ❌', 
            text_color='red'
        )

def abrir_tela_home(usuario_id):
    """Abre a tela principal para usuários comuns"""
    # Limpa a janela
    for widget in app.winfo_children():
        widget.destroy()
    
    # Importa e exibe a tela home
    from tela_home import mostrar_tela_home
    mostrar_tela_home(app, USUARIO_LOGADO_ID)  # Passa o ID do usuário

def abrir_tela_home_admin(usuario_id):
    """Abre a tela principal para administradores"""
    # Limpa a janela
    for widget in app.winfo_children():
        widget.destroy()
    
    # Importa e exibe a tela admin
    from tela_home_adm import TelaHomeAdmin
    TelaHomeAdmin(app, usuario_id)  # Passa o ID do usuário

def cadastrar_usuario():
    """Processa o cadastro de novo usuário"""
    nome = campo_nome.get()
    email = campo_email.get()
    senha = campo_senha.get()
    confirmar = campo_confirmar_senha.get()

    # Validações
    if senha != confirmar:
        resultado.configure(
            text="❌ As senhas não coincidem!", 
            text_color="red"
        )
    elif len(senha) < 6:
        resultado.configure(
            text="❌ A senha deve ter pelo menos 6 caracteres!", 
            text_color="red"
        )
    elif nome and email and senha:
        # Tenta cadastrar no banco
        sucesso, mensagem = cadastrar_no_banco(nome, email, senha)
        
        if sucesso:
            resultado.configure(
                text=f"✅ {mensagem}", 
                text_color="green"
            )
            # Limpa os campos
            campo_nome.delete(0, "end")
            campo_email.delete(0, "end")
            campo_senha.delete(0, "end")
            campo_confirmar_senha.delete(0, "end")
        else:
            resultado.configure(
                text=f"❌ {mensagem}", 
                text_color="red"
            )
    else:
        resultado.configure(
            text="⚠️ Preencha todos os campos.", 
            text_color="yellow"
        )

# ==============================================
# INICIALIZAÇÃO
# ==============================================

# Exibe a tela de login ao iniciar
mostrar_tela_login()

# Inicia o loop principal
app.mainloop()