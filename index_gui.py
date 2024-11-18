import subprocess
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def open_other_page(model_name):
    # Executa o arquivo da outra página, passando o nome do modelo como argumento
    venv_python = Path(sys.executable)  # Usa o Python atual do ambiente virtual
    subprocess.run([venv_python, "model_gui.py", model_name])
    print(f'Button {model_name} clicked')


window = Tk()

window.geometry("700x550")
window.configure(bg="#333333")
window.title("Seleção de Modelos")

canvas = Canvas(
    window,
    bg="#333333",
    height=550,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    52.0,
    image=image_image_1
)

canvas.create_text(
    40.0,
    32.0,
    anchor="nw",
    text="RECONHECIMENTO DE IMAGEM",
    fill="#FFFFFF",
    font=("Noto Sans", 29 * -1)
)

canvas.create_rectangle(
    27.0,
    72.0,
    279.0,
    78.0,
    fill="#9D00FE",
    outline="")

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    350.0,
    165.0,
    image=image_image_2
)

canvas.create_text(
    189.0,
    139.0,
    anchor="nw",
    text=" Esse projeto é uma demonstração do uso de inteligência artificial para o\n reconhecimento de imagens. Essa funcionalidade pode ser usada para diversas\n finalidades, podendo ser muito útil em nossas rotinas.",
    fill="#FFFFFF",
    font=("Noto Sans", 13 * -1)
)

canvas.create_text(
    536.0,
    528.0,
    anchor="nw",
    text="images designed by: flaticon.com",
    fill="#FFFFFF",
    font=("Noto Sans", 10 * -1)
)

canvas.create_text(
    47.0,
    152.0,
    anchor="nw",
    text="PROJETO",
    fill="#9D00FE",
    font=("Noto Sans", 22 * -1)
)

canvas.create_rectangle(
    36.99755859375,
    181.5,
    123.00000064569986,
    184.00000000484903,
    fill="#FFFFFF",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_other_page("face_landmarker"),
    relief="flat"
)
button_1.place(
    x=110.0,
    y=223.0,
    width=118.0,
    height=159.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_other_page("gesture_recognizer"),
    relief="flat"
)
button_2.place(
    x=290.0,
    y=223.0,
    width=118.0,
    height=159.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_other_page("object_detector"),
    relief="flat"
)
button_3.place(
    x=471.0,
    y=223.0,
    width=118.0,
    height=159.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_other_page("image_classifier"),
    relief="flat"
)
button_4.place(
    x=196.0,
    y=386.0,
    width=118.0,
    height=159.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_other_page("pose_landmarker"),
    relief="flat"
)
button_5.place(
    x=386.0,
    y=386.0,
    width=118.0,
    height=159.0
)
window.resizable(False, False)
window.mainloop()
