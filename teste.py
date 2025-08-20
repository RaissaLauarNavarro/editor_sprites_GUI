import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App com Abas")
        self.geometry("800x600")

        # Criar o Tabview (navegação por abas)
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar abas
        tab_principal = tabview.add("Dividir Imagem")
        tab_config = tabview.add("Configurações")
        tab_sobre = tabview.add("Sobre")

        # ---- Conteúdo da aba "Dividir Imagem"
        self.btn_execute = ctk.CTkButton(
            master=tab_principal, 
            text="Executar",
            command=self._handle_split_image
        )
        self.btn_execute.pack(pady=20)

        # ---- Conteúdo da aba "Configurações"
        ctk.CTkLabel(tab_config, text="Configurações aqui...").pack(pady=20)

        # ---- Conteúdo da aba "Sobre"
        ctk.CTkLabel(tab_sobre, text="Feito por Raissa 😄").pack(pady=20)

    def _handle_split_image(self):
        print("Executando divisão de imagem...")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # opcional
    app = App()
    app.mainloop()
