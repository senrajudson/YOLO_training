# YOLOtools - Ferramentas para treinar modelos de detecção de objetos

Este repositório contem uma classe Python, `YOLOTrainer()` que oferece funcionalidades para criar datasets de treinamento de deteção, treinar os modelos e testá-los.

```python
from source.class_yolo_trainer import YOLOTrainer

yolo_trainer = YOLOTrainer
yolo_trainer = YOLOTrainer()
```

## Funções da Classe

### `slicing()`

```python
yolo_trainer.image_folder = "pelotas_19-08/images"
yolo_trainer.annotations_folder = "pelotas_19-08/labels"
yolo_trainer.yolo_Classes = "Pellet"
yolo_trainer.test_percentual_divisor = 20
yolo_trainer.slicing()
```

**Descrição**: Tem a função de dividir as anotações e imagens de dataset em um conjunto de treinamento e validação. Necessita declarar:

- `image_folder`
- `annotations_folder`
- `yolo_Classes` nome da classe
- `test_percentual_divisor` percentual dedicado do dataset para validação

### `training()`

```python
yolo_trainer.img_sz = 960
yolo_trainer.training_epochs = 20
yolo_trainer.task = "detect"
yolo_trainer.training()
```

**Descrição**: Função para treinar o modelo Yolo, requer declar os parâmetros:

- `img_sz`
- `training_epochs` número de épocas
- `task` escolha a tarefa a qual você deseja treinar o seu modelo

### `predict()`

```python
yolo_trainer.train_model = "train16"
yolo_trainer.object_to_predict = "D:/Judson_projetos/Yolo_trainer/vid_1.mp4"
yolo_trainer.predict_confidence = 0.2
yolo_trainer.predict()
```

**Descrição**: Função para realizar predições utilizando o modelo treinado. É necessário declarar:

- `train_model` o nome da pasta que você quer usar, por exemplo "train16"
- `object_to_predict`
- `predict_confidence`

## Utils

Há funções dentro do Utils que podem te ajudar a resolver alguns problemas simples.

### `check_file()`

```python
from utils.check_file import check_file

check_file("any_file")
```

**Descrição**: Muitas vezes indicamos um diretório para o script e este nos retorna que o repositório não existe. Essa função serve para validar se o caminho do diretório que você indicou vai ser encontrado pelo script.

### `torch_is_available()`

```python
from utils.torch_is_available import torch_is_available

torch_is_available()
```

**Descrição**: Um script para rodar todas as funções relevanstes para conferir o seu cuda toolkit:

- `nvcc --version` e `which cuda` no prompt além dos comandos
- `toch.cuda.is_available()`
- `torch.version.cuda`
- `torch.backends.cudnn.version()`

### `cvat_dataset()`

```python
from utils.cvat_dataset import cvat_dataset

cvat_dataset("pelotas_19-08", "pelotas_19-08")
```

**Descrição**: Os datasets que são importados do CVAT estão desatualizados segundo as versões mais recentes do ultralytics.

- Essa função requer dois argumentos, o primeiro é a pasta importada do CVAT, o segundo argumento é o nome de saída desejado para a pasta.
