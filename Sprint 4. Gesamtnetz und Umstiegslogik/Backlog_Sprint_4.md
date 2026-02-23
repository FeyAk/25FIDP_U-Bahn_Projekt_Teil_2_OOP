# Sprint 4 Backlog

---
> ## HINWEIS bis Mittwoch, 25.02., bitte erstmal auf Implementierung des Netzplans und Umstiegslogik konzentrieren!
---

## Zusammenfassung
Der wesentliche Schwerpunkt im Sprint ist die Implementierung der Logik für den Umstieg. Ein zweiter Schwerpunkt ist die Erstellung eines Adapters.

---

## User Story 4.1: Verkehrsbetrieb (Kunde)
**„Die Fahrkartenautomaten arbeiten korrekt für U1. Nun soll das gesamte Netz einbezogen werden.“**

### Abnahmekriterien US 4.1:
* **4.1.1** Alle Stationen der Linien U1, U2 und U3 sind vollständig im System hinterlegt.
* **4.1.2** Die Datenstruktur (Graph) bildet alle Linienverläufe des Gesamtnetzes ab.
* **4.1.3** Die Streckenberechnung liefert korrekte Ergebnisse für Start- und Zielpunkte auf unterschiedlichen Linien.

> Eine Liste mit allen Haltestellen ist in der Datei Netzplan zu finden.

---

## User Story 4.2: Fahrgast
**„Da mein Ziel auf einer anderen Linie liegt, muss ich umsteigen. Ich möchte sicher sein, dass ich genug Zeit habe, meinen Anschlusszug zu erreichen.“**

### Abnahmekriterien US 4.2:
* **4.2.1** Das System identifiziert gültige Umstiegsstationen (Knotenpunkte) zwischen den Linien.
* **4.2.2** Die Umstiegslogik berücksichtigt eine definierte Mindestumstiegszeit (Puffer) zwischen Ankunft und Abfahrt.
* **4.2.3** Bei der Routenausgabe werden die Abfahrtszeiten der Anschlusszüge an den Knotenpunkten korrekt angezeigt.

> Die Abfahrten erfolgen bei Linien U2 und U3 wie bei U1: Um 5 Uhr fährt die erste Bahn von der Heimhaltestelle der Linie ab. Bis 23 Uhr fährt alle 10 Minuten eine Bahn bis zur Endhaltestelle und dann wieder zurück zur Heimhaltestelle. Die letzte Abfahrt an der Heimhaltestelle erfolgt um 23 Uhr.
> 
> Heimhaltestellen:
> U2: Röthenbach
> U3: Gustav-Adolf-Str.

---

## User Story 4.3: Fahrgast
**„Ich möchte möglichst schnell ans Ziel kommen. Wenn ich dadurch nicht früher ankomme, bleibe ich lieber sitzen, statt umzusteigen. Der Automat soll mir nur dann einen Umstieg empfehlen, wenn dieser sinnvoll ist.“**

### Abnahmekriterien US 4.3:
* **4.3.1** Der Suchalgorithmus bevorzugt bei zeitlich gleichwertigen Verbindungen die Route mit der geringsten Anzahl an Umstiegen.
* **4.3.2** Die Gesamtfahrzeit wird inklusive der realen Aufenthaltszeiten an den Umstiegsstationen berechnet und ausgegeben.

---

## User Story 4.4: Verkehrsbetrieb (Kunde)
**„Als Verkehrsbetrieb (Kunde) wünschen wir uns, dass bei der Eingabe der Uhrzeit keine Gedanken zu Trennzeichen oder führenden Nullen notwendig sind.“**

### Abnahmekriterien US 4.4:
* **4.4.1** Das System akzeptiert verschiedene Trennzeichen (Doppelpunkt, Punkt, Komma, Leerzeichen) sowie Eingaben ohne Trenner.
* **4.4.2** Einstellige Stunden- oder Minutenangaben werden automatisch mit führenden Nullen vervollständigt (z. B. „9“ zu „09:00“).
* **4.4.3** Kurzeingaben (nur Stunden) werden als volle Stunde interpretiert.
* **4.4.4** Das System validiert die Eingabe auf logische Korrektheit (00:00 bis 23:59) und gibt bei Fehlern einen Hinweis aus.
* **4.4.5** Nach der Eingabe wird der Wert im UI einheitlich im Format HH:mm dargestellt.

