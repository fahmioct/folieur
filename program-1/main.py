from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import pandas as pd
# from zc import zuc, zdc
import numpy as np
# from stats_HT import *
# from dist_ray import *
# from fo_trf import *
from folieur import *
import matplotlib.pyplot as plt

root = Tk()
root.title("Program 1: Analisis Gelombang Acak Domain Waktu")

# class frame_box(object):
#     global row_count
#     row_count = 0
#     def __init__(self, master, teks):
#         self.row_count = row_count
#         self.myFrame = LabelFrame(master, text=teks, padx=5, pady=5)
#         self.myFrame.grid(row=row_count, column=0, padx=10, pady=5, columnspan=4)
#         self.row_count+=1

# zc_frame = frame_box(root, "Zero-Crossing")
zc_frame = LabelFrame(root, text="Zero-Crossing", padx=5, pady=5)
zc_frame.grid(row=1, column=0, padx=10, pady=5, columnspan=4)

ttk.Label(root, text="Input File EMA : ", width=25, anchor=CENTER).grid(row=0, column=0, padx=5, pady=5)
ttk.Label(zc_frame, text="Output File Zero-Crossing : ", width=26, anchor=E).grid(row=0, column=0, padx=5, pady=5)

ema_inp = ttk.Entry(root, width=35)
ema_inp.grid(row=0, column=1, columnspan=2, padx=5, pady=10)
zc_out = ttk.Entry(zc_frame, width=32)
zc_out.grid(row=0, column=1, columnspan=2, padx=5, pady=10)

def open(entr):
    entr.delete(0, END)
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    open_file = filedialog.askopenfilename(title="Select a File", filetypes=files, defaultextension=files)
    entr.insert(0, open_file)

def save(entr):
    entr.delete(0, END)
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    save_file = filedialog.asksaveasfilename(title="Save as File", filetypes=files, defaultextension=files)
    entr.insert(0, save_file)

ttk.Button(root, text= "Browse", command=lambda: open(ema_inp)).grid(row=0,column=3, padx=5)
ttk.Button(zc_frame, text= "Browse", command=lambda: save(zc_out)).grid(row=0,column=3, padx=5)

def zc_button(mtd):
    global HT, eta0, t, ema
    btn_zc.config(state="disabled")

    if ".csv" in ema_inp.get():
        data=pd.read_csv(ema_inp.get())
    elif ".xls" in ema_inp.get():
        data=pd.read_excel(ema_inp.get())
    else:
        btn_zc.config(state="active")
        raise Exception("File tidak diketahui.")

    t=np.asarray(data["t"])
    ema=np.asarray(data["ema"])
    if mtd == "Zero-Upcrossing":
        HT, eta0=zuc(ema,t)
    elif mtd == "Zero-Downcrossing":
        HT, eta0=zdc(ema,t)
    df_HT=pd.DataFrame(HT,columns=["H (m)","T (s)"])

    if ".csv" in zc_out.get():
        df_HT.to_csv(zc_out.get(),sep=",", header=True, index=False)
    elif ".xls" in zc_out.get():
        df_HT.to_excel(zc_out.get(), header=True, index=False)
    else:
        df_HT.to_csv(zc_out.get(),sep=",", header=True, index=False)

    btn_zc.config(state="active")
    btn_stat_ht.config(state="active")

ttk.Label(zc_frame, text="Metode Zero-Crossing : ", width=26, anchor=E).grid(row=2, column=0, padx=5, pady=5)
combo_zc = ttk.Combobox(zc_frame, value = ["Zero-Upcrossing", "Zero-Downcrossing"])
combo_zc.current(1)
combo_zc.grid(row=2, column=1, columnspan=2, padx=5, pady=10)
btn_zc = ttk.Button(zc_frame, text="Zero-Cross", command=lambda: zc_button(combo_zc.get()), width=73)
btn_zc.grid(row=3, column=0, columnspan=4, padx=5, pady=5)



stat_HT_frame = LabelFrame(root, text="Statistik Gelombang", padx=5, pady=5)
stat_HT_frame.grid(row=2, column=0, padx=10, pady=5, columnspan=4)

