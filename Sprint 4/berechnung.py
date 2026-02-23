# berechnung.py
# Enthält alle Logik: Netzplan, Graph, Fahrplanberechnung, Preise, Zeitparsung.
# KEIN input() in dieser Datei – alle Werte kommen als Parameter.

import re
import difflib
import heapq
from datetime import datetime, timedelta, time
from typing import Optional

# ===========================================================================
# 1. NETZPLANDATEN
# ===========================================================================

# Format: (Linie, Von, Fahrzeit_in_Minuten, Nach)
STRECKEN = [
    # U1 – Langwasser Süd → Fürth Hbf.
    ("U1", "Langwasser Süd",      3, "Gemeinschaftshaus"),
    ("U1", "Gemeinschaftshaus",   2, "Langwasser Mitte"),
    ("U1", "Langwasser Mitte",    2, "Scharfreiterring"),
    ("U1", "Scharfreiterring",    3, "Langwasser Nord"),
    ("U1", "Langwasser Nord",     2, "Messe"),
    ("U1", "Messe",               3, "Bauernfeindstraße"),
    ("U1", "Bauernfeindstraße",   2, "Hasenbuck"),
    ("U1", "Hasenbuck",           2, "Frankenstraße"),
    ("U1", "Frankenstraße",       2, "Maffeiplatz"),
    ("U1", "Maffeiplatz",         1, "Aufseßplatz"),
    ("U1", "Aufseßplatz",         2, "Hauptbahnhof"),
    ("U1", "Hauptbahnhof",        2, "Lorenzkirche"),
    ("U1", "Lorenzkirche",        3, "Weißer Turm"),
    ("U1", "Weißer Turm",         2, "Plärrer"),
    ("U1", "Plärrer",             2, "Gostenhof"),
    ("U1", "Gostenhof",           1, "Bärenschanze"),
    ("U1", "Bärenschanze",        2, "Maximilianstraße"),
    ("U1", "Maximilianstraße",    2, "Eberhardshof"),
    ("U1", "Eberhardshof",        2, "Muggenhof"),
    ("U1", "Muggenhof",           3, "Stadtgrenze"),
    ("U1", "Stadtgrenze",         2, "Jakobinenstraße"),
    ("U1", "Jakobinenstraße",     3, "Fürth Hbf."),
    # U2 – Röthenbach → Flughafen
    ("U2", "Röthenbach",          2, "Hohe Marter"),
    ("U2", "Hohe Marter",         2, "Schweinau"),
    ("U2", "Schweinau",           2, "St. Leonhard"),
    ("U2", "St. Leonhard",        2, "Rothenburger Straße"),
    ("U2", "Rothenburger Straße", 3, "Plärrer"),
    ("U2", "Plärrer",             2, "Opernhaus"),
    ("U2", "Opernhaus",           2, "Hauptbahnhof"),
    ("U2", "Hauptbahnhof",        2, "Wöhrder Wiese"),
    ("U2", "Wöhrder Wiese",       1, "Rathenauplatz"),
    ("U2", "Rathenauplatz",       2, "Rennweg"),
    ("U2", "Rennweg",             2, "Schoppershof"),
    ("U2", "Schoppershof",        2, "Nordostbahnhof"),
    ("U2", "Nordostbahnhof",      3, "Herrnhütte"),
    ("U2", "Herrnhütte",          2, "Ziegelstein"),
    ("U2", "Ziegelstein",         3, "Flughafen"),
    # U3 – Gustav-Adolf-Straße → Friedrich-Ebert-Platz
    ("U3", "Gustav-Adolf-Straße", 4, "Sündersbühl"),
    ("U3", "Sündersbühl",         2, "Rothenburger Straße"),
    ("U3", "Rothenburger Straße", 3, "Plärrer"),
    ("U3", "Plärrer",             2, "Opernhaus"),
    ("U3", "Opernhaus",           2, "Hauptbahnhof"),
    ("U3", "Hauptbahnhof",        2, "Wöhrder Wiese"),
    ("U3", "Wöhrder Wiese",       1, "Rathenauplatz"),
    ("U3", "Rathenauplatz",       2, "Maxfeld"),
    ("U3", "Maxfeld",             3, "Kaulbachplatz"),
    ("U3", "Kaulbachplatz",       2, "Friedrich-Ebert-Platz"),
]

