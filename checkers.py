import pygame
import move
import game_rules as gr
pygame.init()

#Создание классов клеток и шашек
class Cells(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        
    def update(self):
       pygame.draw.rect(sc, (10, 130, 155), (self.x, self.y, 90, 90))

class Checkers(pygame.sprite.Sprite):
    def __init__(self, x, y, ind, ind_k):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.ind = ind
        self.ind_k = ind_k
        
    def update(self):
        if self.ind == 1:
            pygame.draw.circle(sc, (10, 130, 155), (self.x*90+45, self.y*90+45), 35)
            if self.ind_k == 1:
                pygame.draw.circle(sc, (250, 140, 30), (self.x*90+45, self.y*90+45), 20)
        elif self.ind == 2:
            pygame.draw.circle(sc, (150, 0, 0), (self.x*90+45, self.y*90+45), 35)
            if self.ind_k == 1:
                pygame.draw.circle(sc, (250, 140, 30), (self.x*90+45, self.y*90+45), 20)
        else:
            self.kill()

#Создание переменных
cell = pygame.sprite.Group()
checkers = pygame.sprite.Group()

W, H = 720, 720
sc = pygame.display.set_mode((W, H))

field = move.field
move_pl = []
win_a = 1
win_b = 1
move_order = 0
player_order = 0
light = [-40, -40]
text_step = ["ХОДИТ ИГРОК 1", "ХОДИТ ИГРОК 2", "ПОБЕДА ИГРОКА 1", "ПОБЕДА ИГРОКА 2"]
move_sequence = [0, 0, 0, 0]
seq_id = 0
check_mpr = [None, None, None, None]
f = 1

#Создание игрового поля
for i in range(4):
    cell.add(Cells(180*i, 0),
             Cells(180*i, 180),
             Cells(180*i, 360),
             Cells(180*i, 540),
             Cells((180*i)+90, 90),
             Cells((180*i)+90, 270),
             Cells((180*i)+90, 450),
             Cells((180*i)+90, 630))

#Создание шашек по матрице "field"
for iy in range(8):
    for ix in range(8):
            checkers.add(Checkers(ix, iy, field[iy, ix, 0], field[iy, ix, 1]))

#Основной цикл
while f:
#Проверка всех игровых событий
    for event in pygame.event.get():
    #Условие выхода из программы
        if event.type == pygame.QUIT:
            f = 0 

    #Нажатие кнопок
        if event.type == pygame.KEYDOWN:
        #Отмена хода
            if event.key == pygame.K_e and move_sequence == [0, 0, 0, 0]:
                move_pl = []
                move_order = 0
                light = [-40, -40]
    #Отслеживание координат нажатого курсора
        if event.type == pygame.MOUSEBUTTONDOWN:
            moves = move.Move(event.pos)

        #Проверка на выбор правильной шашки (белые)
            if field[moves.move_y(), moves.move_x(), 0] == 1 and move_order == 0 and player_order == 0:
            #Запись начальных координат
                move_pl += [moves.move_y()]+[moves.move_x()]

                light = [moves.move_x()*90+45, moves.move_y()*90+45]
                move_order += 1

        #Проверка правильности хода (белые)
            elif field[moves.move_y(), moves.move_x(), 0] == 0 and move_order == 1 and player_order == 0 and abs(moves.move_y() - move_pl[0]) == abs(moves.move_x() - move_pl[1]):
            #Запись класса игровых правил в переменную
                check_gr = gr.Game_rules((move_pl[0], move_pl[1]), (moves.move_y(), moves.move_x()), 1, field, field[move_pl[0], move_pl[1], 1], seq_id)
                check_mpr = check_gr.move_pl_rule()
            #Возможен ли ход
                if check_mpr[0]:
                #Запись конечных координат и индекса шашки
                    move_pl += [moves.move_y()]+[moves.move_x()]+[1]
                #Если шашка является дамкой
                    if check_mpr[2] == 0:
                    #Съедание дамкой
                        field[(move_pl[2]-(move_pl[2]-move_pl[0])//abs(move_pl[2]-move_pl[0])), (move_pl[3]-(move_pl[3]-move_pl[1])//abs(move_pl[3]-move_pl[1]))] = [0, 0]
                        move_pl += [1]
                    else:
                    #Съедание шашкой назад
                        if check_mpr[1] == 0:
                            field[move_pl[0]+1, move_pl[1]+(moves.move_x()-move_pl[1])//abs(moves.move_x()-move_pl[1])] = [0, 0]
                            move_pl += [0]
                    #Съедание шашкой вперед
                        else:
                            field[move_pl[0]-1, move_pl[1]+(moves.move_x()-move_pl[1])//abs(moves.move_x()-move_pl[1])] = [0, 0]
                            move_pl += [0]

        #Проверка на выбор правильной шашки (черные)
            elif field[moves.move_y(), moves.move_x(), 0] == 2 and move_order == 0 and player_order == 1:
            #Запись начальных координат
                move_pl += [moves.move_y()]+[moves.move_x()]

                light = [moves.move_x()*90+45, moves.move_y()*90+45]
                move_order += 1

        #Проверка правильности хода (черные)
            elif field[moves.move_y(), moves.move_x(), 0] == 0 and move_order == 1 and player_order == 1 and abs(moves.move_y() - move_pl[0]) == abs(moves.move_x() - move_pl[1]):
            #Запись класса игровых правил в переменную
                check_gr = gr.Game_rules((move_pl[0], move_pl[1]), (moves.move_y(), moves.move_x()), -1, field, field[move_pl[0], move_pl[1], 1], seq_id)
                check_mpr = check_gr.move_pl_rule()
            #Возможен ли ход
                if check_mpr[0]:
                #Запись конечных координат и индекса шашки
                    move_pl += [moves.move_y()]+[moves.move_x()]+[2]
                #Если шашка является дамкой
                    if check_mpr[2] == 0:
                    #Съедание дамкой
                        field[move_pl[2]-(move_pl[2]-move_pl[0])//abs(move_pl[2]-move_pl[0]), move_pl[3]-(move_pl[3]-move_pl[1])//abs(move_pl[3]-move_pl[1])] = [0, 0]
                        move_pl += [1]
                    else:
                    #Съедание шашкой назад
                        if check_mpr[1] == 0:
                            field[move_pl[0]-1, move_pl[1]+(moves.move_x()-move_pl[1])//abs(moves.move_x()-move_pl[1])] = [0, 0]
                            move_pl += [0]
                    #Съедание шашкой вперед
                        else:
                            field[move_pl[0]+1, move_pl[1]+(moves.move_x()-move_pl[1])//abs(moves.move_x()-move_pl[1])] = [0, 0]
                            move_pl += [0]
        
#Проверка на несколько съеданий подряд
    if check_mpr[3] == 0:
        move_sequence = check_gr.msr()
        #Может ли шашка съесть несколько шашек подряд
        if move_sequence != [0, 0, 0, 0]:
            light = [moves.move_x()*90+45, moves.move_y()*90+45]
            seq_id = 1
        else:
            seq_id = 0
#Ход
    if len(move_pl) == 6:
        field[move_pl[0], move_pl[1]] = [0, 0]
    #Должна ли шашка стать дамкой после хода
        if move_pl[2] == 0 and move_pl[4] == 1 or move_pl[2] == 7 and move_pl[4] == 2:
            move_pl[5] = 1

        field[move_pl[2], move_pl[3]] = [move_pl[4], move_pl[5]]
        if move_sequence != [0, 0, 0, 0]:
            move_pl = [move_pl[2], move_pl[3]]
        else:
            move_order = 0
            player_order = -player_order+1 
            light = [-40, -40]
            move_pl = []

    #Перезапись матрици "field" с новыми значениями
        checkers = pygame.sprite.Group()
        for iy in range(8):
            for ix in range(8):
                    checkers.add(Checkers(ix, iy, field[iy, ix, 0], field[iy, ix, 1]))

    #Проверка всего поля на наличие шашек (белых и черных)
    #Если одного типа шашек не будет то игра закончится
        win_a, win_b = 0, 0

        for iy in range(8):
            for ix in range(8):
                if field[iy, ix, 0] == 1:
                    win_a += 1
                elif field[iy, ix, 0] == 2:
                    win_b += 1

#Сообщение о том какой игрок должен ходить
    if win_a != 0 and win_b != 0:
        pygame.display.set_caption("////////// "+text_step[player_order]+" //////////")
    else:
        if win_a != 0:
            pygame.display.set_caption("////////// "+text_step[2]+" //////////")
        else:
            pygame.display.set_caption("////////// "+text_step[3]+" //////////")

#Заливка экрана черным цветом, отрисовка клеток, отрисовка окаймления шашек, отрисовка шашек, обновление экрана
    sc.fill((0, 0, 0))
    cell.update()
    pygame.draw.circle(sc, (255, 255, 255), (light[0], light[1]), 40)
    checkers.update()
    pygame.display.update()