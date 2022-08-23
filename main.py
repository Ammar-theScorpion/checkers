import pygame

from checkers.constants import CROWN, WHITE, WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkers.game import Game
from network import Network
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()
pygame.font.init()
pygame.display.set_caption('Checkers')
base_font = pygame.font.Font(None, 32)
upper_font = pygame.font.Font(None, 25)
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
def wait():
    text_surface = upper_font.render("Waiting for players ...", True, (0, 0, 0))
    WIN.fill((244,151,60))
    WIN.blit(text_surface, ( WIDTH/2 - text_surface.get_width()/2, HEIGHT/2 - text_surface.get_height()/2))
    pygame.display.update() 

 
 
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    game = Game(WIN, n)
    print()
   
  
    while run:
        clock.tick(FPS)
        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            
            if event.type == pygame.MOUSEBUTTONDOWN:    
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

            game.update()
        
    pygame.quit()



class Button:
    def __init__(self, str, x, y):
        self.x = x
        self.y = y
        self.str = str
        self.brect = pygame.Rect(x, y, 150, 90)

    def render(self):
        pygame.draw.rect(WIN, (255, 0, 0), self.brect)   
        self.render_text()     

    def render_text(self):
        text_surface = upper_font.render(self.str, True, (0, 0, 0))
        WIN.blit(text_surface, ( int(self.x)+75 - text_surface.get_width()//2 ,  int(self.y)+45 - text_surface.get_height()//2) ) 

def pre_main():
    while True:
        b_play = Button("PLAY", WIDTH/2-75, 150)
        b_inct = Button("Instractions", WIDTH/2-75, 350)

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if b_play.brect.collidepoint(e.pos):
                        main()


            

            WIN.fill((244,151,60))
            b_play.render()
            b_inct.render()
            pygame.display.update()
pre_main()
main()