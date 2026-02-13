import difflib


class StationData:
    """İstasyon verileri ve dil işleme (Normalizasyon)."""

    def __init__(self):
        self.list = [
            "Langwasser Süd", "Gemeinschaftshaus", "Langwasser Mitte",
            "Scharfreiterring", "Langwasser Nord", "Messe", "Bauernfeindstraße",
            "Hasenbuck", "Frankenstraße", "Maffeiplatz", "Aufseßplatz",
            "Hauptbahnhof", "Lorenzkirche", "Weißer Turm", "Plärrer",
            "Gostenhof", "Bärenschanze", "Maximilianstraße", "Eberhardshof",
            "Muggenhof", "Stadtgrenze", "Jakobinenstraße", "Fürth Hauptbahnhof"
        ]
        self.mapping = {"hbf": "hauptbahnhof", "str": "strasse", "fr": "friedrich"}

    def normalize(self, text):
        t = text.strip().lower().replace("-", " ")
        t = t.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        return " ".join([self.mapping.get(w.rstrip("."), w) for w in t.split()])

    def find(self, query):
        norm_q = self.normalize(query)
        best_match, max_rate = None, 0.0
        for s in self.list:
            norm_s = self.normalize(s)
            if norm_q == norm_s: return s
            rate = difflib.SequenceMatcher(None, norm_q, norm_s).ratio()
            if rate > max_rate: max_rate, best_match = rate, s
        return best_match if max_rate >= 0.8 else None


class Ticket:
    """Bir biletin tüm bilgilerini taşıyan veri yapısı."""

    def __init__(self, start, ziel, stations_count, price):
        self.start = start
        self.ziel = ziel
        self.duration = stations_count * 2
        self.price = price

    def display(self):
        print("\n" + "=" * 30 + "\nREISEZUSAMMENFASSUNG")
        print(f"Start:    {self.start}\nZiel:     {self.ziel}")
        print(f"Dauer:    ca. {self.duration} Min\nEndpreis: {self.price:.2f} €")
        print("=" * 30)


class PricingEngine:
    """Fiyatlandırma mantığı ve kurallar."""

    def calculate(self, count):
        # Mesafe kategorisi
        if count <= 3:
            base = (1.50, 5.00)
        elif count <= 8:
            base = (2.00, 7.00)
        else:
            base = (3.00, 10.00)

        typ = input("Einzelticket (e) oder Mehrfahrtenticket (m)? ").lower()
        sozial = input("Haben Sie Anspruch auf Sozialrabatt? (j/n) ").lower()
        zahlung = input("Zahlart: Bar (b) oder Karte (k)? ").lower()

        p = base[0] if typ == 'e' else base[1]
        if typ == 'e': p *= 1.10
        if sozial == 'j': p *= 0.80
        if zahlung == 'b': p *= 1.15
        return round(p, 2)


class App:
    """Uygulama akışı (Main Controller)."""

    def __init__(self):
        self.db = StationData()
        self.engine = PricingEngine()

    def get_valid_station(self, prompt):
        while True:
            name = self.db.find(input(prompt))
            if name: return name
            print("Station nicht erkannt.")

    def start(self):
        print("--- U-Bahn Nürnberg/Fürth (U1) ---")
        s1 = self.get_valid_station("Start: ")
        s2 = self.get_valid_station("Ziel: ")

        count = abs(self.db.list.index(s1) - self.db.list.index(s2))
        final_price = self.engine.calculate(count)

        # Bilet nesnesini oluştur ve göster
        ticket = Ticket(s1, s2, count, final_price)
        ticket.display()


if __name__ == "__main__":
    ReiseApp = App()
    ReiseApp.start()