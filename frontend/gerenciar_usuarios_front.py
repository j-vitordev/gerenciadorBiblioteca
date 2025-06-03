import customtkinter as ctk
from backend.usuarios_back import buscar_usuarios_nao_admin, excluir_usuario, atualizar_senha
from tkinter import messagebox

def TelaGerenciarUsuarios(frame, voltar_callback):

    def carregar_usuarios():
        for widget in lista_frame.winfo_children():
            widget.destroy()

        usuarios = buscar_usuarios_nao_admin()
        for usuario in usuarios:
            id, nome, email, _, is_admin = usuario

            usuario_frame = ctk.CTkFrame(lista_frame)
            usuario_frame.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(usuario_frame, text=f"{nome} ({email})").pack(side="left", padx=10)

            btn_excluir = ctk.CTkButton(usuario_frame, text="Excluir", width=70,
                                        command=lambda uid=id: excluir(uid))
            btn_excluir.pack(side="right", padx=5)

            btn_alterar = ctk.CTkButton(usuario_frame, text="Alterar Senha", width=120,
                                        command=lambda uid=id: alterar_senha(uid))
            btn_alterar.pack(side="right", padx=5)

    def excluir(user_id):
        excluir_usuario(user_id)
        carregar_usuarios()

    def alterar_senha(user_id):
      nova_senha = ctk.CTkInputDialog(text="Digite a nova senha:", title="Alterar Senha").get_input()
      if nova_senha:
        atualizar_senha(user_id, nova_senha)
        messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
        carregar_usuarios()

    # Criar o layout principal
    for widget in frame.winfo_children():
        widget.destroy()

    btn_voltar = ctk.CTkButton(frame, text="🔙 Voltar", command=voltar_callback)
    btn_voltar.pack(pady=(10, 20))

    ctk.CTkLabel(frame, text="Lista de Usuários (não Admin)", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

    lista_frame = ctk.CTkScrollableFrame(frame, width=600, height=400)
    lista_frame.pack(pady=10)

    carregar_usuarios()
