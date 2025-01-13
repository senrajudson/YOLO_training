import albumentations as A
import json
import cv2
import os

""" 
função para augmentar imagens usando albumentations
"""

def aug_dataset(task, dataset_path, n_aug, odd):
        
        if task == 'detect':
            aug_YOLO_detect(dataset_path, n_aug, odd)

        if task == 'classify':
            aug_YOLO_classify(dataset_path, n_aug, odd)

        if task == 'COCO':
            aug_COCO_detect(dataset_path, n_aug, odd)

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

def aug_YOLO_detect(dataset_path, n_aug, odd):

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
                    A.GaussianBlur(blur_limit=(2, 5), p=odd),
                    A.MotionBlur(blur_limit=5, p=odd),
                    A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=odd),
                    A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.2), p=odd),
                    A.SaltAndPepper(p=odd),
                    A.RandomFog(fog_coef_lower=0.05, fog_coef_upper=0.2, alpha_coef=0.05, p=odd),
                    A.RandomSnow(snow_point_lower=0.05, snow_point_upper=0.2, brightness_coeff=1.5, p=odd),
                    A.RandomRain(slant_lower=-3, slant_upper=3, drop_length=5, drop_width=2, blur_value=5, p=odd),
                    A.RandomSunFlare(flare_roi=(0.5, 0.5, 1.0, 1.0), angle_lower=0.0, src_radius=30, p=odd, method="physics_based"),
                    
                    # Transformações no nível espacial
                    A.BBoxSafeRandomCrop(erosion_rate=0.3, p=odd),
                    # A.SmallestMaxSize(max_size=int(img_width*0.75), p=odd),
                    A.SmallestMaxSize(max_size=None, max_size_hw=(int(img_height*0.5), int(img_width*0.5)), p=odd),
                    A.VerticalFlip(p=odd),
                    A.SafeRotate(limit=20, border_mode=0, p=odd),
                    A.GridDropout(ratio=0.1, unit_size_min=30, unit_size_max=60, holes_number_x=1, holes_number_y=1, p=odd),
                    A.HorizontalFlip(p=odd),

                    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'], min_visibility=0.7))

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
        
def aug_YOLO_classify(dataset_path, n_aug, odd):

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
                                A.RandomSunFlare(flare_roi=(0.5, 0.5, 1.0, 1.0), angle_lower=0.0, src_radius=30, p=odd),
                                
                                # Transformações no nível espacial
                                A.RandomGridShuffle(grid=(2, 2), p=odd),
                                # A.SmallestMaxSize(max_size=int(img_width*0.75), p=odd),
                                A.SmallestMaxSize(max_size=None, max_size_hw=(int(img_height*0.75), int(img_width*0.75)), p=odd),
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

def aug_COCO_detect(dataset_path, n_aug, odd):
    os.makedirs(f"datasets/{dataset_path}", exist_ok=True)
    images_dir = f"datasets/{dataset_path}/images"
    train_annotations_file = f"datasets/{dataset_path}/annotations/train.json"
    val_annotations_file = f"datasets/{dataset_path}/annotations/val.json"

    # Função auxiliar para processar um arquivo de anotações
    def process_annotations(annotations_file, images_dir):
        with open(annotations_file, 'r') as f:
            coco_data = json.load(f)

        images = coco_data['images']
        annotations = coco_data['annotations']
        categories = coco_data['categories']

        # Inicializar ID único para novas anotações
        next_image_id = max(image['id'] for image in images) + 1
        next_annotation_id = max(annotation['id'] for annotation in annotations) + 1

        for image_info in images:
            img_id = image_info['id']
            img_path = os.path.join(images_dir, image_info['file_name'])

            image = cv2.imread(img_path)
            if image is None:
                continue  # Ignorar imagens que não existem
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img_height, img_width, _ = image.shape

            # Filtrar anotações relacionadas a essa imagem
            img_annotations = [ann for ann in annotations if ann['image_id'] == img_id]

            bboxes = []
            class_labels = []
            for ann in img_annotations:
                bbox = ann['bbox']
                coco_bbox = [bbox[0] / img_width, bbox[1] / img_height, bbox[2] / img_width, bbox[3] / img_height]
                bboxes.append(coco_bbox)
                class_labels.append(ann['category_id'])

                transform = A.Compose([

                    A.GaussianBlur(blur_limit=(1, 2), p=odd),
                    A.RandomBrightnessContrast(brightness_limit=0.05, contrast_limit=0.05, p=odd),
                    A.ISONoise(color_shift=(0.005, 0.02), intensity=(0.05, 0.1), p=odd),
                    A.SaltAndPepper(p=odd),
                    
                    A.BBoxSafeRandomCrop(erosion_rate=0.05, p=odd),
                    # A.SmallestMaxSize(max_size=int(img_width*0.75), p=odd),
                    A.SmallestMaxSize(max_size=None, max_size_hw=(int(img_height*0.75), int(img_width*0.75)), p=odd),
                    A.VerticalFlip(p=odd),
                    A.SafeRotate(limit=10, border_mode=0, p=odd),
                    A.HorizontalFlip(p=odd),

                ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels'], min_visibility=0.4))

            def validate_bbox(bbox):
                x_min, y_min, x_max, y_max = bbox
                if (0.0 <= x_min <= 1.0 and 0.0 <= y_min <= 1.0 and 0.0 <= x_max <= 1.0 and 0.0 <= y_max <= 1.0):
                    return False
                if x_min >= x_max or y_min >= y_max:
                    return True
                return False

            for i in range(int(n_aug)):
                augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)

                transformed_image = augmented['image']
                transformed_bboxes = augmented['bboxes']
                transformed_class_labels = augmented['class_labels']
                invalid_bboxes = [validate_bbox(bbox) for bbox in augmented['bboxes']]

                if invalid_bboxes:
                    continue

                if len(transformed_bboxes) == 0:
                    continue

                transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR)
                aug_filename = f"{os.path.splitext(image_info['file_name'])[0]}_{i}.png"
                aug_image_path = os.path.join(images_dir, aug_filename)
                cv2.imwrite(aug_image_path, transformed_image)

                new_image_id = next_image_id
                images.append({
                    'id': new_image_id,
                    'file_name': aug_filename,
                    'width': img_width,
                    'height': img_height
                })
                next_image_id += 1

                for bbox, label in zip(transformed_bboxes, transformed_class_labels):
                    x_min, y_min, w, h = bbox
                    abs_bbox = [x_min * img_width, y_min * img_height, w * img_width, h * img_height]

                    annotations.append({
                        'id': next_annotation_id,
                        'image_id': new_image_id,
                        'category_id': label,
                        'bbox': abs_bbox,
                        'area': abs_bbox[2] * abs_bbox[3],
                        'iscrowd': 0
                    })
                    next_annotation_id += 1

        with open(annotations_file, 'w') as f:
            json.dump(coco_data, f, indent=4)

    # Processar os dois arquivos de anotações
    process_annotations(train_annotations_file, images_dir)
    process_annotations(val_annotations_file, images_dir)