# Sprint 2: Linie U1 (Erweiterte Modellierung)
 
### Kurzfassung
 
Wir erweitern das System auf die reale **Linie U1**. 
Im Fokus stehen die Implementierung von **Hin- und Rückfahrt** sowie **variabler Haltezeiten**.
 
### User-Story 2.1: Fahrgast
 
"Als Fahrgast benötige ich Zeit zum Ein- und Aussteigen, deshalb muss die Bahn ein wenig an jeder Station verweilen."

### User-Story 2.2: Fahrgast

"Ich möchte nicht nur in eine Richtung fahren können, sondern auch zurück."
 
 
### User-Story 2.3: Verkehrsbetrieb (Kunde)
 
"Mit Blick auf die reale Anwendung möchten wir die Logik der Teststrecke auf die Struktur der Linie U1 übertragen."
 
 
---

## Technische Spezifikation "U1"
 
### 1. Die Strecke 

* **Datenquelle:** Die Datei Netzplan U1 im Sprintordner enthält die Stationen und die jeweiligen Fahrtzeiten.
 
* **Haltezeiten:**
 
 * Standard: **30 Sekunden**.
 * Hauptknoten (**Plärrer, Hauptbahnhof**): **60 Sekunden**.
 * Endhaltestellen (**Langwasser Süd, Fürth Hbf.**): **60 Sekunden**.
 
### 2. Betrieb & Takt
 
* **Umlauf:** Ein Zug fährt bis zur Endstation, wendet nach der dortigen Haltezeit (60 Sek.) und fährt in die Gegenrichtung zurück. 
* **Zeitrahmen:** 
  Erste Abfahrt (Langwasser Süd): 05:00 Uhr
  Letzte Abfahrt (Langwasser Süd): 23:00 Uhr
* **Taktintervall:** Alle **10 Minuten** startet ein neuer Zug in Langwasser Süd.
 
## Abnahmekriterien für das Inkrement (Code)
 
1. **Datenstruktur:** Statt der Test-Strecke gibt der Code Fahrgastinformationen zu der Linie U1.
 
2. **Eingabe:** Das System verarbeitet nun drei Parameter:
 
  * Start-Haltestelle
  * Ziel-Haltestelle (bestimmt die Fahrtrichtung)
  * Früheste gewünschte Abfahrtszeit
 
3. **Verarbeitung:**
 
  * Berechnung der Ankunfts- und Abfahrtszeiten erfolgt unter **striktem Einbezug der Haltezeiten**.
  * Es können Informationen zu Fahrten in beide Richtungen abgefragt werden.
 
1. **Ausgabe:** Anzeige der nächsten tatsächlichen Abfahrtszeit.
 
  * Genauigkeit: Auf die Minute gerundet.

## Illustration U-Bahn Takt

Siehe U-1 Abfahrten und Ankünfte.jpg

## Beispiel zur Berechnung der Ankunftszeit
 
Ein Fahrgast möchte von **Langwasser Mitte** zur **Messe** und ist um **05:01 Uhr** am Bahnsteig.
 
* **Zugstart (Langwasser Süd):** 05:00:00
* **Fahrt bis Gemeinschaftshaus:** +3 Min (Ankunft 05:03:00)
* **Halt Gemeinschaftshaus:** +30 Sek (Abfahrt 05:03:30)
* **Fahrt bis Langwasser Mitte:** +2 Min (Ankunft 05:05:30)
* **Halt Langwasser Mitte:** +30 Sek (Abfahrt **05:06:00**)
* **Ergebnis:** Das System hat **05:06 Uhr** als Abfahrtszeit berechnet.

