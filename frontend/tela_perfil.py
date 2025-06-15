import customtkinter as ctk
from backend.cadusuario import buscar_dados_usuario  # ajuste se o nome da função for diferente

class TelaPerfil:
    def __init__(self, container, usuario_id):
        self.container = container
        self.usuario_id = usuario_id
        self.carregar_interface()

    def carregar_interface(self):
        # Limpa a tela
        for widget in self.container.winfo_children():
            widget.destroy()

        # Container principal
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Busca os dados do usuário
        dados = buscar_dados_usuario(self.usuario_id)
        nome = dados.get("nome", "Usuário")
        categoria = dados.get("categoria", "Desconhecida")

        # Título
        ctk.CTkLabel(
            frame,
            text="👤 Perfil do Usuário",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 20))

        # Nome
        ctk.CTkLabel(
            frame,
            text=f"Nome: {nome}",
            font=ctk.CTkFont(size=18)
        ).pack(pady=10)

        # Categoria
        ctk.CTkLabel(
            frame,
            text=f"Categoria: {categoria}",
            font=ctk.CTkFont(size=16),
            text_color="#4CAF50"
        ).pack(pady=10)

        # Botão de redefinir senha
        ctk.CTkButton(
            frame,
            text="Redefinir Senha",
            command=self.redefinir_senha
        ).pack(pady=20)

    def redefinir_senha(self):
        # Lógica para redefinição de senha
        print("Abrir tela para redefinição de senha")
