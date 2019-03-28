import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import units
from tools import medit
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

games={}
count=0

class Game:
    
    def start(self):
        for ids in self.players:
            player=self.players[ids]
            enemys=''
            if player.controller!='ai':
                for idss in self.players:
                    enemy=self.players[idss]
                    if enemy.team!=player.team:
                        enemys+=enemy.name+'\n'
                bot.send_message(player.id, 'Ваши соперники:\n\n'+enemys)
        self.turn()
        
        
    def turn(self):
        maxspeed=-1000
        for ids in self.players:
            player=self.players[ids]
            if player.speed>maxspeed:
                maxspeed=player.speed
                
        spisok=[]
        for ids in self.players:
            player=self.players[ids]
            if player.speed==maxspeed:
                spisok.append(player)
                
        self.currentplayer=random.choice(spisok)
        self.currentplayer.turn(self)
        for ids in self.players:
            player=self.players[ids]
            if player.controller!='ai':
                bot.send_message(player.id, 'Начался ход игрока '+self.currentplayer.name+'!')
        self.currentplayer.speed-=self.currentplayer.weight
        self.timer=threading.Timer(60, self.endturn)
        self.timer.start()
        
    def endturn(self):
        try:
            self.timer.stop()
            self.timer=None
        except:
            pass
        for ids in self.players:
            player=self.players[ids]
            if 'stunned' not in player.statuses:
                player.speed+=player.speedregen
            if player.hp<=0:
                player.dead=True
        self.turn+=1
        self.currentplayer=None
        if self.endgame()==False:
            self.turn()
        else:
            for ids in self.players:
                player=self.players[ids]
                try:
                    bot.send_message(player.id, 'Игра окончена!')
                except:
                    pass
            del games[self.id]
            
        
    def endgame(self):
        teams=[]
        for ids in self.players:
            player=self.players[ids]
            if player.team not in teams:
                if player.dead==False:
                    teams.append(player.team)
        if len(teams)<=1:
            return True
        return False    
    
    def __init__(self, fighters):   #{'fighter':ids,  'team':ct}
        global count
        count+=1
        self.players={}
        self.timer=None
        for ids in fighters:
            self.players.update(self.createunit(fighters[ids])) 
        self.turn=1
        self.currentplayer=None
        games.update({count:self})
        self.id=count
        self.start()
    
    
    def createunit(self, unit):
        try:
            unit['fighter']+=''
            if unit['fighter']=='bear':
                x=units.Bear()
                x.controller='ai'
                x.name='Медведь'
        except:
            if unit['fighter']['type']=='basic':
                x=units.Unit()
            elif unit['fighter']['type']=='warrior':
                x=units.Warrior()
            x.name=unit['name']
            x.controller='player'
            x.id=unit['fighter']['id']
                
        x.team=unit['team']
            
        return {unit['id']:x}
        


