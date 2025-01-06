from source.modules.yolo_dataloader import YOLO_Dataset
from torch.utils.data import DataLoader
from torchvision import transforms
from ultralytics import YOLO
import optuna
import torch

    # optimizer = torch.optim.Adam(model.model.parameters(), lr=learning_rate)
def train_epoch(model: YOLO, data_loader: DataLoader, learning_rate: float, epoch: int, optimizer: torch.optim.Optimizer):    # Função para treinar o modelo por uma época
    
    total_loss = 0
    
    scaler = torch.cuda.amp.GradScaler('cuda')  # Usado para escalar gradientes
    for batch in data_loader:
        optimizer.zero_grad()
        inputs, targets = batch
        with torch.cuda.amp.autocast('cuda'):  # Ativa o modo de precisão mista
            results = model(inputs)
            loss = results.loss
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item()  # Acumula a perda do lote

    print(f"Epoch {epoch}, Loss: {total_loss}")
    return total_loss

def evaluate_model_mAP_50_95(model: YOLO, val_loader: DataLoader):    # Função de avaliação usando mAP
    results = model.val(loader=val_loader)
    mAP_50_95 = results['metrics/mAP_50_95']
    return mAP_50_95

def evaluate_model_f1(model: YOLO, val_loader: DataLoader):  
    # Função de avaliação que retorna o F1-Score
    results = model.val(loader=val_loader)
    f1_score = results['metrics/F1']  # Acessando o F1-Score
    return f1_score

def objective(trial: int, images: str, labels: str, model: YOLO, data_yaml: str):   # Função objetivo para o Optuna
    
    # model = YOLO(model)   # Criar modelo YOLO

    # batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])
    c_learning_ratef = trial.suggest_float("lrf", 1e-5, 1e-2)
    c_learning_rate0 = trial.suggest_float("lr0", 1e-5, 1e-1)
    c_weight_decay = trial.suggest_float("weight_decay", 1e-3, 1e-2)
    c_momentum = trial.suggest_float("momentum", 0.8, 0.95)

    c_resize = trial.suggest_categorical("size", [360, 480, 640, 1024])
    c_batch_size = trial.suggest_int("batch", 8, 48)
    c_epochs = trial.suggest_int("epochs", 15, 150)

    c_warmup_epochs = trial.suggest_int("warmup_epochs", 1, 5)
    c_warmup_momentum = trial.suggest_float("warmup_momentum", 0.2, 0.9)
    c_warmup_bias_lr = trial.suggest_float("warmup_bias_lr", 1e-4, 1e-2)


    # transform = Compose([Resize((c_resize, c_resize)), ToTensor()])       # Preparação dos dados
    # train_dataset = ImageFolder(root=train, transform=transform)
    # val_dataset = ImageFolder(root=val, transform=transform)
    # train_loader = DataLoader(train_dataset, batch_size=c_batch_size, shuffle=True)
    # val_loader = DataLoader(val_dataset, batch_size=c_batch_size)

    # transform = transforms.Compose([    # Utilizando o novo Dataset no lugar do ImageFolder:
    #     transforms.Resize((c_resize, c_resize)),
    #     transforms.ToTensor()
    # ])

    # train_dataset = YOLO_Dataset(f"{images}\\train", f"{labels}\\train", transform=transform)
    # val_dataset = YOLO_Dataset(f"{images}\\val", f"{labels}\\val", transform=transform)
    # train_loader = DataLoader(train_dataset, batch_size=c_batch_size, shuffle=True)
    # val_loader = DataLoader(val_dataset, batch_size=c_batch_size)

    results = model.train(
        data=data_yaml, 
        imgsz=c_resize, 
        epochs=c_epochs, 
        batch=c_batch_size,

        weight_decay=c_weight_decay, 
        lrf=c_learning_ratef, 
        lr0=c_learning_rate0,

        warmup_epochs=c_warmup_epochs,
        warmup_momentum=c_warmup_momentum,
        warmup_bias_lr=c_warmup_bias_lr,
        momentum=c_momentum,
        
        ),
    
    cls_loss = results.metrics.get('cls_loss', None)   
    box_loss = results.metrics.get('box_loss', None)          # A perda (loss) ainda está disponível
    mAP_50_95 = results.metrics.get('mAP_50_95', None)  # Usando .get() para evitar erro caso a métrica não exista        # Para acessar o mAP, você pode acessar 'metrics' no resultado
    f1_score = results.metrics.get('F1', None)        # Para acessar o F1-Score


    print(f"Stats : \n\n {cls_loss} \n\n {box_loss} \n\n {mAP_50_95} \n\n {f1_score} \n\n")
    return f1_score
