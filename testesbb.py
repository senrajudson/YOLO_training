import cv2
import numpy as np
import matplotlib.pyplot as plt

# Função para ler as anotações YOLO
def read_yolo_annotations(txt_path, img_width, img_height):
    bboxes = []
    class_labels = []
    with open(txt_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            
            # Convertendo para as coordenadas do formato [x_min, y_min, x_max, y_max]
            x_min = (x_center - width / 2) * img_width
            y_min = (y_center - height / 2) * img_height
            x_max = (x_center + width / 2) * img_width
            y_max = (y_center + height / 2) * img_height
            
            bboxes.append([x_min, y_min, x_max, y_max])
            class_labels.append(class_id)
    return bboxes, class_labels

# Carregar a imagem
image_path = 'D:\Judson_projetos\Yolo_trainer\YOLO_tools\dataset\images\\train\\2024-07-08_11.49.18_0.png'
image = cv2.imread(image_path)

# Obter as dimensões da imagem
img_height, img_width, _ = image.shape

# Caminho do arquivo de anotações
txt_path = 'D:\\Judson_projetos\\Yolo_trainer\\YOLO_tools\\dataset\\labels\\train\\2024-07-08_11.49.18_0.txt'

# Ler as anotações YOLO
bboxes, class_labels = read_yolo_annotations(txt_path, img_width, img_height)

# Desenhar as bounding boxes na imagem
for bbox in bboxes:
    x_min, y_min, x_max, y_max = map(int, bbox)
    # Desenhar a caixa na cor vermelha
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

# Converter a imagem de BGR para RGB (OpenCV usa BGR por padrão)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Exibir a imagem com as bounding boxes usando matplotlib
plt.imshow(image_rgb)
plt.axis('off')  # Não mostrar os eixos
plt.show()
