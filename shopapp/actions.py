from django.contrib import messages
from django.contrib import admin


@admin.action(description='Scarica logo per le marche selezionati')
def manufacturers_download_logo(modeladmin, request, queryset):
    for item in queryset:
        item.download_logo()
    messages.add_message(request, messages.SUCCESS, 'Download completato')
