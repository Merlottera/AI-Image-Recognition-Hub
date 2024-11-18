import sys
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from PIL import Image, ImageTk, ImageDraw
import cv2

import apply_models


model_name = sys.argv[1]


# Inicializa a webcam
webcam = cv2.VideoCapture(0)

# Caminhos dos arquivos
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def add_rounded_corners(img, corner_radius):
    """Aplica cantos arredondados a uma imagem PIL."""
    # Cria uma máscara com cantos arredondados
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)

    # Desenha um retângulo arredondado
    draw.rounded_rectangle(
        [(0, 0), img.size],
        corner_radius,
        fill=255
    )

    # Aplica a máscara na imagem original
    img.putalpha(mask)
    return img

# Função para atualizar o feed da webcam no Canvas
def update_frame():
    validacao, frame = webcam.read()

    if validacao:
        # Converte o frame para RGB e redimensiona
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (404, 276))

        # Aplica detecção facial
        frame_rgb = apply_models.main(model_name, frame_rgb)

        img_pil = Image.fromarray(frame_rgb)

        # Aplica os cantos arredondados
        img_pil = add_rounded_corners(img_pil, 10)

        # Converte o objeto PIL para um formato que o Tkinter reconhece (PhotoImage)
        img_tk = ImageTk.PhotoImage(img_pil)

        # Atualiza a imagem no Canvas
        canvas.itemconfig(image_2, image=img_tk)
        canvas.image_tk = img_tk  # Mantém uma referência à imagem para evitar coleta de lixo

        window.current_image = img_pil  # Armazena a imagem PIL

    # Chama a função repetidamente para atualizar o frame
    window.after(10, update_frame)


# Armazena as imagens capturadas para evitar o erro
captured_images = [None, None, None, None]  # Para armazenar as imagens em image_3, image_4, image_5 e image_6

def capture_image():
    # Verifica se existe uma imagem atual armazenada
    if hasattr(window, 'current_image') and window.current_image is not None:

        # Move as imagens de baixo para cima
        captured_images[3] = captured_images[2]
        captured_images[2] = captured_images[1]
        captured_images[1] = captured_images[0]

        # Redimensiona a imagem atual para caber no `image_3`
        img_pil_resized = window.current_image.resize((122, 69))  # Ajuste o tamanho para o `image_3`
        img_tk = ImageTk.PhotoImage(img_pil_resized)

        # Armazena a imagem atual na posição 0
        captured_images[0] = img_tk

        # Atualiza os canvas com as novas imagens
        if captured_images[0] is not None:
            canvas.itemconfig(image_3, image=captured_images[0])
            canvas.image_3 = captured_images[0]  # Mantém a referência

        if captured_images[1] is not None:
            canvas.itemconfig(image_4, image=captured_images[1])
            canvas.image_4 = captured_images[1]  # Mantém a referência

        if captured_images[2] is not None:
            canvas.itemconfig(image_5, image=captured_images[2])
            canvas.image_5 = captured_images[2]  # Mantém a referência

        if captured_images[3] is not None:
            canvas.itemconfig(image_6, image=captured_images[3])
            canvas.image_6 = captured_images[3]  # Mantém a referência


# Configurando a GUI
window = Tk()
window.geometry("700x550")
window.configure(bg="#FFFFFF")
window.title(f"Demo do modelo {model_name}")

canvas = Canvas(window, bg="#FFFFFF", height=550, width=700, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(350.0, 275.0, image=image_image_1)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=capture_image, relief="flat")
button_1.place(x=72.0, y=460.0, width=358.0, height=71.0)

canvas.create_text(40.0, 32.0, anchor="nw", text="RECONHECIMENTO DE IMAGEM", fill="#FFFFFF", font=("Noto Sans", 29 * -1))
canvas.create_rectangle(27.0, 72.0, 279.0, 78.0, fill="#9D00FE", outline="")

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(251.0, 277.0, anchor="center")

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(590.0, 141.0, image=image_image_3)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(590.0, 230.0, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(590.0, 319.0, image=image_image_5)

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(590.0, 408.0, image=image_image_6)

# Inicia a função de atualizar o frame
update_frame()

window.resizable(False, False)
window.mainloop()

# Libera a webcam após o fechamento da janela
webcam.release()
cv2.destroyAllWindows()