HEIMHALTESTELLEN  = {"U1": "Langwasser Süd", "U2": "Röthenbach", "U3": "Gustav-Adolf-Straße"}
ENDHALTESTELLEN   = {"U1": "Fürth Hbf.",     "U2": "Flughafen",  "U3": "Friedrich-Ebert-Platz"}
HAUPTKNOTEN       = {"Plärrer", "Hauptbahnhof"}

# Haltezeiten in Sekunden
def _haltezeit(station: str, linie: str) -> int:
    if station in (HEIMHALTESTELLEN.get(linie), ENDHALTESTELLEN.get(linie)):
        return 60
    if station in HAUPTKNOTEN:
        return 60
    return 30

# Mindestumstiegszeit in Sekunden
def _umstiegszeit(station: str) -> int:
    return 5 * 60 if station in HAUPTKNOTEN else 3 * 60


# ===========================================================================
# 2. GRAPH & FAHRPLAN AUFBAUEN (einmalig beim Import)
# ===========================================================================

BASIS_DATUM = datetime(2000, 1, 1)

def _baue_netz():
    stationen_pro_linie: dict[str, list[str]] = {}
    fahrzeiten: dict[tuple, int] = {}

    for linie, von, minuten, nach in STRECKEN:
        sl = stationen_pro_linie.setdefault(linie, [])
        if not sl or sl[-1] != von:
            sl.append(von)
        sl.append(nach)
        fahrzeiten[(linie, von, nach)] = minuten
        fahrzeiten[(linie, nach, von)] = minuten

    station_zu_linien: dict[str, set] = {}
    for linie, stationen in stationen_pro_linie.items():
        for s in stationen:
            station_zu_linien.setdefault(s, set()).add(linie)

    umstiegsstationen = {s for s, ln in station_zu_linien.items() if len(ln) > 1}
    return stationen_pro_linie, fahrzeiten, station_zu_linien, umstiegsstationen


def _berechne_abfahrtszeiten(linie, stationen_pro_linie, fahrzeiten):
    stationen = stationen_pro_linie[linie]
    if stationen[0] != HEIMHALTESTELLEN[linie]:
        stationen = list(reversed(stationen))

    abfahrten: dict[str, list] = {s: [] for s in stationen}
    erste  = BASIS_DATUM.replace(hour=5,  minute=0, second=0)
    letzte = BASIS_DATUM.replace(hour=23, minute=0, second=0)
    takt   = timedelta(minutes=10)

    zug_start = erste
    while zug_start <= letzte:
        # Hinfahrt
        t = zug_start
        for i, s in enumerate(stationen):
            abfahrten[s].append(t)
            if i < len(stationen) - 1:
                fz   = fahrzeiten[(linie, s, stationen[i + 1])]
                halt = _haltezeit(s, linie)
                t    = t + timedelta(minutes=fz) + timedelta(seconds=halt)
        # Wenden
        t = t + timedelta(seconds=_haltezeit(stationen[-1], linie))
        # Rückfahrt
        for i, s in enumerate(reversed(stationen)):
            abfahrten[s].append(t)
            if i < len(stationen) - 1:
                prev = stationen[len(stationen) - 2 - i]
                fz   = fahrzeiten[(linie, s, prev)]
                halt = _haltezeit(s, linie)
                t    = t + timedelta(minutes=fz) + timedelta(seconds=halt)
        zug_start += takt

    for s in abfahrten:
        abfahrten[s] = sorted(set(abfahrten[s]))
    return abfahrten


