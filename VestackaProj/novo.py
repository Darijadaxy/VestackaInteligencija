import copy

trenutni_igrac = None  #'X' ili 'O'
trouglovi_X = set()
trouglovi_O = set()
n= None
graf = {}
mat =  None
kolona =  None
vrsta =  None
krajj = False
svi_moguci_potezi= set()
racunar = None
covek= None

def slovo_u_broj(slovo):
    return ord(slovo.upper()) - ord('A')

def inicijalizuj_matricu():
    global mat
    global kolona, vrsta
    kolona = 2 * n - 1 + 5 * (2 * n - 2)
    vrsta = (2 * n - 1) + (2 * n - 2) * 2
    mat = [[' ' for _ in range(kolona)] for _ in range(vrsta)]

def inicijalizuj_moguce_poteze():
    global svi_moguci_potezi, graf

    t= n
    for i in range(0, n):
        j=1
        j_end = t - 3 
        for j in range (1, j_end+1):
            svi_moguci_potezi.add(((i,j), 'D'))
        t+=1
    t= t-2
    for i in range(n, 2*n-1): 
        j = 1
        j_end = t - 3  
        for j in range(1, j_end + 1):
            svi_moguci_potezi.add(((i, j), "D"))
        t -= 1
    
    pocetni_broj =0 
    if n==8:
        pocetni_broj= 12
    else:
        pocetni_broj= n+ n%4
    pom= pocetni_broj
    for j_start in range (1, n+1):
        i=0
        j= j_start
        for _ in range (0, pom):
            svi_moguci_potezi.add(((i, j), "DD"))
            i+=1
            if i< n:
                j+=1
        pom-=1
    pom= pocetni_broj-1
    for i_start in range (1, n):
        i=i_start
        j= 1
        for _ in range (0, pom):
            svi_moguci_potezi.add(((i, j), "DD"))
            i+=1
            if i< n:
                j+=1
        pom-=1
    #dole levo
    pom= pocetni_broj #ulevo od dijagonale
    for j_start in range (n, 0, -1):
        i=0
        j= j_start
        for _ in range (0, pom):
            svi_moguci_potezi.add(((i, j), "DL"))
            i+=1
            if i >= n:
                j-=1
        pom-=1
    #udesno
    pom= pocetni_broj-1
    j_start= n+1
    for i_start in range (1, n):
        i=i_start
        j= j_start
        for _ in range (0, pom):
            svi_moguci_potezi.add(((i, j), "DL"))
            i+=1
            if i>= n:
                j-=1
        pom-=1
        j_start+=1

    print("Svi mogući potezi: ", svi_moguci_potezi)


def covek_igra_prvi():
    unos = ""
    while unos != "Y" and unos != "N" and unos != "y" and unos != "n":
        unos = input("Covek igra prvi? [Y/N]")
    return unos.upper() == "Y"

def protivnik():
    unos=""
    while unos != "Y" and unos != "N" and unos != "y" and unos != "n":
        unos = input("Da li zelite da igrate protiv racunara? [Y/N]")
    return unos.upper() == "Y"


def get_prvi_igrac():
    global trenutni_igrac
    unos = ""
    while unos != "X" and unos != "O" and unos != "x" and unos != "o":
        unos = input("Da li igra prvo X ili O? [X/O]")
        trenutni_igrac = unos.upper()
        print(f"Prvi igrač postavljen na: {trenutni_igrac}")

def kraj():
    rezultat= 0
    poc= 0
    for _ in range(0, n-1):
        rezultat += 2*n-1+poc
        poc+=2
    return rezultat


def get_velicina_table():
    global n
    while n not in range(4,9):
        unos = input("Unesite dimenziju table (4-8): ")
        try:
            n = int(unos)
        except ValueError:
            continue
    inicijalizuj_matricu()

def konvertuj_u_tuple(input_string):
    try:
        delovi = input_string.strip().split(',')
        if len(delovi) != 2:
            return None
        x = slovo_u_broj(delovi[0].strip())
        y = int(delovi[1].strip())
        return (x, y)
    except ValueError:
        return None

