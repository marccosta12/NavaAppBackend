from django.contrib import admin
from .models import MethodCache, FxRateCache

@admin.register(MethodCache)
class MethodCacheAdmin(admin.ModelAdmin):
    list_display = ('method', 'country_from', 'country_to', 'currency_from', 'currency_to', 'fx_rate')
    search_fields = ('method', 'country_from', 'country_to')
    list_filter = ('country_from', 'country_to')

@admin.register(FxRateCache)
class FxRateCacheAdmin(admin.ModelAdmin):
    list_display = ('currency_from', 'currency_to', 'fx_rate', 'provider_name', 'source_updated_at')
    search_fields = ('currency_from', 'currency_to', 'provider_name')
    list_filter = ('currency_from', 'currency_to')