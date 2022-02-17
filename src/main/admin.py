from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import User, Transport, Trip, TravelParticipant, Dialog, Message, FAQ


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthday', 'avatar', 'email', 'phone_number', 'location')
    list_filter = ('location',)


class TravelParticipantInline(admin.TabularInline):
    model = TravelParticipant


class TransportAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)


class TripAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'author', 'get_user_last_name_link', 'description', 'is_available', 'city_information', 'date')
    list_filter = ('is_available', 'date', 'country')
    ordering = ('-is_available',)
    inlines = [TravelParticipantInline, ]

    def get_format_html(self, app: str, model_name: str, model_id: str, page: str, link_name: str):
        # url = reverse(f'admin:main_user_changelist')
        url = reverse(f'admin:{app}_{model_name}_{page}', args=[model_id])
        return format_html(f'<b><a href="{url}">{link_name}</a></b>')

    def get_user_last_name_link(self, obj):
        last_name = obj.author.last_name
        user_id = obj.author.id
        link = self.get_format_html('main', 'user', user_id, 'change', last_name)
        return link


class TravelParticipantAdmin(admin.ModelAdmin):
    list_display = ('trip', 'participant', 'is_approved')
    list_filter = ('is_approved', 'trip')


class DialogAdmin(admin.ModelAdmin):
    list_display = ('first_participant', 'second_participant')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('dialog', 'sender', 'receiver', 'is_read', 'text')
    list_filter = ('is_read',)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    ordering = ('question',)


admin.site.register(Transport, TransportAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(TravelParticipant, TravelParticipantAdmin)
admin.site.register(Dialog, DialogAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(FAQ, FAQAdmin)
