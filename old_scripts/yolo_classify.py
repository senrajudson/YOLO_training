from ultralytics import YOLO
from PIL import Image
import numpy as np
import os

# Lista de imagens de exemplo
dir_img = "Objects_to_predict"
imagens_de_exemplo = os.listdir(dir_img)
# print(imagens_de_exemplo)

# Testar recebimento de imagens da fila de teste
def model_Yolo_classification():
  model = YOLO("runs/classify/train/weights/best.pt")

  def receber_imagem_da_fila_teste():
    if imagens_de_exemplo:
        return imagens_de_exemplo.pop(0)  # Remover e retornar a primeira imagem da lista
    else:
        return None  # Retorna None se a lista estiver vazia
    
  while True:
    imagem = receber_imagem_da_fila_teste()
    if imagem is None:
      print(['#########END##########'])
      break

    image_pil = Image.open(f"{dir_img}/{imagem}")
    image_array = np.array(image_pil)
    #f"{dir_img}/{imagem}"
    resultado = model.predict(image_array , imgsz=640, conf=0.8, verbose=False)
    for result in resultado:
      
      # Encontrar a classe com a maior probabilidade de inferência
      max_prob_class = max(result.names, key=lambda k: result.names[k])
      max_prob_class_cpu = result.probs.cpu()
      max_prob_class_np = max_prob_class_cpu.numpy()
      class_names = result.names[max_prob_class]
      class_prob_value = max_prob_class_np.top5conf[0]

      if float(class_prob_value) < 0.9:
         print(f"A imagem {imagem} é classificada como '{class_names}' com probabilidade {class_prob_value} está abaixo do padrão.")
         continue
      
      print(f"A imagem {imagem} é classificada como '{class_names}' com probabilidade {class_prob_value}.")

model_Yolo_classification()


    # resultado = model.predict(objectToPredict , imgsz=640, conf=predict_confidence, verbose=True)
    # for result in resultado:
      
    # #   # Encontrar a classe com a maior probabilidade de inferência
    # #   max_prob_class = max(result.names, key=lambda k: result.names[k])
    # #   max_prob_class_cpu = result.probs.cpu()
    # #   max_prob_class_np = max_prob_class_cpu.numpy()
    # #   class_names = result.names[max_prob_class]
    # #   class_prob_value = max_prob_class_np.top5conf[0]
    #   boxes = result.boxes
    #   conf = boxes.conf
    #   cls = boxes.cls
    #   result.save(filename=f"{objectToPredict}")

    # # Run batched inference on a list of images
    # results = model(objectToPredict)  # return a generator of Results objects
    # # Process results generator
    # for result in results:
    #     device = result.cuda()
    #     boxes = result.boxes  # Boxes object for bounding box outputs
    #     conf = boxes.conf
    #     cls = boxes.cls
    #     fmt = boxes.xywhn
    #     masks = result.masks  # Masks object for segmentation masks outputs
    #     keypoints = result.keypoints  # Keypoints object for pose outputs
    #     probs = result.probs  # Probs object for classification outputs
    #     obb = result.obb  # Oriented boxes object for OBB outputs
    #     result.save(filename=f"predicted.avi")  # save to disk
    #     print(objectToPredict)
