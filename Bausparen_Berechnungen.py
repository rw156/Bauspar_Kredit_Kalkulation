import numpy as np
import matplotlib.pyplot as plt

from Bausparen_Modul import Bauspar_Berechnung
from Darlehen_Modul import Darlehen_Berechnung

Kredithoehe = 400000.0
Annuitaet = 1500
Zinssatz_darlehen = 2.5 # in Prozent
Zinssatz_Bauspar_Soll = 1.95 # in Prozent
Zinssatz_Bauspar_Haben = 0.5 # in Prozent
zuteilungsreif_prozent = 40
Anpassungsfrequenz = 12 # in Monaten (mindestens 2!!!)
Abschlussgebuehr_anteil = 1 # in Prozent
Darlehen_start_monate = 0 # Darlehen startet soviel Monate nach Bausparbeginn

# Test Zinsen
Zins_Darlehen_test = np.arange(1.8, 2.8, 0.1)
Zins_Bauspar_test = np.arange(1.7, 2.2, 0.1)
Kosten_gesamt = np.zeros((len(Zins_Bauspar_test), len(Zins_Darlehen_test)))
for i, zins_bauspar_iter in enumerate(Zins_Bauspar_test):
    for j, zins_darlehen_iter in enumerate(Zins_Darlehen_test):
        resultdict = Bauspar_Berechnung(
            Kredithoehe=Kredithoehe,
            Annuitaet=Annuitaet,
            Zinssatz_darlehen=zins_darlehen_iter,
            Zinssatz_Bauspar_Soll=zins_bauspar_iter
        )
        Kosten_gesamt[i, j] = resultdict['Gezahlt_gesamt']

plt.figure()
for i, zins_bauspar_iter in enumerate(Zins_Bauspar_test):
    plt.plot(Zins_Darlehen_test, Kosten_gesamt[i,:], label=('Bausparzins = {:.1f}').format(zins_bauspar_iter))
plt.xlabel('Darlehenszins in Prozent')
plt.ylabel('Gesamtkosten')
plt.grid()
plt.legend()
plt.title(('Gesamtkosten bei {:.0f} Euro Kredithöhe, {:.0f} Annuität').format(Kredithoehe, Annuitaet))
plt.show()

# Test Annuität
Annuitaet_test = np.arange(800, 1900, 100)
Summe_test = np.arange(200000, 350000, 50000)
Kosten_gesamt_test2 = np.zeros((len(Summe_test), len(Annuitaet_test)))
for i, summe_iter in enumerate(Summe_test):
    for j, annuitaet_iter in enumerate(Annuitaet_test):
        resultdict = Bauspar_Berechnung(
            Kredithoehe=summe_iter,
            Annuitaet=annuitaet_iter
        )
        Kosten_gesamt_test2[i, j] = resultdict['Gezahlt_gesamt']

plt.figure()
for i, summe_iter in enumerate(Summe_test):
    plt.plot(Annuitaet_test, Kosten_gesamt_test2[i,:], label=('Summe = {:.0f}').format(summe_iter))
plt.grid()
plt.legend()
plt.xlabel('Annuitaet in Euro')
plt.ylabel('Gesamtkosten')
plt.title(('Gesamtkosten bei\n{:.1f} Prozent Darlehenszins, {:.1f} Prozent Bausparzins').format(Zinssatz_darlehen, Zinssatz_Bauspar_Soll))
plt.show()

# Darlehen vs. Bauspar
Zins_1_Darlehen = 2.5 # gilt 120 Monate
Zins_2_Darlehen = 4.0 # gilt weitere 120 Monate
Zins_3_Darlehen = 5.0 # gilt für Restlaufzeit

resultdict_Darlehen = Darlehen_Berechnung(
    Kredithoehe=Kredithoehe,
    Annuitaet=Annuitaet,
    Zins_1=Zins_1_Darlehen, Zins_2=Zins_2_Darlehen, Zins_3=Zins_3_Darlehen
)
resultdict_Bauspar = Bauspar_Berechnung(
    Kredithoehe=Kredithoehe,
    Annuitaet=Annuitaet
)

