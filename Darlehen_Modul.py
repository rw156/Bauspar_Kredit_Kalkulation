import numpy as np
import matplotlib.pyplot as plt

def Darlehen_Berechnung(Kredithoehe, Annuitaet, Zins_1, Zins_2, Zins_3, Monate_1=120, Monate_2=120, Abschlussgebuehr_anteil=1, Anpassungsfrequenz=12, Sondertilgungen=[]):
    Tilgung_monatlich = []
    Zinsen_monatlich = []
    Tilgung_kumuliert = []
    Restschulden_kumuliert = []
    Zinsen_kumuliert = []
    Bezahlt_kumuliert = []
    # Startwerte für kumulierte Listen
    Tilgung_kumuliert.append(0.0)
    Restschulden_kumuliert.append(Kredithoehe)
    Zinsen_kumuliert.append(0.0)
    Abschlussgebuehr = Kredithoehe * Abschlussgebuehr_anteil / 100
    bezahllt_bisher = Abschlussgebuehr
    Bezahlt_kumuliert.append(bezahllt_bisher)

    monat_zaehler = 0
    Zinsbasis = Kredithoehe
    Restschulden = Kredithoehe
    getilgt_bisher = 0
    zinsen_bisher = 0
    while Restschulden > 0.0:
        # Monat weiterzählen
        monat_zaehler += 1
        # print('monat ', monat_zaehler)
        # alle Anpassungsfrequenz Monate Zinsbasis anpassen --> immer im Anpassungsfrequenz+1-ten Monat
        if monat_zaehler % Anpassungsfrequenz == 1:
            Zinsbasis = Restschulden
            # Zinsen in ensprechend der Phase
            if monat_zaehler < Monate_1:
                Zinsen = Zinsbasis * Zins_1/100 / 12
            elif monat_zaehler < Monate_1 + Monate_2:
                Zinsen = Zinsbasis * Zins_2/100 / 12
            else:
                Zinsen = Zinsbasis * Zins_3/100 / 12
            Tilgung = Annuitaet - Zinsen
        Tilgung_monatlich.append(Tilgung)
        Zinsen_monatlich.append(Zinsen)
        getilgt_bisher += Tilgung
        zinsen_bisher += Zinsen
        Restschulden -= Tilgung
        bezahllt_bisher = bezahllt_bisher + Zinsen + Tilgung
        # Sondertilgung diesen Monat ?
        if monat_zaehler in Sondertilgungen:
            Restschulden -= Sondertilgungen[monat_zaehler]
            getilgt_bisher += Sondertilgungen[monat_zaehler]
            bezahllt_bisher += Sondertilgungen[monat_zaehler]
        Restschulden_kumuliert.append(Restschulden)
        Tilgung_kumuliert.append(getilgt_bisher)
        Zinsen_kumuliert.append(zinsen_bisher)
        Bezahlt_kumuliert.append(bezahllt_bisher)
    
    resultdict = {
        'Restschulden_kumuliert': Restschulden_kumuliert,
        'Tilgung_kumuliert': Tilgung_kumuliert,
        'Zinsen_kumuliert': Zinsen_kumuliert,
        'Bezahlt_kumuliert': Bezahlt_kumuliert,
        'Tilgung_monatlich': Tilgung_monatlich,
        'Zinsen_monatlich': Zinsen_monatlich,
        'Anzahl_monate': monat_zaehler,
        'Abschlussgebuehr': Abschlussgebuehr
    }

    return resultdict

    
if __name__ == "__main__":
    Kredithoehe = 400000.0
    Zins_1 = 2.5 # in Prozent
    Zins_2 = 4.0 # in Prozent
    Zins_3 = 4.0 # in Prozent
    Monate_1 = 120
    Monate_2 = 120
    Anpassungsfrequenz = 12 # in Monaten (mindestens 2!!!)
    Abschlussgebuehr_anteil = 1 # in Prozent

    Annuitaet = 1500
    Max_Sondertilgung = 0.05
    Betrag_Sondertilgungen = Max_Sondertilgung*Kredithoehe
    print('Betrag für Sondertilgungen: ', Betrag_Sondertilgungen)
    # Sondertilgungen = {
    #     60: 5000,
    #     120: 5000,
    #     180: 10000}
    Sondertilgungen = []

    resultdict = Darlehen_Berechnung(
        Kredithoehe=Kredithoehe,
        Annuitaet=Annuitaet,
        Zins_1=Zins_1,
        Zins_2=Zins_2,
        Zins_3=Zins_3,
        Monate_1=Monate_1,
        Monate_2=Monate_2,
        Abschlussgebuehr_anteil=Abschlussgebuehr_anteil,
        Anpassungsfrequenz=Anpassungsfrequenz,
        Sondertilgungen=Sondertilgungen
    )

    Restschulden_kumuliert = resultdict['Restschulden_kumuliert']
    Tilgung_kumuliert = resultdict['Tilgung_kumuliert']
    Zinsen_kumuliert = resultdict['Zinsen_kumuliert']
    Bezahlt_kumuliert = resultdict['Bezahlt_kumuliert']
    Tilgung_monatlich = resultdict['Tilgung_monatlich']
    Zinsen_monatlich = resultdict['Zinsen_monatlich']
    Anzahl_monate = resultdict['Anzahl_monate']

    plt.figure()
    plt.plot(Restschulden_kumuliert, label='Schulden')
    plt.plot(Tilgung_kumuliert, label='Tilgung')
    plt.plot(Zinsen_kumuliert, label='gezahlte Zinsen')
    plt.plot(Bezahlt_kumuliert, label='insgesamt gezahlt')
    plt.legend()
    plt.xlabel('Laufzeit in Monaten')
    plt.ylabel('Euro')
    plt.grid()
    plt.title(('Kredithöhe = {:.0f}; Laufzeit = {:.1f} Jahre; Annuität = {:.0f}').format(Kredithoehe, Anzahl_monate/12, Annuitaet))

    plt.figure()
    plt.plot(Tilgung_monatlich, label='monatl. Tilgung')
    plt.plot(Zinsen_monatlich, label='monatl. Zinsen')
    plt.plot(np.arange(Anzahl_monate), Annuitaet*np.ones((Anzahl_monate, 1)), label='Annuität')
    plt.legend()
    plt.xlabel('Laufzeit in Monaten')
    plt.ylabel('Euro')
    plt.grid()
    plt.title('Zusammensetzung der Annuität')

    plt.show()

