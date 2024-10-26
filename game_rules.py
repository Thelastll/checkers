#Класс который проверяет может ли выбранная шашка сделать ход
class Game_rules:
    def __init__(self, start, end, step, field, ind_k, seq_id):
        self.start = start
        self.end = end
        self.step = step
        self.field = field
        self.ind_k = ind_k
        self.seq_id = seq_id

    def move_pl_rule(self):
        qty = 0
    #Подщет шашек на пути дамки
        if self.ind_k == 1:
            for i in range(abs(self.end[0]-self.start[0])):
                if self.field[self.start[0]+(i+1)*((self.end[0]-self.start[0])//(abs(self.end[0]-self.start[0]))), self.start[1]+(i+1)*((self.end[1]-self.start[1])//(abs(self.end[1]-self.start[1]))), 0] == max(1, self.step+1):
                    qty += 1
                if  self.field[self.start[0]+(i+1)*((self.end[0]-self.start[0])//(abs(self.end[0]-self.start[0]))), self.start[1]+(i+1)*((self.end[1]-self.start[1])//(abs(self.end[1]-self.start[1]))), 0] == max(1, -self.step+1):
                    qty += 2

    #Простой ход шашки
        if self.start[0] - self.end[0] == self.step and self.ind_k == 0 and self.seq_id == 0:
            return True, None, None, None
    #Поедание вражеской шашки
        elif self.start[0] - self.end[0] == self.step*2 and self.field[self.start[0]-self.step, self.start[1]+(self.end[1]-self.start[1])//abs(self.end[1]-self.start[1]), 0] == max(1, self.step+1) and self.ind_k == 0:
            return True, None, None, 0
    #Поедание вражеской шашки назад
        elif self.start[0] - self.end[0] == -self.step*2 and self.field[self.start[0]+self.step, self.start[1]+(self.end[1]-self.start[1])//abs(self.end[1]-self.start[1]), 0] == max(1, self.step+1) and self.ind_k == 0:
            return True, 0, None, 0
    #Ход дамки
        elif qty <= 0 and self.ind_k == 1 and self.seq_id == 0:
           return True, None, 0, None
    #Поедание дамкой
        elif qty == 1 and self.field[self.end[0]-((self.end[0]-self.start[0])//abs(self.end[0]-self.start[0])), self.end[1]-((self.end[1]-self.start[1])//abs(self.end[1]-self.start[1])), 0] == max(1, self.step+1) and self.ind_k == 1:
            return True, None, 0, 0
    #Любой другой (невозможный) ход
        else:
            return False, None, None, None
        
    #move sequence rule
    def msr(self):
        move_sequence = [0, 0, 0, 0]
        if self.end[0]-2 >= 0 and self.end[1]-2 >= 0:
            if self.field[self.end[0]-2, self.end[1]-2, 0] == 0 and self.field[self.end[0]-1, self.end[1]-1, 0] == max(1, self.step+1):
                move_sequence[0] = 1
        if self.end[0]-2 >= 0 and self.end[1]+2 <= 7:
            if self.field[self.end[0]-2, self.end[1]+2, 0] == 0 and self.field[self.end[0]-1, self.end[1]+1, 0] == max(1, self.step+1):
                move_sequence[1] = 1
        if self.end[0]+2 <= 7 and self.end[1]-2 >= 0:
            if self.field[self.end[0]+2, self.end[1]-2, 0] == 0 and self.field[self.end[0]+1, self.end[1]-1, 0] == max(1, self.step+1):
                move_sequence[3] = 1
        if self.end[0]+2 <= 7 and self.end[1]+2 <= 7:
            if self.field[self.end[0]+2, self.end[1]+2, 0] == 0 and self.field[self.end[0]+1, self.end[1]+1, 0] == max(1, self.step+1):
                move_sequence[2] = 1
        return move_sequence