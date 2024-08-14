from ultralytics import YOLO

def predict_YOLO_model(self, train="train"):
    model = YOLO(f"runs/detect/{train}/weights/best.pt")
    # model.predict(self.object_to_predict, save=True, conf=self.predict_confidence, device="cuda", save_txt=False, save_conf=True, save_crop=False)

    # Run batched inference on a list of images
    results = model(self.object_to_predict)  # return a generator of Results objects
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
        # result.show()  # display to screen
        result.save(filename=f"{self.object_to_predict}")  # save to disk
        print(self.object_to_predict)
