from datetime import datetime, timedelta


class Route:
    def __init__(self):
        # Definition der Fahrzeiten zwischen den Stationen (in Minuten)
        self.strecke = [
            ('A', 'B', 2),
            ('B', 'C', 3),
            ('C', 'D', 1)
        ]

    def get_offset(self, ziel_name):
        """Berechnet die Gesamtfahrzeit von A bis zur Zielstation."""
        total_minuten = 0
        if ziel_name == 'A':
            return 0

        for start, ziel, dauer in self.strecke:
            total_minuten += dauer
            if ziel == ziel_name:
                return total_minuten
        return None


class FahrplanSystem:
    def __init__(self):
        self.route = Route()
        self.takt = 10
        # Startzeit des Betriebshofes in A
        self.betriebsstart = datetime.strptime("05:00", "%H:%M")
        self.betriebsende = datetime.strptime("23:00", "%H:%M")

    def finde_abfahrt(self):
        print("=== U-Bahn Fahrplanauskunft ===")

        # 1. Eingabe der Station
        station = input("Station (A, B, C, D): ").upper()
        if station == 'D':
            print("Station D ist Endstation. Keine Abfahrt möglich.")
            return

        # 2. Eingabe der Wunschzeit
        zeit_input = input("Gewünschte Abfahrtszeit (HH:MM): ")
        try:
            wunschzeit = datetime.strptime(zeit_input, "%H:%M")
        except ValueError:
            print("Ungültiges Zeitformat!")
            return

        # 3. Offset berechnen
        offset = self.route.get_offset(station)
        if offset is None:
            print("Station nicht gefunden.")
            return

        # 4. Erste Abfahrt an dieser speziellen Station berechnen
        erste_abfahrt_hier = self.betriebsstart + timedelta(minutes=offset)

        # 5. Nächste Taktzeit ermitteln
        # Wir prüfen, wie viele Minuten seit der allerersten Bahn an dieser Station vergangen sind
        if wunschzeit <= erste_abfahrt_hier:
            naechste_bahn = erste_abfahrt_hier
        else:
            differenz = (wunschzeit - erste_abfahrt_hier).total_seconds() / 60
            # Berechne, wie viele Takte (10 min) wir überspringen müssen
            verpasste_takte = int(differenz / self.takt)
            if differenz % self.takt > 0:
                verpasste_takte += 1

            naechste_bahn = erste_abfahrt_hier + timedelta(minutes=verpasste_takte * self.takt)

        # 6. Prüfung auf Betriebsschluss & Ausgabe
        if naechste_bahn > (self.betriebsende + timedelta(minutes=offset)):
            print("Leider fährt heute keine Bahn mehr.")
        else:
            wartezeit = int((naechste_bahn - wunschzeit).total_seconds() / 60)
            print(f"\nErgebnis für Station {station}:")
            print(f"Gewünschte Zeit: {wunschzeit.strftime('%H:%M')} Uhr")
            print(f"Nächste Abfahrt: {naechste_bahn.strftime('%H:%M')} Uhr")
            print(f"Wartezeit:      {wartezeit} Minute(n)")


if __name__ == "__main__":
    app = FahrplanSystem()
    app.finde_abfahrt()