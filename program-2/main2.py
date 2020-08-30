from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from spectra import *

root = Tk()
root.title("Program 2: Analisis Gelombang Acak Domain Frekuensi")


def list_source(event):
    global Sf
    if cmb_list_source.get() == "Data Sendiri":
        label_source.grid(row=1, column=0, padx=5, pady=5)
        data_spec_inp.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        btn_browse.grid(row=1,column=3, padx=5, pady=5)
        btn_hitung_parspec.config(state="active")
        Hs_inp.config(state="disabled")
        Ts_inp.config(state="disabled")
        btn_hitung_spec.config(state="disabled")
        cmb_lispec.config(state="disabled")
        btn_ift.config(state="active")
    else:
        btn_hitung_spec.config(state="active")
        cmb_lispec.config(state="active")
        Hs_inp.config(state="active")
        Ts_inp.config(state="active")
        label_source.grid_forget()
        data_spec_inp.grid_forget()
        btn_browse.grid_forget()
        try:
            Sf == True
            btn_hitung_parspec.config(state="active")
            btn_ift.config(state="active")
        except:
            btn_hitung_parspec.config(state="disabled")
            btn_ift.config(state="disabled")

def open(entr):
    entr.delete(0, END)
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    open_file = filedialog.askopenfilename(title="Select a File", filetype=files, defaultextension=files)
    entr.insert(0, open_file)

ttk.Label(root, text="Pilih Sumber Data : ", anchor=CENTER, width=25).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
cmb_list_source = ttk.Combobox(root, value = ["Default", "Data Sendiri"], width=23)
cmb_list_source.current(0)
cmb_list_source.bind("<<ComboboxSelected>>", list_source)
cmb_list_source.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

label_source = ttk.Label(root, text="Input Spektrum : ", anchor=E)
data_spec_inp = ttk.Entry(root, width=26)
btn_browse = ttk.Button(root, text= "Browse", command=lambda: open(data_spec_inp))

frame_ema_sint = LabelFrame(root, text="Pembuatan Seri Waktu Elevasi Muka Air (EMA) Sintetis", padx=5, pady=5)
frame_ema_sint.grid(row=2, column=0, padx=10, pady=5, columnspan=4)

ttk.Label(frame_ema_sint, text="Tinggi Gelombang Signifikan (Hs) : ", width=33, anchor=E).grid(row=0, column=0, padx=5, pady=5)
Hs_inp = ttk.Entry(frame_ema_sint, width=10)
Hs_inp.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_ema_sint, text="meter", anchor=W).grid(row=0, column=2, padx=5, pady=5)

ttk.Label(frame_ema_sint, text="Perioda Gelombang Signifikan (Ts) : ", width=33, anchor=E).grid(row=1, column=0, padx=5, pady=5)
Ts_inp = ttk.Entry(frame_ema_sint, width = 10)
Ts_inp.grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_ema_sint, text="detik", anchor=W).grid(row=1, column=2, padx=5, pady=5)

ttk.Label(frame_ema_sint, text="Durasi Data Elevasi Muka Air : ", width=33, anchor=E).grid(row=2, column=0, padx=5, pady=5)
Tmak_inp = ttk.Entry(frame_ema_sint, width = 10)
Tmak_inp.insert(0, 3600)
Tmak_inp.grid(row=2, column=1, padx=5, pady=5)
ttk.Label(frame_ema_sint, text="detik", anchor=W).grid(row=2, column=2, padx=5, pady=5)

ttk.Label(frame_ema_sint, text="Interval Data Elevasi Muka Air ("+chr(916)+"t) : ", width=33, anchor=E).grid(row=3, column=0, padx=5, pady=5)
delta_t_inp = ttk.Entry(frame_ema_sint, width=10)
delta_t_inp.insert(0, 0.5)
delta_t_inp.grid(row=3, column=1, padx=5, pady=5)
ttk.Label(frame_ema_sint, text="detik", anchor=W).grid(row=3, column=2, padx=5, pady=5)
# ttk.Label(root, text="", anchor=W, width=15).grid(row=3, column=3, padx=5, pady=5)

