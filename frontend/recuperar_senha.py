import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def recuperar_senha():
    email = campo_email.get()
    if email:
        resultado.configure(text=f"📧 Enviamos instruções para {email}", text_color="green")
    else:
        resultado.configure(text="❗ Digite seu e-mail!", text_color="red")

app = ctk.CTk()
app.title("🔑 Recuperação de Senha")
app.geometry("500x300")

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(pady=60, padx=40, fill="both", expand=True)

titulo = ctk.CTkLabel(frame, text="🔐 Recuperar Senha", font=('Arial', 22, 'bold'))
titulo.pack(pady=(20, 10))

campo_email = ctk.CTkEntry(frame, placeholder_text="Digite seu e-mail")
campo_email.pack(padx=20, pady=10, fill="x")

botao_enviar = ctk.CTkButton(frame, text="Enviar Instruções", command=recuperar_senha)
botao_enviar.pack(pady=10)

resultado = ctk.CTkLabel(frame, text="", font=("Arial", 12, "italic"))
resultado.pack(pady=5)

app.mainloop()
