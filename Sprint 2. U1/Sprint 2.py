from datetime import datetime, timedelta


class U1Strecke:
    def __init__(self):
        # Name, Fahrzeit zur nächsten Station (min), Haltezeit an dieser Station (sek)
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

    def finde_index(self, eingabe):
        """Findet den Index der Station via Name oder Nummer."""
        namen = [s[0].lower() for s in self.stationen_daten]
        eingabe = eingabe.strip().lower()

        # Versuch 1: Ist es eine Nummer? (1-basiert für User)
        if eingabe.isdigit():
            idx = int(eingabe) - 1
            if 0 <= idx < len(self.stationen_daten):
                return idx

        # Versuch 2: Ist es der Name?
        if eingabe in namen:
            return namen.index(eingabe)

        # Versuch 3: Teilweise Übereinstimmung (z.B. "Fürth" findet "Fürth Hbf.")
        for i, name in enumerate(namen):
            if eingabe in name:
                return i
        return None

    def berechne_offset_sekunden(self, ziel_idx):
        """Berechnet Zeit von der ersten Station bis zur Start-Station."""
        sekunden = 0
        for i in range(ziel_idx):
            # Fahrzeit zur nächsten + Haltezeit an der nächsten
            sekunden += (self.stationen_daten[i][1] * 60) + self.stationen_daten[i + 1][2]
        return sekunden


class U1Service:
    def __init__(self):
        self.strecke = U1Strecke()
        self.takt_min = 10
        self.betrieb_start = datetime.strptime("05:00", "%H:%M")
        self.betrieb_ende = datetime.strptime("23:00", "%H:%M")

    def abfrage(self):
        print("\n--- U1 Fahrplanauskunft ---")
        print("Gib den Namen oder die Nummer (1-23) ein.")

        s_in = input("Start-Station: ")
        z_in = input("Ziel-Station: ")
        t_in = input("Wann bist du am Gleis? (HH:MM): ")

        idx_s = self.strecke.finde_index(s_in)
        idx_z = self.strecke.finde_index(z_in)

        try:
            wunschzeit = datetime.strptime(t_in, "%H:%M")
            if idx_s is None or idx_z is None:
                raise ValueError("Station nicht gefunden")
        except ValueError as e:
            print(f"Fehler: {e}")
            return

        # Logik: Zeit von Langwasser Süd bis zur Start-Station
        offset_sek = self.strecke.berechne_offset_sekunden(idx_s)

        # Abfahrt des allerersten Zuges an DEINER Station
        erste_abfahrt_hier = self.betrieb_start + timedelta(seconds=offset_sek)

        # Nächsten Takt berechnen
        if wunschzeit <= erste_abfahrt_hier:
            naechste = erste_abfahrt_hier
        else:
            diff_sek = (wunschzeit - erste_abfahrt_hier).total_seconds()
            takte_zu_addieren = int(diff_sek / (self.takt_min * 60))
            if diff_sek % (self.takt_min * 60) > 0:
                takte_zu_addieren += 1
            naechste = erste_abfahrt_hier + timedelta(minutes=takte_zu_addieren * self.takt_min)

        print(f"\n--- Ergebnis für {self.strecke.stationen_daten[idx_s][0]} ---")
        print(f"Nächste Abfahrt: {naechste.strftime('%H:%M')} Uhr")
        print(f"Wartezeit:      {int((naechste - wunschzeit).total_seconds() / 60)} Min.")


if __name__ == "__main__":
    U1Service().abfrage()