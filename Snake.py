import pygame
import random

violet = (148, 0, 211)
indigo = (75, 0, 130)
blue = (30, 30, 220)
green = (0, 255, 0)
yellow = (250, 255, 0)
orange = (255, 150, 0)
red = (255, 0, 0)

colors = [violet, indigo, blue, green, yellow, orange, red]


class Head:
    direc = 'r'
    clr_idx = 0
    color = colors[clr_idx]
    prev = [None, None]
    def __init__(self, pos) -> None:
        self.pos = pos

        
    
    
    def draw(self, scr, width):
        pygame.draw.rect(scr, self.color, [self.pos[0]*width+1,self.pos[1]*width+1,width-1,width-1])

    def update_prev(self):
        self.prev = self.pos.copy()
        
    def move(self, speed):
        if self.direc=='r':
            self.update_prev()
            self.pos[0] += speed
        if self.direc=='l':              
            self.update_prev()
            self.pos[0] -= speed
        if self.direc=='d':              
            self.update_prev()
            self.pos[1] += speed
        if self.direc=='u':
            self.update_prev()
            self.pos[1] -= speed
                
class Tail(Head):
    color = None
    def __init__(self, pos, ass, idx) -> None:
        super().__init__(pos)
        self.ass = ass
        self.color = idx
        

        
    def follow(self):
        self.update_prev()
        self.pos[0] = self.ass.prev[0]
        self.pos[1] = self.ass.prev[1]
            

class Ringo(Head):
    color = (200, 50, 50)
    img = pygame.image.load(r'.\requirements\apple.png')
    img = pygame.transform.scale(img, (20,20))
    def __init__(self, pos) -> None:
        super().__init__(pos)
        
    def draw(self, scr, width):
        # pygame.draw.rect(scr, self.color, [self.pos[0]*width+1,self.pos[1]*width+1,width-1,width-1])
        scr.blit(self.img, (self.pos[0]*width+1,self.pos[1]*width+1))

 
###########   Functions  ############
def grid(scr, width):
    for i in range(1, 10):
        for j in range(1, 10):
            pygame.draw.line(scr, (255,255,255), [width*i, 0], [width*i, ww], 2)
            pygame.draw.line(scr, (255,255,255), [0, width*j], [ww, width*j], 2)

def detectButt():
    global play
    for e in pygame.event.get():       
        if e.type==pygame.KEYDOWN:
            if e.key == pygame.K_UP and head.direc!='d':
                head.direc = 'u'
            if e.key == pygame.K_DOWN and head.direc!='u':
                head.direc = 'd'
            if e.key == pygame.K_LEFT and head.direc!='r':
                head.direc = 'l'
            if e.key == pygame.K_RIGHT and head.direc!='l':
                head.direc = 'r'
            if e.key == pygame.K_x or e.key == pygame.K_ESCAPE:
                play = False
            if e.key == pygame.K_r:
                reset(snake, ringo)
        if e.type == pygame.QUIT:
            play = False
            
def munchimunch(snake, head, ringo):
    if head.pos == ringo.pos:
        new_munchie(ringo)
        tail = Tail(head.prev, snake[-1], colors[len(snake)%7])
        snake.append(tail)

def new_munchie(ringo):
    avail = availb(field, snake)
    r = random.randint(0, len(avail)-1)
    new_ringo = avail[r]
    ringo.pos = new_ringo
    
def availb(field, snake):
    avlist = []
    for couple in field:
        x = True
        for sq in snake:
            if sq.pos == couple:
                x = False
                break
            avlist.append(couple)
    return avlist

def loser(snake, w):
    loser = False
    head = snake[0]
    for tail in snake[1:]:
        if head.pos == tail.pos:
            loser = True
    if head.pos[1]<0 or head.pos[1]>w-1 or head.pos[0]<0 or head.pos[0]>w-1:
        loser = True
    return loser

    
def lost(scr, w):
    scr.fill((0,0,0))
    font = pygame.font.Font('freesansbold.ttf', 32)
    txt = font.render("U LOZERRRR!", True, (200, 200, 200))
    font2 = pygame.font.Font('freesansbold.ttf', 20)
    txt2 = font2.render("press R to restart", True, (200, 200, 200))
    scr.blit(txt, (w//4, w//2 - 50))
    scr.blit(txt2, (w//4, w//2))
    
def reset(snake, ringo):
    global alive
    alive = True
    while len(snake)>1:
        snake.pop()
    snake[0].pos = [0,0]
    snake[0].direc = 'r'
    new_munchie(ringo)
    


       
###########   Main  ############    
pygame.init()

ww = 800
bloks = 40
width = ww // bloks
scr = pygame.display.set_mode((ww, ww))
pygame.display.set_caption("test")

clk = pygame.time.Clock()
play = True
alive = True

# Init game components
field = [[i, j] for i in range(1, bloks-5) for j in range(1, bloks-5)]
head_pos = [0,0]
head = Head(head_pos)
snake = [head]
r_pos = [random.randint(1, bloks-1), random.randint(1, bloks-1)]
ringo = Ringo(r_pos)


while play:
    pygame.init()
    clk.tick(10)
    scr.fill((30,30,30))
    # grid(scr, width)
    
    # Init game components in loop
    head.draw(scr, width)
    head.move(1)
    ringo.draw(scr, width)
    for sq in snake[1:]:
        sq.draw(scr, width)
        sq.follow()
    
    munchimunch(snake, head, ringo)# Detecting eating food
        
    detectButt() #Detecting button clicking
    
    if loser(snake, bloks):
        alive = False
        
    if not alive:
        lost(scr, ww)
        
    pygame.display.flip()

pygame.quit()
    



    
    
    
                
                
                
            
