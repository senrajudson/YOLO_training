from ultralytics import YOLO

"""
treinar o modelo
"""

def training_YOLO_model(img, epochs, task):

    if task == "detect":
        # model = YOLO("yolov8n.pt")
        model = YOLO("ppe.pt")

    if task == "classify":
        model = YOLO("yolov8n-cls.pt")

    if not task == "detect" or task == "classify":
        print("""
              Choose a task, 'classify' or 'detect'
              ex.
              class.task = 'detect'""")
        return

    try:
        results = model.train(data = "D:/Judson_projetos/Yolo_trainer/YOLO_tools/dataset/dataset_YOLO/dataset.yaml", epochs=epochs, imgsz=img, device="cuda")
    except:
        print("CUDA is not avaible, switching to cpu")
        results = model.train(data = "D:/Judson_projetos/Yolo_trainer/YOLO_tools/dataset/dataset_YOLO/dataset.yaml", epochs=epochs, imgsz=img, device="cpu")

    return results