# Label(stat_HT_frame, text="Input File H T Gelombang : ", width=22, anchor=E).grid(row=0, column=0, padx=5, pady=5)
Label(stat_HT_frame, text="Output Statistik Gelombang : ", width=22, anchor=E).grid(row=0, column=0, padx=5, pady=5)

# HT_inp = Entry(stat_HT_frame, width=30)
# HT_inp.grid(row=0, column=1, columnspan=2, padx=5, pady=10)
stat_out = ttk.Entry(stat_HT_frame, width=32)
stat_out.grid(row=0, column=1, columnspan=2, padx=5, pady=10)
# Button(stat_HT_frame, text= "Browse", command=lambda: open(HT_inp)).grid(row=0,column=3, padx=5)
ttk.Button(stat_HT_frame, text= "Browse", command=lambda: save(stat_out)).grid(row=0,column=3, padx=5)

def stat_HT_button():
    btn_stat_ht.config(state="disabled")
    global HT, H, T
    H=np.asarray(HT[:,0])
    T=np.asarray(HT[:,1])
    global Hmaks, Tmaks, Hmean, Tmean, H_rms, Hs, Ts, H_10, T_10, H_100, T_100, etarms
    etarms = eta_rms(eta0)
    Hmaks,Tmaks=HTmaks(H, T)
    Hmean,Tmean=HTmean(H, T)
    H_rms=Hrms(H)
    Hs,Ts=HT1pern(H,T,3)
    H_10,T_10 = HT1pern(H,T,10)
    H_100,T_100 = HT1pern(H,T,100)
    df_param_HT = pd.DataFrame(
        {
            "H (m)" : [Hmaks, Hmean, H_rms, Hs, H_10, H_100],
            "T (s)" : [Tmaks, Tmean, np.nan, Ts, T_10, T_100]
        }, index=["Maks", "Mean", "RMS", "1/3", "1/10", "1/100"]
    )

    if ".csv" in stat_out.get():
        df_param_HT.to_csv(stat_out.get(),sep=",", header=True, index=True)
    elif ".xls" in stat_out.get():
        df_param_HT.to_excel(stat_out.get(), header=True, index=True)
    else:
        df_param_HT.to_csv(stat_out.get(),sep=",", header=True, index=True)

    btn_stat_ht.config(state="active")
    btn_lihat_stat.config(state="active")
    btn_plot_hist.config(state="active")

def lihat_stat_HT():
    window_stat_HT = Toplevel()
    window_stat_HT.title("Statistik Gelombang Domain Waktu")
    tree = ttk.Treeview(window_stat_HT)
    tree["columns"] = ("#1", "#2")
    tree.heading("#0", text="Parameter Statistik Gelombang")
    tree.heading("#1", text="H (m)")
    tree.heading("#2", text="T (s)")
    tree.insert("",END,text="Maks", values=(Hmaks, Tmaks))
    tree.insert("",END,text="Mean", values=(Hmean, Tmean))
    tree.insert("",END,text="RMS", values=(H_rms, np.nan))
    tree.insert("",END,text="1/3", values=(Hs, Ts))
    tree.insert("",END,text="1/10", values=(H_10, T_10))
    tree.insert("",END,text="1/100", values=(H_100, T_100))
    tree.pack(side=TOP, fill=BOTH, expand=TRUE)

btn_stat_ht = ttk.Button(stat_HT_frame, text="Hitung Statistik H T Gelombang", command=stat_HT_button, width=34, state=DISABLED)
btn_stat_ht.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
btn_lihat_stat = ttk.Button(stat_HT_frame, text="Lihat Tabel", command=lihat_stat_HT, width=34, state=DISABLED)
btn_lihat_stat.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

Label(stat_HT_frame, text="Jumlah Kelas : ", width=22, anchor=E).grid(row=3, column=0, padx=5, pady=5)

def kls_bttn():
    global H
    kmaks, kmin = jml_kls(H)
    Label(
        stat_HT_frame,
        text="Jumlah Kelas yang Direkomendasikan : "+str(round(kmin, 2))+" - "+str(round(kmaks, 2)),
        anchor=CENTER
        ).grid(row=4, column=0, columnspan=4, padx=5, pady=5)

