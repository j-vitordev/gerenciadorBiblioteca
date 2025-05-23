import customtkinter as ctk

class TelaHomeAdmin:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Home Administrador")
        self.janela.geometry("800x500")
        ctk.set_appearance_mode("dark")
        
        self.frame_principal = ctk.CTkFrame(self.janela, corner_radius=0, fg_color="#1e1e1e")
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.carregar_interface()

        self.janela.mainloop()

    def carregar_interface(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.frame_principal, text="Painel do Administrador",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(10, 30))

        botoes = [
            ("📚 Cadastrar Livro", self.cadastrar_livro),
            ("🏆 Cadastrar Conquista", self.cadastrar_conquista),
            ("👥 Ver Usuários da Biblioteca", self.ver_usuarios),
            ("🚪 Sair", self.sair)
        ]

        for texto, comando in botoes:
            btn = ctk.CTkButton(
                self.frame_principal,
                text=texto,
                command=comando,
                font=ctk.CTkFont(size=16),
                height=50,
                width=250,
                corner_radius=10
            )
            btn.pack(pady=10)

    def mostrar_tela_simples(self, titulo, descricao):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.frame_principal, text=titulo,
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self.frame_principal, text=descricao,
            font=ctk.CTkFont(size=14), text_color="#aaaaaa"
        ).pack(pady=10)

        voltar_btn = ctk.CTkButton(
            self.frame_principal, text="🔙 Voltar",
            command=self.carregar_interface,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        voltar_btn.pack(pady=20)

    def cadastrar_livro(self):
        self.mostrar_tela_simples("Cadastrar Livro", "Aqui você pode cadastrar novos livros.")

    def cadastrar_conquista(self):
        self.mostrar_tela_simples("Cadastrar Conquista", "Aqui você pode cadastrar novas conquistas para gamificação.")

    def ver_usuarios(self):
        self.mostrar_tela_simples("Usuários da Biblioteca", "Aqui você pode visualizar e gerenciar os usuários.")

    def sair(self):
        self.janela.destroy()

if __name__ == "__main__":
    TelaHomeAdmin()
