def check_file(file_path):
  import os

  """
  Uma função para checar se algum arquivo existe
  """

  file_name = file_path

  # Check if the file exists
  if os.path.isfile(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
    print(content)
  else:
    print(f"File {file_name} does not exist.")