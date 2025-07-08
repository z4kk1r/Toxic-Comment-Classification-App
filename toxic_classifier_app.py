import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ttkthemes import ThemedTk
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import threading

from full_clean_function import full_clean


# --- Postavke ---
MODEL_PATH = './best_model_epoch_08_valauc_0.9194.keras'
TOKENIZER_PATH = './tokenizer.pickle'
MAX_LEN = 280
CLASSIFICATION_THRESHOLD = 0.01 

try:
    print("Ucitavanje modela...")
    model = keras.models.load_model(MODEL_PATH)
    print("Model uspjesno ucitan.")
    print(f"Ucitavanje tokenizera sa putanje: {TOKENIZER_PATH}...")
    with open(TOKENIZER_PATH, 'rb') as handle:
        tokenizer = pickle.load(handle)
    print("Tokenizer uspjesno ucitan.")
except Exception as e:
    messagebox.showerror("Greska pri Ucitavanju", f"Nije moguce ucitati model ili tokenizer:\n{e}")
    exit()

def preprocess_and_predict(text_to_predict):
    if not text_to_predict.strip(): return "Unesite tekst.", 0.0
    cleaned_text = full_clean(text_to_predict)
    if not cleaned_text.strip(): return "Tekst je postao prazan nakon ciscenja.", 0.0
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded_sequence = pad_sequences(sequence, maxlen=MAX_LEN, padding='post', truncating='post')
    try:
        probability_toxic = model.predict(padded_sequence, verbose=0)[0][0]
        return cleaned_text, probability_toxic
    except Exception as e:
        print(f"Greska tokom predikcije: {e}")
        return f"Greska predikcije: {e}", -1.0

def classify_comment():
    user_text = text_input.get("1.0", tk.END).strip()
    classify_button.config(state=tk.DISABLED, text="Analiziram...")
    result_label.config(text="Analiziram...", foreground="gray")
    probability_label.config(text="")
    def prediction_task():
        cleaned_text_display, prob_toxic = preprocess_and_predict(user_text)
        result_text_final, prob_text_final, color_final = "", "", "gray"
        if prob_toxic == -1.0:
            result_text_final, prob_text_final, color_final = "Greska u Predikciji", cleaned_text_display, "red"
        elif not user_text:
             result_text_final, prob_text_final, color_final = "Molimo unesite tekst.", "", "orange"
        elif not cleaned_text_display.strip() or cleaned_text_display.startswith("Tekst je postao prazan"):
             result_text_final, prob_text_final, color_final = "Tekst nevalidan nakon ciscenja.", "", "orange"
        else:
            print(f"DEBUG: Uneseni tekst: '{user_text}'")
            print(f"DEBUG: Ocisceni tekst: '{cleaned_text_display}'")
            print(f"DEBUG: Dobijena vjerovatnoca toksicnosti: {prob_toxic}")
            print(f"DEBUG: Koristeni prag: {CLASSIFICATION_THRESHOLD}")
            if prob_toxic > CLASSIFICATION_THRESHOLD:
                result_text_final, color_final = "Komentar je: TOKSICAN", "#E74C3C"
            else:
                result_text_final, color_final = "Komentar je: NIJE TOKSICAN", "#2ECC71"
            prob_text_final = f"Vjerovatnoca toksicnosti: {prob_toxic:.4f} (Prag: {CLASSIFICATION_THRESHOLD:.4f})"
        root.after(0, update_ui_after_prediction, result_text_final, prob_text_final, color_final)
    threading.Thread(target=prediction_task, daemon=True).start()

def update_ui_after_prediction(result_text, prob_text, color):
    result_label.config(text=result_text, foreground=color)
    probability_label.config(text=prob_text)
    classify_button.config(state=tk.NORMAL, text="Klasifikuj Komentar")

# --- Kreiranje UI-ja ---
BG_COLOR = "#2E3B4E"  
TEXT_AREA_BG = "#3A475A"
TEXT_AREA_FG = "white"

root = ThemedTk(theme="arc")
root.title("Klasifikator Toksicnih Komentara")
root.geometry("600x450")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.configure("TLabel", background=BG_COLOR, foreground="white", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=10)
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), padding=(0, 10, 0, 10))
style.configure("FrameBG.TFrame", background=BG_COLOR)  

main_frame = ttk.Frame(root, padding="20 20 20 20", style="FrameBG.TFrame")  
main_frame.pack(expand=True, fill=tk.BOTH)

title_label = ttk.Label(main_frame, text="Analizator Toksicnosti Komentara", style="Header.TLabel")
title_label.pack(pady=(0, 20))

input_label = ttk.Label(main_frame, text="Unesite komentar za analizu:")
input_label.pack(anchor=tk.W, pady=(0,5))

text_input_parent = main_frame

text_input = scrolledtext.ScrolledText(text_input_parent, wrap=tk.WORD, width=60, height=8,
                                      font=("Segoe UI", 11),
                                      bg=TEXT_AREA_BG,
                                      fg=TEXT_AREA_FG,
                                      insertbackground="white",  
                                      relief=tk.FLAT,  
                                      borderwidth=0,  
                                      highlightthickness=1,  
                                      highlightbackground=BG_COLOR,  
                                      highlightcolor=TEXT_AREA_BG  
                                      )
if text_input_parent == main_frame:
    text_input.pack(fill=tk.X, pady=5, padx=0)  
else:
    text_input.pack(expand=True, fill=tk.BOTH, padx=1, pady=1)  


classify_button = ttk.Button(main_frame, text="Klasifikuj Komentar", command=classify_comment)
classify_button.pack(pady=20, ipady=5, ipadx=10)

result_label = ttk.Label(main_frame, text="", font=("Segoe UI", 14, "bold"))
result_label.pack(pady=10)

probability_label = ttk.Label(main_frame, text="", font=("Segoe UI", 10))
probability_label.pack()

status_bar = ttk.Label(root, text="Spreman.", relief=tk.SUNKEN, anchor=tk.W, padding=5) 
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()