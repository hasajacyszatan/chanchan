# chanchan

Anonimowy imageboard zbudowany w oparciu o Django 5. Projekt inspirowany klasycznymi serwisami *chan, umożliwiający tworzenie postów, wątków oraz przeglądanie treści bez rejestracji.

## Technologie

- **Backend:** Python 3 / Django ~5.1.6
- **Frontend:** HTML, CSS, JavaScript
- **Baza danych:** SQLite (domyślnie)
- **API:** REST API (moduł `api`)
- **Skrypty pomocnicze:** PowerShell (`pwsh`)

## Struktura projektu

```
chanchan/
├── api/            # REST API
├── mysite/         # Konfiguracja projektu Django (settings, urls, wsgi)
├── posty/          # Główna aplikacja – posty, wątki, modele
├── pwsh/           # Skrypty PowerShell (pomocnicze)
├── static/         # Pliki statyczne (CSS, JS, obrazy)
├── templates/      # Szablony HTML
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## Wymagania

- Python 3.10+
- pip

## Instalacja

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/hasajacyszatan/chanchan.git
cd chanchan

# 2. Stwórz i aktywuj wirtualne środowisko
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Wykonaj migracje
python manage.py migrate

# 5. Uruchom serwer deweloperski
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem `http://127.0.0.1:8000/`.

## Panel administracyjny

Aby korzystać z panelu Django Admin:

```bash
python manage.py createsuperuser
```

Panel dostępny pod adresem `http://127.0.0.1:8000/admin/`.

## API

Projekt udostępnia REST API poprzez moduł `api`. Endpointy dostępne są pod ścieżką `/api/`.

## Licencja

Projekt udostępniony publicznie na GitHubie. Brak jawnie wskazanej licencji – wszelkie prawa zastrzeżone przez autora.