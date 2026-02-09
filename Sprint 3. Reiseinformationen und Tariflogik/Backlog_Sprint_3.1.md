# Sprint 3: Reiseinformationen und Tariflogik

### Kurzfassung

Ziel dieses Sprints ist die fachliche Vervollständigung der Reiseauskunft. Der Fahrgast erhält nun präzise Informationen über die Ankunftszeit und die individuellen Fahrtkosten. Zudem wird das System gegenüber fehlerhaften Benutzereingaben abgesichert.

## User Stories und fachliche Spezifikationen

### User Story 3.1: Verkehrsbetrieb
**„Wenn der Benutzer eine falsche Eingabe macht, darf das Programm nicht abstürzen. Kleine Abweichungen bei der Eingabe sollen möglich sein und die Ausgabe der gewünschten Information nicht behindern.“**

* Das System muss Eingaben eigenständig korrigieren, sofern sie zu mindestens 80 % korrekt sind oder durch ein händisches Mapping (z. B. "Hbf." zu "Hauptbahnhof") eindeutig zugewiesen werden können.
* Das System muss folgende Abweichungen abfangen: Groß-/Kleinschreibung, führende/folgende Leerzeichen, Umlaute, das scharfe S (ß) sowie gängige Abkürzungen (z. B. Str. für Straße, Hbf. für Hauptbahnhof, Fr.- für Friedrich-).
* Bei Eingaben, die auch unter Berücksichtigung der 80 %-Regel und des Mappings nicht eindeutig zugeordnet werden können, muss das System den Benutzer informieren und eine erneute Eingabe ermöglichen, anstatt den Prozess abzubrechen.

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

## Liste der Testfälle für die manuelle Abnahme

Die folgende Tabelle dient als Grundlage für die manuelle Prüfung der Eingabe-Logik. Eine Station gilt als erkannt, wenn das Programm den offiziellen Namen bestätigt oder für die weitere Reiseplanung verwendet.

| Eingabe-Typ | Benutzereingabe | Erwartete Ausgabe / Reaktion |
| :--- | :--- | :--- |
| **Exakter Match** | `Messe` | Station `Messe` erkannt |
| **Mapping (Hbf)** | `Fürth Hbf.` | Station `Fürth Hauptbahnhof` erkannt |
| **Mapping (Str)** | `Rothenburger Str` | Station `Rothenburger Straße` erkannt |
| **Mapping (Fr.-)** | `Fr.-Ebert-Platz` | Station `Friedrich-Ebert-Platz` erkannt |
| **Fuzzy (80% - Tippfehler)** | `Mese` | Station `Messe` erkannt |
| **Fuzzy (80% - Dreher)** | `Lorenzkirhce` | Station `Lorenzkirche` erkannt |
| **Fuzzy (80% - Umlaute)** | `Munchener Freiheit` | Station `Münchner Freiheit` erkannt |
| **Gerade noch Erfolg** | `Bauernfeindstr` | Station `Bauernfeindstraße` erkannt |
| **Zu ungenau (< 80%)** | `Lorenz` | Fehlermeldung & Aufforderung zur Neueingabe |
| **Zu ungenau (< 80%)** | `Freiheit` | Fehlermeldung & Aufforderung zur Neueingabe |
| **Kein Netzbezug** | `Berlin Hbf` | Fehlermeldung & Aufforderung zur Neueingabe |
| **Sonderzeichen** | ` Plärrer!!! ` | Station `Plärrer` erkannt |