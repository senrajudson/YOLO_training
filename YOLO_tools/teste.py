from ultralytics import YOLO
import yaml

# Carregar configurações de um arquivo YAML
with open('hyper_yolo.yaml', 'r') as file:
    config = yaml.safe_load(file)

train_config = config['train']
aug_config = config['train']['augmentation']

model = YOLO("yolov8n.pt")

results = model.train(
    data = "YOLO_tools/datasets/emissoes_YOLO",
    device = "cuda",

    ### training configs. Checkout hyper_yolo.yaml for details
    imgsz = train_config['imgsz'],
    batch = train_config['batch'],
    weight_decay = train_config['weight_decay'],

    warmup_epochs = train_config['warmup_epochs'],
    warmup_momentum = train_config['warmup_momentum'],
    warmup_bias_lr = train_config['warmup_bias_lr'],

    epochs = train_config['epochs'],
    momentum = train_config['momentum'],
    lr0 = train_config['lr0'],
    lrf = train_config['lrf'],
    optimizer = train_config['optimizer'],
    
    
    ### if you r willing to use yolo aug, uncomment section bellow
    ### not recomended if ur data is already aug though
    ### augment args
    # hsv_h = aug_config['hsv_h'],
    # hsv_s = aug_config['hsv_s'],
    # hsv_v = aug_config['hsv_v'],
    # degrees = aug_config['degrees'],
    # translate = aug_config['translate'],
    # scale = aug_config['scale'],
    # shear = aug_config['shear'],
    # perspective = aug_config['perspective'],
    # flipud = aug_config['flipud'],
    # fliplr = aug_config['fliplr'],
    # mosaic = aug_config['mosaic'],
    # mixup = aug_config['mixup'],
    # copy_paste = aug_config['copy_paste'],
    # auto_augment = aug_config['auto_augment'],
)