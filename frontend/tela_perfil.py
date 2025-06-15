import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkInputDialog

from backend.cadusuario import buscar_dados_usuario, atualizar_senha  # Importa as funções necessárias


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
        nova_senha = CTkInputDialog(title="Nova Senha", text="Digite a nova senha:").get_input()
        if not nova_senha:
            return  # usuário cancelou

        confirmar = CTkInputDialog(title="Confirmar Senha", text="Confirme a nova senha:").get_input()
        if not confirmar:
            return

        if nova_senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        if len(nova_senha) < 6:
            messagebox.showwarning("Senha fraca", "A senha deve ter pelo menos 6 caracteres.")
            return

        sucesso, mensagem = atualizar_senha(self.usuario_id, nova_senha)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
        else:
            messagebox.showerror("Erro", mensagem)
