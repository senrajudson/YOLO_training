import albumentations as A
import cv2
import os

""" 
função para augmentar imagens usando albumentations
"""

def aug_dataset(task, dataset_path, n_aug, odd):
        
        if task == 'detect':
            model_detect(dataset_path, n_aug, odd)

        if task == 'classify':
            model_classify(dataset_path, n_aug, odd)

def read_yolo_annotations(txt_path):
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
            
            bboxes.append([x_center, y_center, width, height])
            class_labels.append(class_id)
    return bboxes, class_labels

# Função para salvar as anotações no formato YOLO
def save_yolo_annotations(txt_path, bboxes, class_labels):

    os.makedirs(os.path.dirname(txt_path), exist_ok=True)

    with open(txt_path, 'w') as f:
        for bbox, class_id in zip(bboxes, class_labels):
            x_center, y_center, width, height = bbox
            # Salvando no formato YOLO
            f.write(f"{int(class_id)} {x_center} {y_center} {width} {height}\n")

def model_detect(dataset_path, n_aug, odd):

    os.makedirs(f"datasets/{dataset_path}", exist_ok=True)
    images = f"datasets/{dataset_path}/images"

    for folder in os.listdir(images):
        if folder != None:
            pasta_imagens = f"datasets/{dataset_path}/images/{folder}"
            pasta_labels = f"datasets/{dataset_path}/labels/{folder}"

            for file in os.listdir(pasta_imagens):

                filename, file_extension = os.path.splitext(file)

                txt_path = "/".join([pasta_labels, f"{filename}.txt"])
                images_folder = pasta_imagens
                img_path = os.path.join(images_folder, file)

                image = cv2.imread(img_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Obter as anotações YOLO
                img_height, img_width, _ = image.shape
                bboxes, class_labels = read_yolo_annotations(txt_path)

                # Definir o Compose com as transformações especificadas
                transform = A.Compose([
                    
                    # Transformações no nível de pixel
                    A.GaussianBlur(blur_limit=(1, 3), p=odd),
                    A.MotionBlur(blur_limit=3, p=odd),
                    A.RandomBrightnessContrast(brightness_limit=0.05, contrast_limit=0.05, p=odd),
                    A.ISONoise(color_shift=(0.005, 0.02), intensity=(0.05, 0.1), p=odd),
                    A.SaltAndPepper(p=odd),
                    A.RandomFog(fog_coef_lower=0.02, fog_coef_upper=0.2, alpha_coef=0.02, p=odd),
                    A.RandomSnow(snow_point_lower=0.02, snow_point_upper=0.2, brightness_coeff=1.2, p=odd),
                    A.RandomRain(slant_lower=-2, slant_upper=2, drop_length=5, drop_width=1, blur_value=2, p=odd),
                    A.RandomSunFlare(flare_roi=(0.5, 0.5, 1.0, 1.0), angle_lower=0.0, src_radius=100, p=odd),
                    
                    # Transformações no nível espacial
                    A.BBoxSafeRandomCrop(erosion_rate=0.1, p=odd),
                    A.SmallestMaxSize(max_size=int(img_width*0.75), p=odd),
                    A.VerticalFlip(p=odd),
                    A.SafeRotate(limit=10, border_mode=0, p=odd),
                    A.GridDropout(ratio=0.1, unit_size_min=30, unit_size_max=60, holes_number_x=1, holes_number_y=1, p=odd),
                    A.HorizontalFlip(p=odd),

                    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'], min_visibility=0.4))

                for i in range(int(n_aug)):
                  
                    # Aplicar as transformações
                    augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)

                    # Obter a imagem e as anotações transformadas
                    transformed_image = augmented['image']
                    transformed_bboxes = augmented['bboxes']
                    transformed_class_labels = augmented['class_labels']

                    ### se não houver bboxes, skipar o save, pois a min visibility era baixa
                    if len(transformed_bboxes) == 0:
                        continue

                    transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR)
                    aug_image_path = '/'.join([pasta_imagens, f"{filename}_{i}.png"])
                    os.makedirs(os.path.dirname(aug_image_path), exist_ok=True)
                    cv2.imwrite(aug_image_path, transformed_image)

                    # Caminho para salvar o novo arquivo de anotações
                    new_txt_path = '/'.join([pasta_labels, f"{filename}_{i}.txt"])
                    save_yolo_annotations(new_txt_path, transformed_bboxes, transformed_class_labels)
        
def model_classify(dataset_path, n_aug, odd):

    os.makedirs(f"datasets/{dataset_path}", exist_ok=True)

    for caminho in os.listdir(f"datasets/{dataset_path}"):
        if caminho != None:
            caminho_pasta = '/'.join([f"datasets/{dataset_path}", caminho])
            
            if os.path.isdir(caminho_pasta):
                for folder in os.listdir(caminho_pasta):
                    if folder != None:
                        pasta = '/'.join([caminho_pasta, folder])

                        for file in os.listdir(pasta):

                            filename, file_extension = os.path.splitext(file)
                            images_folder = pasta
                            img_path = os.path.join(images_folder, file)

                            image = cv2.imread(img_path)
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            img_height, img_width, _ = image.shape
                            
                            # Definir o Compose com as transformações especificadas
                            transform = A.Compose([
                                
                                # Transformações no nível de pixel
                                A.GaussianBlur(blur_limit=(1, 3), p=odd),
                                A.MotionBlur(blur_limit=3, p=odd),
                                A.RandomBrightnessContrast(brightness_limit=0.05, contrast_limit=0.05, p=odd),
                                A.ISONoise(color_shift=(0.005, 0.02), intensity=(0.05, 0.1), p=odd),
                                A.SaltAndPepper(p=odd),
                                A.RandomFog(fog_coef_lower=0.02, fog_coef_upper=0.2, alpha_coef=0.02, p=odd),
                                A.RandomSnow(snow_point_lower=0.02, snow_point_upper=0.2, brightness_coeff=1.2, p=odd),
                                A.RandomRain(slant_lower=-2, slant_upper=2, drop_length=5, drop_width=1, blur_value=2, p=odd),
                                A.RandomSunFlare(flare_roi=(0.5, 0.5, 1.0, 1.0), angle_lower=0.0, src_radius=100, p=odd),
                                
                                # Transformações no nível espacial
                                A.RandomGridShuffle(grid=(2, 2), p=odd),
                                A.SmallestMaxSize(max_size=int(img_width*0.75), p=odd),
                                A.VerticalFlip(p=odd),
                                A.SafeRotate(limit=10, border_mode=0, p=odd),
                                A.GridDropout(ratio=0.1, unit_size_min=30, unit_size_max=60, holes_number_x=1, holes_number_y=1, p=odd),
                                A.HorizontalFlip(p=odd),
                            ])
                            
                            for i in range(int(n_aug)):

                                # Aplicar as transformações
                                augmented = transform(image=image)
                                transformed_image = augmented['image']
                                transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR)

                                aug_image_path = '/'.join([pasta, f"{filename}_{i}.png"])
                                os.makedirs(os.path.dirname(aug_image_path), exist_ok=True)
                                cv2.imwrite(aug_image_path, transformed_image)

