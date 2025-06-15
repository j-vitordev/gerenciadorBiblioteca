import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import os
import threading
from dotenv import load_dotenv
from tela_biblioteca import TelaBiblioteca
from tela_de_conquistas import TelaConquistas
from tela_perfil import TelaPerfil
from backend.cadusuario import buscar_dados_usuario
from PIL import Image, ImageTk
import os
import tkinter as tk

load_dotenv('credenciais.env')

class TelaHome:
    def __init__(self, janela_principal, usuario_id):
        self.janela_principal = janela_principal
        self.usuario_id = usuario_id
        self.carregar_interface()

    def carregar_interface(self):
        for widget in self.janela_principal.winfo_children():
            widget.destroy()

        self.janela_principal.title("Biblioteca Digital")
        self.janela_principal.geometry("1100x650")

        ctk.set_appearance_mode("dark")

        self.frame_principal = ctk.CTkFrame(self.janela_principal, corner_radius=0, fg_color="#1e1e1e")
        self.frame_principal.pack(fill="both", expand=True)

        self.frame_menu = ctk.CTkFrame(self.frame_principal, width=250, corner_radius=0, fg_color="#252525")
        self.frame_menu.pack(side="left", fill="y")

        self.frame_conteudo = None
        self.container_conteudo = None
        self.banner_frame = None

        self.configurar_menu_lateral()
        self.mostrar_home()

    def configurar_menu_lateral(self):
        cabecalho_menu = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        cabecalho_menu.pack(pady=(20, 30), padx=10, fill="x")

        try:
            self.logo_img = ctk.CTkImage(Image.open(os.getenv("LOGO_UNI")), size=(50, 50))
            self.logo_label = ctk.CTkLabel(cabecalho_menu, image=self.logo_img, text="", cursor="hand2")
            self.logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            self.logo_label = ctk.CTkLabel(cabecalho_menu, text="📚", font=("Arial", 24), cursor="hand2")
            self.logo_label.pack(side="left", padx=(0, 10))

        self.logo_label.bind("<Button-1>", lambda e: self.recarregar_tela_completa())

        ctk.CTkLabel(
            cabecalho_menu,
            text="Biblioteca",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        opcoes_menu = [
            ("📚 Biblioteca", self.mostrar_biblioteca),
            ("🏆 Conquistas", self.mostrar_conquistas),
            ("👤 Perfil", self.mostrar_perfil),
            ("🚪 Sair", self.sair)
        ]

        for texto, comando in opcoes_menu:
            btn = ctk.CTkButton(
                self.frame_menu,
                text=texto,
                command=comando,
                fg_color="transparent",
                hover_color="#333333",
                anchor="w",
                font=ctk.CTkFont(size=15),
                height=45,
                corner_radius=5,
                border_spacing=15
            )
            btn.pack(fill="x", pady=2, padx=10)

        ctk.CTkFrame(self.frame_menu, height=2, fg_color="#333333").pack(pady=10, fill="x", padx=20)

        versao_label = ctk.CTkLabel(
            self.frame_menu,
            text="v1.0.0",
            text_color="#666666",
            font=ctk.CTkFont(size=10)
        )
        versao_label.pack(side="bottom", pady=10)

    def recarregar_tela_completa(self):
        self.carregar_interface()

    def mostrar_home(self):
        if self.frame_conteudo:
            self.frame_conteudo.destroy()

        self.frame_conteudo = ctk.CTkFrame(self.frame_principal, corner_radius=0, fg_color="#1e1e1e")
        self.frame_conteudo.pack(side="right", expand=True, fill="both")

        self.container_conteudo = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        self.container_conteudo.pack(fill="both", expand=True, padx=20, pady=20)

        dados_usuario = buscar_dados_usuario(self.usuario_id)
        nome_usuario = dados_usuario.get("nome", f"Usuário #{self.usuario_id}")

        self.banner_frame = ctk.CTkFrame(
            self.container_conteudo,
            height=150,
            fg_color="#2a2a2a",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        self.banner_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            self.banner_frame,
            text=f"Bem-vindo, {nome_usuario}",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
            padx=20
        ).pack(side="left", fill="y")

        ctk.CTkLabel(
            self.container_conteudo,
            text="Acesse o menu à esquerda para navegar pela plataforma.",
            font=ctk.CTkFont(size=16),
            text_color="#aaaaaa"
        ).pack(pady=(10, 0))

        # Frame para exibir animação do GIF
        gif_frame = ctk.CTkFrame(
            self.container_conteudo,
            height=300,
            fg_color="transparent"
        )
        gif_frame.pack(pady=20)

        self.label_gif = ctk.CTkLabel(gif_frame, text="")
        self.label_gif.pack()

        caminho_gif = os.path.join("imagens", "book.gif")

        def animar_gif():
            try:
                gif = Image.open(caminho_gif)
                frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
                frame_count = len(frames)
                i = 0
                while True:
                    self.label_gif.configure(image=frames[i])
                    i = (i + 1) % frame_count
                    self.label_gif.after(100)
                    self.label_gif.update_idletasks()
            except Exception as e:
                print(f"Erro ao carregar GIF: {e}")

        threading.Thread(target=animar_gif, daemon=True).start()

    def criar_card_interativo(self, frame, emoji, titulo, descricao, comando):
        card = ctk.CTkFrame(
            frame,
            width=200,
            height=150,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )

        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(content_frame, text=emoji, font=ctk.CTkFont(size=30)).pack(pady=(0, 5))
        ctk.CTkLabel(content_frame, text=titulo, font=ctk.CTkFont(size=16, weight="bold")).pack()
        ctk.CTkLabel(
            content_frame,
            text=descricao,
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
            wraplength=150
        ).pack(pady=5)

        original_color = "#252525"
        hover_color = "#333333"

        def on_enter(e):
            card.configure(fg_color=hover_color)

        def on_leave(e):
            card.configure(fg_color=original_color)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e: comando())
        card.configure(cursor="hand2")

        return card

    def mostrar_biblioteca(self):
        if self.frame_conteudo:
            self.frame_conteudo.destroy()

        self.frame_conteudo = ctk.CTkFrame(self.frame_principal, corner_radius=0, fg_color="#1e1e1e")
        self.frame_conteudo.pack(side="right", expand=True, fill="both")

        TelaBiblioteca(self.frame_conteudo, self.usuario_id)

    def mostrar_conquistas(self):
        if self.frame_conteudo:
            self.frame_conteudo.destroy()

        self.frame_conteudo = ctk.CTkFrame(self.frame_principal, corner_radius=0, fg_color="#1e1e1e")
        self.frame_conteudo.pack(side="right", expand=True, fill="both")

        TelaConquistas(self.frame_conteudo, self.usuario_id)

    def mostrar_perfil(self):
        if self.frame_conteudo:
            self.frame_conteudo.destroy()

        self.frame_conteudo = ctk.CTkFrame(self.frame_principal, corner_radius=0, fg_color="#1e1e1e")
        self.frame_conteudo.pack(side="right", expand=True, fill="both")

        TelaPerfil(self.frame_conteudo, self.usuario_id)

    def sair(self):
        for widget in self.janela_principal.winfo_children():
            widget.destroy()
        from app import mostrar_tela_login
        mostrar_tela_login(self.janela_principal)

def mostrar_tela_home(janela_principal, usuario_id):
    TelaHome(janela_principal, usuario_id)

if __name__ == "__main__":
    janela_teste = ctk.CTk()
    mostrar_tela_home(janela_teste, usuario_id=1)
    janela_teste.mainloop()
