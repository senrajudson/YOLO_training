from ultralytics import YOLO

"""
usar predição do modelo de deteção
"""

def predict_YOLO_model(train, objectToPredict, predict_confidence):
    model = YOLO(f"runs/detect/{train}/weights/best.pt")
    # model.predict(objectToPredict, imgsz=640, save=True, conf=predict_confidence, device="cuda", save_txt=False, save_conf=True, save_crop=False)

    # resultado = model.predict(objectToPredict , imgsz=640, conf=predict_confidence, verbose=True)
    # for result in resultado:
      
    # #   # Encontrar a classe com a maior probabilidade de inferência
    # #   max_prob_class = max(result.names, key=lambda k: result.names[k])
    # #   max_prob_class_cpu = result.probs.cpu()
    # #   max_prob_class_np = max_prob_class_cpu.numpy()
    # #   class_names = result.names[max_prob_class]
    # #   class_prob_value = max_prob_class_np.top5conf[0]
    #   boxes = result.boxes
    #   conf = boxes.conf
    #   cls = boxes.cls
    #   result.save(filename=f"{objectToPredict}")

    # Run batched inference on a list of images
    results = model(objectToPredict)  # return a generator of Results objects
    # Process results generator
    for result in results:
        device = result.cuda()
        boxes = result.boxes  # Boxes object for bounding box outputs
        conf = boxes.conf
        cls = boxes.cls
        fmt = boxes.xywhn
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        result.save(filename=f"predicted.jpg")  # save to disk
        print(objectToPredict)
