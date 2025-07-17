from django.db import models


class Subscriber(models.Model):
    create_date = models.DateTimeField()
    email = models.EmailField(unique=True)
    gdpr_consent = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class SubscriberSMS(models.Model):
    create_date = models.DateTimeField()
    phone = models.CharField(max_length=20, unique=True)
    gdpr_consent = models.BooleanField(default=False)

    def __str__(self):
        return self.phone


class Client(models.Model):
    create_date = models.DateTimeField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)  # NOT unique!

    def __str__(self):
        return self.email


class User(models.Model):
    create_date = models.DateTimeField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    gdpr_consent = models.BooleanField(default=False)

    def __str__(self):
        return self.email
