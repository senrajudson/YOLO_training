from ultralytics import YOLO

"""
treinar o modelo
"""

def training_YOLO_model():
    model = YOLO("yolov8n.pt")
    try:
        results = model.train(data = "D:/Judson_projetos/Yolo_trainer/YOLO_tools/dataset/dataset_YOLO/dataset.yaml", epochs=10, imgsz=640, device="cuda")
    except AssertionError as e:
        e("CUDA is not avaible, switching to cpu")
        results = model.train(data = "D:/Judson_projetos/Yolo_trainer/YOLO_tools/dataset/dataset_YOLO/dataset.yaml", epochs=10, imgsz=640, device="cpu")
    # results = model.train(data = "D:/Judson_projetos/Trainer_YOLO/dataset/dataset_YOLO/dataset.yaml", epochs=10, imgsz=640, device="cpu")

    return results