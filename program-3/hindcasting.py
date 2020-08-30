# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 17:07:35 2020

@author: Fahmi
"""

#import library
import pandas as pd
import numpy as np
from scipy.constants import g, knot
dangin=pd.read_csv('dangin.csv')
fetch_eff=pd.read_csv('fetch_eff.csv')

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
step_durasi=int(input('Interval data angin (dalam jam): '))
durasi[0]=step_durasi
for i in range(1,len(Wind8Dir)):
    if Wind8Dir[i]==Wind8Dir[i-1]:
        durasi[i]=durasi[i-1]+step_durasi
    else:
        durasi[i]=step_durasi

dangin['Duration']=durasi


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

dangin['Hs']=Hs
dangin['Ts']=Ts

#mengeluarkan file output
#kolom 1 = Hs
#kolom 2 = Tp
#df = pd.DataFrame(data=hindcast)
dangin.to_csv('hindcast.csv', sep=',', header=True, index=False)