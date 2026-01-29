from datetime import datetime, timedelta


class U1Strecke:
    """
    Modelliert die physikalische Strecke der U-Bahn Linie U1.

    Diese Klasse verwaltet die Namen der Stationen, die Fahrzeiten zwischen
    ihnen sowie die spezifischen Haltezeiten an jeder Station.
    """

    def __init__(self):
        """
        Initialisiert die Streckendaten der U1.

        Die Datenstruktur enthält: (Name, Minuten zum nächsten Halt, Haltezeit in Sek).
        """
        self.stationen_daten = [
            ("Langwasser Süd", 3, 60), ("Gemeinschaftshaus", 2, 30), ("Langwasser Mitte", 2, 30),
            ("Scharfreiterring", 3, 30), ("Langwasser Nord", 2, 30), ("Messe", 3, 30),
            ("Bauernfeindstraße", 2, 30), ("Hasenbuck", 2, 30), ("Frankenstraße", 2, 30),
            ("Maffeiplatz", 1, 30), ("Aufseßplatz", 2, 30), ("Hauptbahnhof", 2, 60),
            ("Lorenzkirche", 3, 30), ("Weißer Turm", 2, 30), ("Plärrer", 2, 60),
            ("Gostenhof", 1, 30), ("Bärenschanze", 2, 30), ("Maximilianstraße", 2, 30),
            ("Eberhardshof", 2, 30), ("Muggenhof", 3, 30), ("Stadtgrenze", 2, 30),
            ("Jakobinenstraße", 3, 30), ("Fürth Hbf.", 0, 60)
        ]

    def finde_index(self, eingabe: str):
        """
        Sucht den Index einer Station in der Liste.

        Parameters:
            eingabe (str): Der Name der Station oder die Nummer (1-23).

        Returns:
            int: Der Index der Station (0-22) oder None, falls nicht gefunden.
        """
        namen = [s[0].lower() for s in self.stationen_daten]
        eingabe = eingabe.strip().lower()

        if eingabe.isdigit():
            idx = int(eingabe) - 1
            if 0 <= idx < len(self.stationen_daten):
                return idx

        if eingabe in namen:
            return namen.index(eingabe)

        for i, name in enumerate(namen):
            if eingabe in name:
                return i
        return None

    def berechne_offset_sekunden(self, ziel_idx: int) -> int:
        """
        Berechnet die Zeitdauer vom Linienstart bis zur gewünschten Station.

        Parameters:
            ziel_idx (int): Der Index der Zielstation.

        Returns:
            int: Gesamtdauer in Sekunden (Fahrzeit + Haltezeiten).
        """
        sekunden = 0
        for i in range(ziel_idx):
            sekunden += (self.stationen_daten[i][1] * 60) + self.stationen_daten[i + 1][2]
        return sekunden


class U1Service:
    """
    Stellt die Logik für die Fahrplanauskunft bereit.

    Berechnet basierend auf dem 10-Minuten-Takt die nächste Abfahrtzeit
    an einer gewählten Station.
    """

    def __init__(self):
        """Initialisiert den Service mit Takt und Betriebszeiten."""
        self.strecke = U1Strecke()
        self.takt_min = 10
        self.betrieb_start = datetime.strptime("05:00", "%H:%M")

    def abfrage(self):
        """
        Startet den interaktiven Dialog zur Fahrplanabfrage.

        Fragt Start, Ziel und Zeit ab und gibt die nächste Abfahrt aus.
        """
        print("\n--- U1 Fahrplanauskunft ---")

        s_raw = input("\nStart-Haltestelle: ").strip()
        idx_s = self.strecke.finde_index(s_raw)

        if idx_s is None:
            print(f"Fehler: Station '{s_raw.title()}' nicht gefunden.")
            return

        z_raw = input("Ziel-Haltestelle: ").strip()
        idx_z = self.strecke.finde_index(z_raw)

        if idx_z is None:
            print(f"Fehler: Zielstation '{z_raw.title()}' nicht gefunden.")
            return

        t_in = input("Wann bist du am Gleis? (HH:MM): ")
        try:
            wunschzeit = datetime.strptime(t_in, "%H:%M")
        except ValueError:
            print("Fehler: Ungültiges Zeitformat (HH:MM nutzen).")
            return

        # Zeitberechnung
        offset_sek = self.strecke.berechne_offset_sekunden(idx_s)
        erste_abfahrt_hier = self.betrieb_start + timedelta(seconds=offset_sek)

        if wunschzeit <= erste_abfahrt_hier:
            naechste = erste_abfahrt_hier
        else:
            diff_sek = (wunschzeit - erste_abfahrt_hier).total_seconds()
            takte = int(diff_sek / (self.takt_min * 60))
            if diff_sek % (self.takt_min * 60) > 0:
                takte += 1
            naechste = erste_abfahrt_hier + timedelta(minutes=takte * self.takt_min)

        wartezeit = int((naechste - wunschzeit).total_seconds() / 60)

        print(f"\n--- Ergebnis für {self.strecke.stationen_daten[idx_s][0]} ---")
        print(f"Nächste Abfahrt: {naechste.strftime('%H:%M')} Uhr")
        print(f"Wartezeit:      {wartezeit} Minute(n)")


if __name__ == "__main__":
    app = U1Service()
    # Du kannst jetzt help(app.abfrage) oder help(app.strecke.finde_index) nutzen!
    app.abfrage()