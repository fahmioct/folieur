from tkinter import Tk,E,W, HORIZONTAL, END, SUNKEN
from tkinter import filedialog
from tkinter import ttk

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from scipy.constants import g, knot

root = Tk()
root.title("Program 3: Hindcasting Gelombang")

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

#definisi fungsi jika fetch-limited
def fetch_limited(F,U10):
    F=F*1000
    H_1per3=U10**2/g*0.3*(1-(1+0.004*(g*F/U10**2)**(0.5))**(-2))
    T_1per3=U10/g*8.61*(1-(1+0.008*(g*F/U10**2)**(1/3))**(-5))
    return H_1per3, T_1per3

#definisi fungsi jika duration-limited
def duration_limited(F,U10,t_data):
    F_min=1.0*t_data**1.37*U10**0.63 * 1000
    t_data=t_data*3600
    
    H_1per3=U10**2/g*0.3*(1-(1+0.004*(g*F_min/U10**2)**(0.5))**(-2))
    T_1per3=U10/g*8.61*(1-(1+0.008*(g*F_min/U10**2)**(1/3))**(-5))
    return H_1per3, T_1per3


def start_hc():
    global dangin, fetch_eff, WindSpd, durasi, step_durasi, Hs, Ts, fetch, t_min
    btn_hc.config(state="disabled")
    if ".csv" in entr_hc.get():
        dangin = pd.read_csv(entr_hc.get())
    elif ".xls" in entr_hc.get():
        dangin = pd.read_excel(entr_hc.get())
    else:
        raise Exception("File tidak diketahui.")

    if ".csv" in entr_feff.get():
        fetch_eff = pd.read_csv(entr_feff.get())
    elif ".xls" in entr_feff.get():
        fetch_eff = pd.read_excel(entr_feff.get())
    else:
        raise Exception("File tidak diketahui.")

    WindSpd=np.asarray(dangin['WindSpd'])
    WindSpd=WindSpd*knot

    WDLookUp=pd.DataFrame({
        'WD': ['N','N','NE','E','SE','S','SW','W','NW'],
        'Min': [337.5,0,22.5,67.5,112.5,157.5,202.5,247.5,292.5],
        'Max': [360,22.5,67.5,112.5,157.5,202.5,247.5,292.5,337.5]
        })

    val=WDLookUp.loc[:,'Min':'Max'].apply(tuple,1)
    indx=pd.IntervalIndex.from_tuples(val,closed='left')
    Wind8Dir=WDLookUp.loc[indx.get_indexer(dangin['WindDir']),'WD'].values
    dangin['Dir8']=Wind8Dir
    dangin=dangin.merge(fetch_eff[['Dir8','Feff']], on='Dir8', how="left")

    #menghitung durasi untuk setiap data
    durasi=np.zeros(len(Wind8Dir))
    step_durasi=int(entr_step_dur.get())
    durasi[0]=step_durasi
    for i in range(1,len(Wind8Dir)):
        if Wind8Dir[i]==Wind8Dir[i-1]:
            durasi[i]=durasi[i-1]+step_durasi
        else:
            durasi[i]=step_durasi

    dangin['Duration']=durasi

    #definisi variabel Hs dan Ts
    Hs=np.zeros(len(WindSpd))
    Ts=np.zeros(len(WindSpd))

    fetch=np.asarray(dangin['Feff'])
    t_min=1.0*fetch**0.73*WindSpd**(-0.46)
    #perhitungan hindcasting
    for i in range(len(WindSpd)):
        if durasi[i]>t_min[i]:
            Hs[i],Ts[i]=fetch_limited(fetch[i],WindSpd[i])
        else:
            Hs[i],Ts[i]=duration_limited(fetch[i],WindSpd[i],durasi[i])
        prog_hc["value"]+=1/len(WindSpd)*100
        root.update_idletasks()

    dangin['Hs']=Hs
    dangin['Ts']=Ts

    #mengeluarkan file output
    if ".csv" in entr_out.get():
        dangin.to_csv(entr_out.get(), sep=',', header=True, index=False)
    elif ".xls" in entr_out.get():
        dangin.to_excel(entr_out.get(), header=True, index=False)
    else:
        dangin.to_csv(entr_out.get(), sep=',', header=True, index=False)

    btn_hc.config(state="active")

ttk.Label(root, text="Input File Data Angin : ", anchor=E, width=22).grid(row=0, column=0, padx=5, pady=5)
entr_hc = ttk.Entry(root, width=30)
entr_hc.grid(row=0, column=1, columnspan=2, padx=5, pady=10)

ttk.Button(root, text= "Browse", command=lambda: open(entr_hc)).grid(row=0,column=3, padx=5)

ttk.Label(root, text="Input File Fetch Efektif : ", anchor=E, width=22).grid(row=1, column=0, padx=5, pady=5)
entr_feff = ttk.Entry(root, width=30)
entr_feff.grid(row=1, column=1, columnspan=2, padx=5, pady=10)
ttk.Button(root, text= "Browse", command=lambda: open(entr_feff)).grid(row=1,column=3, padx=5)

ttk.Label(root, text="Interval Data Angin : ", anchor=E, width=22).grid(row=2, column=0, padx=5, pady=10)
entr_step_dur = ttk.Entry(root, width=10)
entr_step_dur.insert(0, 1)
entr_step_dur.place(x=151, y=92) #grid(row=2, column=1, padx=5, pady=10)
# ttk.Entry(root, width=10).grid(row=2, column=1, padx=5, pady=10)
ttk.Label(root, text="jam", anchor=W).place(x=230, y=92) #grid(row=2, column=2, padx=5, pady=5)

ttk.Label(root, text="Output File Hindcasting : ", anchor=E, width=22).grid(row=3, column=0, padx=5, pady=5)
entr_out = ttk.Entry(root, width=30)
entr_out.grid(row=3, column=1, columnspan=2, padx=5, pady=10)
ttk.Button(root, text= "Browse", command=lambda: save(entr_out)).grid(row=3,column=3, padx=5)

btn_hc = ttk.Button(root, text="Start Wave Hindcasting!", width=68, command=start_hc)
btn_hc.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

prog_hc = ttk.Progressbar(root, orient=HORIZONTAL, mode="determinate", length=416)
prog_hc.grid(row=5, column=0, columnspan=4, padx=5, pady=5)


ttk.Label(root, text=chr(169)+" 2020 FO ", relief=SUNKEN, anchor=E, width=69).grid(row=6, column=0, columnspan=4, padx=5, pady=5)
root.mainloop()