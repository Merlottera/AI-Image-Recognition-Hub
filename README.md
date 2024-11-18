# AI Image Recognition Hub

Este projeto é uma demonstração interativa de modelos de inteligência artificial para reconhecimento de imagem, utilizando a biblioteca `MediaPipe` para a detecção de rostos, gestos, objetos, classificações de imagens e landmarks corporais. A aplicação é construída com `Tkinter` para a interface gráfica e `OpenCV` para capturar o feed da webcam.

## Sumário
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Modelos Suportados](#modelos-suportados)
- [Funcionalidades](#funcionalidades)
- [Como Executar](#como-executar)

## Tecnologias Utilizadas
- **Python 3.8+**
- **Tkinter**: Para interface gráfica do usuário.
- **OpenCV**: Para captura de vídeo e manipulação de imagens.
- **PIL (Pillow)**: Para manipulação avançada de imagens.
- **MediaPipe**: Para modelos de reconhecimento facial, gestos, objetos, etc.

## Modelos Suportados
A aplicação suporta a execução dos seguintes modelos de reconhecimento de imagem:

1. **Face Landmarker**: Detecta pontos faciais e traça landmarks.
2. **Gesture Recognizer**: Reconhece gestos com base em landmarks da mão.
3. **Object Detector**: Detecta objetos em tempo real.
4. **Image Classifier**: Classifica imagens em categorias predefinidas.
5. **Pose Landmarker**: Detecta a pose do corpo e landmarks.

## Funcionalidades
- **Captura de Vídeo em Tempo Real**: Exibe o feed da webcam em uma interface Tkinter.
- **Detecção de Faces e Gestos**: Usa `MediaPipe` para reconhecimento em tempo real.
- **Classificação de Imagens e Objetos**: Classifica e detecta objetos em tempo real.
- **Captura de Screenshots**: Permite capturar imagens e armazená-las em uma galeria.

## Como Executar
### Pré-requisitos
Certifique-se de ter o Python 3.8+ instalado e as bibliotecas necessárias. Você pode instalá-las usando o seguinte comando:

```bash
pip install -r requirements.txt
```

### Inicialização
Você pode iniciar o projeto usando o seguinte comando:

```bash
python index_gui.py
```