def odigraj_potez(dubina, potez):
    global trenutni_igrac, krajj, svi_moguci_potezi, covek, racunar, graf
    ispravno = -1
    pocetna_pozicija = None
    smer = None
    pot= None
    if covek or not racunar:
        while ispravno == -1:
            pocetna_pozicija_str = input("Unesite poziciju od koje pocinje potez (npr. A, 2): ")
            pocetna_pozicija = konvertuj_u_tuple(pocetna_pozicija_str)
            if pocetna_pozicija is None:
                print("Neispravan format pozicije! Pokušajte ponovo.")
                continue
            smer = input("Unesite smer(D, DD, DL): ")
            ispravno = proveri_unos_poteza(smer, pocetna_pozicija)
            pot = (pocetna_pozicija, smer)
            if pot not in svi_moguci_potezi:
                ispravno= -1
                print("Potez nije validan!")
        svi_moguci_potezi.remove(pot)
        dodaj_vezu(graf, pocetna_pozicija, smer)
    else:
        #racunar
        stanje = (svi_moguci_potezi.copy(), copy.deepcopy(graf),trouglovi_X.copy(),trouglovi_O.copy())
        min_max_alpha_beta_result = min_max_alfa_beta(stanje, dubina, potez)
        pot = min_max_alpha_beta_result[0]
        print("ovaj pot je najbolji")
        print(pot)
        svi_moguci_potezi.remove(pot)
        dodaj_vezu(graf, pot[0], pot[1])

    pronadji_cikluse_duzine_tri(graf,trenutni_igrac, trouglovi_X, trouglovi_O)
    crtaj_oblik(n)
    rez = kraj()
    if len(trouglovi_X) == rez and len(trouglovi_O) == rez:
        print("Nereseno")
        krajj = True
        return
    if trenutni_igrac == 'X':
        if len(trouglovi_X) > rez:
            print("Pobednik je igrac X")
            krajj = True
            return
        trenutni_igrac = 'O'
    elif trenutni_igrac == 'O':
        if len(trouglovi_O) > rez:
            print("Pobednik je igrac O")
            krajj = True
            return
        trenutni_igrac = 'X'
    covek= not covek

def proveri_unos_poteza(smer, pocetna_pozicija):
    validni_smerovi = {"D", "DD", "DL"}
    if smer not in validni_smerovi:
        print(f"Netačna vrednost za smer: '{smer}'. Smer mora biti jedna od sledećih opcija: D, DD, DL.")
        return -1

    if pocetna_pozicija not in graf:
        print(f"Početna pozicija {pocetna_pozicija} nije u grafu.")
        return -1
    return 1

def generisi_graf(n):#svi moguci stubici su nam cvorovi grafa
    global graf
    pom = 0
    for i in range(2 * n - 1):
        if i < n:
            for j in range(1, n + i + 1):
                graf[(i, j)] = []
            pom = j
        else:
            for t in range(1, pom):
                graf[(i, t)] = []
            pom -= 1
    print(graf)


def dodaj_vezu(graf, pocetna_pozicija, smer):
    
    i, j = pocetna_pozicija
    if smer == "D":
        for offset in range(1, 4):
            nova_pozicija = (i, j + offset)
            graf[pocetna_pozicija].append(nova_pozicija)
            graf[nova_pozicija].append(pocetna_pozicija)
            pocetna_pozicija = nova_pozicija
    elif smer== "DD":
        for _ in range(1, 4):
            if(i < n - 1):
                i+=1
                j+=1
                nova_pozicija = (i, j)
            else:
                i += 1
                nova_pozicija = (i, j)
            graf[pocetna_pozicija].append(nova_pozicija)
            graf[nova_pozicija].append(pocetna_pozicija)
            pocetna_pozicija = nova_pozicija
    else :
        for _ in range(1, 4):
            if(i< n-1):
                i += 1
                nova_pozicija = (i, j)
            else:
                i+=1
                j-=1
                nova_pozicija = (i, j)
            graf[pocetna_pozicija].append(nova_pozicija)
            graf[nova_pozicija].append(pocetna_pozicija)
            pocetna_pozicija = nova_pozicija

    return graf

def pronadji_cikluse_duzine_tri(graf,igrac, trougloviX, trougloviO):
    
    for cvor in graf:
        susedi = graf[cvor]
        for i in range(len(susedi)):
            for j in range(i + 1, len(susedi)):
                prvi_sused = susedi[i]
                drugi_sused = susedi[j]
                if prvi_sused in graf[drugi_sused]:
                    ciklus = tuple(sorted([cvor, prvi_sused, drugi_sused]))
                    if ciklus not in trougloviX and ciklus not in trougloviO:
                        if igrac == 'X':
                            trougloviX.add(ciklus)
                        else:
                            trougloviO.add(ciklus)

    return trougloviX, trougloviO

