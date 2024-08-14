from YOLO_tools.source.modules.model_predict import predict_YOLO_model
from YOLO_tools.source.modules.slicing_dataset import slicing_dataset_for_traning
from YOLO_tools.source.modules.training_YOLO_model import training_YOLO_model

class YOLOTrainer:

    def __init__(self):
        self._image_folder = None
        self._annotations_folder = None
        self._test_percentual_divisor = None
        self._predict_YOLO = None
        self._yolo_Classes = None
        self._yolo_Notes = None
        self._object_to_predict = None
        self._predict_confidence = None

    

    @property
    def object_to_predict(self):
        return self._object_to_predict
    
    @object_to_predict.setter
    def object_to_predict(self, predict_object):
        self._object_to_predict = predict_object

    @property
    def predict_confidence(self):
        return self._predict_confidence
    
    @predict_confidence.setter
    def predict_confidence(self, confidence):
        self._predict_confidence = confidence

    @property
    def yolo_Classes(self):
        return self._yolo_Classes
    
    @yolo_Classes.setter
    def yolo_Classes(self, path):
        self._yolo_Classes = path

    @property
    def yolo_Notes(self):
        return self._yolo_Notes
    
    @yolo_Notes.setter
    def yolo_Notes(self, path):
        self._yolo_Notes = path

    
    @property
    def predict_YOLO(self):
        return self._predict_YOLO
    
    @predict_YOLO.setter
    def predict_YOLO(self, predict_object):
        self._predict_YOLO = predict_object

    @property
    def annotations_folder(self):
        return self._annotations_folder
    
    @annotations_folder.setter
    def annotations_folder(self, path):
        self._annotations_folder = (path, "labels")

    @property
    def image_folder(self):
        return self._image_folder
    
    @image_folder.setter
    def image_folder(self, path):
        self._image_folder = (path, "images")

    @property
    def test_percentual_divisor(self):
        return self._test_percentual_divisor
    
    @test_percentual_divisor.setter
    def test_percentual_divisor(self, value):
        try:
            toint = int(value)
            self._test_percentual_divisor = toint
        except ValueError:
            "Value expected does not match, expected an integer value"
            
