import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def zuc(ema,t):
    #zero-mean elevasi muka air
    t=np.asarray(t)
    ema=np.asarray(ema)
    # interval=t[1]-t[0]

    regresi=np.polyfit(t,ema,1)
    eta0=ema-regresi[0]*t
    eta0=eta0-np.mean(eta0)
    
    #akan digunakan untuk zero-upcrossing    
    indeks_zc=[]
    t_temp=[]
    
    #menangkap indeks dari perubahan nilai elevasi muka air
    for j in range(1,len(t)):
        if (eta0[j-1]<eta0[j]) and (eta0[j-1]*eta0[j]<0):
            indeks_zc.append(j)
            t_temp.append(t[j-1]-((t[j]-t[j-1])/(eta0[j]-eta0[j-1]))*eta0[j-1])
        
    #menghitung perioda gelombang dari indeks yang sudah ditangkap
    T=[]
    for j in range(1,len(t_temp)):
        T.append(t_temp[j]-t_temp[j-1])
    
    #menghitung tinggi gelombang dari indeks yang sudah ditangkap
    H=[]
    for j in range(1,len(indeks_zc)):
        maks=np.amax(eta0[indeks_zc[j-1]:indeks_zc[j]])
        mini=np.amin(eta0[indeks_zc[j-1]:indeks_zc[j]])
        H.append(maks-mini)
    
    #membuat tinggi gelombang dan perioda gelombang dalam 1 variabel
    HT=np.zeros((len(H),2))
    for i in range(len(H)):
        HT[i,:]=[H[i],T[i]]
    
    #menyortir tinggi gelombang dari yang terbesar hingga terkecil
    # Sorted_HT=HT[HT[:,0].argsort()[::-1]]
    return HT, eta0

def zdc(ema,t):
    #zero-mean elevasi muka air
    t=np.asarray(t)
    ema=np.asarray(ema)
    # interval=t[1]-t[0]

    regresi=np.polyfit(t,ema,1)
    eta0=ema-regresi[0]*t
    eta0=eta0-np.mean(eta0)
    
    #akan digunakan untuk zero-upcrossing    
    indeks_zc=[]
    t_temp=[]
    
    #menangkap indeks dari perubahan nilai elevasi muka air
    for j in range(1,len(t)):
        if (eta0[j-1]>eta0[j]) and (eta0[j-1]*eta0[j]<0):
            indeks_zc.append(j)
            t_temp.append(t[j-1]-((t[j]-t[j-1])/(eta0[j]-eta0[j-1]))*eta0[j-1])
        
    #menghitung perioda gelombang dari indeks yang sudah ditangkap
    T=[]
    for j in range(1,len(t_temp)):
        T.append(t_temp[j]-t_temp[j-1])
    
    #menghitung tinggi gelombang dari indeks yang sudah ditangkap
    H=[]
    for j in range(1,len(indeks_zc)):
        maks=np.amax(eta0[indeks_zc[j-1]:indeks_zc[j]])
        mini=np.amin(eta0[indeks_zc[j-1]:indeks_zc[j]])
        H.append(maks-mini)
    
    #membuat tinggi gelombang dan perioda gelombang dalam 1 variabel
    HT=np.zeros((len(H),2))
    for i in range(len(H)):
        HT[i,:]=[H[i],T[i]]
    
    #menyortir tinggi gelombang dari yang terbesar hingga terkecil
    # Sorted_HT=HT[HT[:,0].argsort()[::-1]]
    return HT, eta0

def HTmaks(H,T):
    Sorted_H=H[H.argsort()[::-1]]
    Sorted_T=T[H.argsort()[::-1]]
    Hmaks = Sorted_H[0]
    Tmaks = Sorted_T[0]
    return Hmaks, Tmaks

def HTmean(H,T):
    Hmean = np.mean(H)
    Tmean = np.mean(T)
    return Hmean, Tmean

def Hrms(H):
    tinggigelrms = np.sqrt(np.mean(H**2))
    return tinggigelrms

def HT1pern(H,T,n):
    Sorted_H=H[H.argsort()[::-1]]
    Sorted_T=T[H.argsort()[::-1]]
    N=int(np.around(len(H)/n))
    Hpern=np.mean(Sorted_H[:N])
    Tpern=np.mean(Sorted_T[:N])
    return Hpern, Tpern

