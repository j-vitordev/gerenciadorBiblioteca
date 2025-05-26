import customtkinter as ctk
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv

load_dotenv('credenciais.env')

class TelaPerfil:
    def __init__(self, container):
        self.container = container
        self.carregar_interface()

    def carregar_interface(self):
        """Carrega toda a interface do perfil"""
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Container com scroll
        scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Seção do cabeçalho do perfil
        perfil_header = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        perfil_header.pack(fill="x", pady=(0, 20))

        # Foto do perfil
        try:
            foto_perfil = ctk.CTkImage(
                Image.open(os.getenv("FOTO_PERFIL_PADRAO")), 
                size=(100, 100)
            )
            foto_label = ctk.CTkLabel(
                perfil_header,
                image=foto_perfil,
                text="",
                corner_radius=50
            )
            foto_label.pack(side="left", padx=(0, 20))
        except Exception as e:
            print(f"Erro ao carregar foto: {e}")
            foto_label = ctk.CTkLabel(
                perfil_header,
                text="👤",
                font=ctk.CTkFont(size=50),
                width=100,
                height=100
            )
            foto_label.pack(side="left", padx=(0, 20))

        # Informações do usuário
        info_frame = ctk.CTkFrame(perfil_header, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            info_frame,
            text="Maria da Silva",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info_frame,
            text="Leitora Ávida - Nível 5",
            font=ctk.CTkFont(size=14),
            text_color="#4CAF50",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))

        # Botão de editar perfil
        ctk.CTkButton(
            info_frame,
            text="Editar Perfil",
            width=120,
            height=30,
            font=ctk.CTkFont(size=12),
            command=self.editar_perfil
        ).pack(anchor="w")

        # Estatísticas de leitura
        stats_frame = ctk.CTkFrame(
            scroll_frame,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        stats_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            stats_frame,
            text="📊 Estatísticas de Leitura",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 15))

        # Grid de estatísticas
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=10, pady=(0, 10))

        stats = [
            {"valor": "42", "label": "Livros lidos"},
            {"valor": "15", "label": "Dias seguidos"},
            {"valor": "128", "label": "Horas lidas"},
            {"valor": "2023", "label": "Membro desde"}
        ]

        for i, stat in enumerate(stats):
            stat_frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
            stat_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            stats_grid.grid_columnconfigure(i%2, weight=1)

            ctk.CTkLabel(
                stat_frame,
                text=stat["valor"],
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#4FC3F7"
            ).pack()

            ctk.CTkLabel(
                stat_frame,
                text=stat["label"],
                font=ctk.CTkFont(size=12),
                text_color="#aaaaaa"
            ).pack()

        # Metas de leitura
        metas_frame = ctk.CTkFrame(
            scroll_frame,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        metas_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            metas_frame,
            text="🎯 Metas de Leitura",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 15))

        metas = [
            {"titulo": "Meta Anual", "progresso": 0.65, "texto": "26/40 livros"},
            {"titulo": "Gêneros Diversos", "progresso": 0.4, "texto": "4/10 gêneros"},
            {"titulo": "Páginas por Dia", "progresso": 0.8, "texto": "40/50 páginas"}
        ]

        for meta in metas:
            meta_item = ctk.CTkFrame(metas_frame, fg_color="transparent")
            meta_item.pack(fill="x", padx=15, pady=5)

            ctk.CTkLabel(
                meta_item,
                text=meta["titulo"],
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(fill="x")

            progresso = ctk.CTkProgressBar(
                meta_item,
                width=400,
                height=10,
                corner_radius=5,
                progress_color="#4CAF50"
            )
            progresso.pack(fill="x", pady=5)
            progresso.set(meta["progresso"])

            ctk.CTkLabel(
                meta_item,
                text=meta["texto"],
                font=ctk.CTkFont(size=12),
                text_color="#aaaaaa",
                anchor="e"
            ).pack(fill="x")

        # Preferências
        pref_frame = ctk.CTkFrame(
            scroll_frame,
            fg_color="#252525",
            border_width=1,
            border_color="#333333",
            corner_radius=10
        )
        pref_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            pref_frame,
            text="❤️ Preferências",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 15))

        pref_grid = ctk.CTkFrame(pref_frame, fg_color="transparent")
        pref_grid.pack(fill="x", padx=10, pady=(0, 10))

        preferencias = [
            {"emoji": "📖", "categoria": "Ficção Científica"},
            {"emoji": "🏰", "categoria": "Fantasia"},
            {"emoji": "🔍", "categoria": "Mistério"},
            {"emoji": "💔", "categoria": "Romance"}
        ]

        for i, pref in enumerate(preferencias):
            pref_item = ctk.CTkFrame(pref_grid, fg_color="#1e1e1e", corner_radius=5)
            pref_item.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            pref_grid.grid_columnconfigure(i%2, weight=1)

            ctk.CTkLabel(
                pref_item,
                text=pref["emoji"],
                font=ctk.CTkFont(size=16)
            ).pack(side="left", padx=10)

            ctk.CTkLabel(
                pref_item,
                text=pref["categoria"],
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=(0, 10), fill="x", expand=True)

    def editar_perfil(self):
        """Abre a tela de edição de perfil"""
        print("Abrir tela de edição de perfil")
        # Implementação da edição de perfil futuramente...