# Globale Netz-Objekte
_SPL, _FZ, _S2L, _UMST = _baue_netz()
_ABFAHRTEN = {ln: _berechne_abfahrtszeiten(ln, _SPL, _FZ) for ln in _SPL}
ALLE_STATIONEN = sorted(_S2L.keys())


def _naechste_abfahrt(linie, station, ab: datetime) -> Optional[datetime]:
    ab_n = ab.replace(year=2000, month=1, day=1)
    for z in _ABFAHRTEN.get(linie, {}).get(station, []):
        if z >= ab_n:
            return z
    return None


def _ankunft(linie, von, nach, abfahrt: datetime) -> Optional[datetime]:
    stationen = _SPL[linie]
    try:
        i_von  = stationen.index(von)
        i_nach = stationen.index(nach)
    except ValueError:
        return None
    richtung = 1 if i_nach > i_von else -1
    t = abfahrt.replace(year=2000, month=1, day=1)
    i = i_von
    while i != i_nach:
        j   = i + richtung
        fz  = _FZ[(linie, stationen[i], stationen[j])]
        t  += timedelta(minutes=fz) + timedelta(seconds=_haltezeit(stationen[i], linie))
        i   = j
    return t


# ===========================================================================
# 3. STATIONSSUCHE MIT FUZZY-MATCHING
# ===========================================================================

_NORM_MAP = {"hbf": "hauptbahnhof", "str": "strasse", "fr": "friedrich"}

def _norm(text: str) -> str:
    t = text.strip().lower().replace("-", " ")
    t = t.replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    return " ".join(_NORM_MAP.get(w.rstrip("."), w) for w in t.split())

def finde_station(abfrage: str) -> Optional[str]:
    q = _norm(abfrage)
    for s in ALLE_STATIONEN:
        if q == _norm(s):
            return s
    beste, max_rate = None, 0.0
    for s in ALLE_STATIONEN:
        r = difflib.SequenceMatcher(None, q, _norm(s)).ratio()
        if r > max_rate:
            max_rate, beste = r, s
    return beste if max_rate >= 0.8 else None


# ===========================================================================
# 4. ZEITPARSUNG (US 4.4)
# ===========================================================================

def parse_zeit(eingabe: str) -> Optional[time]:
    """
    Akzeptiert: 9, 9:30, 09.30, 14,00, 930, 1430, 9 30
    Gibt datetime.time zurück oder None bei Fehler.
    """
    s = re.sub(r"[.,\s]", ":", eingabe.strip())
    raw = s.replace(":", "")
    if re.fullmatch(r"\d{3,4}", raw):
        raw = raw.zfill(4)
        s = raw[:2] + ":" + raw[2:]
    teile = s.split(":")
    try:
        h = int(teile[0])
        m = int(teile[1]) if len(teile) > 1 and teile[1] else 0
        if 0 <= h <= 23 and 0 <= m <= 59:
            return time(h, m, 0)
    except (ValueError, IndexError):
        pass
    return None


# ===========================================================================
# 5. PREISBERECHNUNG (US 3.2)
# ===========================================================================

def berechne_preis(anzahl_stationen: int, einzelfahrkarte: bool,
                   sozialrabatt: bool, barzahlung: bool) -> float:
    if anzahl_stationen <= 3:
        basis = 1.50 if einzelfahrkarte else 5.00
    elif anzahl_stationen <= 8:
        basis = 2.00 if einzelfahrkarte else 7.00
    else:
        basis = 3.00 if einzelfahrkarte else 10.00

    faktor = 1.0
    if einzelfahrkarte: faktor += 0.10
    if sozialrabatt:    faktor -= 0.20
    if barzahlung:      faktor += 0.15
    return round(basis * faktor, 2)


# ===========================================================================
# 6. ROUTENSUCHE – DIJKSTRA (US 4.1 – 4.3)
# ===========================================================================

