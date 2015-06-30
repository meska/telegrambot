from django.contrib import admin
from telegrambot.models import TelegramUser
# Register your models here.

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id','username', 'first_name', 'last_name')
    #list_filter = ('server__name',)
    
admin.site.register(TelegramUser,TelegramUserAdmin)
