import os
import shutil
from ultralytics import YOLO
import re

class YOLOTrainer:

    def __init__(self):
        self._image_folder = None
        self._annotations_folder = None
        self._test_percentual_divisor = None
        self._predict_YOLO = None
        self._yolo_Classes = None
        self._yolo_Notes = None
        self._object_to_predict = None
        self._predict_confidence = None

    @property
    def object_to_predict(self):
        return self._object_to_predict
    
    @object_to_predict.setter
    def object_to_predict(self, predict_object):
        self._object_to_predict = predict_object

    @property
    def predict_confidence(self):
        return self._predict_confidence
    
    @predict_confidence.setter
    def predict_confidence(self, confidence):
        self._predict_confidence = confidence

    @property
    def yolo_Classes(self):
        return self._yolo_Classes
    
    @yolo_Classes.setter
    def yolo_Classes(self, path):
        self._yolo_Classes = path

    @property
    def yolo_Notes(self):
        return self._yolo_Notes
    
    @yolo_Notes.setter
    def yolo_Notes(self, path):
        self._yolo_Notes = path

    
    @property
    def predict_YOLO(self):
        return self._predict_YOLO
    
    @predict_YOLO.setter
    def predict_YOLO(self, predict_object):
        self._predict_YOLO = predict_object

    @property
    def annotations_folder(self):
        return self._annotations_folder
    
    @annotations_folder.setter
    def annotations_folder(self, path):
        self._annotations_folder = (path, "labels")

    @property
    def image_folder(self):
        return self._image_folder
    
    @image_folder.setter
    def image_folder(self, path):
        self._image_folder = (path, "images")

    @property
    def test_percentual_divisor(self):
        return self._test_percentual_divisor
    
    @test_percentual_divisor.setter
    def test_percentual_divisor(self, value):
        try:
            toint = int(value)
            self._test_percentual_divisor = toint
        except ValueError:
            "Value expected does not match, expected an integer value"
            

    def slicing_dataset_for_traning(self):

        list_archives = [self.image_folder, self.annotations_folder]
        yolo_dataset_dir = "dataset/dataset_YOLO"
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
                        os.makedirs(f"dataset/dataset_YOLO/{name_folder}/train", exist_ok=True)
                        os.makedirs(f"dataset/dataset_YOLO/{name_folder}/val", exist_ok=True)

                        if counter >= (len(os.listdir(path_folder))*(100-int(self.test_percentual_divisor))/100):
                            destination = f"dataset/dataset_YOLO/{name_folder}/val"
                        else:
                            destination = f"dataset/dataset_YOLO/{name_folder}/train"
                            counter += 1
                        
                        path_destination = os.path.join(destination, file)
                        shutil.copy(path_file, path_destination)

        with open("dataset/dataset_YOLO/dataset.yaml", "w") as file:
            file.write(
"""
path: dataset_YOLO
train: images/train
val: images/val
names:
    0 : "Pelota"
"""
            )

    def training_YOLO_model(self):
        model = YOLO("yolov8n.pt")
        try:
            results = model.train(data = "datasets/dataset_YOLO/dataset.yaml", epochs=10, imgsz=640, device="cuda", amp=False)
        except AssertionError as e:
            e("CUDA is not avaible, switching to cpu")
            results = model.train(data = "datasets/dataset_YOLO/dataset.yaml", epochs=10, imgsz=640, device="cpu")
        # results = model.train(data = "D:/Judson_projetos/Trainer_YOLO/dataset/dataset_YOLO/dataset.yaml", epochs=10, imgsz=640, device="cpu")

        return results
    
    def predict_YOLO_model(self):
        model = (YOLO("runs/detect/train/weights/best.pt"))
        model.predict(self.object_to_predict, save=True, conf=self.predict_confidence, device="cpu")


