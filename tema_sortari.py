import time
import random
import copy


def ok_bubblesort(a):
    if len(a) <= 3000:
        return True
    else:
        return False


def bubblesort(a):
    n = len(a)
    ok = 1
    pas = 1             # la finalul pasului i, cele mai mari i numere vor fi pozitionate unde trebuie
    while ok == 1:
        ok = 0
        for i in range(n - pas):    # este suficient sa facem verificari doar pentru primele (n - pas) numere
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                ok = 1
        pas += 1        # pasul creste dupa fiecare set de verificari
    return a


def ok_countsort(a):
    if max(a) <= 10 ** 6:
        return True
    else:
        return False


def countsort(a):
    fr = [0 for i in range(10 ** 6 + 1)]
    minim = 10 ** 6 + 1
    maxim = -1
    for x in a:
        fr[x] += 1
        minim = min(minim, x)
        maxim = max(maxim, x)
    vect = []
    for i in range(minim, maxim + 1):
        while fr[i] > 0:
            vect.append(i)
            fr[i] -= 1
    return vect


def radixsort(vect, b):         # numerele vor fi transformate in baza 2^b, b = {1, 2, ..., 10}
    buck = [[] for i in range(2 ** b)]
    import math
    p = (2 ** b) ** math.floor(math.log(max(vect), 2 ** b))
    for x in vect:
        buck[x & (2 ** b - 1)].append(x)
    import copy
    q = 2 ** b
    while q <= p:
        newb = [[] for i in range(2 ** b)]
        for i in range(2 ** b):
            for x in buck[i]:
                newb[(x // q) & (2 ** b - 1)].append(x)
        buck = copy.deepcopy(newb)
        q *= (2 ** b)
    vect = []
    for i in range(2 ** b):
        for x in buck[i]:
            vect.append(x)
    return vect


def interclasare(a, b):
    i = 0
    j = 0
    n = len(a)
    m = len(b)
    c = []
    while i < n and j < m:
        if a[i] <= b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    c.extend(a[i:])
    c.extend(b[j:])
    return c


def mergesort(vect):
    n = len(vect)
    if n == 1:
        return vect
    else:
        m = n // 2
        v1 = mergesort(vect[: m])
        v2 = mergesort(vect[m:])
        return interclasare(v1, v2)


def quicksort(vect, st, dr, tip_pivot):
    if st <= dr:
        if st == dr:
            return vect
        elif dr == st + 1:
            if vect[st] > vect[dr]:
                vect[st], vect[dr] = vect[dr], vect[st]
            return vect
        else:
            if tip_pivot == 1:      # alegem pivot random
                k = random.randint(st, dr)
                piv = vect[k]
            else:                   # alegem pivot cu mediana din 3
                k = (st + dr) // 2
                if vect[st] <= vect[k] <= vect[dr] or vect[dr] <= vect[k] <= vect[st]:
                    piv = vect[k]
                elif vect[k] <= vect[st] <= vect[dr] or vect[dr] <= vect[st] <= vect[k]:
                    piv = vect[st]
                    k = st
                else:
                    piv = vect[dr]
                    k = dr
            i = st - 1
            j = dr
            vect[k], vect[dr] = vect[dr], vect[k]       # pivotul este mutat pe ultima pozitie
            while i < j:
                i += 1
                while i <= dr and vect[i] < piv:
                    i += 1      # elementele mai mici decat pivotul, care se afla deja in stanga, sunt bine pozitionate
                j -= 1
                while j >= st and vect[j] > piv:
                    j -= 1      # elementele mai mari decat pivotul, care se afla in dreapta, sunt bine pozitionate
                if i < j:
                    vect[i], vect[j] = vect[j], vect[i]     # interschimbam elementele care nu sunt bine pozitionate
            vect[i], vect[dr] = vect[dr], vect[i]           # aducem pivotul pe pozitia buna
            quicksort(vect, st, i - 1, tip_pivot)
            quicksort(vect, i + 1, dr, tip_pivot)
            return vect


def testare(a):
    n = len(a)
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            return False
    else:
        return True


f = open("sortari.in")
g = open("sortari.out", "w")


teste = int(f.readline())
for t in range(teste):
    s = f.readline()
    n, maxim = [int(x) for x in s.split()]
    g.write("n = " + str(n) + ", max = " + str(maxim) + "\n\n")
    v = []
    for i in range(n):
        v.append(random.randint(0, maxim))

    # bubblesort
    w = copy.deepcopy(v)
    if ok_bubblesort(w):
        start = time.time()
        bubblesort(w)
        stop = time.time()
        if testare(w):
            g.write("BUBBLESORT: numerele au fost sortate\n")
        else:
            g.write("BUBBLESORT: numerele nu au fost sortate\n")
    else:
        start = stop = 0
        g.write("BUBBLESORT: numerele nu pot fi sortate\n")
    g.write("\t" + str(stop - start) + " secunde\n\n")

    # countsort
    w = copy.deepcopy(v)
    if ok_countsort(w):
        start = time.time()
        w = countsort(w)
        stop = time.time()
        if testare(w):
            g.write("COUNTSORT: numerele au fost sortate\n")
        else:
            g.write("COUNTSORT: numerele nu au fost sortate\n")
    else:
        start = stop = 0
        g.write("COUNTSORT: numerele nu pot fi sortate\n")
    g.write("\t" + str(stop - start) + " secunde\n\n")

    # radixsort baza 256
    w = copy.deepcopy(v)
    start = time.time()
    w = radixsort(w, 8)     # radixsort in baza 2^8 = 256
    stop = time.time()
    if testare(w):
        g.write("RADIXSORT baza 256: numerele au fost sortate\n")
    else:
        g.write("RADIXSORT baza 256: numerele nu au fost sortate\n")
    g.write("\t" + str(stop - start) + " secunde\n\n")

    # radixsort baza 16
    w = copy.deepcopy(v)
    start = time.time()
    w = radixsort(w, 4)     # radixsort in baza 2^4 = 16
    stop = time.time()
    if testare(w):
        g.write("RADIXSORT baza 16: numerele au fost sortate\n")
    else:
        g.write("RADIXSORT baza 16: numerele nu au fost sortate\n")
    g.write("\t" + str(stop - start) + " secunde\n\n")

    # mergesort
    w = copy.deepcopy(v)
    start = time.time()
    w = mergesort(w)
    stop = time.time()
    if testare(w):
        g.write("MERGESORT: numerele au fost sortate\n")
    else:
        g.write("MERGESORT: numerele nu au fost sortate\n")
    g.write("\t" + str(stop - start) + " secunde\n\n")

    # quicksort cu pivot random
    w = copy.deepcopy(v)
    start = time.time()
    w = quicksort(w, 0, n - 1, 1)     # quicksort cu pivot random
    stop = time.time()
    if testare(w):
        g.write("QUICKSORT pivot random: numerele au fost sortate\n")
    else:
        g.write("QUICKSORT pivot random: numerele nu au fost sortate\n")
    g.write("\t" + str(stop - start) + " secunde\n\n")

    # quicksort cu pivot mediana din 3
    w = copy.deepcopy(v)
    start = time.time()
    w = quicksort(w, 0, n - 1, 2)     # quicksort cu pivot mediana din 3
    stop = time.time()
    if testare(w):
        g.write("QUICKSORT pivot mediana din 3: numerele au fost sortate\n")
    else:
        g.write("QUICKSORT pivot mediana din 3: numerele nu au fost sortate\n")
    g.write("\t" + str(stop - start) + " secunde\n\n\n")


f.close()
g.close()
