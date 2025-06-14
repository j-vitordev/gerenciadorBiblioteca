import customtkinter as ctk
from PIL import Image
import os
from dotenv import load_dotenv
from tela_biblioteca import TelaBiblioteca
from tela_de_conquistas import TelaConquistas
from tela_perfil import TelaPerfil

load_dotenv('credenciais.env')

class TelaHome:
    def __init__(self, janela_principal, usuario_id):
        """
        Inicializa a tela principal
        
        Args:
            janela_principal: A janela root da aplicação
            usuario_id: ID do usuário logado (obtido no login)
        """
        self.janela_principal = janela_principal
        self.usuario_id = usuario_id  # Armazena o ID do usuário
        self.carregar_interface()

    def carregar_interface(self):
        """carrega toda a interface do zero"""
        # limpa a janela principal completamente
        for widget in self.janela_principal.winfo_children():
            widget.destroy()

        # configurações da janela
        self.janela_principal.title("Biblioteca Digital")
        self.janela_principal.geometry("1100x650")
        
        # configuração do tema
        ctk.set_appearance_mode("dark")
        
        # frame principal
        self.frame_principal = ctk.CTkFrame(self.janela_principal, corner_radius=0, fg_color="#1e1e1e")
        self.frame_principal.pack(fill="both", expand=True)

        # frame do menu lateral
        self.frame_menu = ctk.CTkFrame(
            self.frame_principal, 
            width=250, 
            corner_radius=0,
            fg_color="#252525"
        )
        self.frame_menu.pack(side="left", fill="y")

        # frame do conteúdo principal
        self.frame_conteudo = None
        self.container_conteudo = None
        self.banner_frame = None

        # configura o menu lateral
        self.configurar_menu_lateral()

        # carrega a tela inicial
        self.mostrar_home()

    def configurar_menu_lateral(self):
        """configura o menu lateral uma única vez"""
        # cabeçalho do menu com logo
        cabecalho_menu = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        cabecalho_menu.pack(pady=(20, 30), padx=10, fill="x")
        
        try:
            self.logo_img = ctk.CTkImage(Image.open(os.getenv("LOGO_UNI")), size=(50, 50))
            self.logo_label = ctk.CTkLabel(
                cabecalho_menu, 
                image=self.logo_img, 
                text="",
                cursor="hand2"
            )
            self.logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            self.logo_label = ctk.CTkLabel(
                cabecalho_menu, 
                text="📚", 
                font=("Arial", 24),
                cursor="hand2"
            )
            self.logo_label.pack(side="left", padx=(0, 10))
        
        # configura o clique na logo
        self.logo_label.bind("<Button-1>", lambda e: self.recarregar_tela_completa())

        ctk.CTkLabel(
            cabecalho_menu, 
            text="Biblioteca", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        # itens do menu
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

        # Separador
        ctk.CTkFrame(self.frame_menu, height=2, fg_color="#333333").pack(pady=10, fill="x", padx=20)

        # Rodapé do menu
        versao_label = ctk.CTkLabel(
            self.frame_menu, 
            text="v1.0.0", 
            text_color="#666666",
            font=ctk.CTkFont(size=10)
        )
        versao_label.pack(side="bottom", pady=10)

    def recarregar_tela_completa(self):
        """Recarrega toda a interface do zero"""
        self.carregar_interface()

    def mostrar_home(self):
        """Mostra a tela inicial"""
        if self.frame_conteudo:
            self.frame_conteudo.destroy()
        
        self.frame_conteudo = ctk.CTkFrame(
            self.frame_principal, 
            corner_radius=0,
            fg_color="#1e1e1e"
        )
        self.frame_conteudo.pack(side="right", expand=True, fill="both")

        # Container principal com scroll
        self.container_conteudo = ctk.CTkScrollableFrame(self.frame_conteudo, fg_color="transparent")
        self.container_conteudo.pack(fill="both", expand=True, padx=20, pady=20)

        # Banner superior
        self.banner_frame = ctk.CTkFrame(
            self.container_conteudo, 
            height=150, 
            fg_color="#2a2a2a",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        self.banner_frame.pack(fill="x", pady=(0, 20))
        
        # Mensagem personalizada com o ID do usuário
        ctk.CTkLabel(
            self.banner_frame,
            text=f"Bem-vindo, usuário #{self.usuario_id}",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
            padx=20
        ).pack(side="left", fill="y")

        # Frame para os cards
        cards_frame = ctk.CTkFrame(self.container_conteudo, fg_color="transparent")
        cards_frame.pack(fill="x")

        # Cards de funcionalidades
        card_data = [
            ("📚", "Sua Biblioteca", "Acesse seus livros e materiais", self.mostrar_biblioteca),
            ("🔍", "Busca Avançada", "Encontre exatamente o que precisa", lambda: print("Busca avançada clicada")),
            ("🎯", "Metas", "Acompanhe seu progresso", lambda: print("Metas clicadas")),
            ("📊", "Estatísticas", "Veja seus hábitos de leitura", lambda: print("Estatísticas clicadas"))
        ]

        for i, (emoji, titulo, descricao, comando) in enumerate(card_data):
            card = self.criar_card_interativo(cards_frame, emoji, titulo, descricao, comando)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            cards_frame.grid_columnconfigure(i, weight=1)

        # Seção de atividades recentes
        ctk.CTkLabel(
            self.container_conteudo,
            text="Atividades Recentes",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(20, 10))

        atividades_frame = ctk.CTkFrame(
            self.container_conteudo,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        atividades_frame.pack(fill="x", pady=(0, 20))

        atividades = [
            ("Você terminou 'Introdução ao Python'", "2 dias atrás"),
            ("Novo livro adicionado à sua lista", "3 dias atrás"),
            ("Conquista desbloqueada: Leitor Ávido", "1 semana atrás")
        ]

        for texto, tempo in atividades:
            item = ctk.CTkFrame(atividades_frame, fg_color="transparent")
            item.pack(fill="x", padx=10, pady=8)
            
            ctk.CTkLabel(
                item,
                text="•",
                font=ctk.CTkFont(size=14),
                padx=5
            ).pack(side="left")
            
            ctk.CTkLabel(
                item,
                text=texto,
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(
                item,
                text=tempo,
                font=ctk.CTkFont(size=12),
                text_color="#666666"
            ).pack(side="right")

    def criar_card_interativo(self, frame, emoji, titulo, descricao, comando):
        """Cria um card clicável"""
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
        
        ctk.CTkLabel(
            content_frame,
            text=emoji,
            font=ctk.CTkFont(size=30)
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            content_frame,
            text=titulo,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack()
        
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
        """Mostra a tela da biblioteca"""
        if self.frame_conteudo:
            self.frame_conteudo.destroy()
        
        self.frame_conteudo = ctk.CTkFrame(
            self.frame_principal, 
            corner_radius=0,
            fg_color="#1e1e1e"
        )
        self.frame_conteudo.pack(side="right", expand=True, fill="both")
        
        # Passa o usuario_id para a TelaBiblioteca
        TelaBiblioteca(self.frame_conteudo, self.usuario_id)

    def mostrar_conquistas(self):
        """Mostra a tela de conquistas"""
        if self.frame_conteudo:
            self.frame_conteudo.destroy()
        
        self.frame_conteudo = ctk.CTkFrame(
            self.frame_principal, 
            corner_radius=0,
            fg_color="#1e1e1e"
        )
        self.frame_conteudo.pack(side="right", expand=True, fill="both")
        
        # Passa o usuario_id para a TelaConquistas
        TelaConquistas(self.frame_conteudo, self.usuario_id)

    def mostrar_perfil(self):
        """Mostra a tela de perfil"""
        if self.frame_conteudo:
            self.frame_conteudo.destroy()
        
        self.frame_conteudo = ctk.CTkFrame(
            self.frame_principal, 
            corner_radius=0,
            fg_color="#1e1e1e"
        )
        self.frame_conteudo.pack(side="right", expand=True, fill="both")
        
        # Passa o usuario_id para a TelaPerfil
        TelaPerfil(self.frame_conteudo, self.usuario_id)

    def sair(self):
        """Volta para a tela de login"""
        for widget in self.janela_principal.winfo_children():
            widget.destroy()
        from app import mostrar_tela_login
        mostrar_tela_login(self.janela_principal)

def mostrar_tela_home(janela_principal, usuario_id):
    """
    Função de inicialização da tela home
    
    Args:
        janela_principal: Janela root da aplicação
        usuario_id: ID do usuário logado
    """
    TelaHome(janela_principal, usuario_id)

if __name__ == "__main__":
    # Para testes locais
    janela_teste = ctk.CTk()
    mostrar_tela_home(janela_teste, usuario_id=1)  # ID de teste
    janela_teste.mainloop()