def iscrtavanje_gumica():
    global mat
    mat_i = 0
    mat_j = n + (n - 1) * 2 - 1
    brojac = 0
    for key in graf.keys():
        value = graf[key]
        i, j = key
        if i == n - 1:
            break

        if j == 1 and i != 0:
            mat_i += 3
            mat_j = mat_j - 3 - brojac * 6
            brojac = 0

        for vrednost in value:
            pomocna_i = mat_i
            pomocna_j = mat_j
            i1, j1 = vrednost

            if i == i1 and j1>j:
                for _ in range(0, 5):
                    mat[pomocna_i][pomocna_j + 1] = "-"
                    pomocna_j += 1
            elif j == j1 and i1>i:
                mat[pomocna_i + 1][pomocna_j - 1] = "/"
                mat[pomocna_i + 2][pomocna_j - 2] = "/"
            elif j + 1 == j1 and i1>i:
                mat[pomocna_i + 1][pomocna_j + 1] = "\\"
                mat[pomocna_i + 2][pomocna_j + 2] = "\\"

        mat_j += 6
        brojac += 1

    #druga polovina
    mat_i = n+ (n-1)*2 -1
    mat_j =0

    brojac = 0
    filtered_keys = [key for key in graf.keys() if key[0] >= n - 1]
    for key in filtered_keys:
        value = graf[key]
        i, j = key

        if j == 1 and i != n-1:
            mat_i += 3
            mat_j = mat_j + 3 - brojac * 6
            brojac = 0

        for vrednost in value:
            pomocna_i = mat_i
            pomocna_j = mat_j
            i1, j1 = vrednost

            if i == i1 and j1 > j:
                for _ in range(0, 5):
                    mat[pomocna_i][pomocna_j + 1] = "-"
                    pomocna_j += 1
            elif j-1 == j1 and i1 > i:
                mat[pomocna_i + 1][pomocna_j - 1] = "/"
                mat[pomocna_i + 2][pomocna_j - 2] = "/"
            elif j == j1 and i1 > i:
                mat[pomocna_i + 1][pomocna_j + 1] = "\\"
                mat[pomocna_i + 2][pomocna_j + 2] = "\\"

        mat_j += 6
        brojac += 1

def popunjavanje_trouglova():
    global mat
    i = 1
    j = n + (n - 1) * 2 - 1 + 3
    br_trouglova = n-1
    for _ in range(0, n):
        for _ in range(0, br_trouglova): 
            if mat[i][j] != 'X' and mat[i][j] != 'O' and mat[i-1][j] == '-' and mat[i][j-2] == '\\' and mat[i][j+2] == '/':
                mat[i][j] = trenutni_igrac
            j += 6
        j = j - 6 - (br_trouglova- 1)*6 - 3
        i += 3
        br_trouglova += 1

    i = n+ (n-1) * 2 - 1 + 4
    j = 6
    br_trouglova -= 2

    for _ in range(0, n-2):
        for _ in range(0, br_trouglova):
            if mat[i][j] != 'X' and mat[i][j] != 'O' and mat[i-1][j] == '-' and mat[i][j-2] == '\\' and mat[i][j+2] == '/':
                mat[i][j] = trenutni_igrac
            j += 6
        j = j - 6 - (br_trouglova- 1)*6 + 3
        i += 3
        br_trouglova -= 1
 
    i = 2
    j = n + (n - 1) * 2 - 1
    br_trouglova = n
    for _ in range(0, n-1):
        for _ in range(0, br_trouglova):
            if mat[i][j] != 'X' and mat[i][j] != 'O' and mat[i + 1][j] == '-' and mat[i][j - 2] == '/' and mat[i][j + 2] == '\\':
                mat[i][j] = trenutni_igrac
            j += 6
        j = j - 6 - (br_trouglova - 1) * 6 - 3
        i += 3
        br_trouglova += 1

    i = n + (n - 1) * 2 - 1 + 2
    j = 6
    br_trouglova -= 2

    for _ in range(0, n - 1):
        for _ in range(0, br_trouglova): 
            if mat[i][j] != 'X' and mat[i][j] != 'O' and mat[i + 1][j] == '-' and mat[i][j - 2] == '/' and mat[i][j + 2] == '\\':
                mat[i][j] = trenutni_igrac
            j += 6
        j = j - 6 - (br_trouglova - 1) * 6 + 3
        i += 3
        br_trouglova -= 1