def berechne_fahrt(start_haltestelle: str, ziel_haltestelle: str,
                   startzeit: str, einzelfahrkarte: bool = True,
                   sozialrabatt: bool = False, barzahlung: bool = False) -> dict:
    """
    Berechnet die optimale Route. Alle Eingaben als Parameter.
    Gibt ein Dict gemäß Adapter-Spezifikation 4.7.2 zurück.
    """

    def fehler():
        return {"fehler": True, "ausgabe_startzeit_fahrgast": time(0,0),
                "ausgabe_zielzeit_fahrgast": time(0,0), "ausgabe_startzeit_algo": time(0,0,0),
                "ausgabe_zielzeit_algo": time(0,0,0), "bahnlinien_gesamtfahrt": [],
                "route": {}, "umstieg_haltestellen": [], "umstiege_exakt": {},
                "umstiege_fahrgast": {}, "umstieg_bahnlinien": [],
                "dauer_gesamtfahrt": timedelta(0), "preis_endbetrag": 0.0}

    start = finde_station(start_haltestelle)
    ziel  = finde_station(ziel_haltestelle)
    if not start or not ziel or start == ziel:
        return fehler()

    start_time = parse_zeit(startzeit)
    if not start_time:
        return fehler()

    start_dt = BASIS_DATUM.replace(hour=start_time.hour, minute=start_time.minute, second=0)

    # Dijkstra: (ankunft, umstiege, counter, station, linie, pfad)
    pq = []
    counter = 0
    heapq.heappush(pq, (start_dt, 0, counter, start, None, []))
    besucht: dict[tuple, datetime] = {}
    bestes = None

    while pq:
        akt_dt, umst_anz, _, station, linie, pfad = heapq.heappop(pq)

        key = (station, linie)
        if key in besucht and besucht[key] <= akt_dt:
            continue
        besucht[key] = akt_dt

        if station == ziel:
            if bestes is None or (akt_dt, umst_anz) < (bestes[0], bestes[1]):
                bestes = (akt_dt, umst_anz, pfad)
            continue

        for nl in _S2L.get(station, set()):
            if station not in _SPL.get(nl, []):
                continue

            # Umstiegszeit berücksichtigen
            warte_dt = akt_dt + timedelta(seconds=_umstiegszeit(station)) \
                       if (linie is not None and nl != linie) else akt_dt

            abfahrt = _naechste_abfahrt(nl, station, warte_dt)
            if abfahrt is None:
                continue

            stationen_nl = _SPL[nl]
            idx_aktuell  = stationen_nl.index(station)

            for richtung in [1, -1]:
                idx = idx_aktuell + richtung
                while 0 <= idx < len(stationen_nl):
                    nxt = stationen_nl[idx]
                    ankunft = _ankunft(nl, station, nxt, abfahrt)
                    if ankunft is None:
                        break

                    nkey = (nxt, nl)
                    if nkey in besucht and besucht[nkey] <= ankunft:
                        idx += richtung
                        continue

                    neuer_umst = umst_anz + (1 if linie is not None and nl != linie else 0)
                    eintrag = {"linie": nl, "von": station, "nach": nxt,
                               "abfahrt": abfahrt, "ankunft": ankunft}
                    counter += 1
                    heapq.heappush(pq, (ankunft, neuer_umst, counter, nxt, nl, pfad + [eintrag]))

                    if nxt == ziel or nxt in _UMST:
                        break
                    idx += richtung

    if bestes is None:
        return fehler()

    ankunft_dt, _, pfad = bestes

    # Segmente zusammenfassen (pro Linie ein Segment)
    segmente = []
    if pfad:
        sl, sv, sab = pfad[0]["linie"], pfad[0]["von"], pfad[0]["abfahrt"]
        sna, san    = pfad[0]["nach"],  pfad[0]["ankunft"]
        for e in pfad[1:]:
            if e["linie"] == sl:
                sna, san = e["nach"], e["ankunft"]
            else:
                segmente.append((sl, sv, sna, sab, san))
                sl, sv, sab, sna, san = e["linie"], e["von"], e["abfahrt"], e["nach"], e["ankunft"]
        segmente.append((sl, sv, sna, sab, san))

    echt_ab = segmente[0][3] if segmente else start_dt
    echt_an = segmente[-1][4] if segmente else start_dt

    def as_time(dt): return time(dt.hour, dt.minute, dt.second)
    def aufrunden(dt):
        return dt + timedelta(seconds=60 - dt.second) if dt.second > 0 else dt

    # Route-Dict
    route = {}
    for linie, von, nach, ab, an in segmente:
        if von not in route:
            route[von] = [linie, "00:00:00", ab.strftime("%H:%M:%S")]
        route[nach] = [linie, an.strftime("%H:%M:%S"), "–"]

    # Umstiege
    umst_stationen  = [seg[2] for seg in segmente[:-1]]
    umst_bahnlinien = [segmente[i+1][0] for i in range(len(segmente)-1)]
    umstiege_exakt, umstiege_fahrgast = {}, {}
    for i, u in enumerate(umst_stationen):
        an_seg = segmente[i][4]
        ab_seg = segmente[i+1][3]
        umstiege_exakt[u]   = [as_time(an_seg), as_time(ab_seg)]
        umstiege_fahrgast[u] = [as_time(aufrunden(an_seg)), time(ab_seg.hour, ab_seg.minute, 0)]

    # Stationsanzahl für Preis
    anzahl = sum(
        abs(_SPL[ln].index(nach) - _SPL[ln].index(von))
        for ln, von, nach, _, __ in segmente
    )

    return {
        "fehler":                    False,
        "ausgabe_startzeit_fahrgast": time(echt_ab.hour, echt_ab.minute, 0),
        "ausgabe_zielzeit_fahrgast":  as_time(aufrunden(echt_an)),
        "ausgabe_startzeit_algo":     as_time(echt_ab),
        "ausgabe_zielzeit_algo":      as_time(echt_an),
        "bahnlinien_gesamtfahrt":     list(dict.fromkeys(s[0] for s in segmente)),
        "route":                      route,
        "umstieg_haltestellen":       umst_stationen,
        "umstiege_exakt":             umstiege_exakt,
        "umstiege_fahrgast":          umstiege_fahrgast,
        "umstieg_bahnlinien":         umst_bahnlinien,
        "dauer_gesamtfahrt":          echt_an - echt_ab,
        "preis_endbetrag":            berechne_preis(anzahl, einzelfahrkarte, sozialrabatt, barzahlung),
    }


