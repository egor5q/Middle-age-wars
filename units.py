


classes=['warrior', 'bower', 'mage', 'assasin', 'basic']



class Unit:
    
    def __init__(self):
        self.hp=200
        self.dmg=[16, 28]
        self.luck=50
        self.body={
            'righthand':None,
            'lefthand':None,
            'head':None
            
        }
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
    
    
