from django.contrib import messages
from django.contrib import admin

# aggiorna lo slug per le categorie selezionate
@admin.action(description='Aggiorna slug categorie selezionate')
def categories_update_slug(modeladmin, request, queryset):
    for item in queryset:
        item.save()
    messages.add_message(request, messages.SUCCESS, 'Slug aggiornati')
