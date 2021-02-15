import random
import math
import time
from itertools import combinations
import copy

def gnp(n, p):
    a = [[0 for j in range(n)] for i in range(n)]
    for i in range(1, n):
        for j in range(i):
            if random.random() <= p:
                a[i][j] = a[j][i] = random.randint(1, 10)
    return a

def printsvg(n, a, wynik):
    X = [0.0 for _ in range(n)]
    Y = [0.0 for _ in range(n)]
    for i in range(n):
        X[i] = 500 + math.floor(300 * math.sin((2 * math.pi / n) * (i + 1)))
        Y[i] = 500 + math.floor(300 * math.cos((2 * math.pi / n) * (i + 1)))

    svg = '<?xml version="1.0" standalone="no"?>\n'
    svg += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    svg += '<svg width="15cm" height="15cm" viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
    for i in range(n):
        for j in range(i):
            if a[i][j] > 0:
                svg += '<path stroke="black" stroke-width="5" d="M ' + str(X[i]) + ' ' + str(Y[i]) + ' L ' + str(
                    X[j]) + ' ' + str(Y[j]) + '"/>\n'
    for i in range(n):
        svg += '<path stroke="red" stroke-width="10" d="M ' + str(X[wynik[i]]) + ' ' + str(Y[wynik[i]]) + ' L ' + str(
            X[wynik[(i + 1) % n]]) + ' ' + str(Y[wynik[(i + 1) % n]]) + '"/>\n'
    for i in range(n):
        for j in range(i):
            if a[i][j] > 0:
                svg += '<text x="' + str((X[i] + X[j]) / 2) + '" y="' + str(
                    (Y[i] + Y[
                        j]) / 2) + '" text-anchor="south" fill="white" stroke="blue" font-weight="bold" stroke-width="2" font-size="50" >' + str(
                    a[i][j]) + '</text>\n'
    for i in range(n):
        svg += '<circle cx="' + str(X[i]) + '" cy="' + str(Y[i]) + '" r="20" fill="black"/>\n'
        svg += '<text x="' + str(X[i]) + '" y="' + str(
            Y[i] + 7) + '" text-anchor="middle" fill="white" stroke="white" font-size="25" >' + str(i) + '</text>\n'
    svg += '</svg>\n'
    return svg


def TSP(n, graf, v, v0, d, dh, s, sh, odwiedzone):
    sh.append(v)
    if len(sh) == n:
        if graf[v][v0] > 0:
            dh += graf[v][v0]
            if dh < d:
                d = dh
                s = copy.deepcopy(sh)
                wynik.append([d, s])
            dh -= graf[v][v0]
    else:
        odwiedzone[v] = True
        for u in range(n):
            if graf[v][u] > 0:
                if odwiedzone[u] is True:
                    continue
                dh += graf[v][u]
                TSP(n, graf, u, v0, d, dh, s, sh, odwiedzone)
                dh -= graf[v][u]
        odwiedzone[v] = False
    sh.pop()


def dynamicTSP(graf, n,tab):
    lista = []
    sciezka = []
    for i in range(1,n):
        tab[((i,),i)] = graf[0][i]
        lista.append(i)

    for s in range(2,n):
        for S in combinations(lista,s):
            for k in S:
                pom = list(S)
                pom.pop(pom.index(k))
                pom2 =[]
                for m in pom:
                    pom2.append(tab[(tuple(pom),m)] + graf[m][k])
                tab[((S), k)] = min(pom2)

    pom = []
    najm = tab[(tuple(lista),1)]+graf[1][0]
    najm_k = 1
    for k in range(2,n):
        pom.append(tab[(tuple(lista),k)]+graf[k][0])
        if tab[(tuple(lista),k)]+graf[k][0] < najm:
            najm = tab[(tuple(lista),k)]+graf[k][0]
            najm_k = k

    sciezka = [0,najm_k]
    pom = []
    for i in range (1,n):
        pom.append(i)
    pom.pop(pom.index(najm_k))
    while(pom):
        najm = tab[(tuple(pom),pom[0])]+graf[pom[0]][najm_k]
        najm_k1 = pom[0]
        for k in range(1, len(pom)):
            if tab[(tuple(pom), pom[k])] + graf[pom[k]][najm_k] < najm:
                najm = tab[(tuple(pom), pom[k])] + graf[pom[k]][najm_k]
                najm_k1 = pom[k]
        sciezka.append(pom.pop(pom.index(najm_k1)))
        najm_k = najm_k1

    sciezka.append(0)
    suma = 0
    for i in range(1,len(sciezka)):
        suma += graf[sciezka[i-1]][sciezka[i]]

    return sciezka, suma

wybor = 1

graf = []
sciezka1 =[]

while wybor != 0:
    p = 1
    print("Co robic?")
    print("1.Wygenerowanie grafu")
    print("2.Algorytm wyczerpujacy")
    print("3.Algorytm Helda-Karpa")
    print("4.Wygenerowanie pliku html z grafem")
    print("0.Wyjscie")
    wybor = int(input())

    if wybor == 1:
        print("Ile wierzcholkow?")
        n = int(input())
        graf = gnp(n, p)
        print("Macierz sasiedztwa z wagami krawedzi:")
        for i in graf:
            print(i)

    if wybor == 2:
        if not graf:
            print("Graf nie zostal wygenerowany")
        else:
            start = time.time()
            wynik = []
            s = []
            sh = []
            odwiedzone = [0 for i in range(n)]
            d = n * 10
            dh = 0
            TSP(n, graf, 0, 0, d, dh, s, sh, odwiedzone)
            wynik.sort()
            stop = time.time()
            print("Czas:", (stop-start), "s")
            if len(wynik) > 0:
                sciezka1 = wynik[0][1]
                suma1 = wynik[0][0]
                print("Sciezka:")
                for i in sciezka1:
                    print(i, "->", end= " ")
                print(0)
                print("Cena przejscia:")
                print(suma1)

            else:
                print("Brak cyklu Hamiltona, wiec nie da sie rozwiazac dla tego grafu!")

    if wybor == 3:
        if not graf:
            print("Graf nie zostal wygenerowany")
        else:
            start = time.time()
            tab_kosz = {}
            sciezka1, suma1 = dynamicTSP(graf, n, tab_kosz)
            stop = time.time()
            print("Czas:", (stop - start), "s")
            print("Sciezka:")
            for i in range(len(sciezka1)-1):
                print(sciezka1[i], "->", end=" ")
            print(0)
            print("Cena przejscia:")
            print(suma1)


    if wybor == 4:
        if not graf or not sciezka1:
            print("Graf lub najtansza sciezka nie zostaly jeszcze wygenerowane")
        else:
            f = open("projekt.html", 'w')
            text = printsvg(n, graf, sciezka1)
            f.write(text)
            f.close()
            print("Plik wygenerowano w folderze projektu")