# frm_plh_spec = Frame(frame_ema_sint).grid(row=4, column=0, padx=5, pady=5)
ttk.Label(frame_ema_sint, text="     Pilih Spektrum : ", width=33, anchor=W).grid(row=4, column=0, padx=5, pady=5)

cmb_lispec = ttk.Combobox(frame_ema_sint, value = ["Bretschneider","Bretschneider-Mitsuyasu", "Modified Bretschneider-Mitsuyasu",
"JONSWAP", "Wallops", "TMA", "Pierson-Moskowitz", "Modified Pierson-Moskowitz", "Toba 1", "Toba 2"], width=31
)
# cmb_lispec.grid(row=4, column=1, columnspan=3, padx=0, pady=10)
# y 98, y 67
cmb_lispec.place(x=117,y=129)


def hitung_spektrum():
    btn_hitung_spec.config(state="disabled")
    global Hs, Ts, tmak, delta_t, f_nyq, delta_f, f, Sf
    Hs = float(Hs_inp.get())
    Ts = float(Ts_inp.get())
    tmak = float(Tmak_inp.get())
    delta_t = float(delta_t_inp.get())
    f_nyq=1/(2*delta_t)
    delta_f=1/tmak
    f = np.arange(delta_f, f_nyq+delta_f, delta_f)
    if cmb_lispec.get() == "Bretschneider":
        Sf = Bretschneider(Hs, Ts, f)
    elif cmb_lispec.get() == "Bretschneider-Mitsuyasu":
        Sf = BM(Hs, Ts, f)
    elif cmb_lispec.get() == "Modified Bretschneider-Mitsuyasu":
        Sf = MBM(Hs, Ts, f)
    elif cmb_lispec.get() == "JONSWAP":
        Sf = JONSWAP(Hs, Ts, f)
    elif cmb_lispec.get() == "Wallops":
        Sf = Wallops(Hs, Ts, f)
    elif cmb_lispec.get() == "TMA":
        Sf = TMA(Hs, Ts, f)
    elif cmb_lispec.get() == "Pierson-Moskowitz":
        Sf = PM(Hs, Ts, f)
    elif cmb_lispec.get() == "Modified Pierson-Moskowitz":
        Sf = MPM(Hs, Ts, f)
    elif cmb_lispec.get() == "Toba 1":
        Sf = T1(Hs, Ts, f)
    elif cmb_lispec.get() == "Toba 2":
        Sf = T2(Hs, Ts, f)
    else:
        btn_hitung_spec.config(state="active")
        raise Exception("Spektrum Tidak Diketahui")

    Sf=np.asarray(Sf)
    btn_hitung_spec.config(state="active")
    btn_plot_spec.config(state="active")
    btn_export_spec.config(state="active")
    btn_ift.config(state="active")
    btn_hitung_parspec.config(state="active")


def plot_spektrum():
    btn_plot_spec.config(state="disabled")
    global f, Sf
    plt.figure()
    plt.plot(f,Sf,label=cmb_lispec.get())
    plt.xlabel(r'Frekuensi ($Hz$)')
    plt.ylabel(r'$S(f)$ $(m^{2}\cdot s)$')
    plt.legend(loc='upper right')
    plt.title('Spektrum Gelombang')
    plt.show()
    btn_plot_spec.config(state="active")

def export_spektrum():
    btn_export_spec.config(state="disabled")
    global f, Sf
    dict_spec = {
            "f (Hz)" : f,
            "S(f) (m^2.s)" : Sf
    }
    df_spec = pd.DataFrame(dict_spec)

    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    export_spec = filedialog.asksaveasfilename(title="Save as File", filetype=files, defaultextension=files)
    if ".csv" in export_spec:
        df_spec.to_csv(export_spec, sep=",", header=True, index=False)
    elif ".xls" in export_spec:
        df_spec.to_excel(export_spec, header=True, index=False)
    else:
        df_spec.to_csv(export_spec, sep=",", header=True, index=False)
    btn_export_spec.config(state="active")

ttk.Label(frame_ema_sint, text="", anchor=W, width=15).grid(row=5, column=0, padx=5, pady=5) #baris dummy


