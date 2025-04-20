import customtkinter as ctk
from PIL import Image

# Configuração do tema
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

def mostrar_tela_login():
    # Limpar tela
    for widget in frame.winfo_children():
        widget.destroy()

    # Tela de Login
    imagem = ctk.CTkImage(Image.open("imagens/logoUnichristus.png"), size=(80, 80))
    logo = ctk.CTkLabel(master=frame, image=imagem, text="")
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

    # Botão de login
    botao_login = ctk.CTkButton(master=frame, text='Entrar na Biblioteca', command=lambda: validar_login(campo_usuario, campo_senha, resultado_login))
    botao_login.pack(pady=(10, 5))

    # Esqueceu a senha
    botao_esqueceu = ctk.CTkButton(master=frame, text='Esqueceu a senha?', fg_color='transparent', hover_color='#444', text_color='lightblue', command=mostrar_tela_recuperar_senha)
    botao_esqueceu.pack(pady=(0, 10))

    # Criar conta
    botao_cadastrar = ctk.CTkButton(master=frame, text="Criar conta", fg_color='transparent', hover_color='#444', text_color='lightblue', command=mostrar_tela_cadastro)
    botao_cadastrar.pack(pady=(0, 10))

    # Resultado
    global resultado_login
    resultado_login = ctk.CTkLabel(master=frame, text='', font=('Arial', 12, 'italic'))
    resultado_login.pack(pady=5)

def mostrar_tela_cadastro():
    # Limpar tela
    for widget in frame.winfo_children():
        widget.destroy()

    # Tela de Cadastro
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

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame, text="🔙 Voltar para o Login", fg_color='transparent', hover_color='#444', text_color='lightblue', command=mostrar_tela_login)
    botao_voltar.pack(pady=(0, 10))


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

    botao_cadastrar = ctk.CTkButton(frame, text="Cadastrar", command=cadastrar_usuario)
    botao_cadastrar.pack(pady=15)

    resultado = ctk.CTkLabel(frame, text="", font=("Arial", 12, "italic"))
    resultado.pack(pady=5)

def mostrar_tela_recuperar_senha():
    # Limpar tela
    for widget in frame.winfo_children():
        widget.destroy()

    # Tela de Recuperação de Senha
    titulo = ctk.CTkLabel(frame, text="🔐 Recuperar Senha", font=('Arial', 22, 'bold'))
    titulo.pack(pady=(20, 10))

    campo_email = ctk.CTkEntry(frame, placeholder_text="Digite seu e-mail")
    campo_email.pack(padx=20, pady=10, fill="x")

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame, text="🔙 Voltar para o Login", fg_color='transparent', hover_color='#444', text_color='lightblue', command=mostrar_tela_login)
    botao_voltar.pack(pady=(0, 10))


    def recuperar_senha():
        email = campo_email.get()
        if email:
            resultado.configure(text=f"📧 Enviamos instruções para {email}", text_color="green")
        else:
            resultado.configure(text="❗ Digite seu e-mail!", text_color="red")

    botao_enviar = ctk.CTkButton(frame, text="Enviar Instruções", command=recuperar_senha)
    botao_enviar.pack(pady=10)

    resultado = ctk.CTkLabel(frame, text="", font=("Arial", 12, "italic"))
    resultado.pack(pady=5)

def validar_login(campo_usuario, campo_senha, resultado_login):
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    if usuario == 'admin' and senha == 'admin':
        resultado_login.configure(text='Login feito com sucesso ✅', text_color='green')
    else:
        resultado_login.configure(text='Usuário ou senha incorretos ❌', text_color='red')

# Janela principal
app = ctk.CTk()
app.title('📚 Biblioteca - Acesso')
app.geometry('500x500')
app.resizable(True, True)

# Frame centralizado
frame = ctk.CTkFrame(master=app, corner_radius=15)
frame.pack(pady=40, padx=40, fill='both', expand=True)

# Chama a tela de login ao iniciar
mostrar_tela_login()

app.mainloop()
