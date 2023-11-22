import os
import shutil

class YOLOTrainer:

    def __init__(self):
        self._image_folder_origin = None
        self._annotations_folder_origin = None
        self._test_percentual_divisor = None

    @property
    def annotations_folder_origin(self):
        return self._annotations_folder_origin
    
    @annotations_folder_origin.setter
    def annotations_folder_origin(self, path):
        self._annotations_folder_origin = (path, "annotations")

    @property
    def image_folder_origin(self):
        return self._image_folder_origin
    
    @image_folder_origin.setter
    def image_folder_origin(self, path):
        self._image_folder_origin = (path, "images")

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
            

    def slicing_dataset_for_traning(self):

        list_archives = [self.image_folder_origin, self.annotations_folder_origin]

        for folder in list_archives:
            if folder != None:
                path_folder, name_folder = folder
                counter = 0
                for file in os.listdir(path_folder):
                    path_file = os.path.join(path_folder, file)

                    
                    if os.path.isfile(path_file):
                        os.makedirs(f"YOLO/{name_folder}/train", exist_ok=True)
                        os.makedirs(f"YOLO/{name_folder}/test", exist_ok=True)

                        if counter >= (len(os.listdir(path_folder))*(100-int(self.test_percentual_divisor))/100):
                            destination = f"YOLO/{name_folder}/test"
                        else:
                            destination = f"YOLO/{name_folder}/train"
                            counter += 1
                        
                        path_destination = os.path.join(destination, file)
                        shutil.copy(path_file, path_destination)

