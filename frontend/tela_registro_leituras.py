import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime
from tkinter import filedialog

class TelaRegistroLeituras:
    def __init__(self, container):
        self.container = container
        self.livros_exemplo = [
            {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "capa": "capa1.jpg"},
            {"titulo": "1984", "autor": "George Orwell", "capa": "capa2.jpg"},
            {"titulo": "Clean Code", "autor": "Robert Martin", "capa": "capa3.jpg"},
            {"titulo": "O Hobbit", "autor": "J.R.R. Tolkien", "capa": "capa4.jpg"},
            {"titulo": "Orgulho e Preconceito", "autor": "Jane Austen", "capa": "capa5.jpg"},
        ]
        self.carregar_interface()

    def carregar_interface(self):
        """Carrega a interface aprimorada de registro de leituras"""
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Container principal com scroll
        self.scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título com ícone
        titulo_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            titulo_frame,
            text="📖 ",
            font=ctk.CTkFont(size=28)
        ).pack(side="left")

        ctk.CTkLabel(
            titulo_frame,
            text="Registro de Leitura",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(side="left", padx=10)

        # Seção de busca e seleção de livro
        self.criar_secao_busca_livro()

        # Seção de detalhes da leitura
        self.criar_secao_detalhes_leitura()

        # Seção de avaliação
        self.criar_secao_avaliacao()

        # Seção de anotações
        self.criar_secao_anotacoes()

        # Botão de registro
        self.criar_botao_registro()

        # Seção de histórico
        self.criar_secao_historico()

    def criar_secao_busca_livro(self):
        """Cria a seção de busca e seleção de livro"""
        livro_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        livro_frame.pack(fill="x", pady=(0, 20))

        # Barra de busca
        busca_frame = ctk.CTkFrame(livro_frame, fg_color="transparent")
        busca_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            busca_frame,
            text="Buscar livro:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0, 10))

        self.busca_entry = ctk.CTkEntry(
            busca_frame,
            placeholder_text="Digite o título ou autor...",
            width=300
        )
        self.busca_entry.pack(side="left")
        self.busca_entry.bind("<KeyRelease>", self.filtrar_livros)

        # Grid de livros sugeridos
        self.livros_frame = ctk.CTkFrame(livro_frame, fg_color="transparent")
        self.livros_frame.pack(fill="x", pady=10)

        self.carregar_grid_livros(self.livros_exemplo)

    def carregar_grid_livros(self, livros):
        """Carrega o grid de livros com capas"""
        for widget in self.livros_frame.winfo_children():
            widget.destroy()

        for i, livro in enumerate(livros):
            livro_card = ctk.CTkFrame(
                self.livros_frame,
                width=120,
                height=180,
                corner_radius=10,
                fg_color="#252525",
                border_width=1,
                border_color="#333333"
            )
            livro_card.grid(row=i//4, column=i%4, padx=10, pady=10)
            livro_card.grid_propagate(False)

            # Simulação de capa do livro (na prática, carregaria uma imagem)
            capa = ctk.CTkLabel(
                livro_card,
                text="📚",
                font=ctk.CTkFont(size=40),
                width=100,
                height=120,
                corner_radius=5,
                fg_color="#1a1a1a"
            )
            capa.pack(pady=5)

            ctk.CTkLabel(
                livro_card,
                text=livro["titulo"][:15] + ("..." if len(livro["titulo"]) > 15 else ""),
                font=ctk.CTkFont(size=12),
                wraplength=100
            ).pack()

            livro_card.bind("<Button-1>", lambda e, l=livro: self.selecionar_livro(l))
            livro_card.configure(cursor="hand2")

    def filtrar_livros(self, event):
        """Filtra os livros conforme texto digitado"""
        termo = self.busca_entry.get().lower()
        if termo:
            livros_filtrados = [l for l in self.livros_exemplo 
                             if termo in l["titulo"].lower() or termo in l["autor"].lower()]
            self.carregar_grid_livros(livros_filtrados)
        else:
            self.carregar_grid_livros(self.livros_exemplo)

    def selecionar_livro(self, livro):
        """Preenche os campos quando um livro é selecionado"""
        self.livro_selecionado = livro
        self.titulo_livro_var.set(livro["titulo"])
        self.autor_livro_var.set(livro["autor"])
        
        # Atualiza a exibição do livro selecionado
        for widget in self.livro_selecionado_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.livro_selecionado_frame,
            text="📚 " + livro["titulo"],
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")

    def criar_secao_detalhes_leitura(self):
        """Cria a seção de detalhes da leitura"""
        detalhes_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        detalhes_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            detalhes_frame,
            text="📅 Detalhes da Leitura",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        # Livro selecionado
        self.livro_selecionado_frame = ctk.CTkFrame(detalhes_frame, fg_color="transparent")
        self.livro_selecionado_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.titulo_livro_var = ctk.StringVar()
        self.autor_livro_var = ctk.StringVar()

        ctk.CTkLabel(
            detalhes_frame,
            text="Título:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=(5, 0))

        ctk.CTkEntry(
            detalhes_frame,
            textvariable=self.titulo_livro_var,
            font=ctk.CTkFont(size=14),
            state="readonly",
            width=400
        ).pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(
            detalhes_frame,
            text="Autor:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=(5, 0))

        ctk.CTkEntry(
            detalhes_frame,
            textvariable=self.autor_livro_var,
            font=ctk.CTkFont(size=14),
            state="readonly",
            width=400
        ).pack(fill="x", padx=15, pady=(0, 10))

        # Status e datas
        status_frame = ctk.CTkFrame(detalhes_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            status_frame,
            text="Status:",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, sticky="w")

        self.status_var = ctk.StringVar(value="completo")
        status_opcoes = [
            ("Lido completamente", "completo"),
            ("Lendo atualmente", "lendo"),
            ("Abandonado", "abandonado"),
            ("Planejo ler", "planejado")
        ]

        for i, (text, val) in enumerate(status_opcoes):
            ctk.CTkRadioButton(
                status_frame,
                text=text,
                variable=self.status_var,
                value=val,
                font=ctk.CTkFont(size=13)
            ).grid(row=0, column=i+1, padx=5, sticky="w")

        # Datas
        datas_frame = ctk.CTkFrame(detalhes_frame, fg_color="transparent")
        datas_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(
            datas_frame,
            text="Início:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0, 20))

        self.data_inicio_entry = ctk.CTkEntry(
            datas_frame,
            placeholder_text="DD/MM/AAAA",
            width=120
        )
        self.data_inicio_entry.pack(side="left")
        self.data_inicio_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ctk.CTkLabel(
            datas_frame,
            text="Término:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(20, 5))

        self.data_fim_entry = ctk.CTkEntry(
            datas_frame,
            placeholder_text="DD/MM/AAAA",
            width=120
        )
        self.data_fim_entry.pack(side="left")

    def criar_secao_avaliacao(self):
        """Cria a seção de avaliação do livro"""
        avaliacao_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        avaliacao_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            avaliacao_frame,
            text="⭐ Avaliação",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        # Rating com estrelas interativas
        stars_frame = ctk.CTkFrame(avaliacao_frame, fg_color="transparent")
        stars_frame.pack(pady=(0, 15))

        self.rating_var = ctk.IntVar(value=3)
        
        for i in range(1, 6):
            star = ctk.CTkLabel(
                stars_frame,
                text="★" if i <= self.rating_var.get() else "☆",
                font=ctk.CTkFont(size=28),
                text_color="#FFD700" if i <= self.rating_var.get() else "#666666",
                cursor="hand2"
            )
            star.pack(side="left", padx=2)
            star.bind("<Button-1>", lambda e, val=i: self.atualizar_estrelas(val))

        # Comentário rápido
        ctk.CTkLabel(
            avaliacao_frame,
            text="Tags:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=(10, 5))

        tags_frame = ctk.CTkFrame(avaliacao_frame, fg_color="transparent")
        tags_frame.pack(fill="x", padx=15, pady=(0, 15))

        tags = ["Incrível", "Emocionante", "Desafiador", "Inspirador", "Longo"]
        self.tags_selecionadas = []

        for tag in tags:
            btn = ctk.CTkButton(
                tags_frame,
                text=tag,
                width=80,
                height=25,
                font=ctk.CTkFont(size=12),
                fg_color="#333333",
                hover_color="#444444",
                command=lambda t=tag: self.toggle_tag(t)
            )
            btn.pack(side="left", padx=5, pady=2)

    def atualizar_estrelas(self, valor):
        """Atualiza as estrelas de avaliação"""
        self.rating_var.set(valor)
        for i, star in enumerate(self.rating_frame.winfo_children()):
            star.configure(
                text="★" if i < valor else "☆",
                text_color="#FFD700" if i < valor else "#666666"
            )

    def toggle_tag(self, tag):
        """Alterna seleção de tags"""
        if tag in self.tags_selecionadas:
            self.tags_selecionadas.remove(tag)
        else:
            self.tags_selecionadas.append(tag)
        print(f"Tags selecionadas: {self.tags_selecionadas}")

    def criar_secao_anotacoes(self):
        """Cria a seção de anotações pessoais"""
        anotacoes_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        anotacoes_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            anotacoes_frame,
            text="📝 Anotações Pessoais",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        self.anotacoes_text = ctk.CTkTextbox(
            anotacoes_frame,
            height=150,
            font=ctk.CTkFont(size=14),
            wrap="word",
            border_width=1,
            border_color="#444444"
        )
        self.anotacoes_text.pack(fill="x", padx=15, pady=(0, 15))

        # Anexar arquivo
        anexo_frame = ctk.CTkFrame(anotacoes_frame, fg_color="transparent")
        anexo_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(
            anexo_frame,
            text="Anexar Arquivo",
            width=120,
            height=30,
            font=ctk.CTkFont(size=12),
            command=self.anexar_arquivo
        ).pack(side="left")

        self.anexo_label = ctk.CTkLabel(
            anexo_frame,
            text="Nenhum arquivo anexado",
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa"
        )
        self.anexo_label.pack(side="left", padx=10)

    def anexar_arquivo(self):
        """Abre diálogo para anexar arquivo"""
        filepath = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Todos os arquivos", "*.*"), ("Imagens", "*.jpg *.png"), ("PDFs", "*.pdf")]
        )
        if filepath:
            filename = os.path.basename(filepath)
            self.anexo_label.configure(text=filename)
            self.arquivo_anexado = filepath

    def criar_botao_registro(self):
        """Cria o botão de registro"""
        btn_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkButton(
            btn_frame,
            text="Registrar Leitura",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=200,
            fg_color="#2b7de9",
            hover_color="#1a5fb4",
            command=self.registrar_leitura
        ).pack()

    def criar_secao_historico(self):
        """Cria a seção de histórico de leituras"""
        historico_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        historico_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            historico_frame,
            text="📚 Histórico de Leituras",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(fill="x")

        # Filtros do histórico
        filtros_frame = ctk.CTkFrame(historico_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(10, 15))

        ctk.CTkLabel(
            filtros_frame,
            text="Filtrar por:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0, 10))

        filtros = ["Todos", "Lidos", "Lendo", "Abandonados"]
        for filtro in filtros:
            btn = ctk.CTkButton(
                filtros_frame,
                text=filtro,
                width=80,
                height=25,
                font=ctk.CTkFont(size=12),
                fg_color="#333333",
                hover_color="#444444"
            )
            btn.pack(side="left", padx=5)

        # Lista de leituras registradas
        self.historico_lista = ctk.CTkScrollableFrame(
            historico_frame,
            height=200,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        self.historico_lista.pack(fill="x")

        # Exemplo de itens no histórico (seriam buscados do banco de dados)
        historicos = [
            {
                "livro": "Dom Casmurro",
                "autor": "Machado de Assis",
                "status": "Completo",
                "rating": 4,
                "data": "10/05/2023",
                "capa": "capa1.jpg"
            },
            {
                "livro": "1984",
                "autor": "George Orwell",
                "status": "Lendo",
                "rating": 5,
                "data": "15/04/2023",
                "capa": "capa2.jpg"
            },
            {
                "livro": "Clean Code",
                "autor": "Robert Martin",
                "status": "Abandonado",
                "rating": 2,
                "data": "22/03/2023",
                "capa": "capa3.jpg"
            }
        ]

        for hist in historicos:
            self.criar_item_historico(hist)

    def criar_item_historico(self, dados):
        """Cria um item no histórico de leituras"""
        item = ctk.CTkFrame(
            self.historico_lista,
            fg_color="#1e1e1e",
            border_width=1,
            border_color="#333333",
            corner_radius=8
        )
        item.pack(fill="x", padx=5, pady=5)

        # Capa do livro
        capa_frame = ctk.CTkFrame(item, fg_color="transparent", width=50)
        capa_frame.pack(side="left", padx=10, pady=10)
        
        ctk.CTkLabel(
            capa_frame,
            text="📖",
            font=ctk.CTkFont(size=24)
        ).pack()

        # Informações
        info_frame = ctk.CTkFrame(item, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)

        # Linha 1: Título e status
        linha1 = ctk.CTkFrame(info_frame, fg_color="transparent")
        linha1.pack(fill="x")

        ctk.CTkLabel(
            linha1,
            text=dados["livro"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        status_color = "#4CAF50" if dados["status"] == "Completo" else "#FF9800" if dados["status"] == "Lendo" else "#F44336"
        ctk.CTkLabel(
            linha1,
            text=dados["status"],
            font=ctk.CTkFont(size=12),
            text_color=status_color,
            anchor="e"
        ).pack(side="right")

        # Linha 2: Autor e data
        linha2 = ctk.CTkFrame(info_frame, fg_color="transparent")
        linha2.pack(fill="x")

        ctk.CTkLabel(
            linha2,
            text=dados["autor"],
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            linha2,
            text=dados["data"],
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            anchor="e"
        ).pack(side="right")

        # Linha 3: Rating e ações
        linha3 = ctk.CTkFrame(info_frame, fg_color="transparent")
        linha3.pack(fill="x")

        # Rating
        rating_frame = ctk.CTkFrame(linha3, fg_color="transparent")
        rating_frame.pack(side="left")

        for i in range(1, 6):
            ctk.CTkLabel(
                rating_frame,
                text="★" if i <= dados["rating"] else "☆",
                font=ctk.CTkFont(size=14),
                text_color="#FFD700" if i <= dados["rating"] else "#666666"
            ).pack(side="left", padx=1)

        # Ações
        acoes_frame = ctk.CTkFrame(linha3, fg_color="transparent")
        acoes_frame.pack(side="right")

        ctk.CTkButton(
            acoes_frame,
            text="Editar",
            width=60,
            height=20,
            font=ctk.CTkFont(size=10),
            fg_color="transparent",
            hover_color="#333333",
            border_width=1,
            border_color="#444444"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            acoes_frame,
            text="Excluir",
            width=60,
            height=20,
            font=ctk.CTkFont(size=10),
            fg_color="transparent",
            hover_color="#333333",
            border_width=1,
            border_color="#444444",
            text_color="#ff5555"
        ).pack(side="left")

    def registrar_leitura(self):
        """Registra a leitura no sistema"""
        if not hasattr(self, 'livro_selecionado'):
            print("Selecione um livro primeiro!")
            return

        dados = {
            "livro": self.titulo_livro_var.get(),
            "autor": self.autor_livro_var.get(),
            "status": self.status_var.get(),
            "rating": self.rating_var.get(),
            "data_inicio": self.data_inicio_entry.get(),
            "data_fim": self.data_fim_entry.get() if self.data_fim_entry.get() else None,
            "anotacoes": self.anotacoes_text.get("1.0", "end-1c"),
            "tags": self.tags_selecionadas,
            "anexo": getattr(self, 'arquivo_anexado', None)
        }

        print("Dados a serem salvos:", dados)
        # Aqui você faria a conexão com o backend para salvar os dados

        # Adiciona ao histórico (simulação)
        novo_item = {
            "livro": dados["livro"],
            "autor": dados["autor"],
            "status": "Completo" if dados["status"] == "completo" else 
                    "Lendo" if dados["status"] == "lendo" else 
                    "Abandonado",
            "rating": dados["rating"],
            "data": datetime.now().strftime("%d/%m/%Y"),
            "capa": ""
        }
        self.criar_item_historico(novo_item)