# Django – Migracja Subskrybentów do User'a

Projekt zawiera komendy Django do migracji danych:
- python manage.py migrate_subscribers
- python manage.py update_gdpr_consent

## 📦 Wymagania

- Python 3.10
- Django 5.2

## Instalacja

- git clone https://github.com/marcin86junior/MigrationTask.git .
- cd Zadanie_1
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- test 123
- python manage.py runserver
- http://127.0.0.1:8000/admin


## 🚀 Zadanie:
- Załaduj dane testowe: Subscriber, SubscriberSMS, Client:  
- python manage.py load_test_data
- Sprawdź dane -> http://127.0.0.1:8000/admin
- Uruchom migrację do modelu User:  
- python manage.py migrate_subscribers
- Sprawdz zmianę -> http://127.0.0.1:8000/admin
- Zaktualizuj gdpr_consent dla istniejących użytkowników: 
- python manage.py update_gdpr_consent
- Sprawdz zmianę -> http://127.0.0.1:8000/admin


## 🔍 Weryfikacja update_gdpr_consent:

- python manage.py update_gdpr_consent
- Rozpoczynam aktualizację gdpr_consent...
- Zaktualizowano User existing_user@example.com: gdpr_consent False -> True
- Zaktualizowano User sms_exists@example.com: gdpr_consent False -> True
- Zaktualizowano User conflicted@example.com: gdpr_consent False -> True
- Aktualizacja zakończona. Zaktualizowano 3 użytkowników.

