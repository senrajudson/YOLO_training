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
        yolo_dataset_dir = "dataset_YOLO"
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
                        os.makedirs(f"dataset_YOLO/train/{name_folder}", exist_ok=True)
                        os.makedirs(f"dataset_YOLO/val/{name_folder}", exist_ok=True)

                        if counter >= (len(os.listdir(path_folder))*(100-int(self.test_percentual_divisor))/100):
                            destination = f"dataset_YOLO/val/{name_folder}"
                        else:
                            destination = f"dataset_YOLO/train/{name_folder}"
                            counter += 1
                        
                        path_destination = os.path.join(destination, file)
                        shutil.copy(path_file, path_destination)

    def training_YOLO_model(self):
        conteudo = os.listdir("dataset_YOLO")
        for item in conteudo:
            print(item)
        model = YOLO("yolov8n.pt")
        results = model.train(data = "dataset_YOLO", epochs=10, imgsz=640)

        return results