# ===========================================================================
# 7. DIREKTER START – nur hier ist input() erlaubt
# ===========================================================================

if __name__ == "__main__":
    print("=== U-Bahn Nürnberg/Fürth – Fahrkartenrechner ===\n")
    s = input("Start:          ")
    z = input("Ziel:           ")
    t = input("Abfahrtszeit:   ")
    e = input("Einzelticket? (j/n): ").lower() != "n"
    so = input("Sozialrabatt?  (j/n): ").lower() == "j"
    b  = input("Barzahlung?    (j/n): ").lower() == "j"

    r = berechne_fahrt(s, z, t, e, so, b)
    if r["fehler"]:
        print("\n⚠ Keine Verbindung gefunden.")
    else:
        print(f"\nAbfahrt:  {r['ausgabe_startzeit_fahrgast'].strftime('%H:%M')} Uhr")
        print(f"Ankunft:  {r['ausgabe_zielzeit_fahrgast'].strftime('%H:%M')} Uhr")
        print(f"Linie(n): {', '.join(r['bahnlinien_gesamtfahrt'])}")
        if r["umstieg_haltestellen"]:
            for u, ln in zip(r["umstieg_haltestellen"], r["umstieg_bahnlinien"]):
                zeiten = r["umstiege_fahrgast"][u]
                print(f"Umstieg:  {u} ({zeiten[0].strftime('%H:%M')} → {zeiten[1].strftime('%H:%M')}, {ln})")
        print(f"Dauer:    {int(r['dauer_gesamtfahrt'].total_seconds()//60)} min")
        print(f"Preis:    {r['preis_endbetrag']:.2f} €")
