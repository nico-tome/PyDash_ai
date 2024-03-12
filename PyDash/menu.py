import tkinter as tk
from tkinter import ttk
import subprocess
import pandas as pd

def update_volume_text(value):
    volume_text_var.set(f"Volume: {volume_var.get()}")

def Creation():
    global fenetre, mod_var, volume_var, volume_text_var, volume_label  # variables globales
    fenetre = tk.Tk()  # creation d une fenetre
    fenetre.geometry("250x300")  # dimensions
    fenetre.title('PyDash Ai')

    mod_var = tk.StringVar(value='train')
    volume_var = tk.IntVar(value=50)
    volume_text_var = tk.StringVar(value=f'Volume: {volume_var.get()}')

    page_title = tk.Label(text="PyDash AI")
    page_title.pack()

    main_Frame = tk.Frame(master=fenetre)

    selector_frame = tk.Frame(master=main_Frame)
    mode_selector = ttk.Combobox(master=selector_frame, values=['train', 'best'], textvariable=mod_var)
    mode_label = tk.Label(master=selector_frame, text='Select Mod')
    mode_label.pack(anchor='w')
    mode_selector.pack()

    volume_frame = tk.Frame(master=main_Frame)
    volume_label = tk.Label(master=volume_frame, textvariable=volume_text_var)
    slider = ttk.Scale(master=volume_frame, from_=0, to=100, orient="horizontal", variable=volume_var, command=update_volume_text)
    volume_label.pack(anchor='w')
    slider.pack(pady=20)

    selector_frame.pack(pady=20)
    volume_frame.pack(padx=20, pady=10)

    main_Frame.pack(anchor='w', padx=20)

    start_button = tk.Button(master=main_Frame, text='Start', command=start)
    start_button.pack(side='right')

    fenetre.mainloop()  # maintien de la fenetre ouverte

def start():
    settings = [mod_var.get(), volume_var.get()]
    settings_id = [_ for _ in range(len(settings))]
    settings_data = {'id': settings_id, 'settings': settings}
    df = pd.DataFrame(settings_data)
    df.to_csv('PyDash_ai/PyDash/data/settings.csv', index=False)
    subprocess.call(['python', 'PyDash_ai/PyDash/PyDash.py'])

# lancement de la création de la fenêtre
Creation()