---

## User Story 4.5: Verkehrsbetrieb (Kunde)
**„Um eine gleichbleibend hohe Softwarequalität sicherzustellen, möchte der Verkehrsbetrieb (Kunde), dass alle Modullösungen über eine Schnittstelle (Adapter) geprüft werden. Dadurch soll die automatisierte Abnahme effizient, standardisiert und vergleichbar erfolgen.“**

### Abnahmekriterien US 4.5:
* **4.5.1** Für den Code ist ein Adapter nach dem vorgegebenen Muster implementiert.
* **4.5.2** Der Adapter übersetzt die spezifischen internen Datenstrukturen der Gruppe in das standardisierte Format des zentralen Testskripts.
* **4.5.3** Das Testskript kann alle automatisierten Testfälle (z. B. aus US 4.1 bis 4.4) ohne manuelle Anpassungen am Gruppen-Code ausführen.
* **4.5.4** Der Adapter fängt Inkompatibilitäten ab und liefert im Fehlerfall standardisierte Rückmeldungen an die Testumgebung.

## 4.6 Technische Voraussetzung für das automatische Testen: Codestruktur

Damit der automatisierte Test funktioniert, muss der Gruppencode strikt zwischen **Logik** (Berechnung) und **Interaktion** (Eingabe) trennen.

### 4.6.1 Aufbau der Logik-Datei (z. B. `berechnung.py`)
Die Logik darf keine `input()`-Befehle enthalten. Alle benötigten Werte müssen als **Parameter** entgegengenommen werden.

```python
# LOGIK-TEIL (Wird vom Adapter aufgerufen)
def berechne_fahrt(start_haltestelle, ziel_haltestelle, startzeit):
    # Hier findet die Berechnung statt
    # Die Variablen sind hier durch die Parameter definiert
    ergebnis = ... 
    return ergebnis

# MANUELLER TEST-TEIL (Wird beim direkten Starten ausgeführt)
if __name__ == "__main__":
    # **Nur hier ist input() erlaubt!**
    s = input("Start: ")
    z = input("Ziel: ")
    t = input("Zeit: ")
    
    # Aufruf der Logik mit den manuellen Eingaben
    print(berechne_fahrt(s, z, t))
```

### 4.6.2 Funktionsweise des Adapters
Der Adapter importiert eure Logik-Datei. Da der input()-Teil unter if __name__ == "__main__" steht, wird er beim Import ignoriert. Das Testskript bleibt nicht hängen.

```
Python
# So greift der Adapter auf euren Code zu:

from . import berechnung

class adapter_klasse:
    def ausfuehren_testfall(self, eingabe_start, ...):
        # Der Adapter übergibt die Testwerte direkt an eure Funktion
        ergebnis = berechnung.berechne_fahrt(eingabe_start, ...)
        return {"preis_endbetrag": ergebnis, ...}
```

## 4.7 Spezifikation Adapter-Schnittstelle

### 4.7.1 Eingabe-Parameter (Input)
| Variable | Datentyp (Python) | Beschreibung |
| :--- | :--- | :--- |
| `eingabe_start` | `str` | Name der Start-Haltestelle (exakt laut Netzplan) |
| `eingabe_ziel` | `str` | Name der Ziel-Haltestelle (exakt laut Netzplan) |
| `eingabe_startzeit` | `str` | Die vom Nutzer eingegebene Zeit (flexibles Format) |
| `eingabe_einzelfahrkarte`| `bool` | `True` für Einzelkarte, `False` für Mehrfahrtenkarte |
| `eingabe_sozialrabatt` | `bool` | `True`, wenn Rabattberechtigung vorliegt |
| `eingabe_barzahlung` | `bool` | `True` bei Barzahlung, `False` bei Kartenzahlung |

