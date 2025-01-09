from ultralytics import YOLO
from ray import tune
import ray

#pip install -U ultralytics "ray[tune]"

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
                        iterations=100,
                        space=space,
                        gpu_per_trial=1,
                        project_name="YOLO11n-emissoes",

                        )

print(results)