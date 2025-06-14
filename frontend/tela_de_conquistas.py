import customtkinter as ctk
from PIL import Image
import os
from dotenv import load_dotenv
from backend.conexao import conectar  # ajuste o caminho se necessário

load_dotenv('credenciais.env')

class TelaConquistas:
    def __init__(self, container, usuario_id):
        self.container = container
        self.usuario_id = usuario_id
        self.conquistas_data = {}
        self.carregar_dados_conquistas()
        self.carregar_interface()

    def carregar_dados_conquistas(self):
        """Consulta o banco de dados para verificar as conquistas desbloqueadas do usuário"""
        try:
            conn = conectar()
            cursor = conn.cursor()

            # 1. Quantos livros o usuário já leu (com status 'lido')
            cursor.execute("""
                SELECT COUNT(*) FROM usuario_livro
                WHERE usuario_id = ? AND status = 'lido'
            """, self.usuario_id)
            livros_lidos = cursor.fetchone()[0]

            # 2. Buscar conquistas do banco
            cursor.execute("SELECT Nome, QuantidadeLivros FROM Conquistas")
            conquistas = cursor.fetchall()

            for nome, qtd in conquistas:
                desbloqueada = livros_lidos >= qtd

                # Pega a parte final do nome para usar no .env, exemplo: "Leitor Bronze" -> LOGO_BRONZE
                ultima_palavra = nome.split()[-1].upper()
                imagem_var = f"LOGO_{ultima_palavra}"

                self.conquistas_data[nome] = {
                    "imagem_var": imagem_var,
                    "size": (70, 70),
                    "descricao": f"Leu {qtd} livro(s)",
                    "desbloqueada": desbloqueada
                }

            conn.close()

        except Exception as e:
            print("Erro ao carregar conquistas:", e)

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
            height=220,
            corner_radius=10,
            fg_color="#252525" if dados["desbloqueada"] else "#1a1a1a",
            border_width=1,
            border_color="#333333"
        )
        card.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Imagem da conquista (se existir) ou emoji
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

        # Título
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

        # Status se bloqueada
        if not dados["desbloqueada"]:
            ctk.CTkLabel(
                content_frame,
                text="Bloqueada",
                font=ctk.CTkFont(size=12),
                text_color="#ff5555"
            ).pack()
