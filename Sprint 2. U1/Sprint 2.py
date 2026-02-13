import math
from datetime import datetime, timedelta
from PIL import Image



class U1Strecke:
    def __init__(self):
        # Struktur: (Name, Fahrzeit zur NÄCHSTEN Station in Min, Haltezeit an DIESER Station in Sek)
        # Hinweis: Die Fahrzeit bezieht sich immer auf das Segment NACH der Station.
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

    def zeige_netzplan(self):
        """Versucht die Datei netzplan.png zu öffnen."""
        try:
            img = Image.open("netzplan.png")
            img.show()
        except FileNotFoundError:
            print("\n[Hinweis] Datei 'netzplan.png' nicht gefunden. Bitte Bild in den Ordner legen.")
        except Exception as e:
            print(f"\n[Hinweis] Bild konnte nicht geöffnet werden: {e}")

    def finde_index(self, eingabe):
        """Findet den Index der Station via Name (Teilübereinstimmung) oder Nummer."""
        namen = [s[0].lower() for s in self.stationen_daten]
        eingabe = eingabe.strip().lower()

        if eingabe.isdigit():
            idx = int(eingabe) - 1
            return idx if 0 <= idx < len(self.stationen_daten) else None

        for i, name in enumerate(namen):
            if eingabe in name:
                return i
        return None

    def berechne_offset_sekunden(self, start_idx, ziel_idx):
        """
        Berechnet die Zeitdifferenz vom Startbahnhof der Linie (Depot)
        bis zur gewünschten Einstiegsstation.
        """
        sekunden = 0
        # Richtung bestimmen: 1 = Richtung Fürth, -1 = Richtung Langwasser
        richtung = 1 if ziel_idx > start_idx else -1

        if richtung == 1:
            # Hinfahrt: Wir starten bei Index 0 (Langwasser Süd)
            for i in range(start_idx):
                # Fahrzeit von i zu i+1 + Haltezeit an i+1
                sekunden += (self.stationen_daten[i][1] * 60) + self.stationen_daten[i + 1][2]
        else:
            # Rückfahrt: Wir starten am Ende (Fürth Hbf, Index 22)
            for i in range(len(self.stationen_daten) - 1, start_idx, -1):
                # Fahrzeit von i zu i-1 + Haltezeit an i-1
                sekunden += (self.stationen_daten[i - 1][1] * 60) + self.stationen_daten[i - 1][2]

        return sekunden


class U1Service:
    def __init__(self):
        self.strecke = U1Strecke()
        self.takt_sek = 10 * 60  # 10 Minuten Takt
        self.betrieb_start = datetime.strptime("05:00", "%H:%M")
        self.betrieb_ende = datetime.strptime("23:00", "%H:%M")

    def run(self):
        self.strecke.zeige_netzplan()
        print("\n" + "=" * 30)
        print("VAG LINIE U1 - SPRINT 2")
        print("=" * 30)

        s_in = input("Start-Station (Name oder 1-23): ")
        z_in = input("Ziel-Station  (Name oder 1-23): ")
        t_in = input("Früheste Abfahrt (HH:MM): ")

        idx_s = self.strecke.finde_index(s_in)
        idx_z = self.strecke.finde_index(z_in)

        if idx_s is None or idx_z is None or idx_s == idx_z:
            print("\nFehler: Ungültige Stationen eingegeben.")
            return

        try:
            wunschzeit = datetime.strptime(t_in, "%H:%M")
        except ValueError:
            print("\nFehler: Falsches Zeitformat. Bitte HH:MM nutzen.")
            return

        # Berechnung
        offset_sek = self.strecke.berechne_offset_sekunden(idx_s, idx_z)
        erste_abfahrt_hier = self.betrieb_start + timedelta(seconds=offset_sek)

        # Naechsten Takt finden
        if wunschzeit <= erste_abfahrt_hier:
            naechste_abfahrt = erste_abfahrt_hier
        else:
            vergangene_sek = (wunschzeit - erste_abfahrt_hier).total_seconds()
            anzahl_takte = math.ceil(vergangene_sek / self.takt_sek)
            naechste_abfahrt = erste_abfahrt_hier + timedelta(seconds=anzahl_takte * self.takt_sek)

        # Prüfung auf Betriebsende
        if naechste_abfahrt > self.betrieb_ende + timedelta(seconds=offset_sek):
            print("\nLeider keine Fahrten mehr für heute.")
        else:
            wartezeit = int((naechste_abfahrt - wunschzeit).total_seconds() / 60)
            richtung_name = self.strecke.stationen_daten[idx_z][0]

            print("\n" + "-" * 30)
            print(f"FAHRPLANAUSKUNFT")
            print(f"Richtung:      {richtung_name}")
            print(f"Abfahrt an:    {self.strecke.stationen_daten[idx_s][0]}")
            print(f"Uhrzeit:       {naechste_abfahrt.strftime('%H:%M')} Uhr")
            print(f"Wartezeit:     ~ {wartezeit} Min.")
            print("-" * 30)


if __name__ == "__main__":
    service = U1Service()
    service.run()
