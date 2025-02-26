from django.contrib import admin
from .models import Corporation, Investment, Usuario


# Register your models here.
admin.site.register(Corporation)
admin.site.register(Investment)
admin.site.register(Usuario)


class InvestmentAdmin(admin.ModelAdmin):
    readonly_fields = ("total_investment",)
    list_display = (
        "user",
        "corporation",
        "stocks_amount",
        "price_at_purchase",
        "total_investment",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__name", "corporation__name")
    list_filter = ("created_at", "updated_at")
