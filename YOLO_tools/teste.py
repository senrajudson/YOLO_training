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