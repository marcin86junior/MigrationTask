import csv
from django.core.management.base import BaseCommand
from django.db.models import Count
from users.models import User, Client, Subscriber, SubscriberSMS


class Command(BaseCommand):
    help = "Migrates Subscribers and SubscriberSMS to Users"

    def handle(self, *args, **kwargs):
        print("🔁 Start migracji użytkowników...\n")
        self.migrate_subscribers()
        self.migrate_sms_subscribers()
        print("\n✅  Migracja zakończona.\n")

    def migrate_subscribers(self):
        print("📨 Migracja Subscriber → User...")

        conflict_file = open("subscriber_conflicts.csv", "w", newline="", encoding="utf-8")
        conflict_writer = csv.writer(conflict_file)
        conflict_writer.writerow(["subscriber_id", "email"])

        duplicate_phones = (
            Client.objects.values("phone")
            .annotate(count=Count("id"))
            .filter(count__gt=1)
            .values_list("phone", flat=True)
        )
        duplicate_phones_set = set(duplicate_phones)

        for subscriber in Subscriber.objects.all().iterator():
            if User.objects.filter(email=subscriber.email).exists():
                print(f"⏩  Pominięto Subscriber {subscriber.email} – User już istnieje.")
                continue

            client = Client.objects.filter(email=subscriber.email).first()
            if client:
                if client.phone in duplicate_phones_set:
                    conflict_writer.writerow([subscriber.id, subscriber.email])
                    print(f"⚠️ Konflikt (duplikat telefonu): {subscriber.email} → zapisano do subscriber_conflicts.csv")
                    continue

                phone_conflict = User.objects.filter(phone=client.phone).exclude(email=client.email).exists()
                if phone_conflict:
                    conflict_writer.writerow([subscriber.id, subscriber.email])
                    print(f"⚠️ Konflikt (telefon już użyty przez inny email): {subscriber.email} → zapisano do subscriber_conflicts.csv")
                    continue

                User.objects.create(
                    email=client.email,
                    phone=client.phone,
                    gdpr_consent=subscriber.gdpr_consent,
                    create_date=subscriber.create_date,
                )
                print(f"✅  Utworzono użytkownika z Client: {client.email}")
            else:
                User.objects.create(
                    email=subscriber.email,
                    phone="",
                    gdpr_consent=subscriber.gdpr_consent,
                    create_date=subscriber.create_date,
                )
                print(f"✅  Utworzono użytkownika bez Client (brak telefonu): {subscriber.email}")

        conflict_file.close()
        print("✔️ Zakończono migrację Subscriber.\n")

    def migrate_sms_subscribers(self):
        print("📱 Migracja SubscriberSMS → User...")

        conflict_file = open("sms_subscriber_conflicts.csv", "w", newline="", encoding="utf-8")
        conflict_writer = csv.writer(conflict_file)
        conflict_writer.writerow(["subscriber_sms_id", "phone"])

        duplicate_phones = (
            Client.objects.values("phone")
            .annotate(count=Count("id"))
            .filter(count__gt=1)
            .values_list("phone", flat=True)
        )
        duplicate_phones_set = set(duplicate_phones)

        for sms_sub in SubscriberSMS.objects.all().iterator():
            if User.objects.filter(phone=sms_sub.phone).exists():
                print(f"⏩  Pominięto SubscriberSMS {sms_sub.phone} – User już istnieje.")
                continue

            client = Client.objects.filter(phone=sms_sub.phone).first()
            if client:
                if client.phone in duplicate_phones_set:
                    conflict_writer.writerow([sms_sub.id, sms_sub.phone])
                    print(f"⚠️ Konflikt (duplikat telefonu): {sms_sub.phone} → zapisano do sms_subscriber_conflicts.csv")
                    continue

                email_conflict = User.objects.filter(email=client.email).exclude(phone=client.phone).exists()
                if email_conflict:
                    conflict_writer.writerow([sms_sub.id, sms_sub.phone])
                    print(f"⚠️ Konflikt (email już użyty z innym telefonem): {sms_sub.phone} → zapisano do sms_subscriber_conflicts.csv")
                    continue

                User.objects.create(
                    email=client.email,
                    phone=client.phone,
                    gdpr_consent=sms_sub.gdpr_consent,
                    create_date=sms_sub.create_date,
                )
                print(f"✅  Utworzono użytkownika z Client: {client.email}")
            else:
                User.objects.create(
                    email="",
                    phone=sms_sub.phone,
                    gdpr_consent=sms_sub.gdpr_consent,
                    create_date=sms_sub.create_date,
                )
                print(f"✅  Utworzono użytkownika bez Client (brak emaila): {sms_sub.phone}")

        conflict_file.close()
        print("✔️ Zakończono migrację SubscriberSMS.\n")