### 5.7.2 Ausgabe-Werte (Output)
| Variable | Datentyp (Python) | Format / Struktur |
| :--- | :--- | :--- |
| `fehler` | `bool` | `True`, wenn Eingabe ungültig oder keine Route gefunden |
| `ausgabe_startzeit_fahrgast`| `datetime.time` | HH:MM (Sekunden genullt) |
| `ausgabe_zielzeit_fahrgast` | `datetime.time` | HH:MM (aufgerundet laut Vorgabe) |
| `ausgabe_startzeit_algo` | `datetime.time` | HH:MM:SS (Präzise Zeit für Berechnung) |
| `ausgabe_zielzeit_algo` | `datetime.time` | HH:MM:SS (Präzise Zeit für Berechnung) |
| `bahnlinien_gesamtfahrt` | `List[str]` | `["U1", "U2"]` |
| `route` | `Dict[str, List]` | `{"Name": [Linie, An_HHMMSS, Ab_HHMMSS], ...}` |
| `umstieg_haltestellen` | `List[str]` | `["Hauptbahnhof", "Plärrer"]` |
| `umstiege_exakt` | `Dict[str, List]` | `{"Name": [time_ankunft, time_abfahrt], ...}` |
| `umstiege_fahrgast` | `Dict[str, List]` | `{"Name": [time_ankunft, time_abfahrt], ...}` |
| `umstieg_bahnlinien` | `List[str]` | Die Linien, auf die gewechselt wird |
| `dauer_gesamtfahrt` | `timedelta` | Zeitdifferenz (Python-Typ für Zeitspannen) |
| `preis_endbetrag` | `float` | Finaler Ticketpreis (z.B. `1.65`) |

### 4.7.3 Struktur der Adapter-Datei
Erstellt in einem Modul `adapter.py` eine Klasse namens `adapter_klasse`. Diese Klasse muss eine zentrale Methode besitzen, die vom Testskript aufgerufen wird. Das Grundgerüst sieht wie folgt aus:

```python
from datetime import time, timedelta
from typing import List, Dict, Union

# Hier eure eigenen Module importieren, z.B.:
# from mein_projekt import u_bahn_logik

class adapter_klasse:
    def __init__(self):
        """Initialisierung eurer Logik-Klasse"""
        # self.logik = u_bahn_logik()
        pass

    def ausfuehren_testfall(self, 
                           eingabe_start: str, 
                           eingabe_ziel: str, 
                           eingabe_startzeit: str, 
                           eingabe_einzelfahrkarte: bool, 
                           eingabe_sozialrabatt: bool, 
                           eingabe_barzahlung: bool) -> dict:
        """
        Übersetzt die Testskript-Eingaben für euren Code und 
        liefert die Ergebnisse im Zielformat zurück.
        """
        
        # INTERNE VERARBEITUNG:
        # Hier ruft ihr eure Funktionen auf und wandelt die Eingaben um.
        
        # RÜCKGABE:
        # Das Dictionary muss exakt die Keys aus der Spezifikation enthalten.
        return {
            "fehler": False,
            "ausgabe_startzeit_fahrgast": time(0, 0),
            "ausgabe_zielzeit_fahrgast": time(0, 0),
            "ausgabe_startzeit_algo": time(0, 0, 0),
            "ausgabe_zielzeit_algo": time(0, 0, 0),
            "bahnlinien_gesamtfahrt": [],
            "route": {},
            "umstieg_haltestellen": [],
            "umstiege_exakt": {},
            "umstiege_fahrgast": {},
            "umstieg_bahnlinien": [],
            "dauer_gesamtfahrt": timedelta(0),
            "preis_endbetrag": 0.0
        }
```
### 4.7.4 Wichtige Implementierungshinweise

* **Schnittstellentreue:** Die Namen der Variablen (Keys) im zurückgegebenen Dictionary müssen exakt so geschrieben werden wie in der Spezifikation oben. Ein Tippfehler führt zum Scheitern des automatisierten Tests.
* **Zeitformate:**
    * Verwendet für Uhrzeiten den Datentyp `datetime.time`.
    * Verwendet für die `dauer_gesamtfahrt` den Datentyp `datetime.timedelta`.
    * Achtet bei der `ausgabe_zielzeit_fahrgast` auf die Rundungsregeln (aufgerundet auf die volle Minute).
* **Daten-Mapping:** Eure interne Verarbeitung muss in der Lage sein, die String-Eingabe der Haltestellen (z. B. "Langwasser Süd") auf eure interne Datenbank-Struktur abzubilden.
* **Fehlerbehandlung:** Wenn eine Route nicht gefunden werden kann oder die Eingaben ungültig sind, darf der Adapter nicht abstürzen. Setzt in diesem Fall `fehler = True` und füllt die restlichen Felder mit Standardwerten (0 oder leere Listen).

