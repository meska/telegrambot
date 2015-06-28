from telegrambot.signals import message_received
from django.dispatch import receiver


#@receiver(message_received)
#def receive_message(sender, **kwargs):
    #from parser import Parser
    #p = Parser(sender)
    #p.parse(kwargs['message'])