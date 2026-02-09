import math
import re
from datetime import datetime, timedelta
from PIL import Image  # Wichtig für das Pop-up


class U1Strecke:
    def __init__(self):
        # Struktur: (Name, Fahrzeit zur NÄCHSTEN Station in Min, Haltezeit an DIESER Station in Sek)
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
        """Öffnet die Datei netzplan.png im Standard-Bildbetrachter."""
        try:
            img = Image.open("netzplan.png")
            img.show()
        except FileNotFoundError:
            print("\n[System-Info] Netzplan.png nicht gefunden. Fahre ohne Bild fort...")

    def bereinige_string(self, text):
        """User Story 3.1: Normalisierung von Umlauten und Abkürzungen."""
        text = text.lower().strip()
        replacements = {
            "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
            "hauptbahnhof": "hbf", "bahnhof": "hbf", ".": ""
        }
        for alt, neu in replacements.items():
            text = text.replace(alt, neu)
        return text

    def finde_index(self, eingabe):
        """User Story 3.1: Findet Station trotz kleiner Tippfehler oder Abkürzungen."""
        eingabe_clean = self.bereinige_string(eingabe)
        if eingabe_clean.isdigit():
            idx = int(eingabe_clean) - 1
            return idx if 0 <= idx < len(self.stationen_daten) else None

        for i, (name, _, _) in enumerate(self.stationen_daten):
            if eingabe_clean in self.bereinige_string(name):
                return i
        return None

    def berechne_reise(self, start_idx, ziel_idx):
        """Berechnet Offset für Abfahrt und Gesamtfahrtdauer für Ankunft."""
        offset_sek = 0
        fahrt_dauer_sek = 0
        richtung = 1 if ziel_idx > start_idx else -1

        # Offset vom Linienstart (Langwasser oder Fürth) bis zur Einstiegsstation
        if richtung == 1:
            for i in range(start_idx):
                offset_sek += (self.stationen_daten[i][1] * 60) + self.stationen_daten[i + 1][2]
        else:
            for i in range(len(self.stationen_daten) - 1, start_idx, -1):
                offset_sek += (self.stationen_daten[i - 1][1] * 60) + self.stationen_daten[i - 1][2]

        # Fahrtdauer zwischen Start und Ziel
        temp_idx = start_idx
        while temp_idx != ziel_idx:
            if richtung == 1:
                fahrt_dauer_sek += (self.stationen_daten[temp_idx][1] * 60) + self.stationen_daten[temp_idx + 1][2]
                temp_idx += 1
            else:
                fahrt_dauer_sek += (self.stationen_daten[temp_idx - 1][1] * 60) + self.stationen_daten[temp_idx - 1][2]
                temp_idx -= 1
        return offset_sek, fahrt_dauer_sek


class TarifRechner:
    """User Story 3.2: Preislogik basierend auf Stationen und Konditionen."""

    @staticmethod
    def berechne_preis(stationen, mehrfahrt, sozial, bar):
        # Basispreis-Ermittlung
        if stationen <= 3:
            basis = 1.50 if not mehrfahrt else 5.00
        elif stationen <= 8:
            basis = 2.00 if not mehrfahrt else 7.00
        else:
            basis = 3.00 if not mehrfahrt else 10.00

        preis = basis
        if not mehrfahrt: preis *= 1.10  # Einzelticket-Zuschlag
        if sozial: preis *= 0.80  # Sozialrabatt
        if bar: preis *= 1.15  # Bar-Zuschlag
        return round(preis, 2)


class U1Service:
    def __init__(self):
        self.strecke = U1Strecke()
        self.takt_sek = 10 * 60
        self.betrieb_start = datetime.strptime("05:00", "%H:%M")

    def hole_eingabe(self, prompt):
        while True:
            val = input(prompt)
            idx = self.strecke.finde_index(val)
            if idx is not None: return idx
            print("Station unbekannt. Bitte erneut eingeben (z.B. 'Hbf' oder '12').")

    def hole_boolean(self, frage):
        while True:
            ans = input(frage + " (j/n): ").lower()
            if ans in ['j', 'ja']: return True
            if ans in ['n', 'nein']: return False

    def run(self):
        # POP-UP beim Start
        self.strecke.zeige_netzplan()

        print("\n--- VAG U1 FAHRPLAN & TICKETS ---")
        idx_s = self.hole_eingabe("Start-Station: ")
        idx_z = self.hole_eingabe("Ziel-Station:  ")

        t_str = input("Wann sind Sie am Gleis? (HH:MM): ")
        try:
            wunschzeit = datetime.strptime(t_str, "%H:%M")
        except:
            wunschzeit = datetime.now()

        # Zeitberechnung
        offset, dauer = self.strecke.berechne_reise(idx_s, idx_z)
        erste_ab = self.betrieb_start + timedelta(seconds=offset)

        if wunschzeit <= erste_ab:
            abfahrt = erste_ab
        else:
            wait = math.ceil((wunschzeit - erste_ab).total_seconds() / self.takt_sek)
            abfahrt = erste_ab + timedelta(seconds=wait * self.takt_sek)

        ankunft = abfahrt + timedelta(seconds=dauer)

        # Tarifberechnung
        ist_mf = self.hole_boolean("Mehrfahrtenkarte?")
        ist_soz = self.hole_boolean("Sozialrabatt?")
        ist_bar = self.hole_boolean("Barzahlung?")

        stationen = abs(idx_z - idx_s)
        preis = TarifRechner.berechne_preis(stationen, ist_mf, ist_soz, ist_bar)

        # Ausgabe
        print("\n" + "=" * 35)
        print(f"IHR REISEPLAN")
        print("-" * 35)
        print(f"VON:      {self.strecke.stationen_daten[idx_s][0]}")
        print(f"NACH:     {self.strecke.stationen_daten[idx_z][0]}")
        print(f"ABFAHRT:  {abfahrt.strftime('%H:%M')} Uhr")
        print(f"ANKUNFT:  {ankunft.strftime('%H:%M')} Uhr")
        print(f"PREIS:    {preis:,.2f} €".replace(".", ","))
        print(f"STATUS:   Gültig am {datetime.now().strftime('%d.%m.%Y')}")
        print("=" * 35)


if __name__ == "__main__":
    U1Service().run()