#%%
from source.class_yolo_trainer import YOLOTrainer

yolo_trainer = YOLOTrainer
yolo_trainer = YOLOTrainer()
#%%
### vou deixar anotado porque não sei se fiz gambiarra, 
""" no atributo image_folder para tarefas de classificação eu estou passando somente a pasta do dataset, sem indicar a pasta de imagens
"""
yolo_trainer.image_folder = r"emissoes_dataset_YOLO\images"
yolo_trainer.annotations_folder = r"emissoes_dataset_YOLO\labels"
yolo_trainer.yolo_Classes = ["emissao"]
yolo_trainer.dataset_path = "emissoes_YOLO"
yolo_trainer.task = "detect"
yolo_trainer.aug = True
yolo_trainer.n_aug = 10
yolo_trainer.odd = 0.12
yolo_trainer.test_percentual_divisor = 20

yolo_trainer.slicing()
#%%
from source.modules.opt_yolo import objective
from ultralytics import YOLO
import optuna

model = YOLO(r"yolo11m.pt")

images_dir = r'D:\Judson_projetos\Yolo_trainer\YOLO_tools\datasets\emissoes_YOLO\images'
labels_dir = r'D:\Judson_projetos\Yolo_trainer\YOLO_tools\datasets\emissoes_YOLO\labels'
data_yaml = r'D:\Judson_projetos\Yolo_trainer\YOLO_tools\datasets\emissoes_YOLO\dataset.yaml'

storage_url = "sqlite:///emissoes-fugitivas.db"
study = optuna.create_study(direction="maximize", storage=storage_url, study_name="opt-emissoes", load_if_exists=True)      ### study for F1 metric, thats why maximize
study.optimize(lambda trial: objective(trial, images_dir, labels_dir, model, data_yaml), n_trials=50)
#%%
from ultralytics import YOLO
import logging
import json
import yaml

#### YOLO é gambiarra e eu posso provar:
""" Para treinamentos de classificação com YOLO, você deve indicar o dir com o dataset
que deve estar especificado dentro de uma pasta chamada 'datasets'. No entando, para detecção
o YOLO é diferente. Você precisa indicar o caminho do arquivo 'dataset.yaml' para que ele 
possa encontrar o dataset e realizar o treinamento. É a mesma função, de uma mesma lib,
mas os caras fizeram de forma que o mesmo argumento recebe duas entradas completamente 
diferentes a depender do treinamento que você vai fazer.
"""

# # Carregar configurações de um arquivo 
# with open('../hyper_yolo.yaml', 'r') as file:
#     config = yaml.safe_load(file)

# train_config = config['train']
# aug_config = config['train']['augmentation']

with open('params.json', 'r') as file:   # Carregar configurações de um arquivo
    config = json.safe_load(file)

model = YOLO(r"yolo11n.pt")

best_recall = 0.0   # Variáveis globais para rastrear o melhor recall e a época correspondente
best_precision = 0.0
best_f1score = 0.0
best_epoch = 0
patience = 10
limit = patience

def on_train_epoch_end(trainer):
    global best_recall, best_precision, best_f1score, best_epoch, limit

    logging.basicConfig(      # Configuração do logger
        level=logging.INFO,  # Nível mínimo de mensagens para registrar
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="training.log",  # Arquivo onde as mensagens serão salvas
        filemode="w",  # Sobrescreve o arquivo a cada execução
    )

    current_recall = trainer.metrics.get('metrics/recall(B)', 0.0)       # Obtenha o recall atual dos resultados de validação
    current_precision = trainer.metrics.get('metrics/precision(B)', 0.0)
    current_f1score = 2 * (current_precision * current_recall) / (current_precision + current_recall) if current_recall > 0 else 0.0

    if current_recall > best_recall:        # Verifique se o recall atual é melhor que o melhor recall registrado
        best_recall = current_recall
        best_epoch = trainer.epoch

        logging.info(f"\nBest actual metric : {round(best_recall, 4)} on epoch {trainer.epoch}")
        limit = patience

        model.save(f'best_recall.pt')            # Salve os pesos do modelo para a melhor época com base no recall

    print(f"\nActual f1score : {round(current_f1score, 4)}")
    print(f"\nBest actual metric : {round(best_recall, 4)} on epoch {trainer.epoch}")

    limit -= 1

    if limit == 0 :
        logging.warning(f"Patience has reached limit at epoch {trainer.epoch}")
        # logging.error("Erro inesperado no treinamento")
        
        raise KeyboardInterrupt

model.add_callback('on_train_epoch_end', on_train_epoch_end)    # Adicione o callback personalizado ao modelo

model.train(
    data = "datasets/emissoes_YOLO/dataset.yaml",
    device = "cuda",

    batch = config['batch'],    ### training configs
    epochs = config['epochs'],
    imgsz = config['imgsz'],

    lr0 = config['lr0'],
    lrf = config['lrf'],
    momentum = config['momentum'],
    optimizer = config['optimizer'],

    warmup_bias_lr = config['warmup_bias_lr'],
    warmup_epochs = config['warmup_epochs'],
    warmup_momentum = config['warmup_momentum'],
    weight_decay = config['weight_decay'],
)
#%%
import torch
print(torch.cuda.is_available())
#%%
import torch
import torchvision
print(f"PyTorch version: {torch.__version__}")
print(f"TorchVision version: {torchvision.__version__}")
print(torchvision.ops.nms.__module__)
#%%
from ultralytics import YOLO

model = YOLO("runs\\detect\\train52\\weights\\best.pt")

model.info()
#%%
from ultralytics import YOLO

train = 'train52'
model = YOLO(f"runs/detect/{train}/weights/best.pt")
model.predict("../RUIM 23-06-22 (1).mp4", save=True, conf=0.4, device="cuda", save_txt=False, save_conf=True, save_crop=False)
#%%
from utils.check_file import check_file

check_file("datasets\\emissoes_YOLO\\dataset.yaml")
#%%
from utils.torch_is_available import torch_is_available

torch_is_available()
#%%
from utils.cvat_dataset import cvat_dataset

cvat_dataset("../emissoes_dataset_CVAT", "emissoes_dataset_YOLO")
#%%
from utils.remover_labels_vazios import processar_dataset

processar_dataset("emissoes_dataset_YOLO")
#%%