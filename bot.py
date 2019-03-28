# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import game
import units
from tools import medit
import traceback
from telebot import types


token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

lobbys={}
codes=[]

client=MongoClient(os.environ['database'])
db=client.middleagewars
users=db.users

lvls={
    '1':10,
    '2':35,
    '3':100,
    '4':146,
    '5':223,
    '6':349,
    '7':611,
    '8':928,
    '9':1310,
    '10':1700,
    '11':2241,
    '12':2696,
    '13':3200,
    '14':3781,
    '15':4499
}


allids=-1

try:
    pass

except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())

    

@bot.message_handler(commands=['start'])
def start(m):
    tutorial=0
    if m.from_user.id==m.chat.id:
        if users.find_one({'id':m.from_user.id})==None:
            users.insert_one(createuser(m.from_user))
            tutorial=1
        user=users.find_one({'id':m.from_user.id})
        if tutorial==1:
            bot.send_message(m.chat.id, 'Здраствуй, боец! Прокачивай свои боевые навыки, и тогда ты, возможно, выживешь... А \n'+
                            'может и обретёшь богатство славу!')
        mainmenu(user)
        
  
@bot.message_handler(commands=['join'])
def join(m):
    print(lobbys)
    user=users.find_one({'id':m.from_user.id})
    try:
        i=m.text.split(' ')[1]
        for ids in lobbys:
            l=lobbys[ids]
            if l['code']==i:
                l['users'].append(user)
                bot.send_message(m.from_user.id, 'Вы присоединились к игре!')
    except Exception as e:
        bot.send_message(441399484, traceback.format_exc())
        

@bot.message_handler(commands=['testlobby'])
def testduel(m):
    x=createlobby(m.chat.id)
    lobbys.update(x)
    for ids in x:
        code=x[ids]['code']
    bot.send_message(m.chat.id, 'Лобби создано! Код:\n`'+code+'`', parse_mode='markdown')

    
@bot.message_handler(commands=['beginlobby'])
def beginlobby(m):
    try:
        fighters={}
        i=m.text.split(' ')[1]
        ct=1
        for ids in lobbys[i]['users']:
            if ids['battlename']==None:
                name=ids['name'][:12]
            else:
                name=ids['battlename']
            fighters.update({ids['id']:{'fighter':ids,
                                   'team':ct,
                                    'id':ids['id'],
                                    'name':name
                             }
                        })
            ct+=1
        del lobbys[i]
        game.Game(fighters)
        
    except Exception as e:
        bot.send_message(441399484, traceback.format_exc())
        

def createlobby(id):
    rc=randomcode(codes)
    return{rc:{'id':id,
           'code':rc,
           'users':[]
          }}
    
           
def randomcode(x):
    i=0
    txt=''
    while i<7:
        txt+=str(random.randint(1,9))
        i+=1
    while txt in x:
        i=0
        txt=''
        while i<7:
            txt+=str(random.randint(1,9))
            i+=1
    codes.append(txt)
    return txt
        
           
@bot.message_handler()
def messages(m):
    if m.from_user.id==m.chat.id:
        user=users.find_one({'id':m.from_user.id})
        if user['status']=='free':
            text=''
            if m.text=='👁Разведка':
                kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
                kb.add(types.KeyboardButton('🌲Лес'))
                text+='(⚡️)Лес - ближайший к вам лес находится не так уж и далеко.\n\n'
                if user['lvl']>=5:
                    kb.add(types.ReplyKeyboardButton('🏔Горы'))
                    text+='(⚡️⚡️)Горы - подъем в гору требует больше сил, но там происходят вещи поинтереснее, чем в лесу.\n\n'
                kb.add(types.KeyboardButton('Назад'))
                bot.send_message(m.chat.id, 'Вы выходите из своего дома и думаете, куда бы направиться.\n\n'+text, reply_markup=kb)
                
            elif m.text=='🌲Лес':
                if user['energy']>=1:
                    users.update_one({'id':m.from_user.id},{'$inc':{'energy':-1}})
                    users.update_one({'id':m.from_user.id},{'$set':{'status':'busy'}})
                    t=threading.Timer(300, forest, args=[user])
                    t.start()
                    bot.send_message(m.from_user.id, 'Вы отправились в ближайший лес. Вернётесь через 5 минут.')
                    mainmenu(user)
                    
            elif m.text=='⚔️Битвы':
                text=''
                kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
                kb.add(types.KeyboardButton('💀Искать монстров'))
                text+='💀Поиск монстров - побеждая монстров, вы будете получать много опыта, а если повезёт - жители ближайшей деревни отсыпят '+\
                'вам немного серебра!\n\n'
                if user['lvl']>=5:
                    kb.add(types.KeyboardButton('🆚Искать других бойцов'))
                    text+='🆚Искать других бойцов - в разработке.'
                kb.add(types.KeyboardButton('Назад'))
                bot.send_message(m.chat.id, 'Живи охотой или умри добычей! Участвуя в сражениях, '+
                                 'вы будете обретать славу и ценнейший опыт!\n\n'+text, reply_markup=kb)
                
            elif m.text=='💀Искать монстров':
                users.update_one({'id':m.from_user.id},{'$set':{'status':'busy'}})
                players=[user]
                t=threading.Timer(120, findmonster, args=[players])
                t.start()
                
            elif m.text=='Назад':
                mainmenu(user)
                
        else:
            bot.send_message(m.chat.id, 'Вы заняты!')
                    
         
