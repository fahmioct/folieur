# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 17:15:23 2020

@author: Fahmi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.special import gamma

#definisi delta_f dan nilai f(dari 0.01 sampi 10)
#tidak bisa dari 0 karena ada nilai yang dibagi 0
#delta_f=0.001
#f=np.arange(delta_f,1,delta_f)

#definisi 10 fungsi spektrum dengan parameter nilai Hs dan Ts
#spektrum Bretschneider-Mitsuyasu
def BM(Hs,Ts,f):
    Sf=0.257*Hs**2*Ts**(-4)*f**(-5)*np.exp(-1.03*(Ts*f)**(-4))
    return Sf

#spektrum Modified Bretschneider-Mitsuyasu
def MBM(Hs,Ts,f):
    Sf=0.205*Hs**2*Ts**(-4)*f**(-5)*np.exp(-0.75*(Ts*f)**(-4))
    return Sf

#spektrum JONSWAP
def JONSWAP(Hs,Ts,f):
    gam=3.3
    Tp=Ts/(1-0.132*(gam+0.2)**(-0.559))
    Bj=0.0624/(0.230+0.0336*gam-0.185*(1.9+gam)**(-1))*(1.094-0.01915*np.log(gam))
    Sf=[]
    for i in f:
        if i>=(1/Tp):
            sigma=0.09
        else:
            sigma=0.07
        S=Bj*Hs**2*Tp**(-4)*i**(-5)*np.exp(-1.25*(Tp*i)**-4)*gam**np.exp(-(Tp*i-1)**2/(2*sigma**2))
        Sf.append(S)
    return Sf

#spektrum Wallops
def Wallops(Hs,Ts,f):
    m=7
    Bw=0.0624*m**((m-1)/4)/(4**((m-5)/4)*gamma((m-1)/4))*(1+0.7458*(m+2)**(-1.057))
    Tp=Ts/(1-0.283*(m-1.5)**(-0.684))
    Sf=Bw*Hs**2*(Tp**(1-m))*(f**(-m))*np.exp(-m/4*((Tp*f)**(-4)))
    return Sf

#Spektrum TMA
def TMA(Hs,Ts,f):
    gam=3.3 
    h=100
    Tp=Ts/(1-0.132*(gam+0.2)**(-0.559))
    L=1.56*Tp**2
    k=2*np.pi/L
    Bj=0.0624/(0.230+0.0336*gam-0.185*(1.9+gam)**(-1))*(1.094-0.01515*np.log(gam))
    phi=((np.tanh(k*h))**2)/(1+2*k*h/(np.sinh(2*k*h)))
    Sf=[]
    for i in f:
        if i>=(1/Tp):
            sigma=0.09
        else:
            sigma=0.07
        S=Bj*Hs**2*Tp**(-4)*i**(-5)*np.exp(-1.25*(Tp*i)**-4)*gam**np.exp(-(Tp*i-1)**2/(2*sigma**2))*phi
        Sf.append(S)
    return Sf

#spektrum Bretchneider
def Bretschneider(Hs,Ts,f):
    w=2*np.pi*f
    T0=Ts/0.95
    w0=2*np.pi/T0
    Sf=2*np.pi*1.25*(w0**4)*(Hs**2)/4*(w**(-5))*np.exp(-1.25*(w0/w)**4)
    return Sf

#spektrum Pierson-Moskowitz
def PM(Hs,Ts,f):
    fp=0.95/Ts
    A=5*Hs**2*fp**4/16
    B=5*fp**4/4
    Sf=A/(f**5)*np.exp(-B/f**4)
    return Sf

#spektrum Modified Pierson-Moskowitz
def MPM(Hs,Ts,f):
    w=2*np.pi*f
    Tp=Ts/0.95
    Tz=0.71*Tp
    A=4*np.pi**3*Hs**2/(Tz**4)
    B=16*np.pi**3/(Tz**4)
    Sf=2*np.pi*A*w**(-5)*np.exp(-B*w**(-4))
    return Sf

#spektrum Toba1
def T1(Hs,Ts,f):
    w=2*np.pi*f
    T01=Ts/0.95
    Sf=2*np.pi*12.675*Hs**2/(T01**3*w**4)*np.exp(-246.06/(T01**4*w**4))
    return Sf

#spektrum Toba2
def T2(Hs,Ts,f):
    w=2*np.pi*f
    T01=Ts/0.95
    Sf=2*np.pi*23.126*Hs**2/(T01**3*w**4)*np.exp(-548.61/(T01**4*w**4))
    return Sf

#definisi fungsi untuk menghitung momen spektrum gelombang
def momen(Spektrum,f,delta_f):
    mn=np.zeros(4)
    n=np.arange(-1,3)
    for j in range(4):
        mn[j]=np.sum(f**n[j]*Spektrum*delta_f)
    return mn


def pgdf(mn):
    mn_dict = {
        'm-1': mn[0],
        'm0' : mn[1],
        'm1' : mn[2],
        'm2' : mn[3]
    }
    HT_sp = {
        'Hm0' : 4.004*np.sqrt(mn[1]),
        'Te' : mn[0]/mn[1],
        'Tm' : mn[1]/mn[2],
        'Tz' : np.sqrt(mn[1]/mn[3])
    }
    return mn_dict, HT_sp

def ema_syn(Sf,f,t):
    nk = len(f)
    delta_f = f[1] - f[0]
    delta_t = t[1] - t[0]
    nj = len(t)

    fasa=np.random.rand(int(nk))*2*np.pi
    eta_=np.zeros(nj)
    c=np.sqrt(Sf*2*delta_f)
    for j in range(nj):
        eta_[j]=np.sum(c*np.cos(2*np.pi*f*t[j]+fasa))
    return eta_
