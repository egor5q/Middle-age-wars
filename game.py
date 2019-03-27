import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import units


class Game:
    
    def start(self):
        self.turn()
        
        
    def turn(self):
        maxspeed=0
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
        
    
    def __init__(self, fighters):   #{'fighter':ids,  'team':ct}
        self.players={}
        for ids in fighters:
            self.players.update(self.createunit(fighters[ids])) 
        self.turn=1
        self.currentplayer=None
        self.start()
    
    
    def createunit(self, unit):
        try:
            unit['fighter']+=''
            if unit['fighter']=='bear':
                x=units.Bear()
                x.controller='ai'
        except:
            if unit['fighter']['class']=='basic':
                x=units.Basic()
            elif unit['fighter']['class']=='warrior':
                x=units.Warrior()
            x.controller='player'
            x.id=unit['fighter']['id']
                
        x.team=unit['team']
            
        return {unit['id']:x}
        


