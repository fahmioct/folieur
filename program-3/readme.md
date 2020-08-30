# Program 3

Program 3 berfungsi untuk hindcasting gelombang dengan persamaan yang ada pada buku Goda "Random Seas and Design for Maritime Structures 3rd Edition"

Input:
*	Data Kecepatan Angin dan Arah Angin (.csv atau .xls) dengan judul kolom `WindDir` dalam satuan True North dan `WindSpd` dalam knot. Contoh:

|WindDir|WindSpd|
|-|-|
|131.4|15.7|
!130.5|13.5|

*	Data Fetch Efektif dari Arah Angin (.csv atau .xls). `Dir8` merupakan 8 arah mata angin (urutan baris dapat diganti), dan `Feff` dalam `km` Contoh:

|Dir8|Feff|
|-|-|
|N|100|
|S|150|
|NW|169|
|W|157|
|SE|123|
|SW|178|
|E|147|
|NE|249|

*	Interval Data Angin (default: 1 jam)

Output:
*	Data Angin dengan hasil hindcasting gelombang (.csv atau .xls).
