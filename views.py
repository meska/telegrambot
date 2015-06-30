from django.http import HttpResponse
from telegrambot.wrapper import Bot 
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def webhook(request):
    b = Bot(settings.TELEGRAM_BOT_TOKEN)
    return HttpResponse(b.webhook(request))