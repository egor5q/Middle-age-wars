import game
from tools import medit
import os
import telebot
from telebot import types
import traceback
import random

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

classes=['warrior', 'bower', 'mage', 'assasin', 'basic']  #types

resists=['physic', 'magic', 'fire', 'dark', 'light']

class Unit:
    
    def __init__(self):
        self.hp=200
        self.name=None
        self.team=None
        self.id=None
        self.dead=False
        self.dmg=[16, 28]
        self.luck=0
        self.physresist=0
        self.controller=None
        self.body={
            'righthand':None,
            'lefthand':None,
            'head':None,
            'body':None,
            'boots':None
            
        }
        self.dmgbuff=[0, 0]
        self.mainhand='righthand'
        self.inentory=[]
        self.type='basic'
        self.mana=300
        self.statuses=[]
        self.skills=[]
        self.speedregen=400
        self.speed=self.speedregen
        self.weight=400     # В ход у юнита регенится (self.speedregen) скорости. На ход юнит трати (self.weight) скорости. 
        self.agility=50     # У кого на данный момент больше скорости - тот ходит. Если одинаково - рандом.
        self.accuracy=0
        self.message=None
    
    
    def recievedmg(self, dmg):
        self.hp-=dmg
        return dmg
    
    
    def skillmenu(self):
        for ids in self.skills:
            if ids.cd<=0:
                pass # Дать разыграть

        
        
    def recievehit(self, unit):
        d1=0
        d2=0
        cgame=findgame(self)
        if unit.body[unit.mainhand]!=None:
            weapon=unit.body[unit.mainhand]
            d1=weapon.dmg[0]
            d2=weapon.dmg[1]
        try:
            dmg=random.randint((unit.dmg[0]+unit.dmgbuff[0]+d1), (unit.dmg[1]+unit.dmgbuff[1]+d2))
        except Exception as e:
            bot.send_message(441399484, traceback.format_exc())
            dmg=unit.dmg[0]+unit.dmgbuff[0]+d1
        dmg=self.recievedmg(dmg)
        for ids in cgame.players:
            if cgame.players[ids].controller!='ai':
                bot.send_message(cgame.players[ids].id, unit.name+' атакует '+self.name+' с помощью '+weapontoname(unit.body[unit.mainhand])+'! Нанесено '+str(dmg)+' урона.')

    
    
    def attack(self, target):
        pass
    
    
    def endturn(self):
        pass
    
    
    def turn(self, game):
        if self.controller=='player':
            attackmenu(self)
    
    def changedmg(dmg, coef):
        result=[]
        result.append(int(dmg[0]*coef))
        result.append(int(dmg[1]*coef))
        return result
    
    def changecoef(stat, coef):
        return stat*coef
        
    
    
class Warrior(Unit):
    
    def __init__(self):
        super().__init__()
        self.hp=int(self.hp*1.35)
        self.dmg=self.changedmg(self.dmg, 0.75)
        self.type='warrior'
        self.agility=int(self.agility*0.7)
        
        
class Bower(Unit):
    
    def __init__(self):
        super().__init__()
        self.hp=int(self.hp*0.8)
        self.dmg=self.changedmg(self.dmg, 1.2)
        self.type='bower'
        self.accuracy+=30
        self.agility=int(self.agility*1.1)
        self.skills.append('multishot')
    
    
    
class Bear(Warrior):
    def __init__(self):
        super().__init__()
    
    
class Weapon:
    
    def __init__(self):
        self.dmg=[1, 1]
        self.skills=[]
        self.specialattack=None
        self.weight=50
        
        
class Baseball(Weapon):
    
    def __init__(self):
        super().__init__()
        self.dmg=[2, 3]


class Skill:
    
    def __init__(self):
        self.cd=1
        self.maxcd=1
        
        
        
class Multishot(Skill):
    
    def __init__(self):
        super().__init__()
        self.maxcd=4
        self.cd=self.maxcd
        self.name='multishot'
        

def handtotext(x):
    if x=='righthand':
        return 'Правая'
    elif x=='lefthand':
        return 'Левая'
    
    
def armortoname(x):
    if x==None:
        return 'Ничего'
    
    
def classtoname(x):
    y='Ошибка'
    if x=='basic':
        return 'Базовый'
    if x=='warrior':
        return 'Воин'
    if x=='bower':
        return 'Лучник'
    if x=='mage':
        return 'Маг'
    if x=='assasin':
        return 'Ассасин'
    return y
    
def weapontoname(x):
    if x=='baseball':
        return 'битой'
    return 'кулаками'
    

def playerinfo(player):
    text=''
    text+='Класс: '+classtoname(player.type).lower()
    text+='♥️Хп: '+str(player.hp)+'\n'
    text+='💢Урон: '+str(player.dmg[0]+player.dmgbuff[0])+'-'+str(player.dmg[1]+player.dmgbuff[1])+'\n'
    text+='🏃‍♂️Скорость: '+str(player.speedregen)+'\n'
    text+='Экипировка:\n'
    text+='  Голова: '+armortoname(player.body['head']).lower()+'\n'
    a=''
    b=''
    if player.mainhand=='righthand':
        a='(текущая)'
    if player.mainhand=='lefthand':
        b='(текущая) '
    text+='  Правая '+a+'рука: '+armortoname(player.body['righthand']).lower()+'\n'
    text+='  Левая '+b+'рука: '+armortoname(player.body['lefthand']).lower()+'\n'
    text+='  Туловище: '+armortoname(player.body['body']).lower()+'\n'
    return text
    
def findgame(player=None):
    g=None
    cgame=None
    if player!=None:
        for ids in game.games:
            g=game.games[ids]
            if player.id in g.players:
                cgame=g
    return cgame
    
    
def choicetarget(player):
    cgame=findgame(player=player)
    if cgame!=None:
        kb=types.InlineKeyboardMarkup()
        enemys=[]
        for ids in cgame.players:
            target=cgame.players[ids]
            if target.team!=player.team:
                enemys.append(target)
        for ids in enemys:
            kb.add(types.InlineKeyboardButton(text=ids.name+'('+str(ids.hp)+'♥️)', callback_data='atk '+str(ids.id)))
        kb.add(types.InlineKeyboardButton(text='Отмена', callback_data='mainmenu'))
        if player.message!=None:
            medit('Выберите цель.', player.message.chat.id, player.message.message_id, reply_markup=kb)
        else:
            bot.send_message(player['id'], 'Выберите цель.', reply_markup=kb)
    
    
def attackmenu(player):
    text=playerinfo(player)
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Физ. атака', callback_data='p_attack'),types.InlineKeyboardButton(text='Скиллы', callback_data='skills'))
    kb.add(types.InlineKeyboardButton(text='Инвентарь', callback_data='inventory'),types.InlineKeyboardButton(text='Сменить руку', callback_data='handchange'))
    kb.add(types.InlineKeyboardButton(text='Закончить ход', callback_data='endturn'))
    if player.message==None:
        msg=bot.send_message(player.id, text, reply_markup=kb)
        player.message=msg
    else:
        medit(text, player.message.chat.id, player.message.message_id)
    
    
