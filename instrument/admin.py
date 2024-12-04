from django.contrib import admin

from instrument.models import Instrument


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
