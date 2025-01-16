from ultralytics import YOLO
import logging
import json
import yaml

### this are a mix of all YOLO built-in augments, if ur implementing manual augments, it's ideal to disable YOLO augments to avoid overlay
from ultralytics.data.augment import Albumentations, CenterCrop, RandomFlip, RandomHSV, RandomPerspective

"""
eu modifiquei as transformações dentro da classe 'Albumentations' no '.../ultralytics/data/augment, 
foi necessário zerar a probabilidade usando um float 0.0 no transform 'T' e
mudando o valor de 'p' em __init__ para 'p=0' 
"""
albumentations_yolo = Albumentations(p=0.0)
centercrop_yolo = CenterCrop(0)
randomflip_yolo = RandomFlip(p=0.0)
randomhsv_yolo = RandomHSV(hgain=0.0, sgain=0.0, vgain=0.0)
randomperspective_yolo = RandomPerspective(translate=0.0, scale=0.0)

### YOLO é gambiarra e eu posso provar:
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

with open(r'D:\Judson_projetos\Yolo_trainer\YOLO_tools\params.json', 'r') as file:   # Carregar configurações de um arquivo
    config = json.load(file)

model = YOLO(r"D:\Judson_projetos\Yolo_trainer\YOLO_tools\yolo11n.pt")

best_recall = 0.0   # Variáveis globais para rastrear o melhor recall e a época correspondente
best_precision = 0.0
best_f1score = 0.0
best_mAP50 = 0.0
best_mAP5095 = 0.0
best_epoch = 0
patience = 100
limit = patience

def on_train_epoch_end(trainer):
    global best_recall, best_precision, best_f1score, best_mAP5095, best_mAP50, best_epoch, limit

    logging.basicConfig(      # Configuração do logger
        level=logging.INFO,  # Nível mínimo de mensagens para registrar
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="training.log",  # Arquivo onde as mensagens serão salvas
        filemode="w",  # Sobrescreve o arquivo a cada execução
    )

    # current_recall = trainer.metrics.get('metrics/recall(B)', 0.0)       # Obtenha o recall atual dos resultados de validação
    # current_precision = trainer.metrics.get('metrics/precision(B)', 0.0)    # Obtenha o precision atual dos resultados de validação
    # current_f1score = 2 * (current_precision * current_recall) / (current_precision + current_recall) if current_recall > 0 else 0.0      # f1score

    current_mAP50 = trainer.metrics.get('metrics/mAP50(B)', 0.0)       # mAP50 ajuda no melhor 'recall'
    current_mAP5095 = trainer.metrics.get('metrics/mAP50-95(B)', 0.0)       # mAP50-95 ajuda no melhor 'precision'
    

    if current_mAP50 > best_mAP50:        # Verifique se o recall atual é melhor que o melhor recall registrado
        best_mAP50 = current_mAP50
        best_epoch = trainer.epoch

        logging.info(f"\nBest actual metric : {round(best_mAP50, 4)} on epoch {best_epoch}")
        limit = patience

        model.save(f'best_metric.pt')            # Salve os pesos do modelo para a melhor época com base no recall

    print(trainer.metrics)
    print(f"\nActual mAP50 : {round(current_mAP50, 4)}")
    print(f"\nBest actual metric : {round(best_mAP50, 4)} on epoch {best_epoch}")

    limit -= 1

    if limit == 0 :
        logging.warning(f"Patience has reached limit at epoch {trainer.epoch}")
        # logging.error("Erro inesperado no treinamento")
        
        raise KeyboardInterrupt

model.add_callback('on_train_epoch_end', on_train_epoch_end)    # Adicione o callback personalizado ao modelo

if __name__ == '__main__':
    model.train(
        data = r"D:\Judson_projetos\Yolo_trainer\YOLO_tools\datasets\emissoes_YOLO\dataset.yaml",
        device = "cuda",

        batch = config['batch'],    ### training configs
        # epochs = config['epochs'],
        epochs = 300,
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