btn_hitung_spec = ttk.Button(frame_ema_sint, text="Hitung Spektrum", command=hitung_spektrum)
btn_hitung_spec.place(x=5, y=157)

# ttk.Entry(frame_ema_sint, width=10).grid(row=5, padx=5, pady=5)

btn_plot_spec = ttk.Button(frame_ema_sint, text="Plot Spektrum", state=DISABLED, command=plot_spektrum)
# btn_plot_spec.grid(row=5)
btn_plot_spec.place(x=112, y=157)

btn_export_spec = ttk.Button(frame_ema_sint, text="Export Data Spektrum", state=DISABLED, command=export_spektrum)
# btn_export_spec.grid(row=5, column=1, padx=5, pady=5)
btn_export_spec.place(x=202, y=157)

def ift():
    btn_ift.config(state="disabled")
    progress_ift["value"]=0
    global f, Sf, delta_t, tmak, t, delta_f, eta_
    
    if cmb_list_source.get() == "Data Sendiri":
        if ".csv" in data_spec_inp.get():
            spec = pd.read_csv(data_spec_inp.get())
        elif ".xls" in data_spec_inp.get():
            spec = pd.read_excel(data_spec_inp.get())
        else:
            btn_ift.config(state="active")
            raise Exception("File tidak diketahui.")
        f = np.asarray(spec["f"])
        delta_f = f[1]-f[0]
        Sf = np.asarray(spec["S(f)"])
        delta_t = float(delta_t_inp.get())
        tmak = float(Tmak_inp.get())
    
    t = np.arange(delta_t, tmak+delta_t, delta_t)
    nk = len(f)
    nj = len(t)
    fasa=np.random.rand(int(nk))*2*np.pi
    eta_=np.zeros(nj)
    c=np.sqrt(Sf*2*delta_f)
    for j in range(nj):
        eta_[j]=np.sum(c*np.cos(2*np.pi*f*t[j]+fasa))
        progress_ift["value"]+=1/nj*100
        root.update_idletasks()
    btn_ift.config(state="active")
    btn_plot_ema_syn.config(state="active")
    btn_export_ema_syn.config(state="active")

def plot_ema_syn():
    btn_plot_ema_syn.config(state="disabled")
    global t, eta_
    plt.figure()
    plt.plot(t,eta_)
    plt.title('Elevasi Muka Air Sintetis')
    plt.xlabel('Waktu (detik)')
    plt.ylabel(r'Elevasi Muka Air ($m$)')
    plt.show()
    btn_plot_ema_syn.config(state="active")

def export_ema_syn():
    btn_export_ema_syn.config(state="disabled")
    global t, eta_
    dict_ema_syn = {
            "t (s)" : t,
            "ema (m)" : eta_
    }
    df_ema_syn = pd.DataFrame(dict_ema_syn)
    
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    export_ema_syn = filedialog.asksaveasfilename(title="Save as File", filetype=files, defaultextension=files)
    if ".csv" in export_ema_syn:
        df_ema_syn.to_csv(export_ema_syn, sep=",", header=True, index=False)
    elif ".xls" in export_ema_syn:
        df_ema_syn.to_excel(export_ema_syn, header=True, index=False)
    else:
        df_ema_syn.to_csv(export_ema_syn, sep=",", header=True, index=False)
    btn_export_ema_syn.config(state="active")

btn_ift = ttk.Button(frame_ema_sint, text="Start Inverse Fourier Transform!", width=52, state=DISABLED, command=ift)
btn_ift.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

progress_ift = ttk.Progressbar(frame_ema_sint, orient=HORIZONTAL, mode="determinate", length=320)
progress_ift.grid(row=7, column=0, columnspan=3, padx=5, pady=1)

ttk.Label(frame_ema_sint, text="", anchor=W, width=15).grid(row=8, column=0, padx=5, pady=5) #baris dummy
btn_plot_ema_syn = ttk.Button(frame_ema_sint, text="Plot EMA Sintetis", state=DISABLED, width=24, command=plot_ema_syn)
btn_plot_ema_syn.place(x=5, y=245)

