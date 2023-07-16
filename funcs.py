from telebot import types
import os
import sys
import subprocess
import shutil

def buttom():
    markup = types.ReplyKeyboardMarkup(True)
    markup.row('PDF', 'Cancelar')
    return markup

def compress(input_file_path, output_file_path, power=0):
    """Función para comprimir PDF via Ghostscript """
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }

    # Comprovamos si existe el fichero
    if not os.path.isfile(input_file_path):
        print("Error: invalid path for input PDF file")
        sys.exit(1)

    # Comprobamos si es un pdf
    if input_file_path.split('.')[-1].lower() != 'pdf':
        print("Error: input file is not a PDF")
        sys.exit(1)

    gs = get_ghostscript_path()
    print("Compress PDF...")
    initial_size = os.path.getsize(input_file_path)
    subprocess.call([gs, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                     '-dPDFSETTINGS={}'.format(quality[power]),
                     '-dNOPAUSE', '-dQUIET', '-dBATCH',
                     '-sOutputFile={}'.format(output_file_path),
                     input_file_path]
                    )
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / initial_size)
    resul1 = "Initial Size: {0:.1f}MB".format(initial_size / 1000000)
    resul2 = "Compression by {0:.0%}.".format(ratio)
    resul3 = "Final file size is {0:.1f}MB".format(final_size / 1000000)
    result = f'{resul1}\n{resul2}\n{resul3}\nDone'
    return result


def get_ghostscript_path():
    gs_names = ['gs', 'gswin32', 'gswin64']
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(f'No GhostScript executable was found on path ({"/".join(gs_names)})')