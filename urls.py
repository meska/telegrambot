from django.conf.urls import include, url

urlpatterns = [
    url(r'^webhook', 'telegram_bot.views.webhook'),
]
