from operator import truediv
import pygame, sys
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, BG, WHITE
from minimax.algorithm import minimax
from checkers.game import Game
from button import Button

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        
        
        run = True
        clock = pygame.time.Clock()
        game = Game(WIN)

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
    
def playAI():
    while True:
        
        
        run = True
        clock = pygame.time.Clock()
        game = Game(WIN)

        while run:
            clock.tick(FPS)

            if game.turn == WHITE:
                value, new_board = minimax(game.get_board(), 4, WHITE, game)
                game.ai_move(new_board)


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

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WIN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        WIN.blit(BG, (0, 0))
        

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/1v1_Rect.png"), pos=(640, 220), 
                            text_input="1vs1", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        AI_BUTTON = Button(image=pygame.image.load("assets/1v1_Rect.png"), pos=(640, 340),
                            text_input="1vsAI", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/History_Rect.png"), pos=(640, 460), 
                            text_input="HISTORY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit_Rect.png"), pos=(640, 580), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        USER_BUTTON = Button(image=pygame.image.load("assets/Sample_User_Icon.png"), pos=(1150, 580),
                            text_input="", font=get_font(0), base_color="#d7fcd4", hovering_color="#d7fcd4")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, AI_BUTTON, OPTIONS_BUTTON, USER_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if AI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playAI()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if USER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    account()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def account():
    pass


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

"""def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

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

    pygame.quit()"""

main_menu()
