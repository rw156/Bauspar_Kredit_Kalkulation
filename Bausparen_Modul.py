import matplotlib.pyplot as plt

def Bauspar_Berechnung(
        Bausparsumme,
        Annuitaet,
        Zins_Haben = 0.1,
        Zins_Soll = 1.9,
        Abschlussgebuehr_prozent = 1,
        zuteilungsreif_prozent = 40,
        Sonderzahlungen = {},
        Anpassungsfrequenz = 12
    ):
    # init
    Tilgung_monatlich = []
    Tilgung_kumuliert = []
    Zinsen_monatlich = []
    Zinsen_kumuliert = []
    Bauspar_Guthaben_kumuliert = []
    Bezahlt_kumuliert = []
    Sparbetrag_monatlich = []

    monat_zaehler = 0
    bezahlt_bisher = Abschlussgebuehr_prozent/100 * Bausparsumme # Abschlussgebühr
    Zins_bisher = 0.0
    Bauspar_Guthaben = 0.0
    Bezahlt_kumuliert.append(bezahlt_bisher)
    Bauspar_Guthaben_kumuliert.append(Bauspar_Guthaben) # Anfangsbestand
    Sparbetrag_monatlich.append(0.0)
    
    # Ansparphase
    while Bauspar_Guthaben <= (zuteilungsreif_prozent/100 * Bausparsumme):
        monat_zaehler += 1
        # Sonder diesen Monat?
        if monat_zaehler in Sonderzahlungen:
            Bauspar_Guthaben += Sonderzahlungen[monat_zaehler]
            bezahlt_bisher += Sonderzahlungen[monat_zaehler]
        # alle Anpassungsfrequenz Monate Zinsbasis anpassen --> immer im Anpassungsfrequenz+1-ten Monat
        if monat_zaehler % Anpassungsfrequenz == 1:
            Zinsbasis = abs(Bauspar_Guthaben)
            # Habenzins
            Zins_aktuell = Zins_Haben/100 * Zinsbasis / 12
        Bauspar_Guthaben += (Annuitaet + Zins_aktuell)
        Bauspar_Guthaben_kumuliert.append(Bauspar_Guthaben)
        bezahlt_bisher += Annuitaet
        Zins_bisher -= Zins_aktuell # Haben-Zins
        Bezahlt_kumuliert.append(bezahlt_bisher)
        Zinsen_kumuliert.append(Zins_bisher)
        Zinsen_monatlich.append(Zins_aktuell)
        Tilgung_monatlich.append(0.0)
        Tilgung_kumuliert.append(0.0)
        Sparbetrag_monatlich.append(Annuitaet+Zins_aktuell)

    # Auszahlung
    Bauspar_Guthaben -= Bausparsumme
    Zinsbasis = abs(Bauspar_Guthaben)

    # Rückzahlungsphase
    while Bauspar_Guthaben <= 0:
        monat_zaehler += 1
        # Abbruch, wenn zu lange (wenn z.B. Annuitaet zu klein, um Zinsen zu berechnen)
        if monat_zaehler > 1000:
            result_dict = dict()
            return result_dict
        # Sonder diesen Monat
        if monat_zaehler in Sonderzahlungen:
            Bauspar_Guthaben += Sonderzahlungen[monat_zaehler]
            bezahlt_bisher += Sonderzahlungen[monat_zaehler]
        # alle Anpassungsfrequenz Monate Zinsbasis anpassen --> immer im Anpassungsfrequenz+1-ten Monat
        if monat_zaehler % Anpassungsfrequenz == 1:
            Zinsbasis = abs(Bauspar_Guthaben)
        # Bausparkredit abzahlen mit Bausparzins
        Zins_aktuell = Zins_Soll/100 * Zinsbasis / 12
        bezahlt_bisher += Annuitaet
        Bezahlt_kumuliert.append(bezahlt_bisher)
        Tilgung = Annuitaet - Zins_aktuell
        Zinsen_monatlich.append(Zins_aktuell)
        Zins_bisher += Zins_aktuell
        Zinsen_kumuliert.append(Zins_bisher)
        Tilgung_monatlich.append(Tilgung)
        Bauspar_Guthaben += Tilgung
        Bauspar_Guthaben_kumuliert.append(Bauspar_Guthaben)

        result_dict = {
            'Tilgung_monatlich': Tilgung_monatlich,
            'Tilgung_kumuliert': Tilgung_kumuliert,
            'Zinsen_monatlich': Zinsen_monatlich,
            'Zinsen_kumuliert': Zinsen_kumuliert,
            'Bezahlt_kumuliert': Bezahlt_kumuliert,
            'Bauspar_Guthaben_kumuliert': Bauspar_Guthaben_kumuliert,
            'Sparbetrag_monatlich': Sparbetrag_monatlich,
            'Anzahl_monate': monat_zaehler
        }

    return result_dict


if __name__=='__main__':
    Bausparsumme = 120000
    Annuitaet = 600
    Sonderzahlungen = {
        1: 20000
    }
    # Sonderzahlungen = dict()
    Zins_Haben = 0.01
    Zins_Soll = 1.65
    Abschlussgebuehr_prozent = 1.6
    Anpassungsfrequenz = 12
    zuteilungsreif_prozent = 32

    resultdict = Bauspar_Berechnung(
        Bausparsumme=Bausparsumme,
        Annuitaet=Annuitaet,
        Sonderzahlungen=Sonderzahlungen,
        Zins_Haben=Zins_Haben,
        Zins_Soll=Zins_Soll,
        Abschlussgebuehr_prozent=Abschlussgebuehr_prozent,
        Anpassungsfrequenz=Anpassungsfrequenz,
        zuteilungsreif_prozent=zuteilungsreif_prozent
    )

    Tilgung_monatlich = resultdict['Tilgung_monatlich']
    Tilgung_kumuliert = resultdict['Tilgung_kumuliert']
    Zinsen_monatlich =  resultdict['Zinsen_monatlich']
    Zinsen_kumuliert = resultdict['Zinsen_kumuliert']
    Bezahlt_kumuliert = resultdict['Bezahlt_kumuliert']
    Bauspar_Guthaben_kumuliert = resultdict['Bauspar_Guthaben_kumuliert']
    Sparbetrag_monatlich = resultdict['Sparbetrag_monatlich']
    Anzahl_monate = resultdict['Anzahl_monate']

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(Tilgung_kumuliert, label='Tilgung')
    plt.plot(Zinsen_kumuliert, label='Zinsen')
    plt.plot(Bezahlt_kumuliert, label='bezahlt')
    plt.plot(Bauspar_Guthaben_kumuliert, label='Guthaben')
    plt.grid()
    plt.legend()
    plt.title(('Bausparsumme = {:.0f}; Laufzeit = {:.1f} Jahre; Annuität = {:.0f}').format(Bausparsumme, Anzahl_monate/12, Annuitaet))
    plt.subplot(2,1,2)
    plt.plot(Zinsen_monatlich, label='Zinsen')
    plt.plot(Tilgung_monatlich, label='Tilgung')
    plt.plot(Sparbetrag_monatlich, label='Sparbetrag')
    plt.grid()
    plt.legend()
    plt.show()
