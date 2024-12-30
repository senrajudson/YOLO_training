import os
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image

class YOLO_Dataset(Dataset):
    def __init__(self, images_dir, labels_dir, transform=None):
        self.images_dir = images_dir
        self.labels_dir = labels_dir
        self.transform = transform
        self.image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]  # Ajuste para o formato das suas imagens

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        img_path = os.path.join(self.images_dir, img_name)
        image = Image.open(img_path).convert('RGB')
        
        label_name = img_name.replace('.jpg', '.txt')
        label_path = os.path.join(self.labels_dir, label_name)
        
        # Carregar as anotações (caixas delimitadoras)
        boxes = []
        with open(label_path, 'r') as file:
            for line in file.readlines():
                cls, x, y, w, h = map(float, line.strip().split())
                boxes.append([cls, x, y, w, h])  # [classe, x, y, w, h] (relativo à imagem)
        
        boxes = torch.tensor(boxes, dtype=torch.float32)
        
        if self.transform:
            image = self.transform(image)

        return image, boxes

# Utilizando o novo Dataset no lugar do ImageFolder:
transform = transforms.Compose([
    transforms.Resize((640, 640)),
    transforms.ToTensor()
])

train_dataset = YOLO_Dataset(train_dir, 'path/to/train/labels', transform=transform)
val_dataset = YOLO_Dataset(val_dir, 'path/to/val/labels', transform=transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size)
