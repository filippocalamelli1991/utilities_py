# librerie standard
import tkinter as tk
import os

# pacchetti
import numpy as np
from nptdms import TdmsFile

#--------------------------------------------------------------------------
# LIB
#--------------------------------------------------------------------------
def elencaFiles(DIR,EXT):
    """ Elenca files in una cartella con una determinata estensione
    INPUT:
    DIR = directory dove cercare
    EXT = estensione dei files. es: '.mat'/'.tdms'

    OUTPUT:
    FILES = elenco dei files filtrati
    """

    FILES = []
    # seleziono solo i files che finiscono con EXT
    for files in os.listdir(DIR):
        if files.endswith(EXT):
            FILES.append(files)

    return FILES

#--------------------------------------------------------------------------
def scegliFiles(lista,prompt='Select files:',selection_mode='multiple',list_size=(300, 300)):

    """Equivalente di MATLAB listdlg
    #--------------------------------------------------------------------------
    INPUT:
    list_string: lista di stringhe da mostrare
    prompt: titolo della finestra
    selection_mode: "single" oppure "multiple"
    list_size: (larghezza, altezza) in pixel
    
    #--------------------------------------------------------------------------
    OUTPUT
    (sel, ok): sel = lista di indici selezionati,
               ok = True se l'utente ha premuto OK, False se ha annullato.
    """

    res = {"sel": [], "ok": False}

    root = tk.Tk()
    root.attributes('-topmost', True) # attributo che serve per spostare l'interfaccia davanti

    # creo etichetta prompt
    tk.Label(root, text=prompt).pack(padx=10, pady=(10, 0), anchor='nw') # etichetta per il prompt .pack() serve per far apparire il widget
    
    # creo frame
    frame = tk.Frame(root, width=list_size[0], height=list_size[1])
    frame.pack_propagate(False)
    frame.pack(padx=10, pady=10)

    # gestisco modalità di selezione
    if selection_mode == 'single':
        mode = tk.SINGLE            
    else:
        mode = tk.EXTENDED

    # creo scroll a dx
    scroll = tk.Scrollbar(frame)
    scroll.pack(side='right', fill='y')

    # creo listbox
    lb = tk.Listbox(frame, selectmode=mode, exportselection=False, yscrollcommand=scroll.set)
    lb.pack(side='left', fill='both', expand=True)
    scroll.config(command=lb.yview)

    # inserisco stringhe nella listbox
    for ll in lista:
        lb.insert(tk.END, ll)

    # callbacks
    def conferma(event=None):
        res["sel"] = list(lb.curselection())
        res["ok"] = len(res["sel"]) > 0
        root.destroy()
 
    def annulla(event=None):
        root.destroy()
    
    # bottoni che chiamano i callbacks
    # frame_bottoni in questo caso serve per definire un nuovo frame in cui inserire i bottoni
    frame_bottoni = tk.Frame(root)
    frame_bottoni.pack(pady=(0, 10))
    tk.Button(frame_bottoni, text="OK", width=10, command=conferma).pack(side="left", padx=5)
    tk.Button(frame_bottoni, text="Annulla", width=10, command=annulla).pack(side="left", padx=5)

    lb.bind("<Double-Button-1>", conferma)  # serve per assegnare al doppio click il callback conferma
    root.bind("<Return>", conferma) # serve per assegnare a enter il callback conferma
    root.bind("<Escape>", annulla) # serve per chiudere tutto con esc
 
    root.mainloop() # serve per mantenere aperta l'interfaccia

    return res["sel"], res["ok"]

#--------------------------------------------------------------------------
def estrai_tdms(file):
    """ Estrae misure, t e fsamp da tdms
        INPUT:
        file = file .tdms
    
        OUTPUT:
        signals = segnali
        time = vettore tempo
        fsamp = sampling f
    """

    tdms = TdmsFile.read(file)
    group = tdms.groups()[0]

    # t
    t_abs = group.channels()[0][:]
    t0 = t_abs[0]
    time = (t_abs - t0) / np.timedelta64(1, 's')
    dt = np.mean(np.diff(time))
    fsamp = 1.0 / dt

    # misure
    signals = np.column_stack([ch[:] for ch in group.channels()[2:]])

    return signals,time,fsamp



# mi serve per debug
# if __name__ == '__main__':