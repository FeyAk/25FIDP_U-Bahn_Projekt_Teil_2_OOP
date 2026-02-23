# main.py
# Interaktive Benutzeroberfläche – nur hier ist input() erlaubt.

from berechnung import berechne_fahrt, parse_zeit, finde_station


def eingabe_station(prompt):
    while True:
        s = finde_station(input(prompt))
        if s: return s
        print("  ⚠ Nicht gefunden, bitte erneut eingeben.")

def eingabe_zeit(prompt):
    while True:
        e = input(prompt)
        if parse_zeit(e): return e
        print("  ⚠ Ungültige Zeit. Beispiele: 9, 9:30, 930, 14.00")

def ja_nein(prompt):
    while True:
        a = input(prompt).strip().lower()
        if a in ("j","ja"): return True
        if a in ("n","nein"): return False
        print("  ⚠ Bitte j oder n eingeben.")

def main():
    print("=" * 42)
    print("  U-Bahn Nürnberg/Fürth – Ticketautomat")
    print("=" * 42)

    start = eingabe_station("Starthaltestelle: ")
    ziel  = eingabe_station("Zielhaltestelle:  ")
    zeit  = eingabe_zeit   ("Abfahrtszeit:     ")
    einzel  = not ja_nein  ("Mehrfahrtkarte?   (j/n): ")
    sozial  = ja_nein      ("Sozialrabatt?     (j/n): ")
    bar     = ja_nein      ("Barzahlung?       (j/n): ")

    r = berechne_fahrt(start, ziel, zeit, einzel, sozial, bar)

    print("-" * 42)
    if r["fehler"]:
        print("⚠  Keine Verbindung gefunden.")
    else:
        dauer = int(r["dauer_gesamtfahrt"].total_seconds() // 60)
        print(f"  {start}  →  {ziel}")
        print(f"  Linie(n): {' → '.join(r['bahnlinien_gesamtfahrt'])}")
        print(f"  Abfahrt:  {r['ausgabe_startzeit_fahrgast'].strftime('%H:%M')} Uhr")
        print(f"  Ankunft:  {r['ausgabe_zielzeit_fahrgast'].strftime('%H:%M')} Uhr")
        print(f"  Dauer:    {dauer} min")
        for u, ln in zip(r["umstieg_haltestellen"], r["umstieg_bahnlinien"]):
            z = r["umstiege_fahrgast"][u]
            print(f"  Umstieg:  {u}  ({z[0].strftime('%H:%M')} → {z[1].strftime('%H:%M')}, weiter mit {ln})")
        print(f"  Preis:    {r['preis_endbetrag']:.2f} €")
    print("-" * 42)

if __name__ == "__main__":
    main()
