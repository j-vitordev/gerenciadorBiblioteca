import customtkinter as ctk
from backend.conexao import conectar
import os
import subprocess
from pathlib import Path
from datetime import datetime

class TelaBiblioteca:
    def __init__(self, container, usuario_id):
        """
        Inicializa a tela da biblioteca
        
        Args:
            container: Widget pai onde a tela será exibida
            usuario_id: ID do usuário logado (obtido durante o login)
        """
        self.container = container
        self.usuario_id = usuario_id  # Agora recebe o ID do usuário logado
        self.carregar_interface()

    def buscar_livros(self):
        """
        Busca todos os livros disponíveis no banco de dados
        
        Returns:
            Lista de dicionários com informações dos livros
        """
        try:
            conn = conectar()
            cursor = conn.cursor()
            query = """
            SELECT [id], [titulo], [autor], [editora], [ano_publicacao], [isbn], [caminho_pdf]
            FROM [Biblioteca].[dbo].[livros]
            """
            cursor.execute(query)
            livros = cursor.fetchall()
            colunas = [column[0] for column in cursor.description]
            return [dict(zip(colunas, livro)) for livro in livros]
            
        except Exception as e:
            print(f"Erro ao buscar livros: {e}")
            ctk.CTkMessageBox(
                title="Erro", 
                message="Não foi possível carregar os livros", 
                icon="cancel"
            )
            return []
            
        finally:
            if 'conn' in locals():
                conn.close()

    def carregar_interface(self):
        """Carrega todos os elementos da interface gráfica"""
        # Limpa o container principal
        for widget in self.container.winfo_children():
            widget.destroy()

        # Frame principal com scroll
        main_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Cabeçalho
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))

        # Título
        ctk.CTkLabel(
            top_frame,
            text="📚 Biblioteca",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        # Campo de busca
        self.busca_entry = ctk.CTkEntry(
            top_frame, 
            placeholder_text="Buscar livros...", 
            width=200
        )
        self.busca_entry.pack(side="right")
        self.busca_entry.bind("<KeyRelease>", self.filtrar_livros)

        # Container para os cards de livros
        self.livros_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.livros_container.pack(fill="both", expand=True)

        # Carrega e exibe os livros
        self.livros = self.buscar_livros()
        self.mostrar_livros(self.livros)

    def mostrar_livros(self, livros):
        """Exibe os livros em cards na interface"""
        # Limpa o container de livros
        for widget in self.livros_container.winfo_children():
            widget.destroy()

        # Mensagem se não houver livros
        if not livros:
            ctk.CTkLabel(
                self.livros_container,
                text="Nenhum livro encontrado",
                font=ctk.CTkFont(size=16)
            ).pack(pady=50)
            return

        # Organiza em linhas de 3 colunas
        for i, livro in enumerate(livros):
            row = i // 3
            col = i % 3
            if col == 0:
                row_frame = ctk.CTkFrame(self.livros_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)
            self.criar_card_livro(row_frame, livro, col)

    def criar_card_livro(self, frame, livro, column):
        """Cria um card individual para cada livro"""
        card = ctk.CTkFrame(
            frame, 
            width=200, 
            height=200, 
            corner_radius=10,
            fg_color="#252525", 
            border_width=1, 
            border_color="#333333"
        )
        card.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        # Informações do livro
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

        # Botões de ação
        botoes_frame = ctk.CTkFrame(card, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=5, padx=5)

        # Botão para abrir o livro
        btn_abrir = ctk.CTkButton(
            botoes_frame, 
            text="Abrir Livro", 
            width=100,
            command=lambda l=livro: self.abrir_livro(l)
        )
        btn_abrir.pack(side="left", padx=5)

        # Botão para marcar como lido/lendo
        btn_marcador = ctk.CTkButton(
            botoes_frame, 
            text="🔖", 
            width=30, 
            fg_color="transparent", 
            hover_color="#333333"
        )
        btn_marcador.configure(
            command=lambda l=livro, btn=btn_marcador: self.marcar_livro(l, btn))
        btn_marcador.pack(side="right", padx=5)

    def abrir_livro(self, livro):
        """Abre o arquivo PDF do livro e registra a leitura"""
        caminho_pdf = livro['caminho_pdf']
        try:
            caminho_absoluto = Path.cwd() / caminho_pdf
            if not caminho_absoluto.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_absoluto}")

            # Registra no banco que o usuário está lendo o livro
            self.registrar_leitura(usuario_id=self.usuario_id, livro_id=livro["id"])

            # Abre o arquivo conforme o sistema operacional
            if os.name == 'nt':
                os.startfile(str(caminho_absoluto))
            elif os.name == 'posix':
                subprocess.run(['open', str(caminho_absoluto)], check=True)
                
            print(f"Livro aberto com sucesso: {livro['titulo']}")
            
        except Exception as e:
            print(f"Erro ao abrir o livro: {e}")
            ctk.CTkMessageBox(
                title="Erro", 
                message=f"Não foi possível abrir o livro:\n{e}", 
                icon="cancel"
            )

    def registrar_leitura(self, usuario_id, livro_id):
        """
        Registra no banco de dados que o usuário está lendo o livro
        Se já existir registro, não faz nada
        """
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Verifica se já existe registro
            cursor.execute("""
                SELECT COUNT(*) 
                FROM usuario_livro 
                WHERE usuario_id = ? AND livro_id = ?
            """, (usuario_id, livro_id))
            
            existe = cursor.fetchone()[0]

            # Se não existe, cria novo registro
            if existe == 0:
                cursor.execute("""
                    INSERT INTO usuario_livro 
                    (usuario_id, livro_id, status, data_registro)
                    VALUES (?, ?, ?, ?)
                """, (usuario_id, livro_id, 'lendo', datetime.now()))
                
                conn.commit()
                print("Leitura registrada no banco de dados.")
                
        except Exception as e:
            print(f"Erro ao registrar leitura: {e}")
            
        finally:
            if 'conn' in locals():
                conn.close()

    def marcar_livro(self, livro, botao_marcador):
        """Alterna entre status 'lendo' e 'lido' para o livro"""
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Determina o novo status
            if botao_marcador.cget("text") == "🔖":
                novo_status = "lido"
                texto_botao = "✅"
                cor = "#2e8b57"  # Verde
            else:
                novo_status = "lendo"
                texto_botao = "🔖"
                cor = "transparent"

            # Atualiza no banco de dados
            cursor.execute("""
                UPDATE usuario_livro
                SET status = ?, data_registro = ?
                WHERE usuario_id = ? AND livro_id = ?
            """, (novo_status, datetime.now(), self.usuario_id, livro["id"]))
            
            conn.commit()

            # Atualiza a aparência do botão
            botao_marcador.configure(text=texto_botao, fg_color=cor)
            print(f"Livro '{livro['titulo']}' marcado como {novo_status}.")
            
        except Exception as e:
            print(f"Erro ao atualizar marcador: {e}")
            
        finally:
            if 'conn' in locals():
                conn.close()

    def filtrar_livros(self, event=None):
        """Filtra os livros conforme texto digitado na busca"""
        termo_busca = self.busca_entry.get().lower()
        
        if not termo_busca:
            self.mostrar_livros(self.livros)
            return
            
        livros_filtrados = [
            livro for livro in self.livros 
            if (termo_busca in livro["titulo"].lower() or 
                termo_busca in livro["autor"].lower())
        ]
        
        self.mostrar_livros(livros_filtrados)