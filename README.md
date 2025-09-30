
# ✨ Editor de Sprites

Este é um aplicativo de desktop com interface gráfica (GUI) para edição de imagens, ideal para desenvolvedores de jogos e artistas que trabalham com sprites e pixel art. Desenvolvido com customtkinter, o programa oferece várias ferramentas para otimizar e manipular seus arquivos de imagem.


# 🚀 Funcionalidades

Editor de Sprites oferece as seguintes ferramentas em um único lugar:

- Divisor de Sprites: Divide uma imagem spritesheet em blocos individuais de tamanho definido. Você pode configurar o tamanho do bloco e aplicar um fator de escala para ampliar o resultado.

- Gerador de Paleta de Cores: Extrai as cores principais de uma imagem e gera uma paleta clicável.

- Substituição de Cores: Permite substituir uma cor da paleta gerada por outra de sua escolha. É perfeito para criar variações de cores de personagens ou objetos.

- Conversor de Formato: Converte imagens entre diversos formatos de arquivo, como PNG, JPG, BMP, e outros.


# 📥 Como baixar e utilizar

Para a maneira mais fácil de usar o aplicativo, basta baixar o arquivo executável (.exe) da página de releases.

Não é necessário instalar Python ou qualquer outra biblioteca. Apenas baixe e execute o arquivo Editor_de_Sprites.exe.


# ⚙️ Para Desenvolvedores

Se você deseja rodar o projeto a partir do código-fonte ou contribuir com o desenvolvimento, siga as instruções abaixo.

## Requisitos:

  Certifique-se de ter o Python 3.x instalado.

O projeto utiliza as seguintes bibliotecas:

  - customtkinter: Para a interface gráfica.

  - Pillow: Para manipulação de imagens.

  - colorthief: Para extração da paleta de cores.

Instale-as executando o seguinte comando no seu terminal:

```PYTHON

pip install customtkinter pillow colorthief
```

## Como executar
- Clone este repositório ou baixe os arquivos.

- Navegue até o diretório do projeto.

- Execute o arquivo principal app.py:

```PYTHON

python app.py
```

# 🧠 Como Funciona

Divisor: O divisor de sprites percorre a imagem em blocos do tamanho especificado e salva cada bloco como um arquivo PNG separado, ideal para importar em engines de jogos. A função process_and_save_blocks em image_processor.py lida com essa lógica, incluindo um callback de progresso para a barra de status da GUI.

Gerador de Paleta: A biblioteca colorthief é utilizada na função get_color_palette para identificar as cores predominantes da imagem de forma eficiente. Um algoritmo de filtragem personalizado garante que cores muito semelhantes não sejam incluídas na paleta final.

Substituição de Cores: A função replace_color em image_editor.py itera sobre os pixels da imagem e substitui as cores que estão dentro de uma certa tolerância de distância da cor original, permitindo uma substituição precisa.
