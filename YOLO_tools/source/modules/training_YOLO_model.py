def training_YOLO_model(model, size, epochs, dataset_path):
    from ultralytics import YOLO
    import yaml
    
    """
    treinar o modelo
    """

    if model == None:
        print(f"Model is not set, default model value is '{model}'")
        return

    model = YOLO(model)

    # Carregar configurações de um arquivo YAML
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    train_config = config['train']

    try:
        results = model.train(
            data = f"{dataset_path}/dataset.yaml",
            imgsz = 640,
            device = "cuda",
            
            batch = 64,
            weight_decay = 0.001,

            warmup_epochs = 15,
            warmup_momentum = 0.5,
            warmup_bias_lr = 0.001,

            epochs = 50,
            momentum = 0.8,
            lr0 = 0.05,
            
            hsv_h = 0.015,
            hsv_s = 0.7,
            degrees = 10,
            mosaic = 1.0
        )

    except:
        print("CUDA is not avaible, switching to cpu")
        results = model.train(
            data = f"{dataset_path}/dataset.yaml",
            imgsz = 640,
            device = "cpu",
            
            batch = 64,
            weight_decay = 0.001,

            warmup_epochs = 15,
            warmup_momentum = 0.5,
            warmup_bias_lr = 0.001,

            epochs = 50,
            momentum = 0.8,
            lr0 = 0.05,
            
            hsv_h = 0.015,
            hsv_s = 0.7,
            degrees = 10,
            mosaic = 1.0
        )

    return results