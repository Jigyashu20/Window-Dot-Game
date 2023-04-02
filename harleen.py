import pygame

SCREEN = WIDTH, HEIGHT = 700, 700     
CELLSIZE = 50
PADDING = 20
ROWS = COLS = (WIDTH - 4 * PADDING) // CELLSIZE
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (78, 193, 246)
GREEN = (0, 255, 0)
BLACK = (12, 12, 12)

font = pygame.font.SysFont('cursive', 25)


class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.index = self.r * ROWS + self.c

        self.rect = pygame.Rect((self.c * CELLSIZE + 2 * PADDING, self.r * CELLSIZE +
                                 3 * PADDING, CELLSIZE, CELLSIZE))
        self.left = self.rect.left
        self.top = self.rect.top
        self.right = self.rect.right
        self.bottom = self.rect.bottom
        self.edges = [
            [(self.left, self.top), (self.right, self.top)],
            [(self.right, self.top), (self.right, self.bottom)],
            [(self.right, self.bottom), (self.left, self.bottom)],
            [(self.left, self.bottom), (self.left, self.top)]
        ]
        self.sides = [False, False, False, False]
        self.winner = None

    def checkwin(self, winner):
        if not self.winner:
            if self.sides == [True] * 4:
                self.winner = winner
                if winner == 'X':
                    self.color = GREEN
                else:
                    self.color = RED
                self.text = font.render(self.winner, True, WHITE)

                return 1
        return 0

    def update(self, win):
        if self.winner:
            pygame.draw.rect(win, self.color, self.rect)
            win.blit(self.text, (self.rect.centerx - 5, self.rect.centery - 7))

        for index, side in enumerate(self.sides):
            if side:
                pygame.draw.line(win, WHITE, (self.edges[index][0]),
                                 (self.edges[index][1]), 2)

# creating a list of all cells
def create_cells():
    cells = []
    for r in range(ROWS):
        for c in range(COLS):
            cell = Cell(r, c)
            cells.append(cell)
    return cells


def reset_cells():
    pos = None
    ccell = None
    up = False
    right = False
    bottom = False
    left = False
    return pos, ccell, up, right, bottom, left


def reset_score():
    fillcount = 0
    p1_score = 0
    p2_score = 0
    return fillcount, p1_score, p2_score


def reset_player():
    turn = 0
    players = ['X', 'O']
    player = players[turn]
    next_turn = False
    return turn, players, player, next_turn

def find_cell(pos1, pos2):
    if pos1[0] == pos2[0]:
        a = min(pos1[1], pos2[1])
        a = (a-3*PADDING)//50
        b = (pos1[0]-2*PADDING)//50
        if b == 0:
            return a*COLS, 3, -1, -1
        elif b == COLS:
            return (a+1)*COLS-1, 1, -1, -1
        else: 
            return (a)*COLS+b, 3, (a)*COLS+b-1, 1  


    elif pos1[1] == pos2[1]:
        a = min(pos1[0], pos2[0])
        a = (a-2*PADDING)//50
        b = (pos1[1]-3*PADDING)//50
        if b == 0:
            return a, 0, -1, -1
        elif b == ROWS:
            return ROWS*COLS-a, 2, -1, -1
        else: 
            return b*COLS+a, 0, (b-1)*COLS+a, 2 



gameover = False
cells = create_cells()
pos, ccell, up, right, bottom, left = reset_cells()
fillcount, p1_score, p2_score = reset_score()
turn, players, player, next_turn = reset_player()
running = True
pos1=None
pos2=None

while running:
    if pos1 and pos2:
        pos1=None
        pos2=None
    win.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            a = max(((pos[0]-25-2*PADDING)//50), ((pos[0]+25-2*PADDING)//50))
            b = max(((pos[1]-25-3*PADDING)//50), ((pos[1]+25-3*PADDING)//50))
            if a<0 or b<0 or a>=ROWS or b>= COLS:
                pos = None
            else:
                pos = (a*50+2*PADDING, b*50 + 3*PADDING )

            if pos1==None:
                pos1 = pos
            else:
                pos2 = pos        


        if event.type == pygame.MOUSEBUTTONUP:
            pos = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r:
                gameover = False
                cells = create_cells()
                pos, ccell, up, right, bottom, left = reset_cells()
                fillcount, p1_score, p2_score = reset_score()
                turn, players, player, next_turn = reset_player()

            if not gameover:
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_DOWN:
                    bottom = True
                if event.key == pygame.K_LEFT:
                    left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_DOWN:
                bottom = False
            if event.key == pygame.K_LEFT:
                left = False

    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            pygame.draw.circle(win, WHITE, (c * CELLSIZE + 2 * PADDING, r * CELLSIZE + 3 * PADDING), 2)

    ccell = [[-1, -1],[-1, -1]]
    if pos1 and pos2:
        if (pos1[0]==pos2[0] and abs(pos1[1]-pos2[1])==50) or (pos1[1]==pos2[1] and abs(pos1[0]-pos2[0])==50):
            ccell[0][0] , ccell[0][1], ccell[1][0] , ccell[1][1]= find_cell( pos1, pos2)
            if ccell[0][0] != -1:
                cells[ccell[0][0]].sides[ccell[0][1]] = True
            if ccell[1][0] != -1:
                cells[ccell[1][0]].sides[ccell[1][1]] = True

            next_turn=True    
        else:
            pos1 = pos2
            pos2 = None    

       
    for cell in cells:
        cell.update(win)
    
    for i in range(2):
        if ccell[i][0] != -1:
            res = cells[ccell[i][0]].checkwin(player)
            
            if res:
                fillcount += res
                if player == 'X':
                    p1_score += 1
                else:
                    p2_score += 1
                if fillcount == ROWS * COLS:
                    print(p1_score, p2_score)
                    gameover = True

    if next_turn:
        turn = (turn + 1) % len(players)
        player = players[turn]
        next_turn = False

    p1img = font.render(f'Player 1 : {p1_score}', True, BLUE)
    p1rect = p1img.get_rect()
    p1rect.x, p1rect.y = 2 * PADDING, 15

    p2img = font.render(f'Player 2 : {p2_score}', True, BLUE)
    p2rect = p2img.get_rect()
    p2rect.right, p2rect.y = WIDTH - 2 * PADDING, 15

    win.blit(p1img, p1rect)
    win.blit(p2img, p2rect)
    if player == 'X':
        pygame.draw.line(win, BLUE, (p1rect.x, p1rect.bottom + 2),
                         (p1rect.right, p1rect.bottom + 2), 1)
    else:
        pygame.draw.line(win, BLUE, (p2rect.x, p2rect.bottom + 2),
                         (p2rect.right, p2rect.bottom + 2), 1)

    if gameover:
        rect = pygame.Rect((50, 100, WIDTH - 100, HEIGHT - 200))
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, RED, rect, 2)

        over = font.render('Game Over', True, WHITE)
        win.blit(over, (rect.centerx - over.get_width() / 2, rect.y + 10))

        winner = '1' if p1_score > p2_score else '2'
        winner_img = font.render(f'Player {winner} Won', True, GREEN)
        win.blit(winner_img, (rect.centerx - winner_img.get_width() / 2, rect.centery - 10))

        msg = 'Press r:restart, q:quit'
        msgimg = font.render(msg, True, RED)
        win.blit(msgimg, (rect.centerx - msgimg.get_width() / 2, rect.centery + 20))

    pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 2, border_radius=10)
#     if pos1 and pos2:
#         print(pos1, pos2, ccell[0][0], ccell[0][1], ccell[1][0], ccell[1][1])
    pygame.display.update()



pygame.quit()
