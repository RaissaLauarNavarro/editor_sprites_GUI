import customtkinter as ctk

class GUIBuilder:
    """
    Construtor da interface do usuário.
    Cria todos os widgets e os posiciona na janela principal.
    """
    @staticmethod
    def build(app, controller):
        """Constrói a interface para a aplicação."""
        GUIBuilder._create_control_panel_widgets(app, controller)
        GUIBuilder._create_tab_view_widgets(app, controller)


    @staticmethod
    def _create_control_panel_widgets(app, controller):
        app.frame_controles = ctk.CTkFrame(app, fg_color=controller.COLOR_FRAME, width=290)
        app.frame_controles.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="ns")
        app.frame_controles.grid_propagate(False)
        app.frame_controles.grid_columnconfigure(0, weight=1)
        app.frame_controles.grid_rowconfigure(5, weight=1)

        label_title = ctk.CTkLabel(app.frame_controles, text="Editor de Sprites", font=ctk.CTkFont(size=20, weight="bold"))
        label_title.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="ew")

        btn_img = ctk.CTkButton(app.frame_controles, text="Escolher Imagem", height=35, command=controller.handle_choose_image, fg_color=controller.COLOR_SECONDARY_BUTTON, hover_color=controller.COLOR_SECONDARY_HOVER)
        btn_img.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        btn_folder = ctk.CTkButton(app.frame_controles, text="Escolher Pasta de Saída", height=35, command=controller.handle_choose_folder, fg_color=controller.COLOR_SECONDARY_BUTTON, hover_color=controller.COLOR_SECONDARY_HOVER)
        btn_folder.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        controller.log_label = ctk.CTkLabel(app.frame_controles, text="", text_color="white", anchor="w")
        controller.log_label.grid(row=6, column=0, padx=20, pady=(50, 0), sticky="ew")

        btn_open = ctk.CTkButton(app.frame_controles, text="Abrir Pasta de Saída", command=controller.handle_open_folder_exit, fg_color="transparent", border_width=1, border_color=controller.COLOR_SECONDARY_HOVER)
        btn_open.grid(row=7, column=0, padx=20, pady=(10, 20), sticky="ew")


    @staticmethod
    def _create_tab_view_widgets(app, controller):
        """Cria as abas e os widgets específicos para cada funcionalidade."""
        app.main_frame = ctk.CTkFrame(app, fg_color="transparent")
        app.main_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        app.main_frame.grid_columnconfigure(0, weight=1)
        app.main_frame.grid_rowconfigure(0, weight=1)

        # Cria a tabview antes de adicionar as abas
        controller.tabview = ctk.CTkTabview(app.main_frame, fg_color=controller.COLOR_FRAME, segmented_button_selected_color=controller.COLOR_PRIMARY_BUTTON, segmented_button_selected_hover_color=controller.COLOR_PRIMARY_HOVER)
        controller.tabview.grid(row=0, column=0, sticky="nsew")
        
        tab_log = controller.tabview.add("Log de Atividades")
        tab_split = controller.tabview.add("Divisor de Sprites")
        tab_convert = controller.tabview.add("Conversor de Formato")
        # tab_resize = controller.tabview.add("Redimensionar Imagem")
        tab_palette = controller.tabview.add("Gerador de Paleta de Cores")
        
        GUIBuilder._create_log_tab_widgets(tab_log, controller)
        GUIBuilder._create_split_tab_widgets(tab_split, controller)
        GUIBuilder._create_convert_tab_widgets(tab_convert, controller)
        # GUIBuilder._create_resize_tab_widgets(tab_resize, controller)
        GUIBuilder._create_palette_tab_widgets(tab_palette, controller)

        controller.progressbar = ctk.CTkProgressBar(app.main_frame, fg_color=controller.COLOR_FRAME, progress_color=controller.COLOR_PRIMARY_BUTTON)
        controller.progressbar.set(0)
        controller.progressbar.grid(row=1, column=0, sticky="ew", pady=(10, 0), padx=5)
        
        controller.status_label = ctk.CTkLabel(app.main_frame, text="", text_color=controller.COLOR_SUCCESS)
        controller.status_label.grid(row=2, column=0, sticky="sw", padx=5)
        
        controller.progressbar.grid_remove()
        controller.status_label.grid_remove()


    @staticmethod
    def _create_log_tab_widgets(tab, controller):
        """Cria e posiciona os widgets dentro da aba Log de Atividades."""
        controller.log_textbox = ctk.CTkTextbox(tab, text_color=controller.COLOR_TEXT, fg_color="transparent", activate_scrollbars=True)
        controller.log_textbox.pack(padx=0, pady=0, expand=True, fill="both")


    @staticmethod
    def _create_split_tab_widgets(tab, controller):
        """Cria e posiciona os widgets dentro da aba Divisor de Sprites."""

        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        
        # Frame de preview com grid
        preview_frame = ctk.CTkFrame(tab, fg_color="transparent")
        preview_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        controller.preview_label_split = ctk.CTkLabel(preview_frame, text="Selecione uma imagem para ver o preview", text_color=controller.COLOR_TEXT)
        controller.preview_label_split.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Frame para os controles
        controls_frame = ctk.CTkFrame(tab, fg_color="transparent")
        controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        controls_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(controls_frame, text="Tamanho do bloco (px):").grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky="w")
        ctk.CTkLabel(controls_frame, text="Fator de escala:").grid(row=0, column=1, padx=(5, 0), pady=(0, 0), sticky="w")

        ctk.CTkEntry(controls_frame, textvariable=controller.bloco_px_var).grid(row=1, column=0, padx=(0, 5), pady=10, sticky="ew")

        scale_factor_widget = ctk.CTkComboBox(controls_frame, values=["1", "2", "4", "8", "16", "32"], button_color=controller.COLOR_PRIMARY_BUTTON)
        scale_factor_widget.set(controller.scale_factor_var.get())
        scale_factor_widget.grid(row=1, column=1, padx=(5, 0), pady=10, sticky="ew")
        controller.scale_factor_var = scale_factor_widget

        ctk.CTkLabel(controls_frame, text="Nome do arquivo de saída:").grid(row=2, column=0, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="w")
        output_name_entry = ctk.CTkEntry(controls_frame)
        output_name_entry.grid(row=3, column=0, columnspan=2, padx=(0, 0), pady=10, sticky="ew")
        output_name_entry.insert(0, "sprite") 
        controller.output_name_processor = output_name_entry

        controller.btn_execute = ctk.CTkButton(controls_frame, text="✨ Dividir Imagem", height=40, font=ctk.CTkFont(size=16, weight="bold"), command=controller.handle_split_image, fg_color=controller.COLOR_PRIMARY_BUTTON, hover_color=controller.COLOR_PRIMARY_HOVER) 
        controller.btn_execute.grid(row=4, column=0, columnspan=2, padx=0, pady=10, sticky="ew")



    @staticmethod
    def _create_palette_tab_widgets(tab, controller):
        """Cria e posiciona os widgets dentro da aba Gerador de Paleta."""

        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=0)
        
        # Frame de preview com grid
        preview_frame = ctk.CTkFrame(tab, fg_color="transparent")
        preview_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        controller.palette_preview_label = ctk.CTkLabel(preview_frame, text="Selecione uma imagem para ver o preview", text_color=controller.COLOR_TEXT)
        controller.palette_preview_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Frame para os controles
        controls_frame = ctk.CTkFrame(tab, fg_color="transparent")
        controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        
        controller.palette_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        controller.palette_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        controller.palette_frame.grid_columnconfigure(0, weight=1)
        controller.palette_frame.grid_rowconfigure(0, weight=1)

        action_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        action_frame.grid(row=1, column=0, sticky="ew")
        action_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(action_frame, text="🎨 Criar Paleta de Cores", height=40, font=ctk.CTkFont(size=16, weight="bold"), command=controller.handle_create_palette, fg_color=controller.COLOR_PRIMARY_BUTTON, hover_color=controller.COLOR_PRIMARY_HOVER).grid(row=0, column=0, padx=(0, 5), sticky="ew")
        ctk.CTkButton(action_frame, text="💾 Salvar Imagem Modificada", height=40, font=ctk.CTkFont(size=16, weight="bold"), command=controller.handle_save_modified_image, fg_color=controller.COLOR_SECONDARY_BUTTON, hover_color=controller.COLOR_SECONDARY_HOVER).grid(row=0, column=1, padx=(5, 0), sticky="ew")



    @staticmethod
    def _create_convert_tab_widgets(tab, controller):
        """Cria e posiciona os widgets dentro da aba Conversor de Formato."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        
        # Frame de preview com grid
        preview_frame = ctk.CTkFrame(tab, fg_color="transparent")
        preview_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        controller.preview_label_convert = ctk.CTkLabel(preview_frame, text="Selecione uma imagem para ver o preview", text_color=controller.COLOR_TEXT)
        controller.preview_label_convert.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Frame para os controles
        controls_frame = ctk.CTkFrame(tab, fg_color="transparent")
        controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        controls_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(controls_frame, text="Novo formato de arquivo:").grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky="w")
        ctk.CTkLabel(controls_frame, text="Nome do arquivo de saída:").grid(row=1, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        file_type_widget = ctk.CTkComboBox(controls_frame, values=["png", "jpg", "jpeg", "bmp", "tiff", "gif"], button_color=controller.COLOR_PRIMARY_BUTTON)
        file_type_widget.set("png")
        file_type_widget.grid(row=0, column=1, padx=(5, 0), pady=10, sticky="ew")
        controller.file_type_var = file_type_widget

        output_name_entry = ctk.CTkEntry(controls_frame)
        output_name_entry.insert(0, "sprite") 
        output_name_entry.grid(row=1, column=1, padx=(5, 0), pady=10, sticky="ew")
        controller.output_name_conversor = output_name_entry

        controller.btn_execute = ctk.CTkButton(controls_frame,text="↪️ Converter imagem",height=40,font=ctk.CTkFont(size=16, weight="bold"),command=controller._handle_convert_image, fg_color=controller.COLOR_PRIMARY_BUTTON,hover_color=controller.COLOR_PRIMARY_HOVER)
        controller.btn_execute.grid(row=2, column=0, columnspan=2, padx=0, pady=10, sticky="ew")


@staticmethod
def _create_resize_tab_widgets(tab, controller):
    """Cria e posiciona os widgets dentro da aba Redimensionar Imagem."""
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_rowconfigure(0, weight=1)

    # Frame de preview
    preview_frame = ctk.CTkFrame(tab, fg_color="transparent")
    preview_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
    preview_frame.grid_columnconfigure(0, weight=1)
    preview_frame.grid_rowconfigure(0, weight=1)

    controller.preview_label_resize = ctk.CTkLabel(preview_frame, text="Selecione uma imagem para ver o preview", text_color=controller.COLOR_TEXT)
    controller.preview_label_resize.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    # Frame para os controles
    controls_frame = ctk.CTkFrame(tab, fg_color="transparent")
    controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
    controls_frame.grid_columnconfigure((0, 1), weight=1)

    ctk.CTkLabel(controls_frame, text="Nova largura (px):").grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky="w")
    ctk.CTkLabel(controls_frame, text="Nova altura (px):").grid(row=1, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

    width_entry = ctk.CTkEntry(controls_frame)
    width_entry.grid(row=0, column=1, padx=(5, 0), pady=10, sticky="ew")
    controller.resize_width_entry = width_entry

    height_entry = ctk.CTkEntry(controls_frame)
    height_entry.grid(row=1, column=1, padx=(5, 0), pady=10, sticky="ew")
    controller.resize_height_entry = height_entry

    controller.btn_resize = ctk.CTkButton(
        controls_frame,
        text="⤢ Redimensionar Imagem",
        height=40,
        font=ctk.CTkFont(size=16, weight="bold"),
        command=controller.handle_resize_image,
        fg_color=controller.COLOR_PRIMARY_BUTTON,
        hover_color=controller.COLOR_PRIMARY_HOVER
    )
    controller.btn_resize.grid(row=2, column=0, columnspan=2, padx=0, pady=10, sticky="ew")