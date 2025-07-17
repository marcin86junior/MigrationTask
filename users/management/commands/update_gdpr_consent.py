from django.core.management.base import BaseCommand
from users.models import Subscriber, SubscriberSMS, Client, User


class Command(BaseCommand):
    help = "Aktualizuje gdpr_consent w User na podstawie nowszych danych z Subscriber i SubscriberSMS."

    def handle(self, *args, **kwargs):
        self.stdout.write("Rozpoczynam aktualizację gdpr_consent...")

        users = User.objects.all().select_related()

        updated_count = 0

        for user in users:
            # Znajdź powiązanego subskrybenta Subscriber
            subscriber = Subscriber.objects.filter(email=user.email).first()
            # Znajdź powiązanego subskrybenta SubscriberSMS
            subscriber_sms = SubscriberSMS.objects.filter(phone=user.phone).first()

            # Jeśli brak obu, pomiń
            if not subscriber and not subscriber_sms:
                continue

            # Przygotuj listę potencjalnych źródeł aktualizacji (gdpr_consent, create_date)
            candidates = []

            if subscriber:
                candidates.append(('subscriber', subscriber.gdpr_consent, subscriber.create_date))
            if subscriber_sms:
                candidates.append(('subscriber_sms', subscriber_sms.gdpr_consent, subscriber_sms.create_date))

            # Jeśli użytkownik powstał z połączenia Client (email i phone pasujące)
            client_exists = Client.objects.filter(email=user.email, phone=user.phone).exists()

            # Wybierz najnowszy obiekt po create_date
            latest = max(candidates, key=lambda x: x[2])

            # Aktualizacja jeśli data subskrybenta jest nowsza niż użytkownika
            if latest[2] > user.create_date:
                old_gdpr = user.gdpr_consent
                user.gdpr_consent = latest[1]
                user.save(update_fields=['gdpr_consent'])
                updated_count += 1
                self.stdout.write(
                    f"Zaktualizowano User {user.email}: gdpr_consent {old_gdpr} -> {user.gdpr_consent}"
                )

        self.stdout.write(f"Aktualizacja zakończona. Zaktualizowano {updated_count} użytkowników.")
