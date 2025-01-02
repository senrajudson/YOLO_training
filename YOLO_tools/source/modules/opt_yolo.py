from torchvision.transforms import Compose, ToTensor, Resize
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from ultralytics import YOLO
import optuna
import torch

def train_epoch(model: YOLO, data_loader: DataLoader, learning_rate: float, epoch: int):    # Função para treinar o modelo por uma época
    optimizer = torch.optim.Adam(model.model.parameters(), lr=learning_rate)
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

    print(f"Epoch {epoch}, Loss: {total_loss}")
    return total_loss

def evaluate_model(model: YOLO, val_loader: DataLoader):    # Função de avaliação usando mAP
    results = model.val(loader=val_loader)
    mAP_50_95 = results['metrics/mAP_50_95']
    return mAP_50_95

def objective(trial: int, train: str, val: str):   # Função objetivo para o Optuna
    epochs = trial.suggest_int("epochs", 2, 5)
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-3, 1e-2)
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])

    transform = Compose([Resize((640, 640)), ToTensor()])       # Preparação dos dados

    train_dataset = ImageFolder(root=train, transform=transform)
    val_dataset = ImageFolder(root=val, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    optimizer = torch.optim.Adam(model.model.parameters(), lr=learning_rate, weight_decay=1e-5)
    model = YOLO('yolov5s.pt')   # Criar modelo YOLO
    model.train()  # Modo de treinamento

    best_metric = None
    patience = 5  # Número máximo de épocas sem melhoria
    patience_counter = 0
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)   # configurar um trial para isso aqui
    for epoch in range(epochs):
        train_epoch(model, train_loader, learning_rate, epoch)
        scheduler.step()  # Ajuste a taxa de aprendizado

        metric = evaluate_model(model, val_loader)
        if metric > best_metric:
            best_metric = metric
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print("Early stopping...")
                break

        trial.report(metric, step=epoch)

        if trial.should_prune():
            raise optuna.TrialPruned()

        if best_metric is None or metric > best_metric:
            best_metric = metric

    return best_metric