kls_entr = ttk.Entry(stat_HT_frame, width=32)
kls_entr.insert(0, 10)
kls_entr.grid(row=3, column=1, columnspan=2, padx=5, pady=10)
ttk.Button(stat_HT_frame, text= "Saran?", command=kls_bttn).grid(row=3,column=3, padx=5)

Label(stat_HT_frame, text="Tinggi Gelombang Acuan : ", width=22, anchor=E).grid(row=5, column=0, padx=5, pady=5)

combo_Hacuan = ttk.Combobox(stat_HT_frame, value = ["eta_rms", "Hmean", "Hrms", "Hs"])
combo_Hacuan.current(3)
combo_Hacuan.grid(row=5, column=1, columnspan=2, padx=5, pady=10)


def plot_hist():
    btn_plot_hist.config(state="disabled")
    global H, x, x_0, pdf, cdf, frek_H, kls_H, frek_x, kls_x
    if combo_Hacuan.get() == "eta_rms":
        H_acuan = etarms
    elif combo_Hacuan.get() == "Hmean":
        H_acuan = Hmean
    elif combo_Hacuan.get() == "Hrms":
        H_acuan = H_rms
    elif combo_Hacuan.get() == "Hs":
        H_acuan = Hs
    else:
        btn_plot_hist.config(state="active")
        raise Exception("Nilai tinggi gelombang acuan tidak diketahui.")
    x, x_0, pdf,cdf, frek_H, kls_H, frek_x, kls_x=histH(H, H_acuan, int(kls_entr.get()), combo_Hacuan.get())

    plt.show()
    btn_plot_hist.config(state="active")
    btn_export_hist.config(state="active")

def export_hist():
    btn_export_hist.config(state="disabled")
    global x_0, pdf, cdf, frek_H, kls_H, frek_x, kls_x
    dict_export_hist = {
        "x" : x_0,
        "pdf_rayleigh" : pdf,
        "cdf_rayleigh" : cdf,
        "frekuensi_H" : frek_H,
        "bins_H" : kls_H,
        "frekuensi_x" : frek_x,
        "bins_x" : kls_x
    }
    df_export_hist=pd.DataFrame.from_dict(dict_export_hist, orient="index").T
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    export_hist = filedialog.asksaveasfilename(title="Save as File", filetypes=files, defaultextension=files)
    if ".csv" in export_hist:
        df_export_hist.to_csv(export_hist, sep=",", header= True, index=False)
    elif ".xls" in export_hist:
        df_export_hist.to_excel(export_hist, header= True, index=False)
    else:
        df_export_hist.to_csv(export_hist, sep=",", header= True, index=False)
    btn_export_hist.config(state="active")

btn_plot_hist = ttk.Button(stat_HT_frame, text="Plot Histogram", command=plot_hist, width=34, state=DISABLED)
btn_plot_hist.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
btn_export_hist = ttk.Button(stat_HT_frame, text="Export Data Histogram", command=export_hist, width=34, state=DISABLED)
btn_export_hist.grid(row=6, column=2, columnspan=2, padx=5, pady=5)

fourier_trans_frame = LabelFrame(root, text="Transformasi Fourier", padx=5, pady=5)
fourier_trans_frame.grid(row=3, column=0, padx=5, pady=5, columnspan=4)