def findmonster(players):           # Планы: сделать возможность случайному игроку запустить в бой своего монстра и управлять им
    mcount=1
    monsters=[]
    allm=['bear']
    while len(monsters)<mcount:
        monster=random.choice(allm)
        monsters.append(monster)
        
    for ids in players:
        bot.send_message(ids['id'], 'Вы нашли логово монстров! Посмотрим, кто же там обитает...')
    fighters={}
    ct=1
    for ids in players: 
        if ids['battlename']==None:
            name=ids['name'][:12]
        else:
            name=ids['battlename']
        fighters.update({ids['id']:{'fighter':ids,
                                   'team':ct,
                                   'id':ids['id'],
                                   'name':name
                                   }
                        })
    ct=2
    for ids in monsters:
        idd=createid()
        fighters.update({idd:{'fighter':ids,
                                   'team':ct,
                                    'id':idd
                             }
                        })
    game.Game(fighters)
        
        
   
def createid():
    global allids
    allids-=1
    return allids

        
def mainmenu(user):
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('⚔️Битвы'), types.KeyboardButton('👁Разведка'))
    bot.send_message(user['id'], '🏡Главное меню.', reply_markup=kb)
        
        
                
def forest(user):
    actions=['test']
    act=random.choice(actions)
    exp=0
    siler=0
    if act=='test':
        exp=1
        silver=1
        text='Вы вернулись из леса.\n\nПолученные ресурсы:\n'
    users.update_one({'id':user['id']},{'$inc':{'siler':silver, 'exp':exp}})
    users.update_one({'id':user['id']},{'$set':{'status':'free'}})
    if exp>0:
        text+='⭐️Опыт: '+str(exp)+'\n'
    if silver>0:
        text+='💰Серебро: '+str(silver)+'\n'
    bot.send_message(user['id'], text)
        
        
@bot.callback_query_handler(func=lambda call:True)
def inline(call): 
    cgame=None
    for ids in game.games:
        g=game.games[ids]
        if call.from_user.id in g.players:
            cgame=g
            try:
                cunit=cgame.players[cgame.currentplayer.id]
            except:
                cunit=None
    if cgame!=None and cunit!=None:
        if cunit.id==call.from_user.id:
            if call.data=='endturn':
                cgame.timer.cancel()
                medit('Выбрано: закончить ход.', call.message.chat.id, call.message.message_id)
                cgame.endturn()
            if call.data=='p_attack':
                units.choicetarget(cunit)
                
            if 'atk' in call.data:
                cgame.currentplayer=None
                medit('Выбрано: атака.', call.message.chat.id, call.message.message_id)
                t=int(call.data.split(' ')[1])
                target=findunit(cgame, t)
                target.recievehit(cunit)
                cgame.endturn()
        else:
            bot.answer_callback_query(call.id, 'Сейчас не ваш ход!')
        
def findunit(gamee, id):
    for ids in gamee.players:
        if gamee.players[ids].id==id:
            return gamee.players[ids]
    
def createuser(user):
    return {
        'id':user.id,
        'name':user.first_name,
        'username':user.username,
        'type':'basic',
        'energy':4,
        'maxenergy':4,
        'status':'free',
        'stats':{
            'dmg':[0, 0],
            'agility':0,
            'hp':0,
            'luck':0
        
        },
        'equipment':{
            'righthand':None,
            'lefthand':None,
            'head':None,
            'body':None
        
        },
        'silver':0,
        'exp':0,
        'lvl':1,
        'battlename':None
    }
    
    
    
users.update_many({},{'$set':{'status':'free'}}) 
print('7777')
bot.polling(none_stop=True,timeout=600)

