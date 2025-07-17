from django.contrib import admin
from .models import Subscriber, SubscriberSMS, Client, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'gdpr_consent', 'create_date')
    search_fields = ('email', 'phone')
    list_filter = ('gdpr_consent',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'gdpr_consent', 'create_date')
    search_fields = ('email',)
    list_filter = ('gdpr_consent',)


@admin.register(SubscriberSMS)
class SubscriberSMSAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'gdpr_consent', 'create_date')
    search_fields = ('phone',)
    list_filter = ('gdpr_consent',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'create_date')
    search_fields = ('email', 'phone')