def psd(data):
    btn_ft.config(state="disabled")
    trans_progress["value"]=0
    global f, psd, ck
    if ".csv" in data:
        data_ema=pd.read_csv(data)
    elif ".xls" in data:
        data_ema=pd.read_excel(data)
    else:
        btn_ft.config(state="active")
        raise Exception("File tidak diketahui.")

    t=np.asarray(data_ema["t"])
    ema=np.asarray(data_ema["ema"])

    tmak = t[-1]
    delta_t = t[1]-t[0]

    regresi=np.polyfit(t,ema,1)
    eta0=ema-regresi[0]*t
    eta0=eta0-np.mean(eta0)

    nj=len(eta0)        # jumlah titik data ema
    f_nyq=1/(2*delta_t) # frekuensi maksimum
    df=1/tmak           # delta_f
    K=int(f_nyq/df)     # jumlah fungsi harmonik

    ak=np.zeros(K)
    bk=np.zeros(K)
    j=np.arange(1,nj+1)  # 1, 2, 3, ..., nj
    
    for k in range(1,K+1):
        ak[k-1]=2/nj*np.sum(eta0*np.cos(k*2*np.pi/tmak*(j*delta_t)))
        bk[k-1]=2/nj*np.sum(eta0*np.sin(k*2*np.pi/tmak*(j*delta_t)))
        trans_progress["value"]+=1/K*100
        root.update_idletasks()
    ck=np.sqrt(ak**2+bk**2)

    f=np.linspace(df,f_nyq+df,ck.size)
    psd=ck**2/2/df
    btn_ft.config(state="active")
    btn_plot_spec.config(state="active")
    btn_export_spec.config(state="active")

btn_ft = ttk.Button(fourier_trans_frame, text="Start Fourier Transform!", command=lambda: psd(ema_inp.get()), width=74)
btn_ft.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

trans_progress = ttk.Progressbar(fourier_trans_frame, orient=HORIZONTAL, mode="determinate", length=452)
trans_progress.grid(row=2,column=0, columnspan=4, padx=5, pady=5)

def plot_spectra():
    btn_plot_spec.config(state="disabled")
    global f, psd
    plt.figure()
    plt.plot(f,psd,label='PSD')
    plt.title(r'$\mathit{Power\ Spectral\ Density}$')
    plt.xlabel(r'Frekuensi ($Hz$)')
    plt.ylabel(r'$\frac{C^2}{2 \cdot \Delta f}\ (m^2s)$')
    plt.show()
    btn_plot_spec.config(state="active")

def export_spectra():
    btn_export_spec.config(state="disabled")
    global f, sf, ck
    dict_export_spectra = {
        "f (Hz)" : f,
        "PSD (m^2.s)" : psd,
        "ck (m)" : ck
    }
    df_export_spectra=pd.DataFrame.from_dict(dict_export_spectra, orient="index").T
    
    files = [
        ("CSV File", "*.csv"),("Excel File", "*.xls;*.xlsx"),("All Files", "*.*")
    ]
    export_spectra = filedialog.asksaveasfilename(title="Save as File", filetypes=files, defaultextension=files)
    if ".csv" in export_spectra:
        df_export_spectra.to_csv(export_spectra, sep=",", header= True, index=False)
    elif ".xls" in export_spectra:
        df_export_spectra.to_excel(export_spectra, header= True, index=False)
    else:
        df_export_spectra.to_csv(export_spectra, sep=",", header= True, index=False)    

    btn_export_spec.config(state="active")

btn_plot_spec = ttk.Button(fourier_trans_frame, text="Plot Spektrum", command=plot_spectra, width=35, state=DISABLED)
btn_plot_spec.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
btn_export_spec = ttk.Button(fourier_trans_frame, text="Export Data Spektrum", command=export_spectra, width=35, state=DISABLED)
btn_export_spec.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

ttk.Label(root, text=chr(169)+" 2020 FO ", relief=SUNKEN, anchor=E, width=79).grid(row=4, column=0, columnspan=4, padx=5, pady=10)
# Creating a Label Widget
# myLabel1 = Label(root, text="Hello Worlds!")
# myLabel2 = Label(root, text="asdasdasdsa")

# myLabel1.grid(row=0, column=0)
# myLabel2.grid(row=1, column=1)

# Showing it onto the screen == pack it at the first available spot
#myLabel.pack()

# e = Entry(root, width=50, borderwidth=5)
# e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
# e.insert(0, "Enter your name: ")

# def myClick():
#     #myLabel = Label(root, text="Look! Clicked button!")
#     myLabel = Label(root, text= "Hello "+ e.get())
#     myLabel.pack()

# # myButton = Button(root, text= "Click Me!", state=DISABLED, padx=50,pady=50)
# myButton = Button(root, text= "Enter your name", command=myClick, fg="blue", bg="#ffffff")
#myButton.pack()


root.mainloop()