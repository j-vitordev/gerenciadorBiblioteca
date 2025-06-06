import customtkinter as ctk
from backend.conexao import conectar
import os
import subprocess
from pathlib import Path

class TelaBiblioteca:
    def __init__(self, container):
        self.container = container
        self.carregar_interface()

    def buscar_livros(self):
        """Busca todos os livros cadastrados no banco de dados"""
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            query = """
            SELECT [id], [titulo], [autor], [editora], [ano_publicacao], [isbn], [caminho_pdf]
            FROM [Biblioteca].[dbo].[livros]
            """
            
            cursor.execute(query)
            livros = cursor.fetchall()
            
            # Converter para lista de dicionários
            colunas = [column[0] for column in cursor.description]
            livros_formatados = [dict(zip(colunas, livro)) for livro in livros]
            
            return livros_formatados
            
        except Exception as e:
            print(f"Erro ao buscar livros: {e}")
            # Mostrar mensagem de erro na interface
            ctk.CTkMessageBox(title="Erro", 
                             message="Não foi possível carregar os livros do banco de dados", 
                             icon="cancel")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    def carregar_interface(self):
        """Carrega toda a interface da biblioteca"""
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Frame principal com scroll
        main_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título e barra de busca
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            top_frame,
            text="📚 Biblioteca",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        self.busca_entry = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar livros...",
            width=200
        )
        self.busca_entry.pack(side="right")
        self.busca_entry.bind("<KeyRelease>", self.filtrar_livros)

        # Filtros
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            filtros_frame,
            text="Filtrar por:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0, 10))

        self.filtros = ["Todos", "Lidos", "Lendo", "Quero ler"]
        self.filtro_selecionado = ctk.StringVar(value="Todos")
        
        for filtro in self.filtros:
            btn = ctk.CTkRadioButton(
                filtros_frame,
                text=filtro,
                variable=self.filtro_selecionado,
                value=filtro,
                command=self.filtrar_livros
            )
            btn.pack(side="left", padx=5)

        # Container para os livros
        self.livros_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.livros_container.pack(fill="both", expand=True)

        # Carrega os livros do banco de dados
        self.livros = self.buscar_livros()
        self.mostrar_livros(self.livros)

    def mostrar_livros(self, livros):
        """Exibe os livros na interface"""
        # Limpa o container de livros
        for widget in self.livros_container.winfo_children():
            widget.destroy()

        if not livros:
            # Mostra mensagem se não houver livros
            ctk.CTkLabel(
                self.livros_container,
                text="Nenhum livro encontrado",
                font=ctk.CTkFont(size=16)
            ).pack(pady=50)
            return

        # Organiza em grid 3 colunas
        for i, livro in enumerate(livros):
            row = i // 3
            col = i % 3
            
            # Cria frame para a coluna se não existir
            if col == 0:
                row_frame = ctk.CTkFrame(self.livros_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)
            
            self.criar_card_livro(row_frame, livro, col)

    def criar_card_livro(self, frame, livro, column):
        """Cria um card para um livro"""
        card = ctk.CTkFrame(
            frame,
            width=200,
            height=180,
            corner_radius=10,
            fg_color="#252525",
            border_width=1,
            border_color="#333333"
        )
        card.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        # Conteúdo do card
        ctk.CTkLabel(
            card,
            text=livro["titulo"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
            wraplength=180
        ).pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            card,
            text=f"Autor: {livro['autor']}",
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
            anchor="w"
        ).pack(fill="x", padx=10)

        ctk.CTkLabel(
            card,
            text=f"Editora: {livro['editora']}",
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
            anchor="w"
        ).pack(fill="x", padx=10)

        ctk.CTkLabel(
            card,
            text=f"Ano: {livro['ano_publicacao']}",
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
            anchor="w"
        ).pack(fill="x", padx=10)

        # Botão para abrir o livro
        btn_abrir = ctk.CTkButton(
            card,
            text="Abrir Livro",
            width=100,
            command=lambda l=livro: self.abrir_livro(l)
        )
        btn_abrir.pack(pady=5)

    def abrir_livro(self, livro):
        """Abre o livro PDF no visualizador padrão do sistema"""
        caminho_pdf = livro['caminho_pdf']
        
        try:
            # Converter o caminho para um formato absoluto
            caminho_absoluto = Path.cwd() / caminho_pdf
            
            print(f"Tentando abrir: {caminho_absoluto}")
            
            # Verificar se o arquivo existe
            if not caminho_absoluto.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_absoluto}")
            
            # Abrir o arquivo com o programa padrão do sistema
            if os.name == 'nt':  # Windows
                os.startfile(str(caminho_absoluto))
            elif os.name == 'posix':  # macOS e Linux
                subprocess.run(['open', str(caminho_absoluto)], check=True)  # macOS
                # Para Linux, você pode tentar:
                # subprocess.run(['xdg-open', str(caminho_absoluto)], check=True)
            else:
                raise OSError("Sistema operacional não suportado")
                
            print(f"Livro aberto com sucesso: {livro['titulo']}")
            
        except Exception as e:
            print(f"Erro ao abrir o livro: {e}")
            # Mostrar mensagem de erro na interface
            ctk.CTkMessageBox(title="Erro", 
                             message=f"Não foi possível abrir o livro:\n{e}", 
                             icon="cancel")

    def filtrar_livros(self, event=None):
        """Filtra os livros com base na busca e no filtro selecionado"""
        termo_busca = self.busca_entry.get().lower()
        filtro = self.filtro_selecionado.get()

        livros_filtrados = []
        
        for livro in self.livros:
            # Filtro por termo de busca
            busca_match = (termo_busca in livro["titulo"].lower() or 
                          termo_busca in livro["autor"].lower())
            
            # Filtro por status (implementação básica - você pode adaptar)
            status_match = True
            if filtro == "Lidos":
                status_match = False  # Você precisará adicionar um campo 'lido' no seu banco
            elif filtro == "Lendo":
                status_match = False  # Você precisará adicionar um campo 'lendo' no seu banco
            elif filtro == "Quero ler":
                status_match = False  # Você precisará adicionar um campo 'quero_ler' no seu banco
            
            if busca_match and status_match:
                livros_filtrados.append(livro)
        
        self.mostrar_livros(livros_filtrados)