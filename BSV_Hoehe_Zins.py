import numpy as np
import matplotlib.pyplot as plt

# Rückzahlungsphase
def BSV_phase2(BSV_summe, Annu_BSV_1, Annu_BSV_2, monate_1, BSV_zins=1.65):
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
        if monat_zaehler <= monate_1:
            Tilgung = Annu_BSV_1 - Zins_aktuell
        else:
            Tilgung = Annu_BSV_2 - Zins_aktuell
        Zinskosten_BSV += Zins_aktuell
        Bausparschulden -= Tilgung

    return Zinskosten_BSV


def Zwischenzins(Summe, Zins, Laufzeit):
    return Summe * Zins/100 * Laufzeit/12

def Restzins(Summe, Annu, Zins):
    Zins_ges = 0
    Restschulden = Summe
    monat_zaehler = 0
    while Restschulden > 0.0:
        # Monat weiterzählen
        monat_zaehler += 1
        # print('monat ', monat_zaehler)
        # alle Anpassungsfrequenz Monate Zinsbasis anpassen --> immer im Anpassungsfrequenz+1-ten Monat
        if monat_zaehler % 12 == 1:
            Zinsbasis = Restschulden
            Zinsen = Zinsbasis * Zins/100 / 12
            Tilgung = Annu - Zinsen
        Zins_ges += Zinsen
        Restschulden -= Tilgung
    
    return Zins_ges, monat_zaehler

ges = 450000
BSV_test        = [250000, 275000, 300000, 325000, 350000, 375000, 400000]
zuteilung_test  = [42,     47,     51,     56,     60,     65,     68]
# zuteilung_test  = [40,     50,     60,     70,     80,     90,     100]
Annu = 2000
Zins_kredit_test = [1, 2, 3, 4, 5]

Gesamt_zins_test = np.zeros((len(BSV_test), len(Zins_kredit_test)))
for i in range(len(BSV_test)):
    for j in range(len(Zins_kredit_test)):
        zins_Zwischen_temp = Zwischenzins(ges, Zins_kredit_test[j], zuteilung_test[i])
        summe_rest = ges - BSV_test[i]
        if summe_rest > 0:
            Annu_rest = Annu / 2
            Annu_BSV_1 = Annu / 2
        else:
            Annu_rest = 0
            Annu_BSV_1 = Annu
        zins_Rest, monate_rest = Restzins(summe_rest, Annu_rest, Zins_kredit_test[j])
        
        zins_BSV_tmp = BSV_phase2(BSV_test[i], Annu_BSV_1, Annu, monate_rest)
        summe = zins_Zwischen_temp + zins_Rest + zins_BSV_tmp
        Gesamt_zins_test[i, j] = summe


plt.figure()
for j in range(len(Zins_kredit_test)):
    plt.plot(BSV_test, Gesamt_zins_test[:, j], label='Zins: ' + str(Zins_kredit_test[j]) + '%')
plt.grid()
plt.legend()
plt.show()


sofortzahlung_test = [0, 20000, 30000, 40000, 60000]
schneller_BSV_durch_sofort = [0, 6, 9, 12, 18]
BSV = 350000
zuteilung_nach = 60
Gesamt_zins_test2 = np.zeros((len(sofortzahlung_test), len(Zins_kredit_test)))
for i in range(len(sofortzahlung_test)):
    Kredit_tmp = ges - sofortzahlung_test[-(i+1)]
    for j in range(len(Zins_kredit_test)):
        zuteilungsreif_tmp = zuteilung_nach-schneller_BSV_durch_sofort[i]
        zins_Zwischen_temp2 = Zwischenzins(ges, Zins_kredit_test[j], zuteilungsreif_tmp)
        summe_rest2 = Kredit_tmp - BSV
        if summe_rest > 0:
            Annu_rest = Annu / 2
            Annu_BSV_1 = Annu / 2
        else:
            Annu_rest = 0
            Annu_BSV_1 = Annu
        zins_Rest2, monate_rest2 = Restzins(summe_rest2, Annu_rest, Zins_kredit_test[j])
        zins_BSV_tmp2 = BSV_phase2(BSV, Annu_BSV_1, Annu, monate_rest2)
        summe = zins_Zwischen_temp2 + zins_Rest2 + zins_BSV_tmp2
        Gesamt_zins_test2[i, j] = summe

plt.figure()
for j in range(len(Zins_kredit_test)):
    plt.plot(sofortzahlung_test, Gesamt_zins_test2[:, j], label='Zins: ' + str(Zins_kredit_test[j]) + '%')
plt.grid()
plt.legend()
plt.xlabel('Sofortzahlung in BSV')
plt.ylabel('Gesamtzins')
plt.title('BSV Summe: ' + str(BSV))
plt.show()