def crtaj_oblik(n):
    global mat, kolona, vrsta
    i = n + (n - 1) * 2 - 1
    naPocetkuReda = 0
    brojTacaka = 2 * n - 1

    while i >= 0:
        j1 = naPocetkuReda
        for k in range(brojTacaka):
            mat[i][j1] = "."
            j1 += 6
        brojTacaka -= 1
        naPocetkuReda += 3
        i -= 3

    i = n + (n - 1) * 2 - 1 + 3
    naPocetkuReda = 3
    brojTacaka = 2 * n - 2

    while i < vrsta:
        j1 = naPocetkuReda
        for k in range(brojTacaka):
            mat[i][j1] = "."
            j1 += 6
        brojTacaka -= 1
        naPocetkuReda += 3
        i += 3

    iscrtavanje_gumica()
    popunjavanje_trouglova()

    poc = n+(n-1)*2-1+7
    spaces = " " * (poc-1)
    print(spaces, end="")
    for i in range(1, 2*n):
        print(f"{i}", end="")
        spaces=" " * 5
        print(spaces, end="")
    print()
    #
    i=0
    for row in mat:
        if mat.index(row)%3 == 0 :
            print(chr(ord('A')+i), end="  ")
            i+=1
        else:
            print(" ", end="  ")
        print("".join(row))
    #
    spaces = " " * (poc-1)
    print(spaces, end="")
    for i in range(1, 2*n):
        print(f"{i}", end="")
        spaces=" " * 5
        print(spaces, end="")
    print()

def igraj(pot,igrac, stanje):

    stanje0 = stanje[0].copy()
    stanje1 = copy.deepcopy(stanje[1])
    trougloviX=stanje[2].copy()
    trougloviO=stanje[3].copy()
    stanje0.remove(pot)
    stanje1 = dodaj_vezu(stanje1, pot[0], pot[1])
    trougloviX,trougloviO=pronadji_cikluse_duzine_tri(stanje1,igrac, trougloviX, trougloviO) 
    print("igra, tj menja stanje:")
    print(len(stanje0))
    return stanje0, stanje1, trougloviX, trougloviO

def proceni_stanje(stanje, igrac):

    if igrac== "X":

        return (len(stanje[2])-len(trouglovi_X)) - (len(stanje[3])-len(trouglovi_O))
    else:

        return -(len(stanje[3]) - len(trouglovi_O)) + (len(stanje[2]) - len(trouglovi_X))

def min_max_alfa_beta (stanje, dubina, moj_potez, alpha=(None, -100), beta= (None, 100)):
    if moj_potez:
        print("pozivam max igraca")
        return max_value(stanje, dubina, alpha, beta)
    else:
        print("pozivam min igraca")
        return min_value(stanje, dubina, alpha, beta)

def max_value(stanje, dubina, alpha, beta, potez=None):

    stanje1 = stanje[0].copy()
    if dubina == 0  or len(stanje[0]) == 0 :
        print("dubina 0 ili kraj unutar max_value, vraca: ", potez, proceni_stanje(stanje, "X"))
        return (potez, proceni_stanje(stanje, "X"))
    else:
        for pot in stanje1:
            print(f"max_value unutar for i trenutni potez na dubini {dubina}: {pot}")
            alpha = max(alpha, min_value(igraj(pot,"X", stanje), dubina - 1,
                alpha, beta, pot if potez is None else potez), key=lambda x: x[1])
            if alpha[1] >= beta[1]:
                print("alpha[1]Max",alpha[1])
                print("beta[1]Max",beta[1])
                print("max_value vraca beta: ", beta)
                return beta
    print("max_value vraca alpha: ", alpha)
    return alpha

def min_value(stanje, dubina, alpha, beta, potez=None):

    stanje1 = stanje[0].copy()
    if dubina == 0 or len(stanje[0]) == 0 :
        print("dubina 0 ili kraj unutar min_value, vraca: ", potez, proceni_stanje(stanje, "O"))
        return (potez, proceni_stanje(stanje, "O"))
    else:
        for pot in stanje1:
            print(f"min_value unutar for i trenutni potez na dubini {dubina}: {pot}")
            beta = min(beta, max_value(igraj(pot,"O",stanje), dubina - 1,
                alpha, beta,pot if potez is None else potez), key=lambda x: x[1])
            if beta[1] <= alpha[1]:
                print("alpha[1]Min",alpha[1])
                print("beta[1]Min",beta[1])
                print("min_value vraca alpha: ", alpha)
                return alpha
    print("min_value vraca beta: ", beta)
    return beta

print("novii")
get_prvi_igrac()
racunar= protivnik()
if racunar:
    covek= covek_igra_prvi()

get_velicina_table()
generisi_graf(n)
inicijalizuj_moguce_poteze()
crtaj_oblik(n)

potez = True if trenutni_igrac == "X" else False

while not krajj:
    odigraj_potez(2, potez)
    potez = not potez