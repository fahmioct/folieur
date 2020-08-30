# Program 2

Program 2 berisi fungsi:
*	Pembuatan 1 dari 10 pilihan spektrum,
*	Inverse Fourier Transform.

Input:
*	Spektrum Gelombang (.csv atau .xls). Baris pertama memiliki kolom `f` dengan satuan Hertz dan `S(f)` dengan satuan `m^2.s`. Contoh:

|f|S(f)|
|-|-|
|0.00027|0|
|0.00054|0|

*	Tinggi Gelombang Signifikan.
*	Perioda Gelombang Signifikan.
*	Durasi Data Elevasi Muka Air yang akan dibuat (default: 3600 detik).
*	Interval Data Elevasi Muka Air yang akan dibuat (default: 0,5 detik).
*	Pemilihan 1 dari 10 Spektrum.

Output:
*	Plot Spektrum (.png, .jpg,. svg, and any image file).
*	Data Spektrum (.csv atau .xls).
*	Plot Elevasi Muka Air Sintetis (.png, .jpg,. svg, and any image file).
*	Data Elevasi Muka Air Sintetis (.csv atau .xls).
*	Data Parameter Gelombang Domain Frekuensi (.csv atau .xls).
