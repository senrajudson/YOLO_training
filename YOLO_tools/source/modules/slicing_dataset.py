from source.modules.augmentations import aug_dataset 
from sklearn.model_selection import train_test_split
import shutil
import json
import os

""" 
função para dividir imagens e labels em train e val
a depender da task, detect ou classify
"""

def slicing_dataset_for_traning(task, imageFolder, annotationsFolder, yoloClasses, TestPercentualDivisor, dataset_path, aug, n_aug, odd):
        
        if task == 'detect':
            detect_YOLO_dataset(imageFolder, annotationsFolder, yoloClasses, TestPercentualDivisor, dataset_path)

        if task == 'classify':
            classify_YOLO_dataset(imageFolder, yoloClasses, TestPercentualDivisor, dataset_path)

        if task == 'COCO':
            detect_COCO_dataset(imageFolder, annotationsFolder, yoloClasses, TestPercentualDivisor, dataset_path)

        if aug:
            aug_dataset(task, dataset_path, n_aug, odd)

def detect_COCO_dataset(imageFolder, coco_annotation_path, yoloClasses, test_size, output_dir, random_state=42):

    os.makedirs(f"datasets/{output_dir}", exist_ok=True)
    path_folder, name_folder = imageFolder
    for file in os.listdir(path_folder):
        path_file = os.path.join(path_folder, file)

        if os.path.isfile(path_file):
            os.makedirs(f"datasets/{output_dir}/{name_folder}", exist_ok=True)
            destination = f"datasets/{output_dir}/{name_folder}"
            path_destination = os.path.join(destination, file)
            shutil.copy(path_file, path_destination)

    ann_path, ann_name = (coco_annotation_path, 'annotations')
    
    # Carregar o arquivo de anotações COCO
    with open(f"{ann_path}/instances_default.json", 'r') as f:
        coco_data = json.load(f)

    # Extrair as imagens e anotações
    images = coco_data['images']
    annotations = coco_data['annotations']

    # Dividir as imagens em treino e validação
    train_images, val_images = train_test_split(
        images, test_size=test_size, random_state=random_state
    )

    # Criar um mapa para associar as imagens às anotações
    train_image_ids = {img['id'] for img in train_images}
    val_image_ids = {img['id'] for img in val_images}

    train_annotations = [ann for ann in annotations if ann['image_id'] in train_image_ids]
    val_annotations = [ann for ann in annotations if ann['image_id'] in val_image_ids]

    # Estruturar os novos conjuntos de dados
    train_data = {
        'info': coco_data['info'],
        'licenses': coco_data['licenses'],
        'images': train_images,
        'annotations': train_annotations,
        'categories': coco_data['categories']
    }

    val_data = {
        'info': coco_data['info'],
        'licenses': coco_data['licenses'],
        'images': val_images,
        'annotations': val_annotations,
        'categories': coco_data['categories']
    }

    # Salvar os arquivos separados
    os.makedirs(f"datasets/{output_dir}/{ann_name}", exist_ok=True)
    train_path = os.path.join(f"datasets/{output_dir}/{ann_name}", 'train.json')
    val_path = os.path.join(f"datasets/{output_dir}/{ann_name}", 'val.json')
    
    with open(train_path, 'w') as f:
        json.dump(train_data, f, indent=4)
    
    with open(val_path, 'w') as f:
        json.dump(val_data, f, indent=4)

    with open(f"datasets/{output_dir}/dataset.yaml", "w") as file:
        if isinstance(yoloClasses, list):
            nc = len(yoloClasses)
            names = f"{yoloClasses}"
        else:
            nc = 1
            names = f"['{yoloClasses}']"

        file.write(
    f"""
    path: {output_dir}
    train: annotations/train.json
    val: annotations/val.json
    nc: {nc}
    names: {names}
    """
            )

