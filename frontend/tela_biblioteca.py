import customtkinter as ctk
from backend.conexao import conectar
import os
import subprocess
from pathlib import Path
from datetime import datetime

class TelaBiblioteca:
    def __init__(self, container):
        self.container = container
        self.usuario_id = 1  # ID do usuário logado (modifique se necessário)
        self.carregar_interface()

    def buscar_livros(self):
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
            livros_formatados = [dict(zip(colunas, livro)) for livro in livros]
            return livros_formatados
        except Exception as e:
            print(f"Erro ao buscar livros: {e}")
            ctk.CTkMessageBox(title="Erro", message="Não foi possível carregar os livros", icon="cancel")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    def carregar_interface(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        main_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            top_frame,
            text="📚 Biblioteca",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        self.busca_entry = ctk.CTkEntry(top_frame, placeholder_text="Buscar livros...", width=200)
        self.busca_entry.pack(side="right")
        self.busca_entry.bind("<KeyRelease>", self.filtrar_livros)

        self.livros_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.livros_container.pack(fill="both", expand=True)

        self.livros = self.buscar_livros()
        self.mostrar_livros(self.livros)

    def mostrar_livros(self, livros):
        for widget in self.livros_container.winfo_children():
            widget.destroy()

        if not livros:
            ctk.CTkLabel(
                self.livros_container,
                text="Nenhum livro encontrado",
                font=ctk.CTkFont(size=16)
            ).pack(pady=50)
            return

        for i, livro in enumerate(livros):
            row = i // 3
            col = i % 3
            if col == 0:
                row_frame = ctk.CTkFrame(self.livros_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)
            self.criar_card_livro(row_frame, livro, col)

    def criar_card_livro(self, frame, livro, column):
        card = ctk.CTkFrame(
            frame, width=200, height=200, corner_radius=10,
            fg_color="#252525", border_width=1, border_color="#333333"
        )
        card.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        ctk.CTkLabel(card, text=livro["titulo"], font=ctk.CTkFont(size=14, weight="bold"),
                     anchor="w", wraplength=180).pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(card, text=f"Autor: {livro['autor']}", font=ctk.CTkFont(size=12),
                     text_color="#aaaaaa", anchor="w").pack(fill="x", padx=10)
        ctk.CTkLabel(card, text=f"Editora: {livro['editora']}", font=ctk.CTkFont(size=12),
                     text_color="#aaaaaa", anchor="w").pack(fill="x", padx=10)
        ctk.CTkLabel(card, text=f"Ano: {livro['ano_publicacao']}", font=ctk.CTkFont(size=12),
                     text_color="#aaaaaa", anchor="w").pack(fill="x", padx=10)

        botoes_frame = ctk.CTkFrame(card, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=5, padx=5)

        btn_abrir = ctk.CTkButton(
            botoes_frame, text="Abrir Livro", width=100,
            command=lambda l=livro: self.abrir_livro(l)
        )
        btn_abrir.pack(side="left", padx=5)

        btn_marcador = ctk.CTkButton(
            botoes_frame, text="🔖", width=30, fg_color="transparent", hover_color="#333333"
        )
        btn_marcador.configure(command=lambda l=livro, btn=btn_marcador: self.marcar_livro(l, btn))
        btn_marcador.pack(side="right", padx=5)

    def abrir_livro(self, livro):
        caminho_pdf = livro['caminho_pdf']
        try:
            caminho_absoluto = Path.cwd() / caminho_pdf
            if not caminho_absoluto.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_absoluto}")

            self.registrar_leitura(usuario_id=self.usuario_id, livro_id=livro["id"])

            if os.name == 'nt':
                os.startfile(str(caminho_absoluto))
            elif os.name == 'posix':
                subprocess.run(['open', str(caminho_absoluto)], check=True)
            print(f"Livro aberto com sucesso: {livro['titulo']}")
        except Exception as e:
            print(f"Erro ao abrir o livro: {e}")
            ctk.CTkMessageBox(title="Erro", message=f"Não foi possível abrir o livro:\n{e}", icon="cancel")

    def registrar_leitura(self, usuario_id, livro_id):
        try:
            conn = conectar()
            cursor = conn.cursor()
            consulta = """
                SELECT COUNT(*) FROM usuario_livro WHERE usuario_id = ? AND livro_id = ?
            """
            cursor.execute(consulta, (usuario_id, livro_id))
            existe = cursor.fetchone()[0]

            if existe == 0:
                insert = """
                    INSERT INTO usuario_livro (usuario_id, livro_id, status, data_registro)
                    VALUES (?, ?, ?, ?)
                """
                cursor.execute(insert, (usuario_id, livro_id, 'lendo', datetime.now()))
                conn.commit()
                print("Leitura registrada no banco de dados.")
        except Exception as e:
            print(f"Erro ao registrar leitura: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def marcar_livro(self, livro, botao_marcador):
        try:
            conn = conectar()
            cursor = conn.cursor()
            novo_status = "lido" if botao_marcador.cget("text") == "🔖" else "lendo"
            texto_botao = "✅" if novo_status == "lido" else "🔖"
            cor = "#2e8b57" if novo_status == "lido" else "transparent"

            cursor.execute("""
                UPDATE usuario_livro
                SET status = ?, data_registro = ?
                WHERE usuario_id = ? AND livro_id = ?
            """, (novo_status, datetime.now(), self.usuario_id, livro["id"]))
            conn.commit()

            botao_marcador.configure(text=texto_botao, fg_color=cor)
            print(f"Livro '{livro['titulo']}' marcado como {novo_status}.")
        except Exception as e:
            print(f"Erro ao atualizar marcador: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def filtrar_livros(self, event=None):
        termo_busca = self.busca_entry.get().lower()
        if not termo_busca:
            self.mostrar_livros(self.livros)
            return
        livros_filtrados = [livro for livro in self.livros if
                            termo_busca in livro["titulo"].lower() or
                            termo_busca in livro["autor"].lower()]
        self.mostrar_livros(livros_filtrados)
