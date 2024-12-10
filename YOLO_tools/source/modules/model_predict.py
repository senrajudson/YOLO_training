def predict_YOLO_model(train, objectToPredict, predict_confidence):
    from ultralytics import YOLO

    """
    usar predição do modelo de deteção
    """

    model = YOLO(f"runs/detect/{train}/weights/best.pt")
    model.predict(objectToPredict, save=True, conf=predict_confidence, device="cuda", save_txt=False, save_conf=True, save_crop=False)