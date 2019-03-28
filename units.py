


classes=['warrior', 'bower', 'mage', 'assasin', 'basic']



class Unit:
    
    def __init__(self):
        self.hp=200
        self.team=None
        self.id=None
        self.dmg=[16, 28]
        self.luck=50
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
        self.skills=[]
        self.speedregen=400
        self.speed=self.speedregen
        self.weight=400     # В ход у юнита регенится (self.speedregen) скорости. На ход юнит трати (self.weight) скорости. 
        self.agility=50     # У кого на данный момент больше скорости - тот ходит. Если одинаково - рандом.
    
    
    def recievedmg(self, unit, weapon):
        pass
    
    
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
    
   
def handtotext(x):
    if x=='righthand':
        return 'Правая'
    elif x=='lefthand':
        return 'Левая'
    
    
def armortoname(x):
    if x==None:
        return 'Ничего'
    
def attackmenu(player):
    text=''
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
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Физ. атака', callback_data='p_attack'),types.InlineKeyboardButton(text='Скиллы', callback_data='skills'))
    kb.add(types.InlineKeyboardButton(text='Инвентарь', callback_data='inventory'),types.InlineKeyboardButton(text='Сменить руку', callback_data='handchange'))
    kb.add(types.InlineKeyboardButton(text='Закончить ход', callback_data='endturn'))
    bot.send_message(player.id, text, reply_markup=kb)
    
    