btn_export_ema_syn = ttk.Button(frame_ema_sint, text="Export Data EMA Sintetis", state=DISABLED, width=24, command=export_ema_syn)
btn_export_ema_syn.place(x=173, y=245)
# ttk.Entry(frame_ema_sint, width=10).grid(row=8, padx=5, pady=5)

frame_param_spec = LabelFrame(root, text="Parameter Gelombang Domain Frekuensi (PGDF)", padx=5, pady=5)
frame_param_spec.grid(row=3, column=0, padx=10, pady=5, columnspan=4)

def lihat_parspec():
    global df_parspec
    frame_view = Toplevel()
    frame_view.title("Parameter Gelombang Domain Frekuensi")
    tree_parspec = ttk.Treeview(frame_view)
    tree_parspec["columns"] = ("#1", "#2")
    tree_parspec.heading("#0", text="")
    tree_parspec.heading("#1", text="Nilai")
    tree_parspec.heading("#2", text="Satuan")
    for i in range(len(df_parspec.index)):
        tree_parspec.insert("", END, text=df_parspec.index[i], values=tuple(df_parspec.iloc[i]))
    tree_parspec.pack()


def hitung_pgdf():
    btn_hitung_parspec.config(state="disabled")
    global Sf, f, delta_f, s_parspec, dict_mn, parspec, df_parspec

    if cmb_list_source.get() == "Default":
        moment = momen(Sf, f, delta_f)
    elif cmb_list_source.get() == "Data Sendiri":
        if ".csv" in data_spec_inp.get():
            df = pd.read_csv(data_spec_inp.get())
        elif ".xls" in data_spec_inp.get():
            df = pd.read_excel(data_spec_inp.get())
        else:
            btn_hitung_parspec.config(state="active")
            raise Exception("File tidak diketahui.")
            
        Sf = df["S(f)"]
        f = df["f"]
        delta_f = f[1] - f[0]
    moment = momen(Sf, f, delta_f)
    dict_mn, parspec = pgdf(moment)
    s_parspec = pd.Series({**dict_mn, **parspec})
    df_parspec = pd.DataFrame(s_parspec)
    df_parspec.rename(columns={0: "Nilai"}, inplace=True)
    df_parspec["Satuan"] = ["m^2.s", "m^2", "m^2/s", "m^2/s^2", "m", "s", "s", "s"]
    btn_hitung_parspec.config(state="active")
    btn_export_parspec.config(state="active")
    btn_lihat_parspec.config(state="active")

def export_parspec():
    btn_export_parspec.config(state="disabled")
    global df_parspec
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    export_par_spec = filedialog.asksaveasfilename(title="Save as File", filetype=files, defaultextension=files)
    if ".csv" in export_par_spec:
        df_parspec.to_csv(export_par_spec, sep=",", header=True, index=True)
    elif ".xls" in export_par_spec:
        df_parspec.to_excel(export_par_spec, header=True, index=True)
    else:
        df_parspec.to_csv(export_par_spec, sep=",", header=True, index=True)
    btn_export_parspec.config(state="active")


btn_hitung_parspec = ttk.Button(frame_param_spec, text="Hitung PGDF", width=24, state=DISABLED, command=hitung_pgdf)
btn_hitung_parspec.grid(row=2, column=0, columnspan=2, pady=5, padx=5)
btn_export_parspec = ttk.Button(frame_param_spec, text="Export Data PGDF", width=24, state=DISABLED, command=export_parspec)
btn_export_parspec.grid(row=2, column=2, columnspan=2, pady=5, padx=5)

btn_lihat_parspec = ttk.Button(frame_param_spec, text="Lihat Parameter Gelombang Domain Frekuensi", state=DISABLED, command=lihat_parspec, width=52)
btn_lihat_parspec.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
# frame_view = LabelFrame(root, text="Parameter Gelombang Domain Frekuensi", padx=5, pady=5)
# frame_view.grid(padx=10, pady=5)

# tree_parspec = ttk.Treeview(frame_view)
# tree_parspec["columns"] = ("#1")
# tree_parspec.heading("#0", text="")
# tree_parspec.heading("#1", text="Nilai")

ttk.Label(root, text=chr(169)+" 2020 FO ", relief=SUNKEN, anchor=E, width=57).grid(row=4, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()