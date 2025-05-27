import customtkinter as ctk
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv('credenciais.env')

class TelaConquistas:
    def __init__(self, container, voltar_callback):
        self.container = container
        self.voltar_callback = voltar_callback
        self.conquistas_data = {
            "Primeiros Passos": {"livros": 1, "imagem_var": "LOGO_INICIANTE", "size": (60, 60)},
            "Leitor Bronze": {"livros": 5, "imagem_var": "LOGO_BRONZE", "size": (65, 65)},
            "Leitor Prata": {"livros": 10, "imagem_var": "LOGO_PRATA", "size": (70, 70)},
            "Leitor Ouro": {"livros": 20, "imagem_var": "LOGO_OURO", "size": (75, 75)}
        }
        self.carregar_interface()

    def validar_numero(self, action, value_if_allowed):
        """Valida se o input é um número inteiro positivo"""
        if action == '1':  # Inserção
            if value_if_allowed.isdigit() or value_if_allowed == "":
                return True
            return False
        return True

    def carregar_interface(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        # Frame principal com scrollbar se necessário
        main_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Logo principal (tamanho reduzido)
        try:
            logo_path = os.getenv("LOGO_UNI")
            if logo_path and os.path.exists(logo_path):
                imagem = ctk.CTkImage(Image.open(logo_path), size=(60, 60))
                logo = ctk.CTkLabel(master=main_frame, image=imagem, text="")
                logo.pack(pady=(0, 5))
        except Exception as e:
            print(f"Erro ao carregar logo principal: {e}")
            logo = ctk.CTkLabel(master=main_frame, text="🏆", font=("Arial", 24))
            logo.pack(pady=(0, 5))

        # Título (fonte menor)
        ctk.CTkLabel(
            main_frame,
            text="Configuração de Conquistas",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="center"
        ).pack(fill="x", pady=(0, 10))

        # Botão de voltar (compacto)
        btn_voltar = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            command=self.voltar_callback,
            font=ctk.CTkFont(size=12),
            width=80,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#2b2b2b"
        )
        btn_voltar.pack(pady=(0, 10), anchor="w")

        # Frame para as conquistas com grid responsivo
        conquistas_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        conquistas_frame.pack(fill="x", expand=False, pady=(0, 10))

        # Configuração da grid (2 colunas)
        conquistas_frame.grid_columnconfigure(0, weight=1)
        conquistas_frame.grid_columnconfigure(1, weight=1)

        # Criar cards compactos para cada conquista
        for i, (titulo, dados) in enumerate(self.conquistas_data.items()):
            row = i // 2
            col = i % 2
            self.criar_card_conquista(conquistas_frame, titulo, dados, row, col)

        # Botão de salvar compacto
        btn_salvar = ctk.CTkButton(
            main_frame,
            text="Salvar",
            command=self.salvar_configuracoes,
            font=ctk.CTkFont(size=14),
            height=35,
            fg_color="#2e8b57",
            hover_color="#3cb371"
        )
        btn_salvar.pack(pady=(5, 10), fill="x", padx=50)  # Margens laterais para não ficar colado

    def criar_card_conquista(self, frame, titulo, dados, row, col):
        # Card menor (200x180)
        card = ctk.CTkFrame(
            frame,
            width=200,
            height=180,
            corner_radius=8,
            fg_color="#252525",
            border_width=1,
            border_color="#444444"
        )
        card.grid(row=row, column=col, padx=8, pady=5, sticky="nsew")
        card.grid_propagate(False)

        # Imagem da conquista (tamanho reduzido)
        try:
            img_path = os.getenv(dados["imagem_var"])
            if img_path and os.path.exists(img_path):
                img = ctk.CTkImage(Image.open(img_path), size=dados["size"])
                lbl_imagem = ctk.CTkLabel(card, image=img, text="")
                lbl_imagem.pack(pady=(10, 5))
        except Exception as e:
            print(f"Erro ao carregar imagem da conquista {titulo}: {e}")
            lbl_imagem = ctk.CTkLabel(card, text="🏆", font=ctk.CTkFont(size=24))
            lbl_imagem.pack(pady=(10, 5))

        # Título da conquista (fonte menor)
        ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack()

        # Input compacto para quantidade de livros
        frame_input = ctk.CTkFrame(card, fg_color="transparent")
        frame_input.pack(pady=5)

        ctk.CTkLabel(
            frame_input,
            text="Livros:",
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(0, 3))

        # Validação para aceitar apenas números
        vcmd = (self.container.register(self.validar_numero), '%d', '%P')
        
        dados["input_var"] = ctk.StringVar(value=str(dados["livros"]))
        
        input_livros = ctk.CTkEntry(
            frame_input,
            textvariable=dados["input_var"],
            width=50,
            height=25,
            justify="center",
            font=ctk.CTkFont(size=11),
            validate="key",
            validatecommand=vcmd
        )
        input_livros.pack(side="left")

    def salvar_configuracoes(self):
        # Atualiza os valores no dicionário de conquistas
        for titulo, dados in self.conquistas_data.items():
            try:
                valor = dados["input_var"].get()
                if valor:
                    dados["livros"] = int(valor)
                    print(f"Conquista '{titulo}' atualizada para {dados['livros']} livros")
            except ValueError:
                print(f"Valor inválido para {titulo}")
        
        # Feedback visual compacto
        for widget in self.container.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget._text == "✅ Salvo!":
                widget.destroy()
        
        lbl_feedback = ctk.CTkLabel(
            self.container,
            text="✅ Salvo!",
            text_color="#4CAF50",
            font=ctk.CTkFont(size=11)
        )
        lbl_feedback.place(relx=0.95, rely=0.95, anchor="se")
        self.container.after(2000, lbl_feedback.destroy)