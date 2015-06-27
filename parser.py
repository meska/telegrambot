#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Marco Mescalchin --<>
  Purpose: incoming messages parser for telegram bot, TODO: use signals for better separation
  Created: 06/25/15
"""

from cStringIO import StringIO
import re
import requests,json
from threading import Thread



class Parser():
    patterns = [
        ['/help','help'],
        ['/show','show'],
        ['/gnocca','boobs'],
        [u"(.*)\s+\U0001f4f7",'showcam'],   
        [u"(.*)\s+\U0001f514",'alert'],
        [u"(.*)\s+\U0001f515",'alert'],
        ['/alerts','alerts'],
    ]    
    
    
    def __init__(self,bot):
        self.bot = bot
    
    def getUser(self,message):
        # get or create user from db
        from telegrambot.models import TelegramUser
        u,created = TelegramUser.objects.get_or_create(user_id=message['from']['id'])
        save = False

        if 'username' in message['from']:
            if not u.username == message['from']['username']:
                u.username = message['from']['username']
                save =True

        if 'first_name' in message['from']:
            if not u.first_name == message['from']['first_name']:
                u.first_name = message['from']['first_name']
                save =True

        if 'last_name' in message['from']:
            if not u.last_name == message['from']['last_name']:
                u.last_name = message['from']['last_name']
                save =True
        if save:
            u.save()
            
        if created:
            # send welcome message
            self.bot.sendMessage(u.user_id,"Welcome to MotionBot") #,reply_to_message_id=message['message_id'])
        return u
    
    def split(self,arr, size):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr   = arr[size:]
        arrs.append(arr)
        return arrs    


    def boobs(self,message,chat_id,user):
        # just for fun
        print("want boobs!")
        f = requests.get("http://api.oboobs.ru/noise/1")
        res = f.json()
        boobsurl = 'http://media.oboobs.ru/' + res[0]['preview']
        res = requests.get(boobsurl)
        fp = StringIO()
        fp.write(res.content)
        fp.seek(0)
        self.bot.sendPhoto(chat_id,fp)

    def butts(self,message,chat_id,user):
        # just for fun
        print("want butts!")
        f = requests.get("http://api.obutts.ru/noise/1")
        res = f.json()
        boobsurl = 'http://media.obutts.ru/' + res[0]['preview']
        res = requests.get(boobsurl)
        fp = StringIO()
        fp.write(res.content)
        fp.seek(0)
        self.bot.sendPhoto(chat_id,fp)             


    def help(self,message,chat_id,user):
        self.bot.action_typing(chat_id)
        self.bot.sendMessage(chat_id,"Help Text goes here" ) # ,reply_to_message_id=message['message_id'])
        return        
    
    
    def show(self,message,chat_id,user):
        self.bot.action_typing(chat_id)
        # carica l'elenco delle telecamere
        from motioncontrol.models import Cam
        keys = []
        for c in Cam.objects.all():
            if c.name and c.online:
                keys.append(u"%s \U0001f4f7" % c.name) 
        if keys:
            self.bot.sendMessage(chat_id,"Choose online cams?",reply_markup={'keyboard':self.split(keys,3)} )# ,reply_to_message_id=message['message_id'])
        else:
            self.bot.sendMessage(chat_id,"No cams online at the moment")# ,reply_to_message_id=message['message_id'])
        
        return        
    
    def alerts(self,message,chat_id,user):
        self.bot.action_typing(chat_id)
        # carica l'elenco delle telecamere
        from motioncontrol.models import Cam
        from telegrambot.models import TelegramUserAlert
        
        keys = []
        for c in Cam.objects.all():
            if c.name:
                alert,created = TelegramUserAlert.objects.get_or_create(user=user,camera=c)
                if alert.receive_alerts:
                    keys.append(u"%s \U0001f515" % c.name) 
                else:
                    keys.append(u"%s \U0001f514" % c.name) 
                    
        self.bot.sendMessage(chat_id,"Enable / Disable Alert on Camera?",reply_markup={'keyboard':self.split(keys,3)} )# ,reply_to_message_id=message['message_id'])
        user.last_message = message
        user.save()            
        
        return         
    
    def alert(self,message,chat_id,user,args):
        # mostro la telecamera scelta
        from motioncontrol.models import Cam
        self.bot.action_typing(chat_id)

        c = Cam.objects.get(name=args[0])
        alert,created = TelegramUserAlert.objects.get_or_create(user=user,camera=c)
        if created:
            # attivo
            alert.receive_alerts = True
            self.bot.sendMessage( user.user_id,"Alerts Attivati su %s" % args[0] ,reply_markup={'hide_keyboard':True} )
        else:
            if alert.receive_alerts:
                alert.receive_alerts = False
                self.bot.sendMessage( user.user_id,"Alerts Disattivati su %s" % args[0] ,reply_markup={'hide_keyboard':True} )
            else:
                alert.receive_alerts = True
                self.bot.sendMessage( user.user_id,"Alerts Attivati su %s" % args[0] ,reply_markup={'hide_keyboard':True} )
        alert.save()
            
    
    
    def showcam(self,message,chat_id,user,args):
        # mostro la telecamera scelta
        from motioncontrol.models import Cam
        self.bot.action_typing(chat_id)
        try:
            c = Cam.objects.get(name=args[0])
            fp = StringIO()
            c.snapshot().save(fp,'JPEG')
            fp.seek(0)
            self.bot.sendPhoto(user.user_id,fp,reply_markup={'hide_keyboard':True})
        except:
            self.bot.sendMessage( user.user_id,"Error Retrieving Snapshot from %s" % text ,reply_markup={'hide_keyboard':True} )

    
    def parse(self,message):
        user = self.getUser(message)
        text = message['text']

        
        # find method
        for c in self.patterns:
            m = re.match(c[0],text)
            if m:
                if m.groups():
                    getattr(self,c[1])(text,user.user_id,user,m.groups())
                else:
                    getattr(self,c[1])(text,user.user_id,user)
                return True
                

        # defaults
        return True
        # discard
        #self.bot.sendMessage(user.user_id,"",reply_to_message_id=message['message_id'],reply_markup={'hide_keyboard':True})