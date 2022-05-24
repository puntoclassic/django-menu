from django.contrib.admin import SimpleListFilter


class ManufacturerHasLogoFilter(SimpleListFilter):
    title = 'Marche con logo'
    parameter_name = 'hasLogoUrl'

    def lookups(self, request, model_admin):
        return [
            ("yes", "Si"),
            ("no", "No"),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(logo_url__iexact="")
        if self.value():
            return queryset.filter(logo_url__iexact="")
