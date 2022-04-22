import numpy as np
import matplotlib.pyplot as plt

def Bauspar_Berechnung(
    Kredithoehe,
    Annuitaet,
    Zinssatz_darlehen=2.5,
    Zinssatz_Bauspar_Soll=1.95,
    Zinssatz_Bauspar_Haben=1.0,
    zuteilungsreif_prozent=40,
    Abschlussgebuehr_anteil=1,
    Anpassungsfrequenz=12,
    Darlehen_start_monate = 0,
    Sondertilgungen=[]):

    Tilgung_Darlehen_monatlich = []
    Tilgung_Darlehen_kumuliert = []
    Tilgung_Bauspar_monatlich = []
    Tilgung_Bauspar_kumuliert = []
    Zinsen_monatlich = []
    Schulden_Darlehen_kumuliert = []
    Zinsen_Darlehen_kumuliert = []
    Zinsen_Darlehen_monatlich = []
    Zinsen_Bauspar_kumuliert = []
    Zinsen_Bauspar_monatlich = []
    Bezahlt_kumuliert = []
    Bauspar_Guthaben_kumuliert = []
    Bauspar_Sparbetrag_monatlich = []
    # Startwerte für kumulierte Listen
    Tilgung_Darlehen_kumuliert.append(0.0)
    Tilgung_Bauspar_kumuliert.append(0.0)
    Schulden_Darlehen_kumuliert.append(Kredithoehe)
    Zinsen_Darlehen_kumuliert.append(0.0)
    Zinsen_Bauspar_kumuliert.append(0.0)
    Abschlussgebuehr = Kredithoehe * Abschlussgebuehr_anteil / 100
    bezahllt_bisher = Abschlussgebuehr
    Bezahlt_kumuliert.append(bezahllt_bisher)
    Bauspar_Guthaben_kumuliert.append(0.0)
    Bauspar_Sparbetrag_monatlich.append(0.0)

    monat_zaehler = 0
    Bauspar_Guthaben = 0.0
    Zinsbasis_Darlehen = Kredithoehe
    Schulden_Darlehen = Kredithoehe
    Tilgung_Darlehen_bisher = 0.0
    Tilgung_Bauspar_bisher = 0.0
    Zinsen_Darlehen_bisher = 0.0
    Zinsen_Bauspar_bisher = 0.0
    monate_phase_1 = 0
    monate_phase_2 = 0

    # Phase 1: Bausparen bis Kredit benötigt
    while monat_zaehler < Darlehen_start_monate:
        monat_zaehler += 1
        Bauspar_Guthaben += Annuitaet
        bezahllt_bisher += Annuitaet
        Bezahlt_kumuliert.append(bezahllt_bisher)
        Bauspar_Guthaben_kumuliert.append(Bauspar_Guthaben)
        Zinsen_Darlehen_kumuliert.append(0.0)
        Zinsen_Darlehen_monatlich.append(0.0)
        Tilgung_Bauspar_kumuliert.append(0.0)
        Tilgung_Bauspar_monatlich.append(0.0)
        Zinsen_Bauspar_kumuliert.append(0.0) # Rechnung ohne Bauspar-Haben-Zinsen in dieser Phase
        Zinsen_Bauspar_monatlich.append(0.0)
        Bauspar_Sparbetrag_monatlich.append(Annuitaet)

    # Phase 2: Darlehen aufnehmen, Zinsen bedienen und Bausparvertrag füllen
    while Bauspar_Guthaben < zuteilungsreif_prozent/100 * Kredithoehe:
        # Monat weiterzählen
        monat_zaehler += 1
        # print('monat ', monat_zaehler)
        monate_phase_1 += 1
        # Sondertilgung diesen Monat ?
        if monat_zaehler in Sondertilgungen:
            Schulden_Darlehen -= Sondertilgungen[monat_zaehler]
            Zinsbasis_Darlehen = Schulden_Darlehen
            Tilgung_Darlehen_bisher += Sondertilgungen[monat_zaehler]
            bezahllt_bisher += Sondertilgungen[monat_zaehler]
        Zins_Darlehen = Zinsbasis_Darlehen * Zinssatz_darlehen/100 / 12
        Zinsen_Darlehen_bisher += Zins_Darlehen
        Sparbetrag = Annuitaet - Zins_Darlehen
        Bauspar_Guthaben += Sparbetrag
        Bauspar_Sparbetrag_monatlich.append(Sparbetrag)
        Zinsen_Darlehen_monatlich.append(Zins_Darlehen)
        Schulden_Darlehen_kumuliert.append(Schulden_Darlehen)
        Bauspar_Guthaben_kumuliert.append(Bauspar_Guthaben)
        Zinsen_Darlehen_kumuliert.append(Zinsen_Darlehen_bisher)
        
        # alle 12 Monate Guthabenzins --> immer im Folgemonat
        if monat_zaehler % 12 == 1:
            Zins_Bauspar_Haben = -Bauspar_Guthaben*Zinssatz_Bauspar_Haben/100
            Bauspar_Guthaben += Zins_Bauspar_Haben
            Zinsen_Bauspar_bisher += Zins_Bauspar_Haben
            Zinsen_Bauspar_kumuliert.append(Zinsen_Bauspar_bisher)
            Zinsen_Bauspar_monatlich.append(Zins_Bauspar_Haben)
        else:
            Zins_Bauspar_Haben = 0.0
            Zinsen_Bauspar_kumuliert.append(Zinsen_Bauspar_bisher)
            Zinsen_Bauspar_monatlich.append(0.0)
        
        bezahllt_bisher += Annuitaet + Zins_Bauspar_Haben
        Bezahlt_kumuliert.append(bezahllt_bisher)
        Tilgung_Bauspar_kumuliert.append(0.0)
        Tilgung_Bauspar_monatlich.append(0.0)
        
    # Phase 2 beendet, Bausparvertrag zuteilungsreif, Kredit wird getilgt:
    Schulden_Darlehen = 0.0
    Bauspar_Guthaben -= Kredithoehe
    Zinsbasis_Bauspar = abs(Bauspar_Guthaben)

    # Phase 3: Bausparvertrag abzahlen
    while Bauspar_Guthaben <= 0:
        monat_zaehler += 1
        # Sondertilgung diesen Monat?
        Tilgung_sonder = 0
        if monat_zaehler in Sondertilgungen:
            Tilgung_sonder = Sondertilgungen[monat_zaehler]
            Bauspar_Guthaben += Tilgung_sonder
            bezahllt_bisher += Tilgung_sonder
        # alle Anpassungsfrequenz Monate Zinsbasis anpassen --> immer im Anpassungsfrequenz+1-ten Monat
        if monat_zaehler % Anpassungsfrequenz == 1:
            Zinsbasis_Bauspar = abs(Bauspar_Guthaben)
        # Bausparkredit abzahlen mit Bausparzins
        Zins_Bauspar_aktuell = Zinssatz_Bauspar_Soll/100 * Zinsbasis_Bauspar / 12
        Tilgung_Bauspar_aktuell = Annuitaet - Zins_Bauspar_aktuell + Tilgung_sonder
        Tilgung_Bauspar_bisher += Tilgung_Bauspar_aktuell
        Zinsen_Bauspar_bisher += Zins_Bauspar_aktuell
        Tilgung_Bauspar_kumuliert.append(Tilgung_Bauspar_bisher)
        Tilgung_Bauspar_monatlich.append(Tilgung_Bauspar_aktuell)
        Bauspar_Guthaben += Tilgung_Bauspar_aktuell
        
        Zinsen_Bauspar_monatlich.append(Zins_Bauspar_aktuell)
        Zinsen_Bauspar_kumuliert.append(Zinsen_Bauspar_bisher)
        Schulden_Darlehen_kumuliert.append(Schulden_Darlehen)
        Bauspar_Guthaben_kumuliert.append(Bauspar_Guthaben)
        Zinsen_Darlehen_kumuliert.append(Zins_Darlehen)
        Zinsen_Darlehen_monatlich.append(0.0)
        Bauspar_Sparbetrag_monatlich.append(0.0)

        bezahllt_bisher += Annuitaet
        Bezahlt_kumuliert.append(bezahllt_bisher)

    # Wieviel insgesamt für Sondertilgungen
    Sondertilgungen_gesamt = 0
    for keys in Sondertilgungen:
        Sondertilgungen_gesamt += Sondertilgungen[keys]
    
    result_dict = {
        'Schulden_Darlehen_kumuliert': Schulden_Darlehen_kumuliert,
        'Bauspar_Guthaben_kumuliert': Bauspar_Guthaben_kumuliert,
        'Zinsen_Darlehen_kumuliert': Zinsen_Darlehen_kumuliert,
        'Zinsen_Bauspar_kumuliert': Zinsen_Bauspar_kumuliert,
        'Bezahlt_kumuliert': Bezahlt_kumuliert,
        'Zinsen_Darlehen_monatlich': Zinsen_Darlehen_monatlich,
        'Tilgung_Bauspar_monatlich': Tilgung_Bauspar_monatlich,
        'Zinsen_Bauspar_monatlich': Zinsen_Bauspar_monatlich,
        'Bauspar_Sparbetrag_monatlich': Bauspar_Sparbetrag_monatlich,
        'Anzahl_monate': monat_zaehler,
        'Gezahlt_gesamt': bezahllt_bisher,
        'Gezahlt_Bausparzins': Zinsen_Bauspar_bisher,
        'Gezahlt_Darlehenszins': Zinsen_Darlehen_bisher,
        'Abschlussgebuehr': Abschlussgebuehr,
        'Sondertilgungen_gesamt': Sondertilgungen_gesamt
    }

    return result_dict

    
