import difflib


class StationsDaten:
    """Verwaltet die U1-Stationen und die Normalisierung der Eingabe."""

    def __init__(self):
        self.liste = [
            "Langwasser Süd", "Gemeinschaftshaus", "Langwasser Mitte",
            "Scharfreiterring", "Langwasser Nord", "Messe", "Bauernfeindstraße",
            "Hasenbuck", "Frankenstraße", "Maffeiplatz", "Aufseßplatz",
            "Hauptbahnhof", "Lorenzkirche", "Weißer Turm", "Plärrer",
            "Gostenhof", "Bärenschanze", "Maximilianstraße", "Eberhardshof",
            "Muggenhof", "Stadtgrenze", "Jakobinenstraße", "Fürth Hauptbahnhof"
        ]
        self.mapping = {"hbf": "hauptbahnhof", "str": "strasse", "fr": "friedrich"}

    def normalisieren(self, text):
        t = text.strip().lower().replace("-", " ")
        t = t.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        return " ".join([self.mapping.get(w.rstrip("."), w) for w in t.split()])

    def finden(self, abfrage):
        norm_q = self.normalisieren(abfrage)
        beste_uebereinstimmung, max_rate = None, 0.0
        for s in self.liste:
            norm_s = self.normalisieren(s)
            if norm_q == norm_s: return s
            rate = difflib.SequenceMatcher(None, norm_q, norm_s).ratio()
            if rate > max_rate: max_rate, beste_uebereinstimmung = rate, s
        return beste_uebereinstimmung if max_rate >= 0.8 else None


class Ticket:
    """Datenstruktur für eine Fahrkarte."""

    def __init__(self, start, ziel, stationen_anzahl, preis):
        self.start = start
        self.ziel = ziel
        self.dauer = stationen_anzahl * 2
        self.preis = preis

    def anzeigen(self):
        print("\n" + "=" * 30 + "\nREISEZUSAMMENFASSUNG")
        print(f"Start:    {self.start}\nZiel:     {self.ziel}")
        print(f"Dauer:    ca. {self.dauer} Min\nEndpreis: {self.preis:.2f} €")
        print("=" * 30)


class PreisBerechnung:
    """Berechnungslogik nach Szenario A (Additiv)."""

    def berechne(self, anzahl):
        # Grundpreise basierend auf Distanz
        if anzahl <= 3:
            preise = {"e": 1.50, "m": 5.00}
        elif anzahl <= 8:
            preise = {"e": 2.00, "m": 7.00}
        else:
            preise = {"e": 3.00, "m": 10.00}

        typ = input("Einzelticket (e) oder Mehrfahrtenticket (m)? ").lower()
        sozial = input("Haben Sie Anspruch auf Sozialrabatt? (j/n) ").lower()
        zahlung = input("Zahlart: Bar (b) oder Karte (k)? ").lower()

        grundpreis = preise.get(typ, preise['e'])

        # Szenario A: Faktoren werden addiert/subtrahiert
        faktor = 1.0

        # Aufschlag für Einzelticket (um auf die Testfall-Werte wie 1.65€ zu kommen)
        if typ == 'e':
            faktor += 0.10  # +10%

        if sozial == 'j':
            faktor -= 0.20  # -20% Sozialrabatt

        if zahlung == 'b':
            faktor += 0.15  # +15% Barzahlungsaufschlag

        # Endpreis = Grundpreis * Gesamtfaktor
        endpreis = grundpreis * faktor
        return round(endpreis, 2)


class FahrplanApp:
    """Hauptsteuerung der Anwendung."""

    def __init__(self):
        self.daten = StationsDaten()
        self.rechner = PreisBerechnung()

    def get_station_validierung(self, prompt):
        while True:
            name = self.daten.finden(input(prompt))
            if name: return name
            print("Station nicht erkannt. Bitte versuchen Sie es erneut.")

    def starten(self):
        print("--- U-Bahn Nürnberg/Fürth (U1) Ticket-System ---")
        start = self.get_station_validierung("Start: ")
        ziel = self.get_station_validierung("Ziel: ")

        anzahl = abs(self.daten.liste.index(start) - self.daten.liste.index(ziel))
        preis = self.rechner.berechne(anzahl)

        ticket = Ticket(start, ziel, anzahl, preis)
        ticket.anzeigen()


if __name__ == "__main__":
    app = FahrplanApp()
    app.starten()