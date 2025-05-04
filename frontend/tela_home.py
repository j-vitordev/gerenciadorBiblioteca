import customtkinter as ctk
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv('credenciais.env')

class TelaHome:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.carregar_interface()

    def carregar_interface(self):
        """Carrega toda a interface do zero"""
        # Limpa a janela principal completamente
        for widget in self.janela_principal.winfo_children():
            widget.destroy()

        # Configurações da janela
        self.janela_principal.title("Biblioteca Digital")
        self.janela_principal.geometry("1100x650")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.janela_principal, corner_radius=0, fg_color="#1e1e1e")
        self.frame_principal.pack(fill="both", expand=True)

        # Frame do menu lateral
        self.frame_menu = ctk.CTkFrame(
            self.frame_principal, 
            width=250, 
            corner_radius=0,
            fg_color="#252525"
        )
        self.frame_menu.pack(side="left", fill="y")

        # Frame do conteúdo principal (será recriado quando necessário)
        self.frame_conteudo = None
        self.container_conteudo = None
        self.banner_frame = None

        # Configura o menu lateral
        self.configurar_menu_lateral()

        # Carrega a tela inicial
        self.mostrar_home()

    def configurar_menu_lateral(self):
        """Configura o menu lateral uma única vez"""
        # Cabeçalho do menu com logo
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
        
        # Configura o clique na logo para recarregar toda a interface
        self.logo_label.bind("<Button-1>", lambda e: self.recarregar_tela_completa())

        ctk.CTkLabel(
            cabecalho_menu, 
            text="Biblioteca", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        # Itens do menu
        opcoes_menu = [
            ("📖 Leituras", self.mostrar_leitura),
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
        # Destroi o frame de conteúdo se existir
        if self.frame_conteudo:
            self.frame_conteudo.destroy()
        
        # Cria novo frame de conteúdo
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
        
        ctk.CTkLabel(
            self.banner_frame,
            text="Bem-vindo à Biblioteca Digital",
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
        """Cria um card clicável estável"""
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

    def mostrar_tela_generica(self, titulo, conteudo):
        """Método genérico para mostrar conteúdo de uma tela"""
        # Destroi o frame de conteúdo se existir
        if self.frame_conteudo:
            self.frame_conteudo.destroy()
        
        # Cria novo frame de conteúdo
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
        
        ctk.CTkLabel(
            self.banner_frame,
            text=titulo,
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
            padx=20
        ).pack(side="left", fill="y")
        
        # Adiciona o conteúdo específico
        ctk.CTkLabel(
            self.container_conteudo,
            text=conteudo,
            font=ctk.CTkFont(size=16)
        ).pack(pady=50)

    def mostrar_leitura(self):
        self.mostrar_tela_generica("📖 Leituras", "Conteúdo da tela de Leituras")

    def mostrar_biblioteca(self):
        self.mostrar_tela_generica("📚 Biblioteca", "Conteúdo da tela de Biblioteca")

    def mostrar_conquistas(self):
        self.mostrar_tela_generica("🏆 Conquistas", "Conteúdo da tela de Conquistas")

    def mostrar_perfil(self):
        self.mostrar_tela_generica("👤 Perfil", "Conteúdo da tela de Perfil")

    def sair(self):
        for widget in self.janela_principal.winfo_children():
            widget.destroy()
        from app import mostrar_tela_login
        mostrar_tela_login(self.janela_principal)

def mostrar_tela_home(janela_principal):
    TelaHome(janela_principal)