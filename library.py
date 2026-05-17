class Book:
    def __init__(self, tytul, autor, sztuki):
        self.__tytul = tytul
        self.__autor = autor
        self.__liczba_sztuk = sztuki
        self.__dostepne_sztuki = sztuki

    @property
    def tytul(self):
        return self.__tytul

    @property
    def autor(self):
        return self.__autor

    @property
    def liczba_sztuk(self):
        return self.__liczba_sztuk

    @property
    def dostepne_sztuki(self):
        return self.__dostepne_sztuki

    def wypozycz(self):
        if self.__dostepne_sztuki > 0:
            self.__dostepne_sztuki -= 1
            return True
        return False

    def zwroc(self):
        if self.__dostepne_sztuki < self.__liczba_sztuk:
            self.__dostepne_sztuki += 1

    def __str__(self):
        return f"Tytuł: {self.__tytul}\nAutor: {self.__autor}\nDostępne sztuki: {self.__dostepne_sztuki}"


class User:
    def __init__(self, login, haslo, rola):
        self._login = login
        self._haslo = haslo
        self._rola = rola

    @property
    def login(self):
        return self._login

    @property
    def rola(self):
        return self._rola

    def sprawdz_haslo(self, haslo):
        return self._haslo == haslo


class Reader(User):
    def __init__(self, login, haslo):
        super().__init__(login, haslo, "czytelnik")
        self.wypozyczenia = []
        self.prosby_o_przedluzenie = []

    def dodaj_wypozyczenie(self, ksiazka):
        self.wypozyczenia.append(ksiazka)

    def usun_wypozyczenie(self, ksiazka):
        if ksiazka in self.wypozyczenia:
            self.wypozyczenia.remove(ksiazka)

    def dodaj_prosbe(self, ksiazka):
        self.prosby_o_przedluzenie.append(ksiazka)


class Librarian(User):
    def __init__(self, login, haslo):
        super().__init__(login, haslo, "bibliotekarz")


