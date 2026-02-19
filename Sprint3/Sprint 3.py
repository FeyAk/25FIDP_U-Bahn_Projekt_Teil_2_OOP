import difflib
from datetime import datetime, timedelta


class StationsDaten:
    def __init__(self):
        # U1 durak listesi
        self.liste = [
            "Langwasser Süd", "Gemeinschaftshaus", "Langwasser Mitte",
            "Scharfreiterring", "Langwasser Nord", "Messe", "Bauernfeindstraße",
            "Hasenbuck", "Frankenstraße", "Maffeiplatz", "Aufseßplatz",
            "Hauptbahnhof", "Lorenzkirche", "Weißer Turm", "Plärrer",
            "Gostenhof", "Bärenschanze", "Maximilianstraße", "Eberhardshof",
            "Muggenhof", "Stadtgrenze", "Jakobinenstraße", "Fürth Hauptbahnhof"
        ]
        # User Story 3.1: Mapping
        self.mapping = {"hbf": "hauptbahnhof", "str": "strasse", "fr": "friedrich"}

    def normalisieren(self, text):
        t = text.strip().lower().replace("-", " ")
        t = t.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        return " ".join([self.mapping.get(w.rstrip("."), w) for w in t.split()])

    def finden(self, abfrage):
        norm_q = self.normalisieren(abfrage)
        # Testfall 10: Eindeutigkeit (Tam eşleşme önceliği)
        for s in self.liste:
            if norm_q == self.normalisieren(s): return s

        # User Story 3.1: Fuzzy-Matching 80%
        beste, max_rate = None, 0.0
        for s in self.liste:
            rate = difflib.SequenceMatcher(None, norm_q, self.normalisieren(s)).ratio()
            if rate > max_rate:
                max_rate, beste = rate, s
        return beste if max_rate >= 0.8 else None


class PreisBerechnung:
    def berechne(self, anzahl):
        # User Story 3.2: Basispreise
        if 1 <= anzahl <= 3:
            grund = {"e": 1.50, "m": 5.00}
        elif 1 <= anzahl <= 8:
            grund = {"e": 2.00, "m": 7.00}
        else:
            grund = {"e": 3.00, "m": 10.00}

        typ = input("Einzelticket (e) oder Mehrfahrt (m)? ").lower()
        sozial = input("Sozialrabatt (j/n)? ").lower()
        zahlung = input("Zahlart: Bar (b) oder Karte (k)? ").lower()

        # User Story 3.2: Additive Berechnung
        faktor = 1.0
        if typ == "e": faktor += 0.10
        if sozial == "j": faktor -= 0.20
        if zahlung == "b": faktor += 0.15

        preis = grund.get(typ, grund["e"]) * faktor
        return round(preis, 2)


class FahrplanApp:
    def __init__(self):
        self.daten = StationsDaten()
        self.rechner = PreisBerechnung()

    def starten(self):
        # User Story 3.1 & 3.3
        start_name = self.daten.finden(input("Start: "))
        while not start_name:
            start_name = self.daten.finden(input("Nicht erkannt. Start: "))

        ziel_name = self.daten.finden(input("Ziel: "))
        while not ziel_name:
            ziel_name = self.daten.finden(input("Nicht erkannt. Ziel: "))

        wunschzeit = input("Wunschzeit (HH:MM): ")

        # Ankunftszeit Logik (Testfall Tablo 3 gereği 1.5 dk/durak + yuvarlama)
        anzahl = abs(self.daten.liste.index(start_name) - self.daten.liste.index(ziel_name))
        ab_dt = datetime.strptime(wunschzeit, "%H:%M")
        an_dt = ab_dt + timedelta(seconds=anzahl * 90)

        # Aufrunden (Testfall 1 & 4 & 5 gereği saniye varsa tam dakikaya)
        if an_dt.second > 0:
            an_dt = an_dt + timedelta(seconds=60 - an_dt.second)

        preis = self.rechner.berechne(anzahl)

        # User Story 3.3: Zusammenfassung
        print("\n--- REISEINFORMATION ---")
        print(f"Strecke: {start_name} -> {ziel_name}")
        print(f"Abfahrt: {ab_dt.strftime('%H:%M')} Uhr")
        print(f"Ankunft: {an_dt.strftime('%H:%M')} Uhr")
        print(f"Endpreis: {preis:.2f} €")
        print(f"Zeitstempel: {datetime.now().strftime('%d.%m.%Y %H:%M')}")


if __name__ == "__main__":
    app = FahrplanApp()
    app.starten()