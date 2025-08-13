import customtkinter as ctk
from PIL import Image

class GUIBuilder:
    """
    Construtor da interface do usuário.
    Cria todos os widgets e os posiciona na janela principal.
    """
    @staticmethod
    def build(app):
        """Constrói a interface para a aplicação """
        GUIBuilder._create_control_panel_widgets(app)
        GUIBuilder._create_main_panel_widgets(app)

    @staticmethod
    def _create_control_panel_widgets(app):
        """Cria os widgets do painel de controle esquerdo."""
        app.frame_controles = ctk.CTkFrame(app, fg_color=app.COLOR_FRAME, width=280)
        app.frame_controles.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        app.icon = None
        label_titulo = ctk.CTkLabel(app.frame_controles, text="Editor de Sprites", font=ctk.CTkFont(size=20, weight="bold"))
        label_titulo.pack(pady=(20, 20), padx=20)

        ctk.CTkButton(app.frame_controles, text="Escolher Imagem", height=35, command=app._handle_escolher_imagem, fg_color=app.COLOR_SECONDARY_BUTTON, hover_color=app.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(app.frame_controles, text="Escolher Pasta de Saída", height=35, command=app._handle_escolher_pasta, fg_color=app.COLOR_SECONDARY_BUTTON, hover_color=app.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")

        frame_opcoes = ctk.CTkFrame(app.frame_controles, fg_color="transparent")
        frame_opcoes.pack(pady=20, padx=20, fill="x")
        frame_opcoes.grid_columnconfigure((0, 1), weight=1)

        label_bloco = ctk.CTkLabel(frame_opcoes, text="Tamanho do bloco (px):")
        label_bloco.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky="w")

        label_escala = ctk.CTkLabel(frame_opcoes, text="Fator de escala:")
        label_escala.grid(row=0, column=1, padx=(5, 0), pady=(0, 0), sticky="w")

        app.tamanho_bloco_entry = ctk.CTkEntry(frame_opcoes, textvariable=app.bloco_px_var)
        app.tamanho_bloco_entry.grid(row=1, column=0, padx=(0, 5), pady=10, sticky="ew")

        app.fator_escala_combo = ctk.CTkComboBox(frame_opcoes, values=["1", "2", "4", "8", "16", "32"], button_color=app.COLOR_PRIMARY_BUTTON)
        app.fator_escala_combo.set("4")
        app.fator_escala_combo.grid(row=1, column=1, padx=(5, 0), pady=10, sticky="ew")

        ctk.CTkButton(app.frame_controles, text="Abrir Pasta de Saída", command=app._handle_abrir_pasta_saida, fg_color="transparent", border_width=1, border_color=app.COLOR_SECONDARY_HOVER).pack(side="bottom", pady=20, padx=20, fill="x")

    @staticmethod
    def _create_main_panel_widgets(app):
        """Cria os widgets do painel principal direito."""
        app.frame_principal = ctk.CTkFrame(app, fg_color="transparent")
        app.frame_principal.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        app.frame_principal.grid_rowconfigure(1, weight=1)
        app.frame_principal.grid_columnconfigure(0, weight=1)

        app.btn_executar = ctk.CTkButton(app.frame_principal, text="✨ Processar Imagens", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=app._handle_dividir_imagem, fg_color=app.COLOR_PRIMARY_BUTTON, hover_color=app.COLOR_PRIMARY_HOVER)
        app.btn_executar.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 20), sticky="ew")
        
        app.tabview = ctk.CTkTabview(app.frame_principal, fg_color=app.COLOR_FRAME, segmented_button_selected_color=app.COLOR_PRIMARY_BUTTON, segmented_button_selected_hover_color=app.COLOR_PRIMARY_HOVER)
        app.tabview.grid(row=1, column=0, columnspan=2, sticky="nsew")
        app.tabview.add("Preview com Grid")
        app.tabview.add("Log de Atividades")
        app.tabview.set("Preview com Grid")

        app.preview_label = ctk.CTkLabel(app.tabview.tab("Preview com Grid"), text="Selecione uma imagem para ver o preview.", text_color=app.COLOR_TEXT)
        app.preview_label.pack(expand=True, fill="both", padx=20, pady=20)

        app.log_textbox = ctk.CTkTextbox(app.tabview.tab("Log de Atividades"), text_color=app.COLOR_TEXT, fg_color="transparent", activate_scrollbars=True)
        app.log_textbox.pack(expand=True, fill="both", padx=10, pady=10)

        app.status_label = ctk.CTkLabel(app.frame_principal, text="", text_color=app.COLOR_SUCCESS)
        app.status_label.grid(row=2, column=0, columnspan=1, padx=5, pady=(10, 0), sticky="sw")
        app.progressbar = ctk.CTkProgressBar(app.frame_principal, fg_color=app.COLOR_FRAME, progress_color=app.COLOR_PRIMARY_BUTTON)
        app.progressbar.set(0)
