import sys
import random
import numpy as np
import json


# Bestandsnamen voor de huidige telling, doorgegeven voorkeuren, nieuwe telling & selectie output
tellingIn, voorkeurIn, tellingOut, selectieOut = sys.argv[1:]

# test telling vanuit csv
# tellingData = np.genfromtxt("telling.csv", names=True, dtype=None, delimiter=',', encoding=None).T
# telling = {}
# for row in tellingData:
#     telling[row[0]] = {"HR": bool(row[1]), "n": int(row[2])}

# Import telling vanuit json naar dictionary
f = open(tellingIn, 'r')
telling = json.loads(f.read())
f.close()

# Import hardrijders en pas aan waar nodig in de dictionary
f = open("hardrijders.txt")
hardrijders = f.read().split('\n')
for hr in hardrijders:
    if hr in telling:
        telling[hr]["HR"] = True
    else:
        telling[hr] = {"HR": True, "n": 0}

# Import aanmeldingen
# kolommen: Voornaam, Achternaam, email, maandag?, donderdag?, zondag?
TjassersData = np.genfromtxt(voorkeurIn, names=True, dtype=None, delimiter=',', encoding=None)

# recreanten en hardrijders splitsen, zodat die uniform verdeeld kunnen worden over de dagen
# waar nodig voeg toe aan telling dictionary
recreantenData = []
hardrijdersData = []
for Tjasser in TjassersData:
    Tjasser = list(Tjasser)
    email = Tjasser[2]
    if email in telling:
        if telling[email]["HR"]:
            hardrijdersData.append(Tjasser)
        else:
            recreantenData.append(Tjasser)
    else:
        telling[email] = {"HR": False, 'n': 0}
        recreantenData.append(Tjasser)

# sorteer op volgorde van aantal keren geschaatst, zodat het zo uniform mogelijk verdeeld wordt over de dagen
def sorteer(Data):
    Data = np.array(Data)
    emails = Data.T[2]
    nschaatsen = np.array([telling[email]['n'] for email in emails])
    inds = nschaatsen.argsort()
    return Data[inds]

recreantenData = sorteer(recreantenData)
hardrijdersData = sorteer(hardrijdersData)



TjassersMaandag = []
TjassersDonderdag = []
TjassersZondag = []

zf = 22.0/26.0  # compensatiefactor omdat er meer plek is op zondag

# verdeel Tjassers zo gelijk mogelijk over de dagen
for data in (list(recreantenData), list(hardrijdersData)):
    for Tjasser in data:

        m, d, z = Tjasser[3:]

        # Als de Tjasser maar op een dag kan, deel hem daar in
        if m+d+z == 1:
            if m:
                TjassersMaandag.append(Tjasser)
            elif d:
                TjassersDonderdag.append(Tjasser)
            elif z:
                TjassersZondag.append(Tjasser)

        else:
            mN, dN, zN = len(TjassersMaandag), len(TjassersDonderdag), len(TjassersZondag)*zf

            # Als de Tjasser op de dag met de minste mensen kan, deel hem daar in
            if min(mN, dN, zN) == mN and m:
                TjassersMaandag.append(Tjasser)
            elif min(mN, dN, zN) == dN and d:
                TjassersDonderdag.append(Tjasser)
            elif min(mN, dN, zN) == zN and z:
                TjassersZondag.append(Tjasser)
            # Probeer het anders op de dag waar niet de meeste mensen komen
            elif max(mN, dN, zN) != mN and m:
                TjassersMaandag.append(Tjasser)
            elif max(mN, dN, zN) != dN and d:
                TjassersDonderdag.append(Tjasser)
            elif z:
                TjassersZondag.append(Tjasser)
            # Opvanger voor het geval twee dagen even vol zitten
            else:
                TjassersDonderdag.append(Tjasser) # wat als mensen 0 voorkeursdagen hebben ingevuld? dan komen ze ook hier terecht

print("Totaal aantal Tjassers:", len(TjassersData))
print("Pool maandag:", len(TjassersMaandag))
print("Pool donderdag:", len(TjassersDonderdag))
print("Pool zondag:", len(TjassersZondag), "Gecorrigeerd:", len(TjassersZondag)*zf)

geselecteerdenMaandag = []
geselecteerdenDonderdag = []
geselecteerdenZondag = []
gesnDagen = (geselecteerdenMaandag, geselecteerdenDonderdag, geselecteerdenZondag)
TjassersDagen = (TjassersMaandag, TjassersDonderdag, TjassersZondag)
plekkenDagen = (22, 22, 26)
hf = 2/3  #compensatiefactor voor hardrijders

for geselecteerden, Tjassers, plekken in zip(gesnDagen, TjassersDagen, plekkenDagen):
    while len(geselecteerden) < plekken or len(Tjassers) == 1:
        # Zet de Tjassers elke ronde op willekeurige volgorde, dit is eigenlijk de enige loting
        random.shuffle(Tjassers)
        tried = []
        while len(Tjassers) > 1:
            # pak de eerstvolgende Tjasser om te vergelijken met de rest
            Tjasser = Tjassers.pop()
            # vind wat het minst aantal keren geschaatst is van de rest
            emails = [T[2] for T in Tjassers]
            nschaatsen = [telling[e]['n'] for e in emails]
            minN = min(nschaatsen)

            # Compenseer minst aantal keren geschaatst voor hardrijders
            email = Tjasser[2]
            if telling[email]["HR"]:
                minN *= hf
            # Vergelijk het aantal keren geschaatst van de Tjasser met het minste aantal van de rest
            if telling[email]['n'] <= minN:
                geselecteerden.append(Tjasser)
                telling[email]['n'] += 1
            else:
                tried.append(Tjasser)
        # begin opnieuw als de hele groep geprobeerd is maar er nog plekken zijn
        Tjassers += tried
    # opvanger voor als de dag niet vol zit
    if len(Tjassers) == 1 and len(geselecteerden) < plekken:
        geselecteerden.append(Tjassers[0])
        telling[Tjassers[0][2]]['n'] += 1

# Output de selectie
f = open(selectieOut, 'w')
for geselecteerden, pechvogels, dag in zip(gesnDagen, TjassersDagen, ("maandag", "donderdag", "zondag")):
    f.write("Geselecteerden " + dag + ":\n")
    for geselecteerde in geselecteerden:
        f.write(", ".join(geselecteerde[0:3]) + '\n')
    f.write("\nNiet geselecteerd " + dag + ":\n")
    for pechvogel in pechvogels:
        f.write(", ".join(pechvogel[0:3]) + '\n')
    f.write("\n-------------------------------\n")
f.close()

# Export nieuwe telling
s = json.dumps(telling)
f = open(tellingOut, 'w')
f.write(s)
f.close()
