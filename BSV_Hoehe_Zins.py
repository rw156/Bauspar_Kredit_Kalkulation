import numpy as np
import matplotlib.pyplot as plt

ges = 400000
BSV_test        = [200000, 250000, 300000, 350000, 400000]
zuteilung_test  = [42,     51,     60,     69,     78]


# Rückzahlungsphase
def BSV_phase2(BSV_summe, Annu_BSV, BSV_zins=1.65):
    Bausparschulden = BSV_summe*0.6
    monat_zaehler = 0
    Zinskosten_BSV = 0
    while Bausparschulden > 0:
        monat_zaehler += 1
        # alle 12 Monate Zinsbasis anpassen
        if monat_zaehler % 12 == 1:
            Zinsbasis = Bausparschulden
        # Bausparkredit abzahlen mit Bausparzins
        Zins_aktuell = BSV_zins/100 * Zinsbasis / 12
        Tilgung = Annu_BSV - Zins_aktuell
        Zinskosten_BSV += Zins_aktuell
        Bausparschulden -= Tilgung

    return Zinskosten_BSV


test = BSV_phase2(250000, 2000)
print(test)
