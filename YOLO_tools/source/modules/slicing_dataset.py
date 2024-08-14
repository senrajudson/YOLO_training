import os
import re
import shutil

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