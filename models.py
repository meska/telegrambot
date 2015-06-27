from django.db import models
from django.core.cache import cache
from django.conf import settings
from cStringIO import StringIO
import sys


# Create your models here.
class TelegramUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    last_message = models.TextField(blank=True,null=True)

    
    class Meta:
        app_label = 'telegram_bot'    
    
    
    
########################################################################
class TelegramUserAlert(models.Model):
    """
    """
    user = models.ForeignKey(TelegramUser)
    camera = models.CharField(max_length=100)
    receive_alerts = models.BooleanField(default=False)
    receive_alerts_from = models.TimeField(null=True,blank=True)
    receive_alerts_to = models.TimeField(null=True,blank=True)
    

    #----------------------------------------------------------------------
    def sendAlert(self,event,tipo):
        from telegram_bot.wrapper import Bot
        if tipo == 'motion':
            if not cache.get("%s-%s-%s" % (__name__,tipo,self.user.user_id)):
                b = Bot(settings.TELEGRAM_BOT_TOKEN)
                fp = StringIO()
                event.snapshot().save(fp,'JPEG')
                fp.seek(0)            
                b.sendPhoto(self.user.user_id, fp, caption='motion alert %s' % self.camera.name)
                cache.set("%s-%s-%s" % (__name__,tipo,self.user),True,30)

        if tipo == 'picture':
            img = event.img()
            if img:
                if not cache.get("%s-%s-%s" % (__name__,tipo,self.user.user_id)):
                    b = Bot(settings.TELEGRAM_BOT_TOKEN)
                    fp = StringIO()
                    event.img().save(fp,'JPEG')
                    fp.seek(0)            
                    b.sendPhoto(self.user.user_id, fp, caption='picture alert %s' % self.camera.name)
                    cache.set("%s-%s-%s" % (__name__,tipo,self.user.user_id),True,30)
        
    class Meta:
        app_label = 'telegram_bot'      
        
    
    