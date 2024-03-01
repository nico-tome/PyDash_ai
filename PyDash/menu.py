import tkinter as tk
from tkinter import*
from tkinter import ttk
import subprocess
import pandas as pd
    
def Creation() :
    
    global fenetre,mod_var, height_var, width_var   # variables globales 
    fenetre = Tk()   #creation d une fenetre
    fenetre.geometry("600x200")   # dimensions
    fenetre.title('PyDash Ai')

    mod_var = tk.StringVar(value='train')
    height_var = tk.StringVar(value='600')
    width_var = tk.StringVar(value='400')
    
    
    page_title = tk.Label(text="PyDash AI")
    page_title.pack()
    
    main_Frame = tk.Frame(master=fenetre)

    selector_frame = tk.Frame(master=main_Frame)
    mode_selector = ttk.Combobox(master=selector_frame, values=['train', 'best'], textvariable=mod_var)
    mode_label = tk.Label(master=selector_frame, text='Select Mod')
    start_button = tk.Button(master=selector_frame, text='Start', command=start)
    mode_label.pack(anchor='w')
    mode_selector.pack()

    dimension_frame = tk.Frame(master=main_Frame)
    height = ttk.Spinbox(master=dimension_frame, from_=400, to=fenetre.winfo_screenheight(), increment=100, textvariable=height_var)
    width = ttk.Spinbox(master=dimension_frame, from_=600, to=fenetre.winfo_screenwidth(), increment=100, textvariable=width_var)
    height_text = tk.Label(master=dimension_frame, text='Window Height:')
    width_text = tk.Label(master=dimension_frame, text='Window Width:')
    height_text.pack(anchor='w')
    height.pack()
    width_text.pack(anchor='w')
    width.pack()

    start_button.pack(side='right')

    selector_frame.pack(pady=20)
    dimension_frame.pack(padx= 20, pady=10)

    main_Frame.pack(anchor='w', padx=20)


    fenetre.mainloop()      # maintien de la fenetre ouverte

def start():
    settings = [mod_var.get(), height_var.get(), width_var.get()]
    settings_id = [_ for _ in range(len(settings))]
    settings_data = {'id': settings_id, 'settings': settings}
    df = pd.DataFrame(settings_data)
    df.to_csv('PyDash/data/settings.csv', index=False)
    subprocess.call(['python', 'PyDash/PyDash.py'])


# lancement de la création de la fenêtre

Creation()
    