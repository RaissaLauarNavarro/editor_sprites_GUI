import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw
import os
import subprocess
import platform

# --- Classe principal da Aplicação com a identidade Gemini ---
class GeminiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Paleta de Cores Gemini ---
        self.COLOR_BACKGROUND = "#1e1e1e"
        self.COLOR_FRAME = "#2d2d30"
        self.COLOR_TEXT = "#E3E3E3"
        self.COLOR_PRIMARY_BUTTON = "#4a80f5"
        self.COLOR_PRIMARY_HOVER = "#3a70e5"
        self.COLOR_SECONDARY_BUTTON = "#404040"
        self.COLOR_SECONDARY_HOVER = "#505050"
        self.COLOR_GRID = "#ff4d4d"

        # --- Configuração da Janela Principal ---
        self.title("Gemini Art Cutter")
        self.geometry("850x650")
        self.minsize(800, 600)
        self._set_appearance_mode("dark")
        self.configure(fg_color=self.COLOR_BACKGROUND)

        self.imagem_path = ""
        self.pasta_saida = ""
        self._after_id = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Painel de Controle (Esquerda) ---
        self.frame_controles = ctk.CTkFrame(self, fg_color=self.COLOR_FRAME, width=280)
        self.frame_controles.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        try:
            gemini_icon_image = Image.open("gemini_icon.png")
            self.gemini_icon = ctk.CTkImage(light_image=gemini_icon_image, size=(24, 24))
            label_titulo = ctk.CTkLabel(self.frame_controles, text=" Gemini Art Cutter", image=self.gemini_icon, compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        except FileNotFoundError:
            label_titulo = ctk.CTkLabel(self.frame_controles, text="Gemini Art Cutter", font=ctk.CTkFont(size=20, weight="bold"))
        
        label_titulo.pack(pady=(20, 20), padx=20)

        ctk.CTkButton(self.frame_controles, text="Escolher Imagem", height=35, command=self.escolher_imagem, fg_color=self.COLOR_SECONDARY_BUTTON, hover_color=self.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.frame_controles, text="Escolher Pasta de Saída", height=35, command=self.escolher_pasta, fg_color=self.COLOR_SECONDARY_BUTTON, hover_color=self.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")

        frame_opcoes = ctk.CTkFrame(self.frame_controles, fg_color="transparent")
        frame_opcoes.pack(pady=20, padx=20, fill="x")
        frame_opcoes.grid_columnconfigure((0, 1), weight=1)

        self.bloco_px_var = ctk.StringVar(value="16")
        self.bloco_px_var.trace_add("write", self.agendar_atualizacao_preview)
        self.tamanho_bloco_entry = ctk.CTkEntry(frame_opcoes, textvariable=self.bloco_px_var)
        self.tamanho_bloco_entry.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="ew")

        self.fator_escala_combo = ctk.CTkComboBox(frame_opcoes, values=["1", "2", "4", "8", "16", "32"], button_color=self.COLOR_PRIMARY_BUTTON)
        self.fator_escala_combo.set("4")
        self.fator_escala_combo.grid(row=0, column=1, padx=(5, 0), pady=10, sticky="ew")

        ctk.CTkButton(self.frame_controles, text="Abrir Pasta de Saída", command=self.abrir_pasta_saida, fg_color="transparent", border_width=1, border_color=self.COLOR_SECONDARY_HOVER).pack(side="bottom", pady=20, padx=20, fill="x")

        # --- Painel Principal (Direita) ---
        self.frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_principal.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.btn_executar = ctk.CTkButton(self.frame_principal, text="✨ Processar Imagens", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=self.dividir_imagem, fg_color=self.COLOR_PRIMARY_BUTTON, hover_color=self.COLOR_PRIMARY_HOVER)
        self.btn_executar.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 20), sticky="ew")
        
        self.tabview = ctk.CTkTabview(self.frame_principal, fg_color=self.COLOR_FRAME, segmented_button_selected_color=self.COLOR_PRIMARY_BUTTON, segmented_button_selected_hover_color=self.COLOR_PRIMARY_HOVER)
        self.tabview.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.tabview.add("Preview com Grid")
        self.tabview.add("Log de Atividades")
        self.tabview.set("Preview com Grid")

        self.log_textbox = ctk.CTkTextbox(self.tabview.tab("Log de Atividades"), text_color=self.COLOR_TEXT, fg_color="transparent", activate_scrollbars=True)
        self.log_textbox.pack(expand=True, fill="both", padx=10, pady=10)
        self.atualizar_log("Bem-vindo ao Gemini Art Cutter!")

        self.preview_label = ctk.CTkLabel(self.tabview.tab("Preview com Grid"), text="Selecione uma imagem para ver o preview.", text_color=self.COLOR_TEXT)
        self.preview_label.pack(expand=True, fill="both", padx=20, pady=20)

        self.progressbar = ctk.CTkProgressBar(self.frame_principal, fg_color=self.COLOR_FRAME, progress_color=self.COLOR_PRIMARY_BUTTON)
        self.progressbar.set(0)

    def escolher_imagem(self):
        self.imagem_path = filedialog.askopenfilename(title="Selecione um arquivo de imagem", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp")])
        if self.imagem_path:
            self.atualizar_log(f"Imagem selecionada: {os.path.basename(self.imagem_path)}")
            self.atualizar_preview()
            self.tabview.set("Preview com Grid")

    def escolher_pasta(self):
        self.pasta_saida = filedialog.askdirectory(title="Selecione a pasta de saída")
        if self.pasta_saida:
            self.atualizar_log(f"Pasta de saída definida.")

    def abrir_pasta_saida(self):
        if not self.pasta_saida or not os.path.exists(self.pasta_saida):
            self.atualizar_log("Erro: Pasta de saída inválida ou não selecionada.")
            return
        if platform.system() == "Windows": os.startfile(self.pasta_saida)
        elif platform.system() == "Darwin": subprocess.run(["open", self.pasta_saida])
        else: subprocess.run(["xdg-open", self.pasta_saida])

    def atualizar_log(self, mensagem):
        self.log_textbox.insert("0.0", f"● {mensagem}\n\n")

    def agendar_atualizacao_preview(self, *args):
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(500, self.atualizar_preview)

    def atualizar_preview(self):
        if not self.imagem_path: return
        try:
            bloco_px = int(self.bloco_px_var.get())
            if bloco_px <= 0: return

            original_image = Image.open(self.imagem_path)
            orig_w, orig_h = original_image.size

            # Pega o tamanho disponível no widget de preview para calcular a escala
            preview_box_w = self.preview_label.winfo_width() - 40
            preview_box_h = self.preview_label.winfo_height() - 40
            if preview_box_w <= 1 or preview_box_h <= 1: return # Evita erro se o widget não estiver visível

            # --- NOVA LÓGICA DE REDIMENSIONAMENTO PARA PIXEL ART ---
            # Calcula o fator de escala para ampliar a imagem até caber na caixa
            scale = min(preview_box_w / orig_w, preview_box_h / orig_h)
            
            # Calcula o novo tamanho, garantindo que seja pelo menos 1x1
            new_w = max(1, int(orig_w * scale))
            new_h = max(1, int(orig_h * scale))

            # Redimensiona a imagem com NEAREST para manter os pixels nítidos
            preview_image = original_image.resize((new_w, new_h), Image.Resampling.NEAREST)
            # --- FIM DA NOVA LÓGICA ---
            
            # A lógica de desenhar o grid continua a mesma, pois se adapta à nova escala
            draw = ImageDraw.Draw(preview_image)
            scale_w = new_w / orig_w
            scale_h = new_h / orig_h

            for x in range(bloco_px, orig_w, bloco_px):
                line_x = x * scale_w
                draw.line([(line_x, 0), (line_x, new_h)], fill=self.COLOR_GRID, width=1)
            for y in range(bloco_px, orig_h, bloco_px):
                line_y = y * scale_h
                draw.line([(0, line_y), (new_w, line_y)], fill=self.COLOR_GRID, width=1)

            ctk_img = ctk.CTkImage(light_image=preview_image, size=preview_image.size)
            self.preview_label.configure(image=ctk_img, text="")
        except (ValueError, FileNotFoundError):
            self.preview_label.configure(image=None, text="Digite um tamanho de bloco válido.")
        except Exception as e:
            self.preview_label.configure(image=None, text=f"Erro no preview:\n{e}")

    def dividir_imagem(self):
        if not self.imagem_path or not self.pasta_saida:
            self.atualizar_log("Erro: Selecione a imagem e a pasta de saída.")
            return

        try:
            bloco_px = int(self.bloco_px_var.get())
            escala = int(self.fator_escala_combo.get())
        except (ValueError, TypeError):
            self.atualizar_log("Erro: Tamanho do bloco ou fator de escala inválido.")
            return

        self.btn_executar.configure(state="disabled")
        self.progressbar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10,0))
        self.progressbar.start()
        self.update_idletasks()

        try:
            imagem = Image.open(self.imagem_path).convert("RGBA")
            largura, altura = imagem.size
            if largura % bloco_px != 0 or altura % bloco_px != 0:
                raise ValueError(f"Dimensões ({largura}x{altura}) não são múltiplas de {bloco_px}px.")

            contador = 0
            total_rows = altura // bloco_px
            for i, y in enumerate(range(0, altura, bloco_px)):
                for x in range(0, largura, bloco_px):
                    bloco = imagem.crop((x, y, x + bloco_px, y + bloco_px))
                    if bloco.getbbox():
                        if escala > 1:
                            bloco = bloco.resize((bloco_px * escala, bloco_px * escala), Image.Resampling.NEAREST)
                        nome_base = os.path.splitext(os.path.basename(self.imagem_path))[0]
                        nome_arquivo = f"{nome_base}_{contador:04}.png"
                        bloco.save(os.path.join(self.pasta_saida, nome_arquivo))
                        contador += 1
                progress = (i + 1) / total_rows
                self.progressbar.set(progress)
                self.update_idletasks()

            self.atualizar_log(f"✨ Sucesso! {contador} blocos foram salvos.")
        except Exception as e:
            self.atualizar_log(f"ERRO: {e}")
        finally:
            self.progressbar.stop()
            self.progressbar.grid_remove()
            self.btn_executar.configure(state="normal")


if __name__ == "__main__":
    app = GeminiApp()
    app.mainloop()