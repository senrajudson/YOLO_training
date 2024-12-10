from source.modules.augmentations import aug_dataset 
import shutil
import json
import os

""" 
função para dividir imagens e labels em train e val
a depender da task, detect ou classify
"""

def slicing_dataset_for_traning(task, imageFolder, annotationsFolder, yoloClasses, TestPercentualDivisor, dataset_path, aug):
        
        if task == 'detect':
            model_detect(imageFolder, annotationsFolder, yoloClasses, TestPercentualDivisor, dataset_path)

        if task == 'classify':
            model_classify(imageFolder, yoloClasses, TestPercentualDivisor, dataset_path)

        if aug:
            aug_dataset(task, dataset_path)

def model_detect(imageFolder, annotationsFolder, yoloClasses, TestPercentualDivisor, dataset_path):

    list_archives = [imageFolder, annotationsFolder]

    os.makedirs(dataset_path, exist_ok=True)

    for folder in list_archives:
        if folder != None:
            path_folder, name_folder = folder
            counter = 0
            for file in os.listdir(path_folder):
                path_file = os.path.join(path_folder, file)

                if os.path.isfile(path_file):
                    os.makedirs(f"{dataset_path}/{name_folder}/train", exist_ok=True)
                    os.makedirs(f"{dataset_path}/{name_folder}/val", exist_ok=True)

                    if counter >= (len(os.listdir(path_folder))*(100-int(TestPercentualDivisor))/100):
                        destination = f"{dataset_path}/{name_folder}/val"
                    else:
                        destination = f"{dataset_path}/{name_folder}/train"
                        counter += 1
                    
                    path_destination = os.path.join(destination, file)
                    shutil.copy(path_file, path_destination)

    with open(f"{dataset_path}/dataset.yaml", "w") as file:
        if isinstance(yoloClasses, list):
            nc = len(yoloClasses)
            names = "\n".join([f"  {i}: '{v}'" for i, v in enumerate(yoloClasses)])
        else:
            nc = 1
            names = f"  0: '{yoloClasses}'"

        file.write(
    f"""path: {dataset_path}
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

    with open(f"{dataset_path}/notes.json", "w") as file:
        json.dump(data, file, indent=2)

    if isinstance(yoloClasses, list):
        classes = "\n".join(yoloClasses)
    else:
        classes = yoloClasses

    data = f"""
{classes}
"""

    with open(f"{dataset_path}/classes.txt", "w") as file:
        file.write(
f"""{data}
"""
)
        
def model_classify(imageFolder, yoloClasses, TestPercentualDivisor, dataset_path):

    os.makedirs(dataset_path, exist_ok=True)
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
                    os.makedirs(f"{dataset_path}/train/{folder}", exist_ok=True)
                    os.makedirs(f"{dataset_path}/val/{folder}", exist_ok=True)

                    if counter >= (len(os.listdir(path_folder))*(100-int(TestPercentualDivisor))/100):
                        destination = f"{dataset_path}/val/{folder}"
                    else:
                        destination = f"{dataset_path}/train/{folder}"
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

    with open(f"{dataset_path}/classes.txt", "w") as file:
        file.write(
f"""{data}
"""
)