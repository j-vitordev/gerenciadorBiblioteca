import customtkinter as ctk
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv('credenciais.env')

class TelaHomeAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("📚 Biblioteca - Painel Admin")
        self.master.geometry("800x600")
        
        # Remove todos os widgets existentes
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Configurações de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.master, corner_radius=15)
        self.frame_principal.pack(fill="both", expand=True, padx=40, pady=40)
        
        self.carregar_interface()

    def carregar_interface(self):
        """Carrega a interface principal do admin"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Cabeçalho
        try:
            imagem = ctk.CTkImage(Image.open(os.getenv("LOGO_UNI")), size=(80, 80))
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

        # Botões principais
        botoes = [
            ("📚 Gerenciar Livros", self.gerenciar_livros),
            ("👥 Gerenciar Usuários", self.gerenciar_usuarios),
            ("📊 Relatórios", self.mostrar_relatorios),
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
        """Mostra uma tela secundária com opção de voltar"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Botão voltar
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

        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text=titulo,
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(0, 20))

        # Conteúdo personalizado se fornecido
        if conteudo:
            conteudo(self.frame_principal)

    def gerenciar_livros(self):
        self.mostrar_tela_secundaria("📚 Gerenciamento de Livros")

    def gerenciar_usuarios(self):
        self.mostrar_tela_secundaria("👥 Gerenciamento de Usuários")

    def mostrar_relatorios(self):
        self.mostrar_tela_secundaria("📊 Relatórios")

    def mostrar_configuracoes(self):
        self.mostrar_tela_secundaria("⚙️ Configurações")

    def sair(self):
        self.master.destroy()  # Fecha completamente a aplicação
        # Alternativa: Voltar para tela de login
        # from app import mostrar_tela_login
        # mostrar_tela_login(self.master)

if __name__ == "__main__":
    # Para testes isolados
    janela = ctk.CTk()
    TelaHomeAdmin(janela)
    janela.mainloop()