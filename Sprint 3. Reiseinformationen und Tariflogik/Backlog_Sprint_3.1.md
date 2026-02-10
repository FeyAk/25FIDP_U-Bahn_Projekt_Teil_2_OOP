# Sprint 3: Reiseinformationen und Tariflogik

### Kurzfassung

Ziel dieses Sprints ist die fachliche Vervollständigung der Reiseauskunft. Der Fahrgast erhält nun präzise Informationen über die Ankunftszeit und die individuellen Fahrtkosten. Zudem wird das System gegenüber fehlerhaften Benutzereingaben abgesichert.

## User Stories und fachliche Spezifikationen

### User Story 3.1: Verkehrsbetrieb
**„Wenn der Benutzer eine falsche Eingabe macht, darf das Programm nicht abstürzen. Kleine Abweichungen bei der Eingabe sollen möglich sein und die Ausgabe der gewünschten Information nicht behindern.“**

* **Normalisierungs-Pflicht:** Das System muss die Eingabe vor dem Vergleich händisch vorverarbeiten:
    * Entfernen von führenden/folgenden Leerzeichen.
    * Umwandlung in Kleinschreibung.
    * Vereinheitlichung von Sonderzeichen (Bindestriche zu Leerzeichen).
    * Ersetzung von Umlauten (ä -> ae, etc.) und ß (-> ss).
* **Ersetzung von Kürzeln (Mapping):** Das System muss vordefinierte Abkürzungen in der Benutzereingabe erkennen und durch die entsprechenden Vollwörter aus der Haltestellenliste ersetzen (z. B. wird aus "Hbf." automatisch "Hauptbahnhof", aus "Str." wird "Straße" und aus "Fr.-" wird "Friedrich-"). Hierbei muss darauf geachtet werden, dass die Eindeutigkeit erhalten bleibt - siehe dazu Testfälle und Anmerkungen unten in diesem Dokument.
* **Fuzzy-Matching:** Nach der Normalisierung muss das System eine Übereinstimmung von mindestens 80 % zum Datenbestand erkennen.
* **Fehlerbehandlung:** Bei nicht eindeutigen Eingaben muss eine freundliche Fehlermeldung ausgegeben und die Eingabe wiederholt werden.

### User Story 3.2: Verkehrsbetrieb
**„Als Verkehrsplaner möchten wir ein Rabattsystem implementieren, das unserem Selbstverständnis als sozialem Unternehmen gerecht wird. Außerdem möchten wir Anreize für bargeldloses Zahlen schaffen und die Kundenbindung durch Mehrfachkarten erhöhen.“**

> **Hinweis:** Preis- und Rabattmodelle entsprichen den Spezifikationen aus Teil 1 des U-Bahn-Projektes (S5-01 bis S5-04 im Dokument SPRINT5_BACKLOG.md). In Teil 1 des Projektes erstellter Code kann also als Vorlage für die Implementierung in diesem Sprint in OOP dienen.

* **(Ticket-Kategorisierung):** Die Wahl des Tickets richtet sich nach der Anzahl der Stationen:
    * **Kurzticket:** 1 bis 3 Stationen.
    * **Mittelticket:** 1 bis 8 Stationen.
    * **Langticket:** beliebig viele Stationen.
* **(Ticket-Art):** Der Fahrgast kann zwischen Einzeltickets und Mehrfahrtentickets (4 Fahrten) wählen.
* **(Preisfindung):** Die Berechnung erfolgt auf Basis der in Teil 1 definierten Preise und Regeln:
    * **Basispreise:**
        * Einzelticket: Kurz 1,50 €, Mittel 2 €, Lang 3 €.
        * Mehrfahrtenticket: Kurz 5 €, Mittel 7 €, Lang 10 €.
    * **Konditionen:**
        * Ticketart-Zuschlag: +10% für Einzeltickets.
        * Sozialrabatt: -20% auf den Preis.
        * Zahlart-Zuschlag: +15% bei Barzahlung.

