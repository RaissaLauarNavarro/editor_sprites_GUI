import customtkinter as ctk
import os
import threading
from typing import Optional

# Importa as classes e funções dos outros arquivos
from gui_builder import GUIBuilder
from image_processor import process_and_save_blocks
from utils import update_log, open_output_folder, select_image_path, select_output_folder

# --- Classe principal da Aplicação ---
class App(ctk.CTk):
    """
    Aplicativo principal "Divisor de Imagem em Blocos".
    Gerencia a janela, o estado e a interação entre a GUI e a lógica de processamento.
    """
    def __init__(self) -> None:
        super().__init__()

        # --- Paleta de Cores Personalizada ---
        self.COLOR_BACKGROUND: str = "#1e1e1e"
        self.COLOR_FRAME: str = "#2d2d30"
        self.COLOR_TEXT: str = "#E3E3E3"
        self.COLOR_PRIMARY_BUTTON: str = "#e74af5"
        self.COLOR_PRIMARY_HOVER: str = "#7c0b80"
        self.COLOR_SECONDARY_BUTTON: str = "#404040"
        self.COLOR_SECONDARY_HOVER: str = "#505050"
        self.COLOR_GRID: str = "#4dff4d"

        # --- Variáveis de estado ---
        self.imagem_path: str = ""
        self.pasta_saida: str = ""
        self._after_id: Optional[str] = None
        self.ctk_img_preview: Optional[ctk.CTkImage] = None

        # Variáveis de controle para os widgets (referências)
        self.bloco_px_var = ctk.StringVar(value="16")
        self.fator_escala_combo = None
        self.btn_executar = None
        self.progressbar = None
        self.preview_label = None
        self.log_textbox = None
        self.tabview = None
        
        # --- Configuração da Janela Principal ---
        self._setup_window()
        
        # --- Configuração do Layout da Janela ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Criação dos Widgets usando o construtor da GUI ---
        GUIBuilder.build(self)
        self.bloco_px_var.trace_add("write", self._agendar_atualizacao_preview)
        
        update_log(self.log_textbox, "Bem-vindo ao Divisor de Imagem em Blocos!")

    def _setup_window(self) -> None:
        """Configura as propriedades da janela principal."""
        self.title("Divisor de Imagem em Blocos")
        self.geometry("850x650")
        self.minsize(800, 600)
        self._set_appearance_mode("dark")
        self.configure(fg_color=self.COLOR_BACKGROUND)

    # --- Funções de Manipulação de Eventos e Lógica da Aplicação ---

    def _safe_configure_preview(self, image: Optional[ctk.CTkImage] = None, text: str = "") -> None:
        """Configura o label de preview de forma segura."""
        try:
            if image is None:
                self.ctk_img_preview = None
                self.preview_label.configure(image="", text=text)
            else:
                self.preview_label.configure(image=image, text="")
        except Exception:
            pass

    def _handle_escolher_imagem(self) -> None:
        """Abre a caixa de diálogo para selecionar uma imagem e atualiza o estado."""
        path = select_image_path()
        if path:
            self.imagem_path = path
            update_log(self.log_textbox, f"Imagem selecionada: {os.path.basename(self.imagem_path)}")
            self._agendar_atualizacao_preview()
            self.tabview.set("Preview com Grid")

    def _handle_escolher_pasta(self) -> None:
        """Abre a caixa de diálogo para selecionar a pasta de saída e atualiza o estado."""
        pasta = select_output_folder()
        if pasta:
            self.pasta_saida = pasta
            update_log(self.log_textbox, "Pasta de saída definida.")

    def _handle_abrir_pasta_saida(self) -> None:
        """Tenta abrir a pasta de saída no explorador de arquivos do sistema."""
        open_output_folder(self.pasta_saida, self.log_textbox)

    def _agendar_atualizacao_preview(self, *args) -> None:
        """Agenda a atualização do preview para evitar múltiplas chamadas rápidas."""
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
        
        try:
            self._after_id = self.after(500, self._atualizar_preview)
        except Exception:
            self._after_id = None

    def _atualizar_preview(self) -> None:
        """Gera e exibe a imagem de preview com o grid."""
        self._after_id = None
        if not self.imagem_path: return
        
        from PIL import Image, ImageDraw
        try:
            self.update_idletasks()
            bloco_px = int(self.bloco_px_var.get())
            if bloco_px <= 0:
                self._safe_configure_preview(text="Digite um tamanho de bloco válido.")
                return

            original_image = Image.open(self.imagem_path).convert("RGBA")
            orig_w, orig_h = original_image.size
            preview_box_w = self.preview_label.winfo_width() - 40
            preview_box_h = self.preview_label.winfo_height() - 40
            if preview_box_w <= 1 or preview_box_h <= 1:
                self._after_id = self.after(200, self._atualizar_preview)
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

    def _handle_dividir_imagem(self) -> None:
        """Inicia o processo de divisão da imagem."""
        if not self.imagem_path or not self.pasta_saida:
            update_log(self.log_textbox, "Erro: Selecione a imagem e a pasta de saída.")
            return

        try:
            bloco_px = int(self.bloco_px_var.get())
            escala = int(self.fator_escala_combo.get())
            if bloco_px <= 0 or escala <= 0:
                raise ValueError("Tamanho do bloco e escala devem ser maiores que zero.")
        except (ValueError, TypeError):
            update_log(self.log_textbox, "Erro: Tamanho do bloco ou fator de escala inválido.")
            return
        
        self._iniciar_processamento_com_thread(bloco_px, escala)

    def _iniciar_processamento_com_thread(self, bloco_px: int, escala: int) -> None:
        """Configura e executa o processamento da imagem em uma thread separada."""
        self.btn_executar.configure(state="disabled")
        self.progressbar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10,0))
        self.progressbar.set(0)
        update_log(self.log_textbox, "Iniciando processamento...")

        processing_thread = threading.Thread(
            target=self._processar_em_thread,
            args=(self.imagem_path, self.pasta_saida, bloco_px, escala)
        )
        processing_thread.start()

    def _processar_em_thread(self, image_path: str, output_folder: str, bloco_px: int, escala: int) -> None:
        """Função que será executada na thread de processamento."""
        try:
            process_and_save_blocks(
                image_path,
                output_folder,
                bloco_px,
                escala,
                lambda progress: self.after(0, self._update_progress, progress)
            )
            self.after(0, update_log, self.log_textbox, "✨ Processamento concluído!")
        except Exception as e:
            self.after(0, update_log, self.log_textbox, f"ERRO: {e}")
        finally:
            self.after(500, self._finalizar_processamento)
    
    def _update_progress(self, progress: float) -> None:
        """Atualiza a barra de progresso na GUI (chamado da thread principal)."""
        self.progressbar.set(progress)
    
    def _finalizar_processamento(self) -> None:
        """Reseta a interface após o processamento."""
        self.progressbar.grid_remove()
        self.btn_executar.configure(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()
