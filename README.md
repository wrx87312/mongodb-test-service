📊 MongoDB Test Service
Aplikacja webowa oparta na Flask, która automatycznie testuje połączenie z bazą danych MongoDB, wykonuje serię testów diagnostycznych, generuje raporty (CSV + HTML), pakuje je do archiwum ZIP i umożliwia ich pobranie przez przeglądarkę.

🧪 Zakres testów:
Połączenie z bazą MongoDB

Wstawienie i odczyt dokumentu

Obsługa pustej kolekcji

Walidacja struktury dokumentu

🧰 Technologie:
Python 3.10+
Flask
PyMongo
MongoDB Atlas (lub inny URI MongoDB)
Render (do hostingu aplikacji)

🚀 Instrukcja uruchomienia
🔧 Lokalnie
Wymagania:
Python 3.10+
MongoDB URI (np. z MongoDB Atlas)
Plik .env zawierający zmienną środowiskową MONGO_URI

Krok po kroku:
bash
Kopiuj
Edytuj
# 1. Klonuj repozytorium
git clone https://github.com/twoj-login/mongodb-test-service.git
cd mongodb-test-service

# 2. Utwórz i aktywuj środowisko
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Stwórz plik .env
echo "MONGO_URI=mongodb+srv://uzytkownik:haslo@..." > .env

# 5. Uruchom aplikację
python app.py
Otwórz w przeglądarce: http://localhost:5000

☁️ W chmurze (Render.com)
Krok po kroku:
Zaloguj się lub zarejestruj na https://render.com

Połącz swoje konto z GitHubem

Utwórz nowy Web Service

Wybierz swoje repozytorium mongodb-test-service

Ustaw parametry:

Build Command: (puste — nie jest wymagane)

Start Command: python app.py

Environment: Python 3

Dodaj zmienną środowiskową:

MONGO_URI=mongodb+srv://uzytkownik:haslo@... (upewnij się, że znaki specjalne jak @, /, itp. są zakodowane — np. @ jako %40)

Deploy i poczekaj aż aplikacja wystartuje

✅ Gotowy link
Po wdrożeniu aplikacja będzie dostępna pod publicznym URL, np.:

👉 https://mongodb-test-service-j2xc.onrender.com

Wejdź na:
📄 https://mongodb-test-service-j2xc.onrender.com/generuj-raport
...aby pobrać raport ZIP.

📁 Struktura projektu
bash
Kopiuj
Edytuj
mongodb-test-service/
├── app.py              # Główna aplikacja Flask
├── requirements.txt    # Zależności
├── .env                # Zmienna MONGO_URI (niewersjonowana)
├── raport.csv          # Raport CSV (generowany)
├── raport.html         # Raport HTML (generowany)
├── raport_mongodb.zip  # ZIP z raportami (generowany)
└── README.md           # Ten plik
🧼 Przykład działania
✔️ Połączenie z MongoDB: OK

✔️ Insert i odczyt dokumentu: OK

✔️ Pusta kolekcja: OK

✔️ Walidacja dokumentu: OK

📎 Raporty: raport.csv, raport.html, raport_mongodb.zip

🔐 Uwaga bezpieczeństwa
Nie przechowuj prawdziwego hasła w MONGO_URI w repozytorium. Użyj .env i Render Environment Variables.
