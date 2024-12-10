def cvat_dataset(path_folder, output_folder_name):
    import shutil
    import os
    import re

    """
    Uma função para separar os arquivos de um dataset importado pelo CVAT
    """

    path_folder = f"{path_folder}/obj_Train_data"
    os.makedirs(f"{output_folder_name}/images", exist_ok=True)
    os.makedirs(f"{output_folder_name}/labels", exist_ok=True)

    image_path  = f"{output_folder_name}/images"
    text_path = f"{output_folder_name}/labels"
    text = re.compile(r'\.txt')
    image = re.compile(r'\.png')

    for file in os.listdir(path_folder):
        path_file = os.path.join(path_folder, file)

        if image.search(file):
            file_destination = os.path.join(image_path, file)
            shutil.copy(path_file, file_destination)
            continue

        if text.search(file):
            file_destination = os.path.join(text_path, file)
            shutil.copy(path_file, file_destination)
            continue
        
        print("???", file)
