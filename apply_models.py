from PIL import ImageFont, ImageDraw, Image
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import sys

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 2
TEXT_COLOR = (255, 0, 0)  # red


# Face Landmarker model object
base_options = python.BaseOptions(model_asset_path='models/face_landmarker_v2_with_blendshapes.task')
options = vision.FaceLandmarkerOptions(base_options=base_options, num_faces=1)
face_landmarker = vision.FaceLandmarker.create_from_options(options)

# Gesture Recognizer model object
base_options = python.BaseOptions(model_asset_path='models/gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

# Object Detector model object
base_options = python.BaseOptions(model_asset_path='models/efficientdet.tflite')
options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.5)
detector = vision.ObjectDetector.create_from_options(options)

# Image Classifier model object
base_options = python.BaseOptions(model_asset_path='models/classifier.tflite')
options = vision.ImageClassifierOptions(base_options=base_options, max_results=4)
classifier = vision.ImageClassifier.create_from_options(options)

# Pose Landmarker model object
base_options = python.BaseOptions(model_asset_path='models/pose_landmarker.task')
options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
pose_detector = vision.PoseLandmarker.create_from_options(options)


# Função para desenhar os landmarks de detecção facial
def draw_face_landmarker_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image


# Mapeamento de gestos para emojis
# Mapeamento de gestos para emojis
gesture_to_emoji = {
    "None": "emojis/x.png",  # Caminho para o emoji X
    "Closed_Fist": "emojis/closed_fist.png",  # Caminho para o emoji de punho fechado
    "Open_Palm": "emojis/open_palm.png",  # Caminho para o emoji de palma aberta
    "Pointing_Up": "emojis/pointing_up.png",  # Caminho para o emoji de apontar para cima
    "Thumb_Down": "emojis/thumb_down.png",  # Caminho para o emoji de polegar para baixo
    "Thumb_Up": "emojis/thumb_up.png",  # Caminho para o emoji de polegar para cima
    "Victory": "emojis/victory.png",  # Caminho para o emoji de vitória
    "ILoveYou": "emojis/i_love_you.png"  # Caminho para o emoji de eu te amo
}

def draw_gesture_recognizer_on_image(frame_rgb, gesture_name):
    # Converte o frame RGB do OpenCV (numpy array) para uma imagem PIL
    img_pil = Image.fromarray(frame_rgb)

    # Obtém o caminho da imagem do emoji correspondente ao gesto
    emoji_path = gesture_to_emoji.get(gesture_name, gesture_to_emoji["None"])  # Usa o emoji X como fallback

    try:
        # Abre a imagem do emoji
        emoji_image = Image.open(emoji_path).convert("RGBA")
    except IOError:
        print("A imagem do emoji não foi encontrada. Verifique o nome e o caminho do arquivo.")
        return frame_rgb  # Retorna o frame original se não conseguir carregar a imagem

    # Redimensiona o emoji se necessário
    emoji_image = emoji_image.resize((70, 70))  # Ajuste o tamanho conforme necessário

    # Calcula a posição do emoji: centralizado na parte inferior
    img_width, img_height = img_pil.size
    emoji_width, emoji_height = emoji_image.size
    position = ((img_width - emoji_width) // 2, img_height - emoji_height - 10)  # Ajuste a posição conforme necessário

    # Coloca o emoji na imagem
    img_pil.paste(emoji_image, position, emoji_image)  # Usa a máscara para preservar a transparência

    # Converte a imagem PIL de volta para um frame RGB (numpy array) do OpenCV
    annotated_image = np.array(img_pil)

    return annotated_image


def draw_object_detector_on_image(image, detection_result) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (MARGIN + bbox.origin_x,
                     MARGIN + ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text.upper(), text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

  return image


def draw_image_classifier_on_image(frame_rgb, classification_result):
    # Converte o frame RGB do OpenCV (numpy array) para uma imagem PIL
    img_pil = Image.fromarray(frame_rgb)

    # Cria um objeto de desenho da PIL
    draw = ImageDraw.Draw(img_pil)

    # Carrega a fonte personalizada
    font = ImageFont.truetype('Montserrat-Semibold.ttf', 30)

    # Define a posição do texto: centralizado na parte inferior
    text_bbox = draw.textbbox((0, 0), classification_result, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width, image_height = img_pil.size
    position = ((image_width - text_width) // 2, image_height - text_height - 10)  # 10px de margem inferior

    # Adiciona borda ao redor do texto para simular o negrito
    # Desenha o texto ligeiramente deslocado em várias direções para criar um efeito de borda
    for x_offset, y_offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        draw.text((position[0] + x_offset, position[1] + y_offset), classification_result, font=font, fill=(255, 255, 255))

    # Desenha o texto principal no centro (o preenchimento real)
    draw.text(position, classification_result, font=font, fill=(255, 255, 255))  # Cor branca (R, G, B)

    # Converte a imagem PIL de volta para um frame RGB (numpy array) do OpenCV
    annotated_image = np.array(img_pil)

    return annotated_image


def draw_pose_landmarker_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image


def main(model, frame_rgb):
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    if model == 'face_landmarker':
        detection_result = face_landmarker.detect(mp_image)
        if detection_result.face_landmarks:
            frame_rgb = draw_face_landmarker_on_image(frame_rgb, detection_result)

    elif model == 'gesture_recognizer':
        recognition_result = recognizer.recognize(mp_image)

        if recognition_result.gestures and recognition_result.gestures[0]:
            category_name = recognition_result.gestures[0][0].category_name
        else:
            category_name = None

        if category_name:
            frame_rgb = draw_gesture_recognizer_on_image(frame_rgb, category_name)

    elif model == 'object_detector':
        detection_result = detector.detect(mp_image)
        frame_rgb = draw_object_detector_on_image(frame_rgb, detection_result)

    elif model == 'image_classifier':
        classification_result = classifier.classify(mp_image)
        top_category = classification_result.classifications[0].categories[0]
        classification_text = f"{top_category.category_name} ({top_category.score:.2f})".upper()
        frame_rgb = draw_image_classifier_on_image(frame_rgb, classification_text)

    elif model == 'pose_landmarker':
        detection_result = pose_detector.detect(mp_image)
        frame_rgb = draw_pose_landmarker_on_image(frame_rgb, detection_result)

    return frame_rgb