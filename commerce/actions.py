from django.contrib import messages
from django.contrib import admin


# scarica il logo per le categorie selezionate
@admin.action(description='Scarica logo per le marche selezionati')
def manufacturers_download_logo(modeladmin, request, queryset):
    for item in queryset:
        item.download_logo()
    messages.add_message(request, messages.SUCCESS, 'Download completato')


# aggiorna lo slug per le categorie selezionate
@admin.action(description='Aggiorna slug categorie selezionate')
def categories_update_slug(modeladmin, request, queryset):
    for item in queryset:
        item.save()
    messages.add_message(request, messages.SUCCESS, 'Slug aggiornati')