def detect_YOLO_dataset(imageFolder, annotationsFolder, yoloClasses, TestPercentualDivisor, dataset_path):

    annotationsFolder = (annotationsFolder, "labels")

    list_archives = [imageFolder, annotationsFolder]

    os.makedirs(f"datasets/{dataset_path}", exist_ok=True)

    for folder in list_archives:
        if folder != None:
            path_folder, name_folder = folder
            counter = 0
            for file in os.listdir(path_folder):
                path_file = os.path.join(path_folder, file)

                if os.path.isfile(path_file):
                    os.makedirs(f"datasets/{dataset_path}/{name_folder}/train", exist_ok=True)
                    os.makedirs(f"datasets/{dataset_path}/{name_folder}/val", exist_ok=True)

                    if counter >= (len(os.listdir(path_folder))*(1-TestPercentualDivisor)):
                        destination = f"datasets/{dataset_path}/{name_folder}/val"
                    else:
                        destination = f"datasets/{dataset_path}/{name_folder}/train"
                        counter += 1
                    
                    path_destination = os.path.join(destination, file)
                    shutil.copy(path_file, path_destination)

    with open(f"datasets/{dataset_path}/dataset.yaml", "w") as file:
        if isinstance(yoloClasses, list):
            nc = len(yoloClasses)
            names = "\n".join([f"  {i}: '{v}'" for i, v in enumerate(yoloClasses)])
        else:
            nc = 1
            names = f"  0: '{yoloClasses}'"

        file.write(
    f"""
    path: {dataset_path}
    train: images/train
    val: images/val
    nc: {nc}
    names:
    {names}
    """
            )

    # Construa o dicionário de dados.
    if isinstance(yoloClasses, list):
        categories = [{"id": i, "name": name} for i, name in enumerate(yoloClasses)]
    else:
        categories = [{"id": 0, "name": yoloClasses}]

    data = {
        "categories": categories,
        "info": {
            "year": 2024,
            "version": "1.0",
            "contributor": "senrajudson"
        }
    }

    with open(f"datasets/{dataset_path}/notes.json", "w") as file:
        json.dump(data, file, indent=2)

    if isinstance(yoloClasses, list):
        classes = "\n".join(yoloClasses)
    else:
        classes = yoloClasses

    data = f"""
{classes}
"""

    with open(f"datasets/{dataset_path}/classes.txt", "w") as file:
        file.write(
f"""{data}
"""
)
        
def classify_YOLO_dataset(imageFolder, yoloClasses, TestPercentualDivisor, dataset_path):

    os.makedirs(f"datasets/{dataset_path}", exist_ok=True)
    caminho_pasta, nome_pasta = imageFolder

    for folder in os.listdir(caminho_pasta):
        path_folder = '/'.join([caminho_pasta, folder])
        print(folder)
        print(path_folder)
        if folder != None:
            counter = 0
            for file in os.listdir(path_folder):
                path_file = os.path.join(path_folder, file)

                if os.path.isfile(path_file):
                    os.makedirs(f"datasets/{dataset_path}/train/{folder}", exist_ok=True)
                    os.makedirs(f"datasets/{dataset_path}/val/{folder}", exist_ok=True)

                    if counter >= (len(os.listdir(path_folder))*(1-TestPercentualDivisor)):
                        destination = f"datasets/{dataset_path}/val/{folder}"
                    else:
                        destination = f"datasets/{dataset_path}/train/{folder}"
                        counter += 1
                    
                    path_destination = os.path.join(destination, file)
                    shutil.copy(path_file, path_destination)

    if isinstance(yoloClasses, list):
        classes = "\n".join(yoloClasses)
    else:
        classes = yoloClasses

    data = f"""
{classes}
"""

    with open(f"datasets/{dataset_path}/classes.txt", "w") as file:
        file.write(
f"""{data}
"""
        )

    with open(f"datasets/{dataset_path}/dataset.yaml", "w") as file:
        if isinstance(yoloClasses, list):
            nc = len(yoloClasses)
            names = f"{yoloClasses}"
        else:
            nc = 1
            names = f"['{yoloClasses}']"

        file.write(
    f"""
    path: {dataset_path}
    train: train
    val: val
    nc: {nc}
    names: {names}
    """
            )

    # Construa o dicionário de dados.
    if isinstance(yoloClasses, list):
        categories = [{"id": i, "name": name} for i, name in enumerate(yoloClasses)]
    else:
        categories = [{"id": 0, "name": yoloClasses}]

    data = {
        "categories": categories,
        "info": {
            "year": 2024,
            "version": "1.0",
            "contributor": "senrajudson"
        }
    }

    with open(f"datasets/{dataset_path}/notes.json", "w") as file:
        json.dump(data, file, indent=2)
