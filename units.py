


class Unit:
    self.hp=50
    self.dmg=[4, 7]
    self.luck=50
    self.inentory=[]
    self.class=None
    self.mana=300
    self.speedregen=400
    self.speed=0
    self.weight=800     # В ход у юнита регенится (self.speedregen) скорости. На ход юнит трати (self.weight) скорости. У кого на данный момент 
    self.agility=50     # больше скорости - тот ходит. Если одинаково - рандом.
