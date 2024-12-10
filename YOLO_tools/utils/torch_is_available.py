def torch_is_available():
  import torch
  import subprocess

  """
  Uma função para testar se o torch está funcionando
  """

  list_commands = ['nvcc --version',"which cuda"]

  for command in list_commands: 
      print(subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True).stdout)

  print("Is torch available? ", torch.cuda.is_available())
  print("CUDA version: ", torch.version.cuda)
  print("cuDNN version: ", torch.backends.cudnn.version())