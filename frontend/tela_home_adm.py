import customtkinter as ctk
from PIL import Image
import os
import sys
from dotenv import load_dotenv
from frontend.tela_de_conquistas_adm import TelaConquistas

# Define o caminho absoluto para o .env na pasta backend
caminho_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'credenciais.env'))
load_dotenv(dotenv_path=caminho_env)

class TelaHomeAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("📚 Biblioteca - Painel Admin")
        self.master.geometry("800x600")
        
        for widget in self.master.winfo_children():
            widget.destroy()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.frame_principal = ctk.CTkFrame(self.master, corner_radius=15)
        self.frame_principal.pack(fill="both", expand=True, padx=40, pady=40)
        
        self.carregar_interface()

    def carregar_interface(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        try:
            logo_path = os.getenv("LOGO_UNI")
            if not logo_path:
                raise ValueError("Variável LOGO_UNI não encontrada no .env")

            # Ajuste se o caminho for relativo: converte para absoluto
            logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', logo_path))

            imagem = ctk.CTkImage(Image.open(logo_path), size=(80, 80))
            logo = ctk.CTkLabel(master=self.frame_principal, image=imagem, text="")
            logo.pack(pady=(10, 5))
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            logo = ctk.CTkLabel(master=self.frame_principal, text="👑", font=("Arial", 30))
            logo.pack(pady=(10, 5))

        ctk.CTkLabel(
            self.frame_principal, 
            text="Painel do Administrador",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(5, 20))

        botoes = [
            ("📚 Gerenciar Livros", self.gerenciar_livros),
            ("👥 Gerenciar Usuários", self.gerenciar_usuarios),
            ("🏆 Conquistas", self.gerenciar_conquistas),
            ("⚙️ Configurações", self.mostrar_configuracoes),
            ("🚪 Sair", self.sair)
        ]

        for texto, comando in botoes:
            btn = ctk.CTkButton(
                self.frame_principal,
                text=texto,
                command=comando,
                font=ctk.CTkFont(size=16),
                height=50,
                width=250,
                corner_radius=10,
                fg_color="#2b2b2b",
                hover_color="#3a3a3a"
            )
            btn.pack(pady=10)

    def mostrar_tela_secundaria(self, titulo, conteudo=None):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        btn_voltar = ctk.CTkButton(
            self.frame_principal,
            text="🔙 Voltar",
            command=self.carregar_interface,
            font=ctk.CTkFont(size=14),
            width=100,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#2b2b2b"
        )
        btn_voltar.pack(pady=(10, 20), anchor="w", padx=20)

        ctk.CTkLabel(
            self.frame_principal,
            text=titulo,
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(0, 20))

        if conteudo:
            conteudo(self.frame_principal, self.carregar_interface)

    def gerenciar_livros(self):
        self.mostrar_tela_secundaria("📚 Gerenciamento de Livros")

    def gerenciar_usuarios(self):
        self.mostrar_tela_secundaria("👥 Gerenciamento de Usuários")

    def gerenciar_conquistas(self):
        self.mostrar_tela_secundaria("🏆 Conquistas", TelaConquistas)

    def mostrar_configuracoes(self):
        self.mostrar_tela_secundaria("⚙️ Configurações")

    def sair(self):
        self.master.destroy()

if __name__ == "__main__":
    janela = ctk.CTk()
    TelaHomeAdmin(janela)
    janela.mainloop()
