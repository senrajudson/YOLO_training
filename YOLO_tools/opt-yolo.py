from ultralytics import YOLO
from ray import tune
import ray

#pip install -U ultralytics "ray[tune]"

### this are a mix of all YOLO built-in augments, if ur implementing manual augments, it's ideal to disable YOLO augments to avoid overlay
from ultralytics.data.augment import Albumentations, CenterCrop, RandomFlip, RandomHSV, RandomPerspective

albumentations_yolo = Albumentations(p=0.0)
centercrop_yolo = CenterCrop(0)
randomflip_yolo = RandomFlip(p=0.0)
randomhsv_yolo = RandomHSV(hgain=0.0, sgain=0.0, vgain=0.0)
randomperspective_yolo = RandomPerspective(translate=0.0, scale=0.0)

space={     # Configurar o espaço de busca
    "lr0": tune.uniform(1e-5, 1e-1),
    "lrf": tune.uniform(1e-5, 1e-2),
    "weight_decay": tune.uniform(1e-3, 1e-2),
    "momentum": tune.uniform(0.8, 0.95),
    "warmup_epochs": tune.randint(1, 5),
    "warmup_momentum": tune.uniform(0.4, 0.8),
    "warmup_bias_lr": tune.uniform(1e-5, 1e-1),
    "epochs": tune.randint(50, 200),
    "optimizer": tune.choice(['SGD', "AdamW"]),
    "imgsz": tune.choice([360, 480, 640]),
    "batch": tune.randint(8, 48),
    }

ray.init(_temp_dir=r"D:\Judson_projetos\Yolo_trainer\YOLO_tools\ray_sessions")

model = YOLO(r"yolo11n.pt")
data_yaml = r'D:\Judson_projetos\Yolo_trainer\YOLO_tools\datasets\emissoes_YOLO\dataset.yaml'
results = model.tune(
                        data=data_yaml,
                        use_ray=True, 
                        iterations=30,
                        space=space,
                        gpu_per_trial=1,
                        project_name="YOLO11n-emissoes_noaug",

                        )

print(results)