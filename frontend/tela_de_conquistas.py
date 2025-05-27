import customtkinter as ctk
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv('credenciais.env')

class TelaConquistas:
    def __init__(self, container):
        self.container = container
        self.conquistas_data = {
            "Primeiros Passos": {
                "imagem_var": "LOGO_INICIANTE",
                "size": (70, 70),
                "descricao": "Leu seu primeiro livro",
                "desbloqueada": True
            },
            "Leitor Bronze": {
                "imagem_var": "LOGO_BRONZE", 
                "size": (70, 70),
                "descricao": "Leu 5 livros",
                "desbloqueada": True
            },
            "Leitor Prata": {
                "imagem_var": "LOGO_PRATA",
                "size": (70, 70),
                "descricao": "Leu 10 livros",
                "desbloqueada": False
            },
            "Leitor Ouro": {
                "imagem_var": "LOGO_OURO",
                "size": (70, 70),
                "descricao": "Leu 20 livros", 
                "desbloqueada": False
            }
        }
        self.carregar_interface()

    def carregar_interface(self):
        """Carrega toda a interface de conquistas"""
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Título centralizado
        ctk.CTkLabel(
            self.container,
            text="🏆 Minhas Conquistas",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(0, 20))

        # Frame principal para as conquistas
        main_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        # Grid 2x2 para as conquistas
        for i, (titulo, dados) in enumerate(self.conquistas_data.items()):
            row = i // 2
            col = i % 2
            self.criar_card_conquista(main_frame, titulo, dados, row, col)

    def criar_card_conquista(self, frame, titulo, dados, row, col):
        """Cria um card de conquista padronizado"""
        card = ctk.CTkFrame(
            frame,
            width=200,
            height=220,  # Altura fixa para todos os cards
            corner_radius=10,
            fg_color="#252525" if dados["desbloqueada"] else "#1a1a1a",
            border_width=1,
            border_color="#333333"
        )
        card.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")
        card.grid_propagate(False)  # Mantém o tamanho fixo
        card.grid_columnconfigure(0, weight=1)

        # Container interno para centralizar conteúdo
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Imagem da conquista (ou fallback)
        try:
            img_path = os.getenv(dados["imagem_var"])
            if img_path and os.path.exists(img_path):
                img = ctk.CTkImage(Image.open(img_path), size=dados["size"])
                ctk.CTkLabel(content_frame, image=img, text="").pack(pady=(0, 10))
            else:
                raise FileNotFoundError
        except:
            emoji = "🏆" if dados["desbloqueada"] else "🔒"
            ctk.CTkLabel(
                content_frame,
                text=emoji,
                font=ctk.CTkFont(size=24)
            ).pack(pady=(0, 10))

        # Título da conquista
        ctk.CTkLabel(
            content_frame,
            text=titulo,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack()

        # Descrição
        ctk.CTkLabel(
            content_frame,
            text=dados["descricao"],
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa"
        ).pack(pady=5)

        # Status (apenas para conquistas bloqueadas)
        if not dados["desbloqueada"]:
            ctk.CTkLabel(
                content_frame,
                text="Bloqueada",
                font=ctk.CTkFont(size=12),
                text_color="#ff5555"
            ).pack()