Gesamtkosten_Bauspar = resultdict_Bauspar['Gezahlt_gesamt']
Zinsen_Bauspar_Darlehen = resultdict_Bauspar['Gezahlt_Darlehenszins']
Zinsen_Bauspar_Bauspar = resultdict_Bauspar['Gezahlt_Bausparzins']
Abschlussgebuehr_Bauspar = resultdict_Bauspar['Abschlussgebuehr']

Gesamtkosten_Darlehen_kumuliert = resultdict_Darlehen['Bezahlt_kumuliert']
Zinsen_Darlehen_kumuliert = resultdict_Darlehen['Zinsen_kumuliert']
Abschlussgebuehr_Darlehen = resultdict_Darlehen['Abschlussgebuehr']

labels_Bauspar = ['Tilgung', 'Zinsen Darlehen', 'Zinsen Bauspar', 'Abschlussgebühr']
labels_Darlehen = ['Tilgung', 'Zinsen', 'Abschlussgebühr']
plt.figure()
plt.subplot(1,2,1)
plt.pie([Kredithoehe, Zinsen_Darlehen_kumuliert[-1], Abschlussgebuehr_Darlehen],
    labels=labels_Darlehen,
    radius=0.6*Gesamtkosten_Darlehen_kumuliert[-1]/Kredithoehe)
plt.title(('Gesamtkosten = {:.0f}\n(Darlehen)').format(Gesamtkosten_Darlehen_kumuliert[-1]))
plt.subplot(1,2,2)
plt.pie([Kredithoehe, Zinsen_Bauspar_Darlehen, Zinsen_Bauspar_Bauspar, Abschlussgebuehr_Bauspar],
    labels=labels_Bauspar,
    radius=0.6*Gesamtkosten_Bauspar/Kredithoehe)
plt.title(('Gesamtkosten = {:.0f}\n(Bauspar)').format(Gesamtkosten_Bauspar))
plt.show()




# zwei Bausparverträge mit halber Annuität?
resultdict_voll = Bauspar_Berechnung(
    Kredithoehe=Kredithoehe,
    Annuitaet=Annuitaet)

resultdict_halb = Bauspar_Berechnung(
    Kredithoehe=Kredithoehe/2,
    Annuitaet=Annuitaet/2)

Gesamtkosten_voll = resultdict_voll['Gezahlt_gesamt']
Bausparzins_voll = resultdict_voll['Gezahlt_Bausparzins']
Darlehenszins_voll = resultdict_voll['Gezahlt_Darlehenszins']
Tilgung_voll = Kredithoehe
Abschlussgebuehr_voll = resultdict_voll['Abschlussgebuehr']

Gesamtkosten_halb = resultdict_halb['Gezahlt_gesamt']
Bausparzins_halb = resultdict_halb['Gezahlt_Bausparzins']
Darlehenszins_halb = resultdict_halb['Gezahlt_Darlehenszins']
Tilgung_halb = Kredithoehe/2
Abschlussgebuehr_halb = resultdict_halb['Abschlussgebuehr']

labels = ['Tilgung', 'Zinsen Darlehen', 'Zinsen Bauspar', 'Abschlussgebühr']
plt.figure()
plt.subplot(1,2,1)
plt.pie([Tilgung_halb*2, Darlehenszins_halb*2, Bausparzins_halb*2, Abschlussgebuehr_halb*2], radius=0.7*Gesamtkosten_halb*2/Kredithoehe, labels=labels)
plt.title(('Gesamtkosten = {:.0f}\n(zwei Halbe)').format(Gesamtkosten_halb*2))
plt.subplot(1,2,2)
plt.pie([Tilgung_voll, Darlehenszins_voll, Bausparzins_voll, Abschlussgebuehr_voll], radius=0.7*Gesamtkosten_voll/Kredithoehe, labels=labels)
plt.title(('Gesamtkosten = {:.0f}\n(ein Ganzer)').format(Gesamtkosten_voll))
plt.show()
