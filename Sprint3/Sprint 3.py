import math
import os
from datetime import datetime, timedelta
from PIL import Image



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
        """Versucht das Bild netzplan.png zu öffnen."""
        try:
            img = Image.open("netzplan.png")
            img.show()
        except Exception:
            print("\n[Info] Netzplan.png konnte nicht automatisch geöffnet werden.")

    def bereinige_string(self, text):
        """User Story 3.1: Normalisierung (Umlaute, ß, Leerzeichen)."""
        text = text.lower().strip()
        replacements = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
                        "hauptbahnhof": "hbf", "bahnhof": "hbf", ".": ""}
        for alt, neu in replacements.items():
            text = text.replace(alt, neu)
        return text

    def finde_index(self, eingabe):
        """User Story 3.1: Findet Index via Nummer (1-23) oder Name."""
        clean_in = self.bereinige_string(eingabe)
        if clean_in.isdigit():
            idx = int(clean_in) - 1
            return idx if 0 <= idx < len(self.stationen_daten) else None

        for i, (name, _, _) in enumerate(self.stationen_daten):
            if clean_in in self.bereinige_string(name):
                return i
        return None

    def berechne_reise_details(self, start_idx, ziel_idx):
        """Berechnet Offset für Abfahrt und Fahrtdauer für Ankunft."""
        offset_sek = 0
        fahrt_dauer_sek = 0
        richtung = 1 if ziel_idx > start_idx else -1

        # Offset vom Linienstart bis zur Einstiegsstation
        if richtung == 1:
            for i in range(start_idx):
                offset_sek += (self.stationen_daten[i][1] * 60) + self.stationen_daten[i + 1][2]
        else:
            for i in range(len(self.stationen_daten) - 1, start_idx, -1):
                offset_sek += (self.stationen_daten[i - 1][1] * 60) + self.stationen_daten[i - 1][2]

        # Fahrtdauer zwischen den Stationen
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
    """User Story 3.2: Preislogik mit Zuschlägen und Rabatten."""

    @staticmethod
    def berechne(anzahl_stationen, ist_mehrfahrt, hat_sozial, ist_bar):
        # Basispreise
        if anzahl_stationen <= 3:
            basis = 1.50 if not ist_mehrfahrt else 5.00
        elif anzahl_stationen <= 8:
            basis = 2.00 if not ist_mehrfahrt else 7.00
        else:
            basis = 3.00 if not ist_mehrfahrt else 10.00

        preis = basis
        if not ist_mehrfahrt: preis *= 1.10  # Einzelticket-Zuschlag
        if hat_sozial:       preis *= 0.80  # Sozialrabatt
        if ist_bar:          preis *= 1.15  # Bar-Zuschlag
        return round(preis, 2)


class U1Service:
    def __init__(self):
        self.strecke = U1Strecke()
        self.takt_sek = 600  # 10 Minuten
        self.betrieb_start = datetime.strptime("05:00", "%H:%M")

    def zeige_stationen_liste(self):
        print("\nLINIE U1 - STATIONENÜBERSICHT:")
        print("-" * 45)
        for i in range(0, len(self.strecke.stationen_daten), 2):
            s1 = f"{i + 1:2}: {self.strecke.stationen_daten[i][0]}"
            s2 = ""
            if i + 1 < len(self.strecke.stationen_daten):
                s2 = f"{i + 2:2}: {self.strecke.stationen_daten[i + 1][0]}"
            print(f"{s1:<22} | {s2}")
        print("-" * 45)

    def hole_station(self, prompt):
        while True:
            val = input(prompt)
            idx = self.strecke.finde_index(val)
            if idx is not None: return idx
            print("Eingabe ungültig. Bitte Name oder Nummer (1-23) eingeben.")

    def hole_ja_nein(self, frage):
        while True:
            ans = input(frage + " (j/n): ").lower()
            if ans in ['j', 'ja']: return True
            if ans in ['n', 'nein']: return False

    def run(self):
        self.strecke.zeige_netzplan()
        self.zeige_stationen_liste()

        print("\n--- NEUE REISEPLANUNG ---")
        idx_s = self.hole_station("START: ")
        idx_z = self.hole_station("ZIEL:  ")

        while idx_s == idx_z:
            print("Start und Ziel dürfen nicht identisch sein.")
            idx_z = self.hole_station("ZIEL:  ")

        t_str = input("Wann sind Sie am Gleis? (HH:MM): ")
        try:
            wunsch = datetime.strptime(t_str, "%H:%M")
        except:
            wunsch = datetime.now()

        # Zeitlogik
        offset, dauer = self.strecke.berechne_reise_details(idx_s, idx_z)
        startzeit_linie = self.betrieb_start + timedelta(seconds=offset)

        if wunsch <= startzeit_linie:
            abfahrt = startzeit_linie
        else:
            diff = (wunsch - startzeit_linie).total_seconds()
            anzahl_takte = math.ceil(diff / self.takt_sek)
            abfahrt = startzeit_linie + timedelta(seconds=anzahl_takte * self.takt_sek)

        ankunft = abfahrt + timedelta(seconds=dauer)

        # Tariflogik
        print("\n--- TARIFINFORMATIONEN ---")
        ist_mf = self.hole_ja_nein("Mehrfahrtenkarte (4 Fahrten)?")
        ist_soz = self.hole_ja_nein("Anspruch auf Sozialrabatt?")
        ist_bar = self.hole_ja_nein("Zahlung in bar?")

        anzahl_stat = abs(idx_z - idx_s)
        preis = TarifRechner.berechne(anzahl_stat, ist_mf, ist_soz, ist_bar)

        # Zusammenfassung (User Story 3.3)
        print("\n" + "=" * 45)
        print("VAG REISEAUSKUNFT - TICKET-QUITTUNG")
        print("-" * 45)
        print(f"STRECKE:   {self.strecke.stationen_daten[idx_s][0]} -> {self.strecke.stationen_daten[idx_z][0]}")
        print(f"ABFAHRT:   {abfahrt.strftime('%H:%M')} Uhr")
        print(f"ANKUNFT:   {ankunft.strftime('%H:%M')} Uhr")
        print(f"DAUER:     {int(dauer / 60)} Min. ({anzahl_stat} Stationen)")
        print("-" * 45)
        print(f"TICKET:    {'Mehrfahrt' if ist_mf else 'Einzelfahrt'} (Tarifstufe: {anzahl_stat})")
        print(f"PREIS:     {preis:,.2f} €".replace(".", ","))
        print(f"DATUM:     {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print("=" * 45)


if __name__ == "__main__":
    U1Service().run()