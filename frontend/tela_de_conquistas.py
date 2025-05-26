import customtkinter as ctk

class TelaConquistas:
    def __init__(self, container):
        self.container = container
        self.carregar_interface()

    def carregar_interface(self):
        """Carrega toda a interface de conquistas"""
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Título
        ctk.CTkLabel(
            self.container,
            text="🏆 Conquistas",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 20))

        # Sistema de níveis
        nivel_frame = ctk.CTkFrame(
            self.container,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        nivel_frame.pack(fill="x", pady=10)

        # Barra de progresso
        ctk.CTkLabel(
            nivel_frame,
            text="Nível 5 - Leitor Ávido",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))

        progresso = ctk.CTkProgressBar(
            nivel_frame,
            width=400,
            height=20,
            corner_radius=10,
            progress_color="#4CAF50"
        )
        progresso.pack(pady=5)
        progresso.set(0.75)  # 75% do nível

        ctk.CTkLabel(
            nivel_frame,
            text="75% completo - 15/20 livros lidos",
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 10))

        # Conquistas
        ctk.CTkLabel(
            self.container,
            text="📌 Suas Conquistas",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(20, 10))

        conquistas_frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )
        conquistas_frame.pack(fill="x")

        # Lista de conquistas
        conquistas = [
            {"emoji": "📚", "titulo": "Primeiros Passos", "descricao": "Leu seu primeiro livro", "desbloqueada": True},
            {"emoji": "🏆", "titulo": "Leitor Bronze", "descricao": "Leu 5 livros", "desbloqueada": True},
            {"emoji": "🔥", "titulo": "Leitor Prata", "descricao": "Leu 10 livros", "desbloqueada": False},
            {"emoji": "💎", "titulo": "Leitor Ouro", "descricao": "Leu 20 livros", "desbloqueada": False}
        ]

        for i, conquista in enumerate(conquistas):
            self.criar_card_conquista(conquistas_frame, conquista, i)

    def criar_card_conquista(self, frame, conquista, col):
        """Cria um card de conquista"""
        card = ctk.CTkFrame(
            frame,
            width=200,
            corner_radius=10,
            fg_color="#252525" if conquista["desbloqueada"] else "#1a1a1a",
            border_width=1,
            border_color="#333333"
        )
        card.grid(row=0, column=col, padx=10, pady=5)

        emoji = ctk.CTkLabel(
            card,
            text=conquista["emoji"],
            font=ctk.CTkFont(size=24)
        )
        emoji.pack(pady=(10, 5))

        ctk.CTkLabel(
            card,
            text=conquista["titulo"],
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack()

        ctk.CTkLabel(
            card,
            text=conquista["descricao"],
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa"
        ).pack(pady=5)

        if not conquista["desbloqueada"]:
            ctk.CTkLabel(
                card,
                text="🔒 Bloqueada",
                font=ctk.CTkFont(size=12),
                text_color="#ff5555"
            ).pack(pady=(0, 10))