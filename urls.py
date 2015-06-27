from django.conf.urls import include, url

urlpatterns = [
    url(r'^webhook', 'telegrambot.views.webhook'),
]
