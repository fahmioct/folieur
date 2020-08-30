from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from spectra import *

root = Tk()
root.title("Program 4: Perbandingan Spektrum Lapangan dengan Spektrum Teori")


def open(entr):
    entr.delete(0, END)
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    open_file = filedialog.askopenfilename(title="Select a File", filetype=files, defaultextension=files)
    entr.insert(0, open_file)

label_source = ttk.Label(root, text="Nama File : ", anchor=E, width=10)
data_spec_inp = ttk.Entry(root, width=28)
btn_browse = ttk.Button(root, text= "Browse", command=lambda: open(data_spec_inp))
label_source.grid(row=1, column=1, padx=5, pady=5)
data_spec_inp.grid(row=1, column=2,columnspan=4, padx=5, pady=5)
btn_browse.grid(row=1,column=6,columnspan=3, padx=5, pady=5)

ttk.Label(root, text="Tinggi Gelombang Signifikan (Hs) : ", width=35, anchor=E).grid(row=2, column=0, padx=5, pady=5, columnspan=5)
Hs_inp = ttk.Entry(root, width=10)
Hs_inp.grid(row=2, column=5, padx=5, pady=5)
ttk.Label(root, text="meter", anchor=W, width=10).grid(row=2, column=6, padx=5, pady=5)

ttk.Label(root, text="Perioda Gelombang Signifikan (Ts) : ", width=35, anchor=E).grid(row=3, column=0, padx=5, pady=5, columnspan=5)
Ts_inp = ttk.Entry(root, width = 10)
Ts_inp.grid(row=3, column=5, padx=5, pady=5)
ttk.Label(root, text="detik", anchor=W, width=10).grid(row=3, column=6, padx=5, pady=5)

frame_cocok = ttk.LabelFrame(root, text="Hasil Pemeriksaan Error")
frame_cocok.grid(row=5, column=0, columnspan=9, padx=5, pady=5)
def cocek():
    global f, S_BM, S_Bretschneider, S_JONSWAP, S_MBM, S_MPM, S_PM, S_T1, S_T2, S_TMA, S_Wallops, Sf, sorted_df, df_rame
    if ".csv" in data_spec_inp.get():
        data = pd.read_csv(data_spec_inp.get())
    elif ".xls" in data_spec_inp.get():
        data = pd.read_excel(data_spec_inp.get())
    else:
        raise Exception("File tidak diketahui")
    f = np.asarray(data["f"])
    Sf = np.asarray(data["S(f)"])

    Hs=float(Hs_inp.get())
    Ts=float(Ts_inp.get())

    S_BM=BM(Hs,Ts,f)
    S_MBM=MBM(Hs,Ts,f)
    S_JONSWAP=JONSWAP(Hs,Ts,f)
    S_Wallops=Wallops(Hs,Ts,f)
    S_TMA=TMA(Hs,Ts,f)
    S_Bretschneider=Bretschneider(Hs,Ts,f)
    S_PM=PM(Hs,Ts,f)
    S_MPM=MPM(Hs,Ts,f)
    S_T1=T1(Hs,Ts,f)
    S_T2=T2(Hs,Ts,f)

    dict_Sf = {
        "Bretschneider" : S_Bretschneider,
        "Bretschneider-Mitsuyasu" : S_BM,
        "Modified Bretschneider-Mitsuyasu" : S_MBM,
        "JONSWAP" : S_JONSWAP,
        "Wallops" : S_Wallops,
        "TMA" : S_TMA,
        "Pierson-Moskowitz" : S_PM,
        "Modified Pierson-Moskowitz" : S_MPM,
        "Toba 1" : S_T1,
        "Toba 2" : S_T2
    }
    df_rame = pd.DataFrame(dict_Sf)
    df = df_rame.sub(Sf,axis=0)**2
    df = df.mean().agg("sqrt")*100
    sorted_df = df.sort_values(ascending=True)
    label_hasil = ttk.Label(frame_cocok, text="Spektrum dengan Error Terkecil: "+sorted_df.index[0]+".", width=60, anchor=CENTER)
    label_hasil.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
    label_error = ttk.Label(frame_cocok, text="Besar Error: "+"%.2f"% sorted_df.values[0]+"%", width=60, anchor=CENTER)
    label_error.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
    btn_export.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
    btn_plot.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


btn_cocok = ttk.Button(root, text="Periksa Error", command=cocek, width=62)
btn_cocok.grid(row=4, column=0, columnspan=9)

def plot_cocok():
    plt.plot(f, Sf, label="Data")
    plt.plot(f, df_rame[sorted_df.index[0]], label=sorted_df.index[0])
    plt.title("Perbandingan Spektrum Data dengan Spektrum "+str(sorted_df.index[0]), wrap=True)
    plt.xlabel(r'Frekuensi ($Hz$)')
    plt.ylabel(r'$S(f)$ $(m^{2}\cdot s)$')
    plt.legend(loc='upper right')
    plt.show()


btn_cocok.grid(row=4, column=0, columnspan=9)
btn_plot = ttk.Button(frame_cocok, text="Plot Spektrum", command=plot_cocok, width=27)

def export_data():
    global sorted_df
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    export_spec = filedialog.asksaveasfilename(title="Save as File", filetype=files, defaultextension=files)
    
    dict_error = {
        "Spektrum" : list(sorted_df.index),
        "Error (%)" : sorted_df.values
    }

    df_baru = pd.DataFrame(dict_error)

    if ".csv" in export_spec:
        df_baru.to_csv(export_spec, sep=",", header=True, index=False)
    elif ".xls" in export_spec:
        df_baru.to_excel(export_spec, header=True, index=False)
    else:
        df_baru.to_csv(export_spec, sep=",", header=True, index=False)


btn_export = ttk.Button(frame_cocok, text="Export Error Data", command=export_data, width=27)

ttk.Label(root, text=chr(169)+" 2020 FO ", relief=SUNKEN, anchor=E, width=63).grid(row=6, column=0, columnspan=9, padx=5, pady=5)
root.mainloop()