### User Story 3.3: Fahrgast
**„Ich möchte nach Eingabe meines Ziels sehen, wann ich dort ankomme und was die Fahrt kostet, um Planungssicherheit zu haben.“**

* Das System muss die voraussichtliche Ankunftszeit am Zielort berechnen und anzeigen.
* Dem Fahrgast muss nach Beantwortung der Tarif-Fragen der endgültige Ticketpreis klar ausgewiesen werden.
* Die Zusammenfassung der Reise (Start, Ziel, Abfahrt, Ankunft und Endpreis, Zeitstempel) bildet den Abschluss des Beratungsvorgangs.

---

## Abnahmekriterien für das Inkrement (Code)
1. Der Code jeder Gruppe muss auf der Fork dieser Gruppe zugänglich sein.
2. Stationseingaben werden korrekt verarbeitet, auch wenn sie nur zu 80 % korrekt sind oder Abkürzungen (Hbf., Str.) enthalten.
3. Die Ankunftszeit an der Zielstation wird korrekt ausgegeben.
4. Die Preisberechnung liefert für alle Kombinationen (Ticket-Typ, Rabatt, Zahlart) korrekte Ausgaben.
5. Der Fahrgast erhält eine abschließende Übersicht aller relevanten Reisedaten.

---

## Liste der Testfälle für die Abnahme

| Nr. | Eingabe-Typ                | Benutzereingabe   | Erwartete Ausgabe / Reaktion | Logik-Prüfung                    |
| :--- |:---------------------------|:------------------| :--- |:---------------------------------|
| 1 | **exakte Übereinstimmung** | `Messe`           | `Messe` erkannt | Standardfall                     |
| 2 | **Mapping & Punkt**        | `Fürth Hbf.`      | `Fürth Hauptbahnhof` erkannt | Abkürzung mit Punkt              |
| 3 | **Kleinschreibung**        | `aufseßplatz`     | `Aufseßplatz` erkannt | Klein- und Großschreibung        |
| 4 | **ß-Ersetzung**            | `Aufsessplatz`    | `Aufseßplatz` erkannt | ß vs. ss Handling                |
| 5 | **Umlaute**                | `Baerenchanze`    | `Bärenschanze` erkannt | ae -> ä Konvertierung            |
| 6 | **Tippfehler (80%)**       | `Maffeiplat`      | `Maffeiplatz` erkannt | Fehlendes 'z'                    |
| 7 | **Tippfehler (80%)**       | `Jakobinenstrase` | `Jakobinenstraße` erkannt | Buchstabendreher/Fehler          |
| 8 | **Leerzeichen**            | `  Gostenhof  `   | `Gostenhof` erkannt | Trim / Strip Funktion            |
| 9 | **langer Name**            | `Langwasser Nord` | `Langwasser Nord` erkannt | Mehrwort-Erkennung               |
| 10 | **nicht eindeutig**        | `Hauptbahnhof`    | `Hauptbahnhof` erkannt | Korrekte Wahl (nicht Fürth)      |
| 11 | **zu ungenau**             | `Wasser`          | Fehlermeldung | < 80% (zu viele Treffer möglich) |
| 12 | **linienfremd**            | `Flughafen`       | Fehlermeldung | Station existiert nicht auf U1   |

Erläuterung zu Testfall 10 & 12:

    Testfall 8: Hier ist vor und nach Gostenhof ein Leerzeichen: ' Gostenhof '     

    Testfall 10: Da die Eingabe exakt "Hauptbahnhof" lautet, muss das System diesen auch wählen und nicht den "Fürth Hauptbahnhof", da hier ein 100% Match vorliegt.

    Testfall 12: Da die U2/U3 noch nicht implementiert sind, muss das System den "Flughafen" als unbekannt ablehnen, um die Integrität der U1-Reiseplanung zu wahren.
