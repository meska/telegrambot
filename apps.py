from django.apps import AppConfig
from django.conf import settings
from threading import Timer
import sys

class TelegramBotConfig(AppConfig):
    name = 'telegrambot'
    verbose_name = "Telegram Bot"

    def ready(self):
        from django.conf import settings
        if 'runserver' in sys.argv:
            from telegrambot.wrapper import Bot
            b = Bot(settings.TELEGRAM_BOT_TOKEN)
            if not settings.TELEGRAM_USE_WEBHOOK:
                b.post('setWebhook',{'url':''})
                print("Telegram WebHook Disabled")
                Timer(10,b.getUpdates).start()
                
        if settings.TELEGRAM_USE_WEBHOOK:
            from telegrambot.wrapper import Bot
            b = Bot(settings.TELEGRAM_BOT_TOKEN)            
            b.setWebhook()               

        import telegrambot.signals
        import telegrambot.connectors