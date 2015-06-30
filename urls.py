from django.conf.urls import url

urlpatterns = [
    url(r'^webhook', 'telegrambot.views.webhook'),
]
