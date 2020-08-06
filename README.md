# Zadanie rekrutacyjne Profil Software
## 1. Uruchomienie programu
### Krok 1
Uruchom plik `models.py`, który stworzy bazę danych.
### Krok 2
Urochom plik `db_populate.py`, który wypełni bazę danymi uzyskanymi z API.
### Krok 3
Uruchom plik `app.py` w terminalu by odpalić wybrane komendy.
## 2. Dostępne komendy
Użyj `/app.py` z dostępnymi komendami:
- `-h, --help` - Menu pomocy,
- `-g, --gender_proportion` - Proporcję płci w badanej grupie,
- `-a PARAMETR, --average_age PARAMETR` - Średni wiek badanej grupy. `PARAMETR` do wyboru z `["total", "male", "female"]`. W przypadku gdy nie podany, domyślnie zwraca `total`,
- `-c N, --common_cities N` - `N`-liczba najczęsciej występujących miast wrac z ilością wystąpień,
- `-p N, --common_password N` - `N`-liczba najczęściej występujących haseł wraz z ilością wystąpień,
- `born_between` - Lista osób urodzonych pomiędzy podaną `START_DAT` a `END_DATE`. Obie daty są wymagane. 
    Przykład: `app.py born_between -s 2000-10-10 -e 2000-11-11`:
    - `-s START_DATE, --start_date START_DATE` - Data początku badanego okresu(YYYY-MM-DD),
    - `-e END_DATE, --end_date END_DATE` - Data końca badanego okresu(YYYY-MM-DD),
- `-s, --safest_password` - Najbezpieczniejsze hasło w bazie wraz z liczbą zdobtyh punktów.
## 3. Dodatkowe informacje
- Poprawnie utworzona baza danych zawierać będzie dane 1000 losowo wygenerowanych osób,
- Hasła zawierać będą od 1 do 16 znaków (w tym wielkie i małe litery, cyfry oraz znaki specjalne),
- Lista wszystkich wymaganych wtyczek dostępna jest w pliku `requirement.txt`
## 4. Informację i kontakt do autora
Łukasz Sanewski email: lukaszsanewski@gmail.com