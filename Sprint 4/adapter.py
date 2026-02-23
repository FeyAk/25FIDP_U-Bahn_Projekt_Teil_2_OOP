# adapter.py
# Adapter-Klasse für das automatisierte Testskript (US 4.5).

from datetime import time, timedelta
from berechnung import berechne_fahrt


class adapter_klasse:

    def __init__(self):
        pass

    def ausfuehren_testfall(self,
                            eingabe_start: str,
                            eingabe_ziel: str,
                            eingabe_startzeit: str,
                            eingabe_einzelfahrkarte: bool,
                            eingabe_sozialrabatt: bool,
                            eingabe_barzahlung: bool) -> dict:

        try:
            erg = berechne_fahrt(
                eingabe_start, eingabe_ziel, eingabe_startzeit,
                eingabe_einzelfahrkarte, eingabe_sozialrabatt, eingabe_barzahlung
            )
        except Exception:
            erg = {"fehler": True}

        def t(v): return v if isinstance(v, time) else time(0, 0, 0)
        def td(v): return v if isinstance(v, timedelta) else timedelta(0)

        return {
            "fehler":                     bool(erg.get("fehler", True)),
            "ausgabe_startzeit_fahrgast": t(erg.get("ausgabe_startzeit_fahrgast")),
            "ausgabe_zielzeit_fahrgast":  t(erg.get("ausgabe_zielzeit_fahrgast")),
            "ausgabe_startzeit_algo":     t(erg.get("ausgabe_startzeit_algo")),
            "ausgabe_zielzeit_algo":      t(erg.get("ausgabe_zielzeit_algo")),
            "bahnlinien_gesamtfahrt":     list(erg.get("bahnlinien_gesamtfahrt", [])),
            "route":                      dict(erg.get("route", {})),
            "umstieg_haltestellen":       list(erg.get("umstieg_haltestellen", [])),
            "umstiege_exakt":             dict(erg.get("umstiege_exakt", {})),
            "umstiege_fahrgast":          dict(erg.get("umstiege_fahrgast", {})),
            "umstieg_bahnlinien":         list(erg.get("umstieg_bahnlinien", [])),
            "dauer_gesamtfahrt":          td(erg.get("dauer_gesamtfahrt")),
            "preis_endbetrag":            float(erg.get("preis_endbetrag", 0.0)),
        }
