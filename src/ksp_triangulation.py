import math
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-A", metavar='Astre', default="", type=str, help="nom de l'astre")
parser.add_argument("-nbs", metavar='Nb_sats', default=0, type=int, help="nombre de satellites")
parser.add_argument("-ap", metavar='Apoapsis', default=0, type=int, help="altitude de l'apoapsis")
parser.add_argument("-pe", metavar='Periapsis', default=0, type=int, help="altitude du periapsis, si 0 alors égal à l'apoapsis")
args = parser.parse_args()

def format_secondes(nb_secondes):
    minutes = nb_secondes/60
    secondes = nb_secondes%60
    heures = minutes/60
    minutes = minutes%60
    return str(math.floor(heures)) + "h " + str(math.floor(minutes)) + "m " + str(math.floor(secondes)) + "s"

def format_altitude(altitude):
    return format(altitude, '0,.3f')

astres = [
    [ "kerbin", 1200000, 3531600000000, 70000 ],
    [ "mun", 400000, 65138398000, 0 ],
    [ "minmus", 120000, 1765800000, 0 ],
    [ "duna", 640000, 301363210000, 50000 ],
    [ "ike", 260000, 18568369000, 0 ],
    [ "eve", 1400000, 8171730200000, 90000 ],
    [ "gilly", 26000, 8289449.8, 0 ],
    [ "moho", 500000, 168609380000, 0 ],
    [ "dres", 276000, 21484489000, 0 ],
    [ "jool", 12000000, 282528000000000, 200000 ],
    [ "laythe", 1000000, 1962000000000, 50000 ],
    [ "vall", 600000, 207481500000, 0 ],
    [ "tylo", 1200000, 2825280000000, 0 ],
    [ "bop", 130000, 2486834900, 0 ],
    [ "pol", 88000, 721702080, 0 ],
    [ "eeloo", 420000, 74410815000, 0 ],
    [ "kerbol", 523200000, 1172332800000000000, 600000 ],
]

if args.A != "":
    astre = args.A
else:
    print("Astre:")
    astre = input()
astre_existe = False
for temp in astres:
    if astre.lower() == temp[0]:
        astre_existe = True
        d = temp[1]
        gm = temp[2]
        pemin = temp[3]
        break
if not astre_existe:
    print("!!! ERREUR !!! Configuration manuelle de l'astre")
    print("Diamètre:")
    d = int(input())
    print("Force G:")
    gm = int(input())
    print("Altitude de l'atmosphère (option):")
    pemin = input()
    if len(pemin) > 0:
        pemin = int(pemin)
    else:
        pemin = 0


if args.nbs > 0:
    nb_sats = args.nbs
else:
    print("Nombre de satellites:")
    nb_sats = int(input())

if args.ap > 0:
    ap = args.ap
else:    
    print("Apoapsis:")
    ap = int(input())

pe = 0
if args.pe > 0:
    pe = args.pe
if pe == 0:
    pe = ap

a = (ap+pe+d)/2
p = 2*math.pi*math.sqrt(a**3/gm)
te = p / nb_sats
tp = p - te
ta = ((tp**(2/3)) * (2*gm)**(1/3)) / ( 2 * math.pi**(2/3))
tpe = 2*ta - ap - d
    
print()
print("|-----------------------")
print("|[ ORBITE FINALE ]")
print("|  + Apoapsis      =", format_altitude(ap), "mètres")
print("|  + Periapsis     =", format_altitude(pe), "mètres")
print("|  + 1/2 grand axe =", format_altitude(a), "mètres")
print("|  + Période       =", format_secondes(p))
print("|  + Ecart / Sat   =", format_secondes(te), "(", nb_sats, "satellites )")
print("|-----------------------")
print("|[ ORBITE DE TRANSFERT ]")
print("|  + Apoapsis      =", format_altitude(ap), "mètres")
print("|  + Periapsis     =", format_altitude(tpe), "mètres")
print("|  + 1/2 grand axe =", format_altitude(ta), "mètres")
print("|  + Période       =", format_secondes(tp))
print("|-----------------------")
print()

if tpe <= 0:
    print("[KO] L'orbite de transfert provoque un impact avec l'astre")
    print("     Augmenter l'apoapsis ou le nombre de satellites")
elif pemin > 0 and tpe < pemin:
    print("[KO] L'orbite de transfert rentre dans l'atmosphère")
    print("     Augmenter l'apoapsis ou le nombre de satellites")
else:    
    print("[OK] Final Ap:", format_altitude(ap), "| Transfert Pe:", format_altitude(tpe), "-> Final Pe:", format_altitude(pe))
print()
print("... Fin ...")
