import customtkinter as ctk
import os
import threading
from typing import Optional
from PIL import Image, ImageOps, ImageDraw
from tkinter import colorchooser, filedialog

from image_processor import process_and_save_blocks
from color_palette_generator import get_color_palette
from file_conversor import convert_image_type
from utils import update_log, open_output_folder, select_image_path, select_output_folder
from image_editor import replace_color, hex_to_rgb


class MainController:
    """
    Controlador principal que gerencia o estado e a lógica de negócio do aplicativo
    """
    def __init__(self, app_instance: ctk.CTk) -> None:
        self.app = app_instance

        self.preview_label_split = None  
        self.preview_label_convert = None

        # --- Paleta de Cores e Estilo ---
        self.COLOR_BACKGROUND: str = "#1e1e1e"
        self.COLOR_FRAME: str = "#2d2d30"
        self.COLOR_FRAME_LOG: str = "#004b15"
        self.COLOR_TEXT: str = "#E3E3E3"
        self.COLOR_PRIMARY_BUTTON: str = "#b43dbe"
        self.COLOR_PRIMARY_HOVER: str = "#7c0b80"
        self.COLOR_SECONDARY_BUTTON: str = "#404040"
        self.COLOR_SECONDARY_HOVER: str = "#505050"
        self.COLOR_GRID: str = "#4dff4d"
        self.COLOR_SUCCESS: str = "#4dff4d"
        self.COLOR_ERROR: str = "#ed8484"

        # --- Variáveis de estado ---
        self.image_path: str = ""
        self.end_folder: str = ""
        self.modified_image: Optional[Image.Image] = None
        self._after_id: Optional[str] = None
        self.ctk_img_preview: Optional[ctk.CTkImage] = None
        self.palette_colors: list = []

        # Variáveis de controle para os widgets
        self.bloco_px_var = ctk.StringVar(value="16")
        self.scale_factor_var = ctk.StringVar(value="4")
        self.btn_execute = None
        self.preview_label = None
        self.log_textbox = None
        self.tabview = None
        self.status_label = None
        self.palette_preview_label = None
        self.output_name_conversor = None
        self.output_name_processor = None
        self.file_type_var = None
        self.palette_frame = None
        
        self.bloco_px_var.trace_add("write", lambda *args: self._update_grid_preview())

    # ======================
    #  Inicialização / Utils
    # ======================

    def _initialize(self) -> None:
        """Chamado após a construção da GUI para inicializações finais"""
        update_log(self.log_textbox, "Bem-vindo ao Editor de Sprites!", self.status_label)


    def _is_light_color(self, hex_color: str) -> bool:
        """Verifica se uma cor em formato hexadecimal é clara ou escura"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        luminosity = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        return luminosity > 0.5


    def _copy_to_clipboard(self, text: str) -> None:
        """Copia o texto para a área de transferência e atualiza o log"""
        self.app.clipboard_clear()
        self.app.clipboard_append(text)
        update_log(self.log_textbox, f"'{text}' copiado para a área de transferência", self.status_label)

    # ======================
    #  Arquivos e Pastas
    # ======================

    def _load_image_path(self, path: str) -> None:
        """Carrega o caminho da imagem e atualiza os previews"""
        if path:
            if self.palette_frame:
                for widget in self.palette_frame.winfo_children():
                    widget.destroy()

            self.image_path = path
            self.modified_image = None
            update_log(self.log_textbox, f"Imagem selecionada: {os.path.basename(self.image_path)}", self.status_label)
            self._update_grid_preview()
            self._update_convert_preview(path)
            self._update_palette_preview_from_path(path, self.palette_preview_label)


    def handle_choose_image(self) -> None:
        """Define a imagem e a carrega para o projeto"""
        path = select_image_path()
        self._load_image_path(path)


    def handle_choose_folder(self) -> None:
        """Define a pasta de saída e atualiza o log"""
        folder = select_output_folder()
        if folder:
            self.end_folder = folder
            update_log(self.log_textbox, "Pasta de saída definida", self.status_label)


    def handle_open_folder_exit(self) -> None:
        """Abre a pasta de saída"""
        open_output_folder(self.end_folder, self.log_textbox, self.status_label)

    # ======================
    #  Previews
    # ======================

    def _safe_configure_preview(self, image: Optional[ctk.CTkImage] = None, text: str = "") -> None:
        """Configura o label de preview de forma segura"""
        try:
            if image is None:
                self.ctk_img_preview = None
                self.preview_label_split.configure(image="", text=text)
            else:
                self.preview_label_split.configure(image=image, text="")
        except Exception:
            pass


    def _update_preview_from_image_object(self, image: Image.Image, preview_label: ctk.CTkLabel) -> None:
        """Atualiza um label de preview com um objeto de imagem PIL."""
        try:
            preview_box_w = preview_label.winfo_width()
            preview_box_h = preview_label.winfo_height()

            if preview_box_w <= 0 or preview_box_h <= 0:
                preview_box_w = 400
                preview_box_h = 300
            scale = min(preview_box_w / image.width, preview_box_h / image.height)
            new_w = max(1, int(image.width * scale))
            new_h = max(1, int(image.height * scale))
            
            preview_image = image.resize((new_w, new_h), Image.Resampling.NEAREST)
            ctk_image = ctk.CTkImage(light_image=preview_image, size=preview_image.size)
            
            preview_label.configure(image=ctk_image, text="")
            preview_label.image = ctk_image
        except Exception as e:
            preview_label.configure(text=f"Erro ao atualizar preview: {e}")


    def _update_grid_preview(self) -> None:
        """Atualiza o preview da grade com base na imagem e tamanho do bloco"""
        self._after_id = None
        if not self.image_path: return
        
        try:
            self.app.update_idletasks()
            bloco_px = int(self.bloco_px_var.get())
            if bloco_px <= 0:
                self._safe_configure_preview(text="Erro: Digite um tamanho de bloco válido")
                self.log_label.configure(text="Erro: Digite um tamanho de bloco válido")
                return

            original_image = Image.open(self.image_path).convert("RGBA")
            orig_w, orig_h = original_image.size
            
            image_for_preview = self.modified_image if self.modified_image else original_image

            preview_box_w = self.preview_label_split.winfo_width() - 40
            preview_box_h = self.preview_label_split.winfo_height() - 40
            if preview_box_w <= 1 or preview_box_h <= 1:
                self._after_id = self.app.after(200, self._update_grid_preview)
                return

            scale = min(preview_box_w / orig_w, preview_box_h / orig_h)
            new_w = max(1, int(orig_w * scale))
            new_h = max(1, int(orig_h * scale))
            preview_image = original_image.resize((new_w, new_h), Image.Resampling.NEAREST)
            
            draw = ImageDraw.Draw(preview_image)
            scale_w, scale_h = new_w / orig_w, new_h / orig_h
            for x in range(bloco_px, orig_w, bloco_px):
                draw.line([(x * scale_w, 0), (x * scale_w, new_h)], fill=self.COLOR_GRID, width=1)
            for y in range(bloco_px, orig_h, bloco_px):
                draw.line([(0, y * scale_h), (new_w, y * scale_h)], fill=self.COLOR_GRID, width=1)

            self.ctk_img_preview = ctk.CTkImage(light_image=preview_image, size=preview_image.size)
            self._safe_configure_preview(self.ctk_img_preview)
        except Exception as e:
            self._safe_configure_preview(text=f"Erro no preview:\n{e}")


    def _update_palette_preview_from_path(self, path: str) -> None:
        """Atualiza o preview da paleta de cores a partir de um caminho de arquivo."""
        try:
            image_to_preview = self.modified_image if self.modified_image else Image.open(path).convert("RGBA")
            self._update_preview_from_image_object(image_to_preview, self.palette_preview_label)
        except Exception as e:
            self.palette_preview_label.configure(text=f"Erro ao carregar preview: {e}")


    def _update_convert_preview(self, path: str) -> None:
        """Atualiza o preview da imagem convertida"""
        try:
            original_image = Image.open(path).convert("RGBA")
            preview_box_w = self.preview_label_convert.winfo_width() - 20
            preview_box_h = 250
            if preview_box_w <= 0:
                preview_box_w = 300
            scale = min(preview_box_w / original_image.width, preview_box_h / original_image.height)
            new_w = max(1, int(original_image.width * scale))
            new_h = max(1, int(original_image.height * scale))
            preview_image = original_image.resize((new_w, new_h), Image.Resampling.NEAREST)
            self.ctk_convert_preview = ctk.CTkImage(light_image=preview_image, size=preview_image.size)
            self.preview_label_convert.configure(image=self.ctk_convert_preview, text="")
        except Exception as e:
            self.preview_label_convert.configure(text=f"Erro ao carregar preview: {e}")

    # ======================
    #  Processamento (split)
    # ======================

    def handle_split_image(self) -> None:
        """Inicia o processamento da imagem em blocos"""
        if not self.image_path:
            update_log(self.log_textbox, "Erro: Selecione a imagem", self.status_label)
            self.log_label.configure(text="Erro: Selecione a imagem")
            return
        
        if not self.end_folder:
            update_log(self.log_textbox, "Erro: Selecione a pasta de saída", self.status_label)
            self.log_label.configure(text="Erro: Selecione a pasta de saída")
            return
        try:
            bloco_px = int(self.bloco_px_var.get())
            scale = int(self.scale_factor_var.get())
            if bloco_px <= 0 or scale <= 0:
                raise ValueError("Tamanho do bloco e escala devem ser maiores que zero.")
        except (ValueError, TypeError):
            update_log(self.log_textbox, "Erro: Tamanho do bloco ou fator de escala inválido", self.status_label)
            self.log_label.configure(text="Erro: Tamanho do bloco ou fator de escala inválido")
            return
        self._start_threaded_processing(bloco_px, scale)


    def _start_threaded_processing(self, bloco_px: int, scale: int) -> None:
        """Inicia o processamento em uma thread separada para evitar travamento da UI"""
        self.btn_execute.configure(state="disabled")
        update_log(self.log_textbox, "Iniciando processamento...", self.status_label)
        if self.status_label:
            self.status_label.configure(text="Iniciando processamento...", text_color=self.COLOR_TEXT)
        processing_thread = threading.Thread(
            target=self._thread_processing,
            args=(self.image_path, self.end_folder, bloco_px, scale)
        )
        processing_thread.start()


    def _thread_processing(self, image_path: str, output_folder: str, bloco_px: int, scale: int) -> None:
        """Processa a imagem em blocos e salva na pasta de saída"""
        output_name = self.output_name_processor.get() 
        try:
            process_and_save_blocks(
                image_path,
                output_folder,
                output_name,
                bloco_px,
                scale,
                lambda progress: self.app.after(0, self._update_progress, progress)
            )
            self.app.after(0, update_log, self.log_textbox, "✨ Processamento concluído!", self.status_label)
            self.log_label.configure(text="Peocessamento concluído!")
        except Exception as e:
            self.app.after(0, update_log, self.log_textbox, f"ERRO: {e}", self.status_label)
        finally:
            self.app.after(0, self._end_processing)


    def _end_processing(self) -> None:
        """Finaliza o processamento e atualiza a UI"""
        self.btn_execute.configure(state="normal")

    # ======================
    #  Paleta de Cores / Edição
    # ======================

    def handle_create_palette(self) -> None:
        """Cria a paleta de cores a partir da imagem"""
        path = self.image_path
        if not path:
            update_log(self.log_textbox, "Erro: Selecione uma imagem primeiro", self.status_label)
            self.log_label.configure(text="Erro: Selecione uma imagem primeiro")
            return

        update_log(self.log_textbox, f"Criando paleta de cores para: {os.path.basename(path)}", self.status_label)

        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        try:
            image_for_palette = self.modified_image if self.modified_image else Image.open(path).convert("RGBA")
            self.palette_colors = get_color_palette(image_for_palette) 
            
            self._update_palette_preview_from_path(path)
            max_cols = 8
            num_rows = (len(self.palette_colors) + max_cols - 1) // max_cols

            for idx, color_hex in enumerate(self.palette_colors): 
                row = idx // max_cols
                col = idx % max_cols
                color_button = ctk.CTkButton(
                    self.palette_frame, text=color_hex, fg_color=color_hex, 
                    text_color="black" if self._is_light_color(color_hex) else "white",
                    hover_color=color_hex, 
                    command=lambda c_hex=color_hex, btn=None: self.handle_replace_color_request(c_hex, btn)
                )
                color_button.configure(command=lambda c_hex=color_hex, btn=color_button: self.handle_replace_color_request(c_hex, btn))
                color_button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            for col in range(max_cols):
                self.palette_frame.grid_columnconfigure(col, weight=1)
            for row in range(num_rows):
                self.palette_frame.grid_rowconfigure(row, weight=1)
        except Exception as e:
            self.palette_colors = []
            update_log(self.log_textbox, f"ERRO ao criar paleta de cores: {e}", self.status_label)
        update_log(self.log_textbox, "Paleta de cores criada! Clique em uma cor para substituí-la.", self.status_label)
        self.log_label.configure(text="Paleta de cores criada com sucesso!")


    def handle_replace_color_request(self, old_color_hex: str, clicked_button: ctk.CTkButton) -> None:
        """Solicita ao usuário uma nova cor e inicia a substituição."""
        if not self.image_path:
            update_log(self.log_textbox, "Erro: Nenhuma imagem carregada.", self.status_label)
            return

        color_data = colorchooser.askcolor(title="Escolha a nova cor")
        if color_data and color_data[0]:
            new_color_rgb = tuple(int(c) for c in color_data[0])
            new_color_hex = color_data[1]

            update_log(self.log_textbox, f"Substituindo {old_color_hex} por {new_color_hex}...", self.status_label)

            image_to_process = self.modified_image.copy() if self.modified_image else Image.open(self.image_path).convert("RGBA")
            old_color_rgb = hex_to_rgb(old_color_hex)

            self.modified_image = replace_color(image_to_process, old_color_rgb, new_color_rgb)
            
            self._update_preview_from_image_object(self.modified_image, self.palette_preview_label)
            
            if clicked_button:
                clicked_button.configure(
                    fg_color=new_color_hex,
                    text_color="black" if self._is_light_color(new_color_hex) else "white",
                    text=new_color_hex, 
                    hover_color=new_color_hex
                )
            
            update_log(self.log_textbox, "Substituição concluída. Preview e botão atualizados.", self.status_label)
        else:
            update_log(self.log_textbox, "Seleção de nova cor cancelada.", self.status_label)


    def handle_save_modified_image(self) -> None:
        """Salva a imagem que teve suas cores modificadas."""
        if not self.modified_image:
            update_log(self.log_textbox, "Nenhuma modificação para salvar. Substitua uma cor primeiro.", self.status_label)
            return

        file_path = filedialog.asksaveasfilename(
            title="Salvar imagem modificada como...",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("Todos os arquivos", "*.*")]
        )

        if file_path:
            try:
                self.modified_image.save(file_path)
                update_log(self.log_textbox, f"Imagem modificada salva em: {file_path}", self.status_label)
            except Exception as e:
                update_log(self.log_textbox, f"Erro ao salvar a imagem: {e}", self.status_label)

    # ======================
    #  Conversão de Imagem
    # ======================

    def _handle_convert_image(self) -> None:
        """Converte a imagem selecionada para o formato escolhido e salva na pasta de saída"""
        if not self.image_path:
            update_log(self.log_textbox, "Erro: Selecione a imagem", self.status_label)
            self.log_label.configure(text="Erro: Selecione a imagem") 
            return
        
        if not self.end_folder:
            update_log(self.log_textbox, "Erro: Selecione a pasta de saída", self.status_label)
            self.log_label.configure(text="Erro: Selecione a pasta de saída")
            return
        
        file_type = self.file_type_var.get()
        if not file_type:
            update_log(self.log_textbox, "Erro: Selecione um formato de arquivo válido", self.status_label)
            self.log_label.configure(text="Erro: Selecione um formato de arquivo válido")
            return

        output_name = self.output_name_conversor.get().strip()
        if not output_name:
            update_log(self.log_textbox, "Erro: Digite um nome para o arquivo convertido", self.status_label)
            self.log_label.configure(text="Erro: Digite um nome para o arquivo convertido")
            return
        
        try:
            convert_image_type(self.image_path, self.end_folder, output_name, file_type)
            update_log(self.log_textbox, f"Imagem convertida para {file_type.upper()} com sucesso!", self.status_label)
            self.log_label.configure(text="Imagem convertida com sucesso!") 
        except Exception as e:
            update_log(self.log_textbox, f"Erro ao converter a imagem: {e}", self.status_label)
            self.log_label.configure(text="Erro ao converter a imagem") 
