import game


classes=['warrior', 'bower', 'mage', 'assasin', 'basic']



class Unit:
    
    def __init__(self):
        self.hp=200
        self.name=None
        self.team=None
        self.id=None
        self.dead=False
        self.dmg=[16, 28]
        self.luck=0
        self.controller=None
        self.body={
            'righthand':None,
            'lefthand':None,
            'head':None,
            'body':None
            
        }
        self.dmgbuff=[0, 0]
        self.mainhand='righthand'
        self.inentory=[]
        self.class='basic'
        self.mana=300
        self.statuses=[]
        self.skills=['charge']
        self.speedregen=400
        self.speed=self.speedregen
        self.weight=400     # В ход у юнита регенится (self.speedregen) скорости. На ход юнит трати (self.weight) скорости. 
        self.agility=50     # У кого на данный момент больше скорости - тот ходит. Если одинаково - рандом.
        self.message=None
    
    
    def recievedmg(self, dmg):
        self.hp-=dmg

        
        
    def recievehit(self, unit):
        d1=0
        d2=0
        if unit.body[unit.mainhand]!=None:
            weapon=unit.body[unit.mainhand]
            d1=weapon.dmg[0]
            d2=weapon.dmg[1]
        try:
            dmg=random.randint(unit.dmg[0]+unit.dmgbuff[0]+d1, unit.dmg[1]+unit.dmgbuff[1]+d2)
        except:
            dmg=unit.dmg[0]+unit.dmgbuff[0]+d1
        self.recievedmg(dmg)
    
    
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
        self.class='warrior'
        self.agility=int(self.agility*0.7)
    
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
    

def playerinfo(player):
    text=''
    text+='Класс: '+classtoname(player.class).lower()
    text+='♥️Хп: '+str(player.hp)+'\n'
    text+='💢Урон: '+str(player.dmg[0]+player.dmgbuff[0])+'-'+str(player.dmg[1]+player.dmgbuff[1])+'\n'
    text+='🏃‍♂️Скорость: '+str(player.speedregen)+'\n'
    text+='Экипировка:\n'+
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
    if player!=None:
        for ids in game.games:
            g=game.games[ids]
            if player.id in g:
                cgame=g
    return g
    
    
def choicetarget(player):
    cgame=findgame(player=player)
    if cgame!=None:
        enemys=[]
        for ids in cgame.players:
            target=cgame.players[ids]
            if target.team!=player.team:
                enemys.append(target)
        for ids in enemys:
            kb.add(types.InlineKeyboardButton(text=ids.name+'('+str(ids.hp)+'♥️)', callback_data='atk '+str(ids.id)))
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
    bot.send_message(player.id, text, reply_markup=kb)
    
    