def eta_rms(ema):
    ema = np.asarray(ema)
    return np.sqrt(np.mean(ema**2))

def jml_kls(H):
    stat_H=H[H.argsort()]
    
    Hpd=pd.Series(stat_H)
    Q1,Q3=Hpd.quantile([0.25,0.75],'midpoint')
    iqr=Q3-Q1
    
    N=len(H)
    k_1=np.sqrt(N)
    k_2=1+3.3*np.log10(N)
    r=np.amax(H)-np.amin(H)
    k_3=(r*N**(1/3))/(2*iqr)

    k=np.array([k_1,k_2,k_3])
    k_maks=np.amax(k)
    k_min=np.amin(k)
    return k_maks, k_min

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{:.0f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def histH(H,H_acuan,jml_kls,a):
    if a=='eta_rms':
        A=0.5*np.sqrt(2)
    elif a=='Hmean':
        A=np.sqrt(np.pi)/2
    elif a=='Hrms':
        A=1
    elif a=='Hs':
        A=1.416
    else:
        raise Exception('Nilai a tidak diketahui')
    H=np.asarray(H)
    H.sort()
    x=H/H_acuan
    
    rentang=np.amax(x)-np.amin(x)
    dx=rentang/jml_kls
    
    plt.figure(num=1)
    frek_H, kls_H, patches_H = plt.hist(H,bins=jml_kls,edgecolor='k')
    # plt.grid(axis='y')
    plt.xticks(np.around(kls_H,2))
    plt.title('Histogram Tinggi Gelombang')
    plt.xlabel(r'Tinggi Gelombang ($m$)')
    plt.ylabel('Frekuensi Kejadian')
    autolabel(patches_H)

    plt.figure(num=2)
    frek_x, kls_x, patches_x = plt.hist(x,bins=jml_kls,density=True,edgecolor='k', label=r'$\mathit{Normalized}$ Histogram')
    # frek_x, kls_x, patches_x = plt.hist(x,bins=jml_kls,weights=np.ones_like(x)/(len(x)*dx),edgecolor='k', label=r'$\mathit{Normalized}$ Histogram')
    
    x_1=np.insert(x,0,0)
    pdf_rayleigh=2*A**2*x_1*np.exp(-A**2*x_1**2)
    cdf_rayleigh=1-np.exp(-A**2*x_1**2)
    
    plt.plot(x_1,pdf_rayleigh, label='Distribusi Rayleigh')
    plt.title('Histogram yang Dinormalisasi')
    # plt.grid(axis='y')
    plt.xlabel(r'$H/H_*$')
    plt.ylabel(r'$\frac{n}{N \cdot \Delta (H/H_*)}$')
    plt.legend(loc='upper right')

    # plt.figure(num=3)
    # plt.plot(x_1,pdf_rayleigh,label='PDF')
    # plt.plot(x_1,cdf_rayleigh,label='CDF')
    # plt.title('PDF dan CDF Rayleigh')
    # plt.grid(axis='y')
    # plt.xlabel(r'$H/H_*$')
    # plt.ylabel(r'$f(H/H_*)$')
    # plt.legend(loc='upper left')
    
    return x, x_1, pdf_rayleigh, cdf_rayleigh, frek_H, kls_H, frek_x, kls_x

def psd(elev,tmak,delta_t=0.5):
    nj=len(elev)        # jumlah titik data ema
    f_nyq=1/(2*delta_t) # frekuensi maksimum
    df=1/tmak           # delta_f
    K=int(f_nyq/df)     # jumlah fungsi harmonik

    ak=np.zeros(K)
    bk=np.zeros(K)
    elev=np.asarray(elev)
    j=np.arange(1,nj+1)  # 1, 2, 3, ..., nj
    
    for k in range(1,K+1):
        ak[k-1]=2/nj*np.sum(elev*np.cos(k*2*np.pi/tmak*(j*delta_t)))
        bk[k-1]=2/nj*np.sum(elev*np.sin(k*2*np.pi/tmak*(j*delta_t)))
    ck=np.sqrt(ak**2+bk**2)

    f=np.linspace(df,f_nyq,ck.size)
    pow_spec_d=ck**2/2/df
    return f,pow_spec_d,ck