class Library:
    def __init__(self):
        self.ksiazki = []
        self.uzytkownicy = []
        self.kolejka_prosb = []
        self.rezerwacje = []

    def dodaj_ksiazke(self, ksiazka):
        self.ksiazki.append(ksiazka)

    def dodaj_uzytkownika(self, uzytkownik):
        self.uzytkownicy.append(uzytkownik)

    def logowanie(self):
        liczba_prob = 0

        while liczba_prob < 3:
            login = input("Podaj login: ")
            haslo = input("Podaj hasło: ")

            for uzytkownik in self.uzytkownicy:
                if uzytkownik.login == login and uzytkownik.sprawdz_haslo(haslo):
                    print("Zalogowano pomyślnie.\n")
                    return uzytkownik

            liczba_prob += 1
            print("Nieprawidłowy login lub hasło.")
            print("Pozostało prób:", 3 - liczba_prob)

        print("Przekroczono limit prób logowania. Program zakończony.")
        return None

    def wyswietl_katalog(self):
        print("\n--- Katalog książek ---")

        for ksiazka in self.ksiazki:
            print(ksiazka)
            print("----------------------")

    def znajdz_ksiazke_po_tytule(self, tytul):
        for ksiazka in self.ksiazki:
            if ksiazka.tytul.lower() == tytul.lower():
                return ksiazka

        return None

    def wypozycz_ksiazke(self, czytelnik):
        print("\n--- Wypożyczenie książki ---")
        tytul = input("Podaj tytuł książki: ")

        ksiazka = self.znajdz_ksiazke_po_tytule(tytul)

        if ksiazka is None:
            print("Nie znaleziono książki o takim tytule.")
        elif ksiazka.wypozycz():
            czytelnik.dodaj_wypozyczenie(ksiazka)
            print("Wypożyczono książkę:", ksiazka.tytul)
        else:
            print("Brak dostępnych sztuk tej książki.")
            decyzja = input("Czy chcesz zarezerwować tę książkę? (tak/nie): ")

            if decyzja.lower() == "tak":
                self.dodaj_rezerwacje(czytelnik, ksiazka)

    def pokaz_moje_wypozyczenia(self, czytelnik):
        print("\n--- Moje wypożyczenia ---")

        if len(czytelnik.wypozyczenia) == 0:
            print("Nie masz aktualnie wypożyczonych książek.")
        else:
            for numer, ksiazka in enumerate(czytelnik.wypozyczenia, start=1):
                print(numer, "-", ksiazka.tytul)

    def popros_o_przedluzenie(self, czytelnik):
        print("\n--- Prośba o przedłużenie ---")

        if len(czytelnik.wypozyczenia) == 0:
            print("Nie masz książek, które można przedłużyć.")
            return

        self.pokaz_moje_wypozyczenia(czytelnik)

        numer = int(input("Podaj numer książki do przedłużenia: "))

        if numer < 1 or numer > len(czytelnik.wypozyczenia):
            print("Nieprawidłowy numer książki.")
            return

        ksiazka = czytelnik.wypozyczenia[numer - 1]

        prosba = {
            "czytelnik": czytelnik,
            "ksiazka": ksiazka
        }

        self.kolejka_prosb.append(prosba)
        czytelnik.dodaj_prosbe(ksiazka)

        print("Prośba o przedłużenie została wysłana.")

    def pokaz_wszystkie_wypozyczenia(self):
        print("\n--- Aktualne wypożyczenia ---")

        wypozyczenia = [
            (uzytkownik, ksiazka)
            for uzytkownik in self.uzytkownicy
            if isinstance(uzytkownik, Reader)
            for ksiazka in uzytkownik.wypozyczenia
        ]

        if len(wypozyczenia) == 0:
            print("Brak aktualnych wypożyczeń.")
        else:
            list(map(
                lambda element: print(
                    "Czytelnik:", element[0].login,
                    "\nKsiążka:", element[1].tytul,
                    "\n----------------------"
                ),
                wypozyczenia
            ))

    def obsluz_prosby(self):
        print("\n--- Obsługa próśb o przedłużenie ---")

        if len(self.kolejka_prosb) == 0:
            print("Brak próśb o przedłużenie.")
            return

        while len(self.kolejka_prosb) > 0:
            prosba = self.kolejka_prosb[0]
            czytelnik = prosba["czytelnik"]
            ksiazka = prosba["ksiazka"]

            print("Czytelnik:", czytelnik.login)
            print("Książka:", ksiazka.tytul)

            if self.czy_ksiazka_ma_rezerwacje(ksiazka):
                print("Uwaga: na tę książkę istnieje rezerwacja.")
            else:
                print("Brak rezerwacji na tę książkę.")

            decyzja = input("Czy zaakceptować prośbę? (tak/nie): ")

            if decyzja.lower() == "tak":
                print("Prośba została zaakceptowana.")
            else:
                print("Prośba została odrzucona.")

            self.kolejka_prosb.pop(0)

    # Funkcja wyższego rzędu — przyjmuje funkcję jako argument
    def wyswietl_kolekcje(self, kolekcja, predykat=lambda element: True):
        przefiltrowane = list(filter(predykat, kolekcja))

        if len(przefiltrowane) == 0:
            print("Brak wyników.")
        else:
            list(map(lambda element: print(element, "\n----------------------"), przefiltrowane))

    def filtruj_katalog(self):
        print("\n--- Filtrowanie katalogu ---")
        fraza = input("Podaj frazę z tytułu lub autora: ").lower()

        wynik = list(filter(
            lambda ksiazka: fraza in ksiazka.tytul.lower() or fraza in ksiazka.autor.lower(),
            self.ksiazki
        ))

        self.wyswietl_kolekcje(wynik)

    def pokaz_dostepne_ksiazki(self):
        print("\n--- Dostępne książki ---")

        dostepne = [
            ksiazka
            for ksiazka in self.ksiazki
            if ksiazka.dostepne_sztuki > 0
        ]

        self.wyswietl_kolekcje(dostepne)

    def sortuj_katalog(self):
        print("\n--- Sortowanie katalogu ---")
        print("1. Sortuj po tytule")
        print("2. Sortuj po autorze")
        print("3. Sortuj po liczbie dostępnych sztuk")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            posortowane = sorted(self.ksiazki, key=lambda ksiazka: ksiazka.tytul)
        elif wybor == "2":
            posortowane = sorted(self.ksiazki, key=lambda ksiazka: ksiazka.autor)
        elif wybor == "3":
            posortowane = sorted(self.ksiazki, key=lambda ksiazka: ksiazka.dostepne_sztuki)
        else:
            print("Nieprawidłowa opcja.")
            return

        self.wyswietl_kolekcje(posortowane)

    def dodaj_rezerwacje(self, czytelnik, ksiazka):
        czy_juz_istnieje = any(map(
            lambda rezerwacja: rezerwacja["czytelnik"] == czytelnik and rezerwacja["ksiazka"] == ksiazka,
            self.rezerwacje
        ))

        if czy_juz_istnieje:
            print("Masz już rezerwację na tę książkę.")
        else:
            rezerwacja = {
                "czytelnik": czytelnik,
                "ksiazka": ksiazka
            }

            self.rezerwacje.append(rezerwacja)
            print("Książka została zarezerwowana.")

    def zarezerwuj_ksiazke(self, czytelnik):
        print("\n--- Rezerwacja książki ---")
        tytul = input("Podaj tytuł książki do rezerwacji: ")

        ksiazka = self.znajdz_ksiazke_po_tytule(tytul)

        if ksiazka is None:
            print("Nie znaleziono książki o takim tytule.")
        elif ksiazka.dostepne_sztuki > 0:
            print("Ta książka jest dostępna, możesz ją wypożyczyć.")
        else:
            self.dodaj_rezerwacje(czytelnik, ksiazka)

    def czy_ksiazka_ma_rezerwacje(self, ksiazka):
        return any(map(
            lambda rezerwacja: rezerwacja["ksiazka"] == ksiazka,
            self.rezerwacje
        ))

    def pokaz_statystyki(self):
        print("\n--- Statystyki biblioteki ---")

        wypozyczone_liczby = list(map(
            lambda ksiazka: ksiazka.liczba_sztuk - ksiazka.dostepne_sztuki,
            self.ksiazki
        ))

        liczba_aktywnych_wypozyczen = sum(wypozyczone_liczby)

        if liczba_aktywnych_wypozyczen == 0:
            print("Brak aktywnych wypożyczeń.")
        else:
            najpopularniejsza = max(
                self.ksiazki,
                key=lambda ksiazka: ksiazka.liczba_sztuk - ksiazka.dostepne_sztuki
            )

            print("Najpopularniejsza książka:", najpopularniejsza.tytul)

        print("Liczba aktywnych wypożyczeń ogółem:", liczba_aktywnych_wypozyczen)

        czytelnicy = [
            uzytkownik
            for uzytkownik in self.uzytkownicy
            if isinstance(uzytkownik, Reader)
        ]

        czytelnicy_posortowani = sorted(
            czytelnicy,
            key=lambda czytelnik: len(czytelnik.wypozyczenia),
            reverse=True
        )

        statystyki_czytelnikow = {
            czytelnik.login: len(czytelnik.wypozyczenia)
            for czytelnik in czytelnicy_posortowani
        }

        print("\nCzytelnicy według liczby wypożyczonych książek:")

        list(map(
            lambda element: print(element[0], "-", element[1], "wypożyczeń"),
            statystyki_czytelnikow.items()
        ))

        def wyswietl_menu_czytelnika():
            print("\n--- Menu czytelnika ---")
            print("1. Przeglądaj katalog")
            print("2. Wypożycz książkę")
            print("3. Moje wypożyczenia")
            print("4. Poproś o przedłużenie książki")
            print("5. Filtruj katalog")
            print("6. Pokaż dostępne książki")
            print("7. Sortuj katalog")
            print("8. Zarezerwuj niedostępną książkę")
            print("9. Wyloguj")

        def wyswietl_menu_bibliotekarza():
            print("\n--- Menu bibliotekarza ---")
            print("1. Przeglądaj katalog")
            print("2. Pokaż wszystkie wypożyczenia")
            print("3. Obsłuż prośby o przedłużenie")
            print("4. Filtruj katalog")
            print("5. Pokaż dostępne książki")
            print("6. Sortuj katalog")
            print("7. Statystyki")
            print("8. Wyloguj")

        def menu_czytelnika(biblioteka, czytelnik):
            while True:
                wyswietl_menu_czytelnika()
                wybor = input("Wybierz opcję: ")

                if wybor == "1":
                    biblioteka.wyswietl_katalog()
                elif wybor == "2":
                    biblioteka.wypozycz_ksiazke(czytelnik)
                elif wybor == "3":
                    biblioteka.pokaz_moje_wypozyczenia(czytelnik)
                elif wybor == "4":
                    biblioteka.popros_o_przedluzenie(czytelnik)
                elif wybor == "5":
                    biblioteka.filtruj_katalog()
                elif wybor == "6":
                    biblioteka.pokaz_dostepne_ksiazki()
                elif wybor == "7":
                    biblioteka.sortuj_katalog()
                elif wybor == "8":
                    biblioteka.zarezerwuj_ksiazke(czytelnik)
                elif wybor == "9":
                    print("Wylogowano. Do widzenia!")
                    break
                else:
                    print("Nieprawidłowa opcja. Spróbuj ponownie.")

        def menu_bibliotekarza(biblioteka):
            while True:
                wyswietl_menu_bibliotekarza()
                wybor = input("Wybierz opcję: ")

                if wybor == "1":
                    biblioteka.wyswietl_katalog()
                elif wybor == "2":
                    biblioteka.pokaz_wszystkie_wypozyczenia()
                elif wybor == "3":
                    biblioteka.obsluz_prosby()
                elif wybor == "4":
                    biblioteka.filtruj_katalog()
                elif wybor == "5":
                    biblioteka.pokaz_dostepne_ksiazki()
                elif wybor == "6":
                    biblioteka.sortuj_katalog()
                elif wybor == "7":
                    biblioteka.pokaz_statystyki()
                elif wybor == "8":
                    print("Wylogowano. Do widzenia!")
                    break
                else:
                    print("Nieprawidłowa opcja. Spróbuj ponownie.")

        def uruchom_program():
            biblioteka = Library()

            biblioteka.dodaj_ksiazke(Book("Ostatnie życzenie", "Andrzej Sapkowski", 3))
            biblioteka.dodaj_ksiazke(Book("Instytut", "Stephen King", 2))
            biblioteka.dodaj_ksiazke(Book("Metro 2033", "Dmitrij Głuchowski", 4))
            biblioteka.dodaj_ksiazke(Book("Harry Potter i Kamień Filozoficzny", "J.K. Rowling", 1))
            biblioteka.dodaj_ksiazke(Book("Zbrodnia i kara", "Fiodor Dostojewski", 2))

            biblioteka.dodaj_uzytkownika(Reader("Amelia", "1234"))
            biblioteka.dodaj_uzytkownika(Reader("Adrianna", "abcd"))
            biblioteka.dodaj_uzytkownika(Reader("Kacper", "haslo"))
            biblioteka.dodaj_uzytkownika(Librarian("Admin", "admin"))

            print("=== System obsługi biblioteki ===")

            while True:
                zalogowany_uzytkownik = biblioteka.logowanie()

                if zalogowany_uzytkownik is not None:
                    if isinstance(zalogowany_uzytkownik, Reader):
                        menu_czytelnika(biblioteka, zalogowany_uzytkownik)
                    elif isinstance(zalogowany_uzytkownik, Librarian):
                        menu_bibliotekarza(biblioteka)

                decyzja = input("\nCzy chcesz zalogować się ponownie? (tak/nie): ")

                if decyzja.lower() != "tak":
                    print("Program zakończony.")
                    break

        uruchom_program()