from django.contrib import admin
from telegram_bot.models import *
# Register your models here.

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id','username', 'first_name', 'last_name')
    #list_filter = ('server__name',)
    
admin.site.register(TelegramUser,TelegramUserAdmin)