if __name__ == "__main__":
    Kredithoehe = 400000.0
    Zinssatz_darlehen = 2.5 # in Prozent
    Zinssatz_Bauspar_Soll = 1.95 # in Prozent
    Zinssatz_Bauspar_Haben = 0.5 # in Prozent
    zuteilungsreif_prozent = 40
    Anpassungsfrequenz = 12 # in Monaten (mindestens 2!!!)
    Abschlussgebuehr_anteil = 1 # in Prozent
    Darlehen_start_monate = 10 # Darlehen startet soviel Monate nach Bausparbeginn

    Annuitaet = 1500
    Max_Sondertilgung = 0.05
    max_Betrag_Sondertilgungen = 0.2*Max_Sondertilgung*Kredithoehe
    # Sondertilgungen = {
    #     60: 5000,
    #     120: 5000,
    #     180: 10000}
    Sondertilgungen = []
    resultdict = Bauspar_Berechnung(
        Kredithoehe=Kredithoehe,
        Annuitaet=Annuitaet
    )
    
    Schulden_Darlehen_kumuliert = resultdict['Schulden_Darlehen_kumuliert']
    Bauspar_Guthaben_kumuliert = resultdict['Bauspar_Guthaben_kumuliert']
    Zinsen_Darlehen_kumuliert = resultdict['Zinsen_Darlehen_kumuliert']
    Zinsen_Bauspar_kumuliert = resultdict['Zinsen_Bauspar_kumuliert']
    Bezahlt_kumuliert = resultdict['Bezahlt_kumuliert']
    Zinsen_Darlehen_monatlich = resultdict['Zinsen_Darlehen_monatlich']
    Tilgung_Bauspar_monatlich = resultdict['Tilgung_Bauspar_monatlich']
    Zinsen_Bauspar_monatlich = resultdict['Zinsen_Bauspar_monatlich']
    Bauspar_Sparbetrag_monatlich = resultdict['Bauspar_Sparbetrag_monatlich']
    Anzahl_monate = resultdict['Anzahl_monate']
    Gezahlt_gesamt = resultdict['Gezahlt_gesamt']
    Gezahlt_Bausparzins = resultdict['Gezahlt_Bausparzins']
    Gezahlt_Darlehenszins = resultdict['Gezahlt_Darlehenszins']
    Abschlussgebuehr = resultdict['Abschlussgebuehr']
    Sondertilgungen_gesamt = resultdict['Sondertilgungen_gesamt']

    plt.figure()
    plt.plot(Schulden_Darlehen_kumuliert, label='Darlehen')
    plt.plot(Bauspar_Guthaben_kumuliert, label='Bausparguthaben')
    plt.plot(Zinsen_Darlehen_kumuliert, label='Darlehenszinsen')
    plt.plot(Zinsen_Bauspar_kumuliert, label='Bausparzinsen')
    plt.plot(Bezahlt_kumuliert, label='insgesamt gezahlt')
    plt.legend()
    plt.xlabel('Laufzeit in Monaten')
    plt.ylabel('Euro')
    plt.grid()
    plt.title(('Kredithöhe = {:.0f}; Laufzeit = {:.1f} Jahre; Annuität = {:.0f}').format(Kredithoehe, Anzahl_monate/12, Annuitaet))

    plt.figure()
    plt.plot(Zinsen_Darlehen_monatlich, label='monatl. Darlehenszinsen')
    plt.plot(Tilgung_Bauspar_monatlich, label='monatl. Tilgung Bauspar')
    plt.plot(Zinsen_Bauspar_monatlich, label='monatl. Bausparzinsen')
    plt.plot(Bauspar_Sparbetrag_monatlich, label='monatl. Sparbetrag')
    plt.plot(np.arange(Anzahl_monate), Annuitaet*np.ones((Anzahl_monate, 1)), label='Annuität')
    plt.legend()
    plt.xlabel('Laufzeit in Monaten')
    plt.ylabel('Euro')
    plt.grid()
    plt.title('Zusammensetzung der Annuität')

    plt.show()

