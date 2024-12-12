
import shutil
import os

def processar_dataset(dataset_dir):
    pasta_labels = os.path.join(dataset_dir, 'labels')
    pasta_imagens = os.path.join(dataset_dir, 'images')
    pasta_labels_sem_nada = os.path.join(pasta_labels, 'sem_nada_lb')
    pasta_imagens_sem_nada = os.path.join(pasta_imagens, 'sem_nada_im')

    # Verificar se as pastas labels e imagens existem
    if not os.path.exists(pasta_labels):
        print(f"Erro: O diretório '{pasta_labels}' não existe.")
        return

    if not os.path.exists(pasta_imagens):
        print(f"Erro: O diretório '{pasta_imagens}' não existe.")
        return

    # Criar a pasta sem_nada dentro de labels
    os.makedirs(pasta_labels_sem_nada, exist_ok=True)

    # Mover arquivos .txt vazios para labels/sem_nada
    for arquivo in os.listdir(pasta_labels):
        caminho_arquivo = os.path.join(pasta_labels, arquivo)
        if os.path.isfile(caminho_arquivo) and os.path.getsize(caminho_arquivo) == 0:
            shutil.move(caminho_arquivo, os.path.join(pasta_labels_sem_nada, arquivo))

    # Criar a pasta sem_nada dentro de imagens
    os.makedirs(pasta_imagens_sem_nada, exist_ok=True)

    # Mover imagens correspondentes para imagens/sem_nada
    for arquivo_txt in os.listdir(pasta_labels_sem_nada):
        if arquivo_txt.endswith('.txt'):
            nome_base = os.path.splitext(arquivo_txt)[0]
            print(nome_base)
            imagem_correspondente = os.path.join(pasta_imagens, f"{nome_base}.png")

            if os.path.exists(imagem_correspondente):
                shutil.move(imagem_correspondente, os.path.join(pasta_imagens_sem_nada, f"{nome_base}.png"))

# dataset_dir = 'YOLO_tools/emissoes_dataset_YOLO'
# processar_dataset(dataset_dir)
