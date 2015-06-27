import sys


def setWebhook():
    from django.conf import settings
    from telegram_bot.wrapper import Bot
    b = Bot(settings.TELEGRAM_BOT_TOKEN)
    b.setWebhook()

if 'runserver' in sys.argv:
    from threading import Timer
    Timer(10,setWebhook).start()
