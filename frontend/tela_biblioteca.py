import customtkinter as ctk

class TelaBiblioteca:
    def __init__(self, container):
        self.container = container
        self.carregar_interface()

    def carregar_interface(self):
        """Carrega toda a interface da biblioteca"""
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Título e barra de busca
        top_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            top_frame,
            text="📚 Biblioteca",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        busca_entry = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar livros...",
            width=200
        )
        busca_entry.pack(side="right")

        # Filtros
        filtros_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            filtros_frame,
            text="Filtrar por:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0, 10))

        filtros = ["Todos", "Lidos", "Lendo", "Quero ler"]
        for i, filtro in enumerate(filtros):
            btn = ctk.CTkButton(
                filtros_frame,
                text=filtro,
                width=80,
                fg_color="#252525",
                hover_color="#333333"
            )
            btn.pack(side="left", padx=5)

        # Grid de livros
        livros_frame = ctk.CTkScrollableFrame(
            self.container,
            fg_color="transparent"
        )
        livros_frame.pack(fill="both", expand=True)

        # Exemplo de livros (seriam buscados do banco de dados)
        livros = [
            {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "lido": True},
            {"titulo": "1984", "autor": "George Orwell", "lido": False},
            {"titulo": "Clean Code", "autor": "Robert Martin", "lido": True},
            {"titulo": "O Hobbit", "autor": "J.R.R. Tolkien", "lido": False}
        ]

        for i, livro in enumerate(livros):
            self.criar_card_livro(livros_frame, livro, i)

    def criar_card_livro(self, frame, livro, row):
        """Cria um card para um livro"""
        card = ctk.CTkFrame(
            frame,
            width=200,
            height=100,
            corner_radius=10,
            fg_color="#252525",
            border_width=1,
            border_color="#333333"
        )
        card.grid(row=row//3, column=row%3, padx=10, pady=10, sticky="nsew")
        frame.grid_columnconfigure(row%3, weight=1)

        # Conteúdo do card
        ctk.CTkLabel(
            card,
            text=livro["titulo"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            card,
            text=livro["autor"],
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
            anchor="w"
        ).pack(fill="x", padx=10)

        status = ctk.CTkLabel(
            card,
            text="✅ Lido" if livro["lido"] else "📖 Lendo",
            font=ctk.CTkFont(size=12),
            text_color="#4CAF50" if livro["lido"] else "#FF9800"
        )
        status.pack(pady=5)