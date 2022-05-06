import numpy as np
import matplotlib.pyplot as plt

from Darlehen_Modul import Darlehen_Berechnung
from Bausparen_Modul import Bauspar_Berechnung


result_Bauspar = Bauspar_Berechnung(
    Bausparsumme=40000,
    Annuitaet=2000,
    Zins_Haben=0.1,
    Zins_Soll=1.9
) 
result_Kredit = Darlehen_Berechnung(
    Kredithoehe=200000,
    Annuitaet=1500,
    Zins_1=2.5,
    Zins_2=2.5,
    Zins_3=2.5
)


Laufzeit_Bauspar = result_Bauspar['Anzahl_monate']
Kosten_Bauspar = result_Bauspar['Bezahlt_kumuliert'][-1]
Laufzeit_Kredit = result_Kredit['Anzahl_monate']
Kosten_Kredit = result_Kredit['Bezahlt_kumuliert'][-1]
Kosten_gesamt = Kosten_Bauspar + Kosten_Kredit

print(('Bausparkosten = {:.0f}, Laufzeit = {:.0f} Monate\nKreditkosten = {:.0f}, Laufzeit = {:.0f} Monate').format(Kosten_Bauspar, Laufzeit_Bauspar, Kosten_Kredit, Laufzeit_Kredit))


# reines Bausparen
Annuitaet_test = np.arange(1200, 2400, 200)
Summe_test = np.arange(200000, 401000, 50000)
Sollzins = 1.65
Sonder = {
    5: 50000,
    10: 50000
}
Kosten_gesamt_test2 = np.zeros((len(Summe_test), len(Annuitaet_test)))
for i, summe_iter in enumerate(Summe_test):
    for j, annuitaet_iter in enumerate(Annuitaet_test):
        resultdict = Bauspar_Berechnung(
            Bausparsumme=summe_iter,
            Annuitaet=annuitaet_iter,
            Sonderzahlungen=Sonder,
            Zins_Soll=Sollzins
        )
        Kosten_gesamt_test2[i, j] = resultdict['Bezahlt_kumuliert'][-1]

plt.figure()
for i, summe_iter in enumerate(Summe_test):
    plt.plot(Annuitaet_test, Kosten_gesamt_test2[i,:], label=('Summe = {:.0f}').format(summe_iter))
plt.grid()
plt.legend()
plt.xlabel('Annuitaet in Euro')
plt.ylabel('Gesamtkosten')
plt.title(('Gesamtkosten bei\n{:.1f} Sollzins, {:.1f} Sonderzahlungen').format(Sollzins, 100000))
plt.show()

plt.figure()
for j, annuitaet_iter in enumerate(Annuitaet_test):
    plt.plot(Summe_test, Kosten_gesamt_test2[:,j], label=('Annuität = {:.0f}').format(annuitaet_iter))
plt.grid()
plt.legend()
plt.xlabel('Höhe in Euro')
plt.ylabel('Gesamtkosten')
plt.title(('Gesamtkosten bei\n{:.1f} Sollzins, {:.1f} Sonderzahlungen').format(Sollzins, 100000))
plt.show()

