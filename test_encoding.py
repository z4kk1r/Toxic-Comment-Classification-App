# test_encoding.py
print("Start test_encoding.py")

try:
    import sys
    print(f"Python verzija: {sys.version}")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"Filesystem encoding: {sys.getfilesystemencoding()}")

    print("Importujem tkinter...")
    import tkinter as tk
    print("tkinter OK")

    print("Importujem ttk i scrolledtext...")
    from tkinter import ttk, scrolledtext
    print("ttk, scrolledtext OK")

    print("Importujem ttkthemes...")
    from ttkthemes import ThemedTk
    print("ttkthemes OK")

    print("Importujem tensorflow...")
    import tensorflow as tf
    print(f"TensorFlow OK, verzija: {tf.__version__}")

    print("Importujem keras iz tensorflow...")
    from tensorflow import keras
    print("keras OK")

    print("Importujem pad_sequences...")
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    print("pad_sequences OK")

    print("Importujem numpy...")
    import numpy as np
    print("numpy OK")

    print("Importujem pickle...")
    import pickle
    print("pickle OK")

    print("Importujem threading...")
    import threading
    print("threading OK")

    print("Importujem full_clean_function...")
    from full_clean_function import full_clean # Ovo je sada ključni test
    print("full_clean_function OK")

    # Ako sve ovo prođe, onda probajte učitati model i tokenizer
    MODEL_PATH = 'vas_model.keras' # Postavite ispravnu putanju
    TOKENIZER_PATH = 'tokenizer.pickle' # Postavite ispravnu putanju

    print(f"Pokušavam učitati model: {MODEL_PATH}")
    model = keras.models.load_model(MODEL_PATH)
    print("Model učitan.")

    print(f"Pokušavam učitati tokenizer: {TOKENIZER_PATH}")
    with open(TOKENIZER_PATH, 'rb') as handle:
        tokenizer = pickle.load(handle)
    print("Tokenizer učitan.")

    print("Svi glavni importi i učitavanja su prošli!")

except UnicodeDecodeError as ude:
    print(f"!!! UnicodeDecodeError se desio: {ude}")
    import traceback
    traceback.print_exc()
except ModuleNotFoundError as mnfe:
    print(f"!!! ModuleNotFoundError se desio: {mnfe}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"!!! Neka druga greška se desila: {e}")
    import traceback
    traceback.print_exc()

print("End test_encoding.py")