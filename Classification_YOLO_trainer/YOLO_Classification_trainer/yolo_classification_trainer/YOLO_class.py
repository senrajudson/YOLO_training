from ultralytics import YOLO
import shutil
import os
import re

class YOLOClassificationTrainer:
    def __init__(self):
        self._image_folder = None
        self._percentual_data_divisor = None
        self._predict_object = None
        
    @property
    def image_folder(self):
        return self._image_folder
    
    @image_folder.setter
    def image_folder(self, folder):
        self._image_folder = folder
    
    @property
    def percentual_data_divisor(self):
        return self._percentual_data_divisor
    
    @percentual_data_divisor.setter
    def percentual_data_divisor(self, divisor):
        self._percentual_data_divisor = divisor
    
    @property
    def predict_object(self):
        return self._predict_object

    @predict_object.setter
    def predict_object(self, object):
        self._predict_objetc = object

    def slicing_dataset_for_traning(self):

        list_archives = [self.image_folder]
        yolo_dataset_dir = "datasets/dataset_YOLO"
        os.makedirs(yolo_dataset_dir, exist_ok=True)

        # Padrão para encontrar a última pasta no caminho
        padrao = re.compile(r'\/([^\/]+)\/?$')
        # Substituir a última pasta por uma string vazia
        novo_caminho = re.sub(padrao, '', self.yolo_Classes)

        if self._yolo_Classes:
            yolo_classes_path = os.path.join(f"{novo_caminho}", "classes.txt")
            shutil.copy(yolo_classes_path, yolo_dataset_dir)

        if self._yolo_Notes:
            yolo_notes_path = os.path.join(f"{novo_caminho}", "notes.json")
            shutil.copy(yolo_notes_path, yolo_dataset_dir)

        for folder in list_archives:
            if folder != None:
                path_folder, name_folder = folder
                counter = 0
                for file in os.listdir(path_folder):
                    path_file = os.path.join(path_folder, file)


                    if os.path.isfile(path_file):
                        os.makedirs(f"datasets/dataset_YOLO/{name_folder}/train", exist_ok=True)
                        os.makedirs(f"datasets/dataset_YOLO/{name_folder}/test", exist_ok=True)

                        if counter >= (len(os.listdir(path_folder))*(100-int(self.test_percentual_divisor))/100):
                            destination = f"datasets/dataset_YOLO/{name_folder}/test"
                        else:
                            destination = f"datasets/dataset_YOLO/{name_folder}/train"
                            counter += 1

                        path_destination = os.path.join(destination, file)
                        shutil.copy(path_file, path_destination)

    def training_YOLO_model(self, YOLO_model="yolov8m-cls.pt", num_epochs=10,img_size=640, training_device="cuda"):
        model = YOLO(YOLO_model)
        results = model.train(data = "datasets/dataset_YOLO/dataset.yaml", epochs=num_epochs, imgsz=img_size, device=training_device)
        return results

    def predict_YOLO_model(self, YOLO_model="runs/detect/train/weights/best.pt", save_predict=True, img_size=640, predict_confidence=0.7):
        model = YOLO(YOLO_model)
        model.predict(self.object_to_predict, save=save_predict, imgz=img_size, conf=predict_confidence)
    
