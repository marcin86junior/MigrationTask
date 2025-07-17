from django.core.management.base import BaseCommand
from users.models import Subscriber, SubscriberSMS, Client, User
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Load test data into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Tworzenie danych testowych...")

        # Czyścimy dane w bazie do testów
        User.objects.all().delete()
        Subscriber.objects.all().delete()
        SubscriberSMS.objects.all().delete()
        Client.objects.all().delete()

        base_time = timezone.now()

        # Subscriber

        # 1. Subscriber, który ma już odpowiadającego Usera (ma być pominięty)
        # Jeśli istnieje User z polem email takim samym jak w Subscriber pomiń subskrybenta
        # i nie twórz nowego użytkownika.

        existing_user = User.objects.create(
            email="existing_user@example.com",
            phone="123456789",
            gdpr_consent=False,
            create_date=base_time - timedelta(days=10)
        )
        Subscriber.objects.create(
            email="existing_user@example.com",
            gdpr_consent=True,
            create_date=base_time - timedelta(days=5)
        )

        # 2. Subscriber + Client = OK (unikalny telefon, brak konfliktu)
        # Jeśli istnieje Client z polem email takim jak Subscriber.email i nie istnieje
        # User z polem phone takim jak Client.phone i polem email różnym od
        # Client.email stwórz użytkownika na podstawie modelu Client

        Client.objects.create(
            email="new_subscriber_without_conflicts@example.com",
            phone="111111111",
            create_date=base_time - timedelta(days=6)
        )
        Subscriber.objects.create(
            email="new_subscriber_without_conflicts@example.com",
            gdpr_consent=True,
            create_date=base_time - timedelta(days=5)
        )

        # 3. Subscriber + Client + konflikt (User z tym telefonem, ale inny email)
        # Jeśli istnieje Client z polem email takim jak Subscriber.email i istnieje User z
        # polem phone takim jak Client.phone i polem email różnym od Client.email
        # zapisz id i email subskrybenta do pliku subscriber_conflicts.csv

        Client.objects.create(
            email="conflict@example.com",
            phone="222222222",
            create_date=base_time - timedelta(days=6)
        )
        User.objects.create(
            email="other@example.com",
            phone="222222222",
            gdpr_consent=False,
            create_date=base_time - timedelta(days=7)
        )
        Subscriber.objects.create(
            email="conflict@example.com",
            gdpr_consent=True,
            create_date=base_time - timedelta(days=3)
        )

        # 4. Subscriber bez odpowiadającego Clienta (stwórz User bez telefonu)
        # Jeśli nie istnieje Client z polem email takim jak Subscriber.email stwórz użytkownika z pustym polem phone.

        Subscriber.objects.create(
            email="new_subscriber_with_no_client@example.com",
            gdpr_consent=True,
            create_date=base_time - timedelta(days=2)
        )

        # 5. Client z nieunikalnym numerem telefonu (ma być zapisany do CSV)
        Client.objects.create(email="dup1@example.com", phone="999999999", create_date=base_time - timedelta(days=8))
        Client.objects.create(email="dup2@example.com", phone="999999999", create_date=base_time - timedelta(days=8))
        Subscriber.objects.create(email="dup1@example.com", gdpr_consent=False, create_date=base_time - timedelta(days=4))

        # SubscriberSMS

        # 6. SubscriberSMS już istnieje jako User
        User.objects.create(email="sms_exists@example.com", phone="777777777", gdpr_consent=False, create_date=base_time - timedelta(days=10))
        SubscriberSMS.objects.create(phone="777777777", gdpr_consent=True, create_date=base_time - timedelta(days=5))

        # 7. SMS bez Clienta
        SubscriberSMS.objects.create(phone="888888888", gdpr_consent=True, create_date=base_time - timedelta(days=3))

        # 8. SMS + Client = OK
        Client.objects.create(email="smsok@example.com", phone="333333333", create_date=base_time - timedelta(days=6))
        SubscriberSMS.objects.create(phone="333333333", gdpr_consent=True, create_date=base_time - timedelta(days=4))

        # 9. SMS + Client + konflikt
        Client.objects.create(email="smsconflict@example.com", phone="444444444", create_date=base_time - timedelta(days=6))
        User.objects.create(email="conflicted@example.com", phone="444444444", gdpr_consent=False, create_date=base_time - timedelta(days=7))
        SubscriberSMS.objects.create(phone="444444444", gdpr_consent=True, create_date=base_time - timedelta(days=2))

        # 10. Client z nieunikalnym numerem telefonu (SMS przypadek)
        Client.objects.create(email="smsdup1@example.com", phone="555555555", create_date=base_time - timedelta(days=8))
        Client.objects.create(email="smsdup2@example.com", phone="555555555", create_date=base_time - timedelta(days=8))
        SubscriberSMS.objects.create(phone="555555555", gdpr_consent=True, create_date=base_time - timedelta(days=2))

        self.stdout.write(self.style.SUCCESS("Testowe dane zostały załadowane."))
