import customtkinter as ctk
from PIL import Image  # Para lidar com a imagem

# Configuração do tema
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    if usuario == 'admin' and senha == 'admin':
        resultado_login.configure(text='Login feito com sucesso ✅', text_color='green')
    else:
        resultado_login.configure(text='Usuário ou senha incorretos ❌', text_color='red')

def esqueceu_senha():
    ctk.CTkMessagebox(title="Recuperar senha", 
                      message="Entre em contato com o suporte da biblioteca para redefinir sua senha.",
                      icon="info")

# Janela principal
app = ctk.CTk()
app.title('📚 Biblioteca - Login')
app.geometry('500x500')
app.resizable(False, False)

# Frame centralizado
frame = ctk.CTkFrame(master=app, corner_radius=15)
frame.pack(pady=40, padx=40, fill='both', expand=True)

# Imagem da biblioteca
imagem = ctk.CTkImage(Image.open("imagens/logoUnichristus.png"), size=(80, 80))
logo = ctk.CTkLabel(master=frame, image=imagem, text="")
logo.pack(pady=(10, 5))

# Título
titulo = ctk.CTkLabel(master=frame, text='🔒 Acesso à Biblioteca', font=('Arial', 22, 'bold'))
titulo.pack(pady=(5, 10))

# Campos de login
label_usuario = ctk.CTkLabel(master=frame, text='Usuário:', anchor='w')
label_usuario.pack(padx=20, pady=(10, 0), fill='x')

campo_usuario = ctk.CTkEntry(master=frame, placeholder_text="Digite o seu usuário")
campo_usuario.pack(padx=20, pady=5, fill='x')

label_senha = ctk.CTkLabel(master=frame, text='Senha:', anchor='w')
label_senha.pack(padx=20, pady=(10, 0), fill='x')

campo_senha = ctk.CTkEntry(master=frame, placeholder_text="Digite sua senha", show='*')
campo_senha.pack(padx=20, pady=5, fill='x')

# Botão de login
botao_login = ctk.CTkButton(master=frame, text='Entrar na Biblioteca', command=validar_login)
botao_login.pack(pady=(10, 5))

# Esqueceu a senha
botao_esqueceu = ctk.CTkButton(master=frame, text='Esqueceu a senha?', fg_color='transparent', hover_color='#444', text_color='lightblue', command=esqueceu_senha)
botao_esqueceu.pack(pady=(0, 10))

# Resultado
resultado_login = ctk.CTkLabel(master=frame, text='', font=('Arial', 12, 'italic'))
resultado_login.pack(pady=5)

app.mainloop()
