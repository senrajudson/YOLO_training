No **Ultralytics**, nem todas as configurações do YAML são lidas automaticamente quando você passa o arquivo no argumento `data`. Aqui está uma explicação sobre quais configurações o **Ultralytics** lê diretamente e quais precisam ser passadas explicitamente no código Python:

---

### **Configurações que o Ultralytics lê automaticamente do YAML**
Essas configurações fazem parte do argumento `data`:

1. **Estrutura do Dataset**:
   - `path` (Caminho base do dataset)
   - `train` (Imagens de treinamento)
   - `val` (Imagens de validação)
   - `test` (Imagens de teste, opcional)
   - `train_annot` (Rótulos de treinamento)
   - `val_annot` (Rótulos de validação)
   - `test_annot` (Rótulos de teste, opcional)

2. **Número de classes e nomes**:
   - `nc` (Número de classes)
   - `names` (Dicionário de classes)

---

### **Configurações que devem ser passadas no código**
Essas configurações precisam ser explicitamente configuradas no método `.train()` ou como argumentos ao inicializar o modelo:

1. **Hiperparâmetros de treinamento**:
   - `epochs`
   - `batch`
   - `lr0`
   - `lrf`
   - `momentum`
   - `weight_decay`
   - `warmup_epochs`
   - `warmup_bias_lr`
   - `warmup_momentum`
   - `gradient_clip_val`

   Exemplo:
   ```python
   model.train(data='dataset.yaml', epochs=50, batch=32, lr0=0.01)
   ```

2. **Augmentation**:
   Configurações como `hsv_h`, `degrees`, `mosaic`, etc., são definidas automaticamente pelo **Ultralytics**, mas podem ser sobrescritas apenas via código.

   Exemplo:
   ```python
   model.train(data='dataset.yaml', augment=True, hsv_h=0.015, degrees=10, mosaic=1.0)
   ```

3. **Configurações de computação**:
   - `device` (GPU ou CPU)
   - `workers` (Threads para carregar dados)
   - `sync_bn` (Batch Normalization sincronizado para multi-GPU)

   Exemplo:
   ```python
   model.train(data='dataset.yaml', device='cuda', workers=8)
   ```

4. **Logging e saída**:
   - `project`
   - `name`
   - `save_period`

---

### **Resumo**
- Tudo relacionado ao **dataset** (como `path`, `train`, `val`, `names`) é lido diretamente do arquivo YAML.
- Hiperparâmetros e augmentations não são lidos do YAML automaticamente. Esses devem ser configurados explicitamente no código ao chamar `.train()`.
- Se quiser automatizar mais configurações, você pode criar um script para carregar o YAML, extrair os valores e usá-los diretamente:

```python
import yaml
from ultralytics import YOLO

# Carregar configurações do YAML
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

model = YOLO('yolov8n.pt')
model.train(
    data='dataset.yaml',
    epochs=config['train']['epochs'],
    batch=config['train']['batch'],
    lr0=config['train']['lr0'],
    weight_decay=config['train']['weight_decay']
)
```