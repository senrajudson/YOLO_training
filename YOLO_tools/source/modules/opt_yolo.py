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
    c_opts = trial.suggest_int("epochs", 5, 30)
    c_epochs = trial.suggest_int("epochs", 15, 150)
    c_learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-2)
    c_batch_size = trial.suggest_int("batch_size", 8, 128)
    c_weight_decay = trial.suggest_float("weight_decay", 1e-3, 1e-2)
    c_step_size = trial.suggest_int("step_size", 1, 1000)
    c_gamma = trial.suggest_float("c_gamma", 1e-3, 1e-1)
    c_resize = trial.suggest_categorical("size", [360, 480, 640, 1024])

    # transform = Compose([Resize((c_resize, c_resize)), ToTensor()])       # Preparação dos dados
    # train_dataset = ImageFolder(root=train, transform=transform)
    # val_dataset = ImageFolder(root=val, transform=transform)
    # train_loader = DataLoader(train_dataset, batch_size=c_batch_size, shuffle=True)
    # val_loader = DataLoader(val_dataset, batch_size=c_batch_size)

    transform = transforms.Compose([    # Utilizando o novo Dataset no lugar do ImageFolder:
        transforms.Resize((c_resize, c_resize)),
        transforms.ToTensor()
    ])

    train_dataset = YOLO_Dataset(f"{images}\\train", f"{labels}\\train", transform=transform)
    val_dataset = YOLO_Dataset(f"{images}\\val", f"{labels}\\val", transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=c_batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=c_batch_size)

    optimizer = torch.optim.Adam(model.model.parameters(), lr=c_learning_rate, weight_decay=c_weight_decay)

    # model.train(data=data_yaml, epochs=c_epochs)  # Modo de treinamento
    with torch.cuda.amp.autocast('cuda'):  # Ativa o modo de precisão mista
        results = model.train()

        # loss = results.loss   # para pegar a métrica loss
        f1_score = results.metrics.get('F1', None)    # para pegar a métrica f1
        # mAP_50_95 = results.metrics.get('mAP_50_95', None)    # para pegar a métrica mAP

    best_metric = None
    patience = 5  # Número máximo de épocas sem melhoria
    patience_counter = 0

    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=c_step_size, gamma=c_gamma)   # configurar um trial para isso aqui
    for epoch in range(c_epochs):
        train_epoch(model, train_loader, c_learning_rate, epoch, optimizer=optimizer)
        scheduler.step()  # Ajuste a taxa de aprendizado

        metric = evaluate_model_f1(model, val_loader)
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

    return f1_score
