from source.modules.slicing_dataset import slicing_dataset_for_traning
# from source.modules.training_YOLO_model import training_YOLO_model
# from source.modules.model_predict import predict_YOLO_model

class YOLOTrainer:

    def __init__(self):
        self.image_folder = None
        self.annotations_folder = None
        self.yolo_Classes = None
        self.test_percentual_divisor = 1
        self.dataset_path = None
        self.task = None
        self.aug = False
        self.n_aug = 2
        self.odd = 0.5

    def slicing(self):
        slicing_dataset_for_traning(self.task, self.image_folder, self.annotations_folder, self.yolo_Classes, self.test_percentual_divisor, self.dataset_path, self.aug, self.n_aug, self.odd)

    @property
    def image_folder(self):
        return self._image_folder
    
    @image_folder.setter
    def image_folder(self, path):
        self._image_folder = (path, "images")

    @property
    def annotations_folder(self):
        return self._annotations_folder
    
    @annotations_folder.setter
    def annotations_folder(self, path):
        self._annotations_folder = path

    @property
    def yolo_Classes(self):
        return self._yolo_Classes
    
    @yolo_Classes.setter
    def yolo_Classes(self, cls):
        self._yolo_Classes = cls

    @property
    def test_percentual_divisor(self):
        return self._test_percentual_divisor
    
    @test_percentual_divisor.setter
    def test_percentual_divisor(self, value):
        self._test_percentual_divisor = value/100

    @property
    def dataset_path(self):
        return self._dataset_path
    
    @dataset_path.setter
    def dataset_path(self, value):
        self._dataset_path = value

    @property
    def task(self):
        return self._task
    
    @task.setter
    def task(self, value):
        self._task = value

    @property
    def aug(self):
        return self._aug
    
    @aug.setter
    def aug(self, value):
        self._aug = value

    @property
    def n_aug(self):
        return self._n_aug
    
    @n_aug.setter
    def n_aug(self, value):
        self._n_aug = value

    # def training(self):
    #     training_YOLO_model(self.training_model, self.img_sz, self.training_epochs)

    # def predict(self):
    #     predict_YOLO_model(self.train_model, self.object_to_predict, self.predict_confidence)

    # self.predict_YOLO = None
    # self.object_to_predict = None
    # self.predict_confidence = None
    # self.train_model = None
    # self.img_sz = None
    # self.training_epochs = None
    # self.training_model = None

    # @property
    # def img_sz(self):
    #     return self._img_sz
    
    # @img_sz.setter
    # def img_sz(self, img):
    #     self._img_sz = img

    # @property
    # def training_epochs(self):
    #     return self._training_epochs
    
    # @training_epochs.setter
    # def training_epochs(self, epochs):
    #     self._training_epochs = epochs

    # @property
    # def object_to_predict(self):
    #     return self._object_to_predict
    
    # @object_to_predict.setter
    # def object_to_predict(self, object):
    #     self._object_to_predict = object

    # @property
    # def train_model(self):
    #     return self._train_model
    
    # @train_model.setter
    # def train_model(self, model):
    #     self._train_model = model

    # @property
    # def predict_confidence(self):
    #     return self._predict_confidence
    
    # @predict_confidence.setter
    # def predict_confidence(self, confidence):
    #     self._predict_confidence = confidence

    # @property
    # def predict_YOLO(self):
    #     return self._predict_YOLO
    
    # @predict_YOLO.setter
    # def predict_YOLO(self, predict_object):
    #     self._predict_YOLO = predict_object

    # @property
    # def training_model(self):
    #     return self._training_model
    
    # @training_model.setter
    # def training_model(self, value):
    #     self._training_model = value