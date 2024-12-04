from django.contrib import admin

from wallet.models import Wallet, Statement

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'withdrawable_balance')


class StatementAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'type')


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Statement, StatementAdmin)
