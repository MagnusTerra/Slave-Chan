import os
try:
    os.mkdir('hola')
    print('La carpeta se ha creado correctamente.')
except OSError:
    print('La creación de la carpeta ha fallado.')