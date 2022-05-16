from operator import truediv
from unittest import result
import pygame, sys
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, BG, WHITE, RED
from minimax.algorithm import minimax
from checkers.game import Game
from button import Button
from datetime import datetime
import pymysql

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Define font
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Local 1v1 
def play():
    while True:
        
        # Run the game and display it
        run = True
        clock = pygame.time.Clock()
        game = Game(WIN)

        # Save current time when starting the game
        start = datetime.now()

        while run:
            clock.tick(FPS)

            # If winner is RED, save current time when ending the game
            if game.winner() == RED:
                end = datetime.now()

                # Match lenght
                deltaD = end - start

                # Database connection
                connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="", database="bdd_dame")
                cursor = connection.cursor()
                print(connection)

                # Store the SQL query in a variable
                sql = "INSERT INTO `history` (`RESULT`, `TIME`, `GAMETYPE`) VALUES (%s, %s, %s)"

                # Execute the query with arguments
                cursor.execute(sql, ('RED WON',deltaD, '1V1'))

                # Commit query and close connection
                connection.commit()
                connection.close()

            # If winner is WHITE, save current time when ending the game
            elif game.winner() == WHITE:
                end = datetime.now()

                # Match lenght
                deltaD = end - start

                # Database connection
                connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="", database="bdd_dame")
                cursor = connection.cursor()
                print(connection)
    
                # SQL query
                sql = "INSERT INTO `history` (`RESULT`, `TIME`, `GAMETYPE`) VALUES (%s, %s, %s)"

                # Execute querry with arguments
                cursor.execute(sql, ('WHITE WON',deltaD, '1v1'))

                # Commit query, close connection
                connection.commit()
                connection.close()

            if game.winner() != None:
               winscreen()
        
            # If we close the window, stop the program
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   run = False

                # Get the position of the cursor when clicking, return the corresponding row and col
               if event.type == pygame.MOUSEBUTTONDOWN:
                   pos = pygame.mouse.get_pos()
                   row, col = get_row_col_from_mouse(pos)

                   game.select(row, col)

            game.update()

        pygame.quit()

# Local 1vAI
def playAI():
    while True:
        
        # Run the game
        run = True
        clock = pygame.time.Clock()
        game = Game(WIN)

        # Save match start time
        start = datetime.now()

        while run:
            clock.tick(FPS)

            # If it is WHITE turn, the AI will play
            if game.turn == WHITE:
                value, new_board = minimax(game.get_board(), 3, WHITE, game)
                game.ai_move(new_board)

            # If RED wins, save current time
            if game.winner() == RED:

                end = datetime.now()

                # Match lenght
                deltaD = end - start
                
                # Database connection
                connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="", database="bdd_dame")
                cursor = connection.cursor()
                print(connection)
                                
                # SQL query
                sql = "INSERT INTO `history` (`RESULT`, `TIME`, `GAMETYPE`) VALUES (%s, %s, %s)"

                # Execute query with arguments
                cursor.execute(sql, ('YOU WON',deltaD, '1vAI'))

                # Commit query, close connection
                connection.commit()
                connection.close()

            # If WHITE wins, save current time
            elif game.winner() == WHITE:

                end = datetime.now()

                # Match lenght
                deltaD = end - start

                # database connection
                connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="", database="bdd_dame")
                cursor = connection.cursor()
                print(connection)
                # some other statements  with the help of cursor
    
                sql = "INSERT INTO `history` (`RESULT`, `TIME`, `GAMETYPE`) VALUES (%s, %s, %s)"

                # Execute the query
                cursor.execute(sql, ('AI WON',deltaD, '1vAI'))
                # the connection is not autocommited by default. So we must commit to save our changes.
                connection.commit()
                connection.close()
            

            if game.winner() != None:
               winscreen()
        
            # If we close the window, stop the program
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   run = False

                # Return the row and col corresponding to the cursor position when clicking 
               if event.type == pygame.MOUSEBUTTONDOWN:
                   pos = pygame.mouse.get_pos()
                   row, col = get_row_col_from_mouse(pos)

                   game.select(row, col)

            game.update()

        pygame.quit()

# Match history
def history():
    while True:
        # Track cursor
        HISTORY_MOUSE_POS = pygame.mouse.get_pos()

        # Display background
        WIN.blit(BG, (0, 0))

        # Database connection
        connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="", database="bdd_dame")
        cursor = connection.cursor()
        print(connection)

        # SQL query to get previous match information 
        sql = "SELECT `RESULT`, `TIME`, `GAMETYPE` AS `result` FROM `history` ORDER BY id DESC LIMIT 1"

        # Execute the query
        cursor.execute(sql)

        # Store the result of the query
        result = cursor.fetchone()

        
        sql2 = "SELECT `RESULT`, `TIME`, `GAMETYPE` AS `result` FROM `history` ORDER BY id DESC LIMIT 1, 1"        
        cursor.execute(sql2)
        result2 = cursor.fetchone()
  
        sql3 = "SELECT `RESULT`, `TIME`, `GAMETYPE` AS `result` FROM `history` ORDER BY id DESC LIMIT 2, 1"        
        cursor.execute(sql3)
        result3 = cursor.fetchone()

        sql4 = "SELECT `RESULT`, `TIME`, `GAMETYPE` AS `result` FROM `history` ORDER BY id DESC LIMIT 3, 1"
        cursor.execute(sql4)
        result4 = cursor.fetchone()

        sql5 = "SELECT `RESULT`, `TIME`, `GAMETYPE` AS `result` FROM `history` ORDER BY id DESC LIMIT 4, 1"
        cursor.execute(sql5)
        result5 = cursor.fetchone()
        
        # Commit the queries
        connection.commit()
        
        # Display some text
        HISTORY_TEXT = get_font(50).render("Your last 5 matches", True, "#b68f40")
        HISTORY_RECT = HISTORY_TEXT.get_rect(center=(640, 100))
        WIN.blit(HISTORY_TEXT, HISTORY_RECT)

        # Join the stored values of the query and separates them with ' '
        # Then display the results
        str = ' '.join(result)
        RESULT_TEXT = get_font(35).render(str, True, "White")
        HISTORY_RECT = RESULT_TEXT.get_rect(center=(640, 200))
        WIN.blit(RESULT_TEXT, HISTORY_RECT)

        str2 = ' '.join(result2)
        RESULT_TEXT = get_font(35).render(str2, True, "White")
        HISTORY_RECT = RESULT_TEXT.get_rect(center=(640, 280))
        WIN.blit(RESULT_TEXT, HISTORY_RECT)
        
        str3 = ' '.join(result3)
        RESULT_TEXT = get_font(35).render(str3, True, "White")
        HISTORY_RECT = RESULT_TEXT.get_rect(center=(640, 360))
        WIN.blit(RESULT_TEXT, HISTORY_RECT)
        
        str4 = ' '.join(result4)
        RESULT_TEXT = get_font(35).render(str4, True, "White")
        HISTORY_RECT = RESULT_TEXT.get_rect(center=(640, 440))
        WIN.blit(RESULT_TEXT, HISTORY_RECT)

        str5 = ' '.join(result5)
        RESULT_TEXT = get_font(35).render(str5, True, "White")
        HISTORY_RECT = RESULT_TEXT.get_rect(center=(640, 520))
        WIN.blit(RESULT_TEXT, HISTORY_RECT)
        
        # Back button
        HISTORY_BACK = Button(image=None, pos=(640, 640), 
                            text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")

        HISTORY_BACK.changeColor(HISTORY_MOUSE_POS)
        HISTORY_BACK.update(WIN)

        # Quits the game if window gets closed, returns to main menu if clicking on the Back button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HISTORY_BACK.checkForInput(HISTORY_MOUSE_POS):
                    connection.close()
                    main_menu()

        pygame.display.update()

# Main menu
def main_menu():
    while True:
        # Display background
        WIN.blit(BG, (0, 0))
        
        # Get mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Main menu text
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # Buttons
        PLAY_BUTTON = Button(image=pygame.image.load("assets/1v1_Rect.png"), pos=(640, 220), 
                            text_input="1vs1", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        AI_BUTTON = Button(image=pygame.image.load("assets/1v1_Rect.png"), pos=(640, 340),
                            text_input="1vsAI", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        HISTORY_BUTTON = Button(image=pygame.image.load("assets/History_Rect.png"), pos=(640, 460), 
                            text_input="HISTORY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit_Rect.png"), pos=(640, 580), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        USER_BUTTON = Button(image=pygame.image.load("assets/Sample_User_Icon.png"), pos=(1150, 580),
                            text_input="", font=get_font(0), base_color="#d7fcd4", hovering_color="#d7fcd4")

        WIN.blit(MENU_TEXT, MENU_RECT)

        # Changes the color if cursor hovers the buttons
        for button in [PLAY_BUTTON, AI_BUTTON, HISTORY_BUTTON, USER_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        # Open specific window if clicking on certain button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if AI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playAI()
                if HISTORY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    history()
                if USER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    account()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# User account
def account():
    pass

# Game over screen
def winscreen():
    while True:
        WINSCR_MOUSE_POS = pygame.mouse.get_pos()

        # Display game over text
        WINSCR_TEXT = get_font(45).render("GAME OVER !", True, "White")
        WINSCR_RECT = WINSCR_TEXT.get_rect(center=(640, 260))
        WIN.blit(WINSCR_TEXT, WINSCR_RECT)
        
        # Main menu button
        WINSCR_BACK = Button(image=None, pos=(640, 460), 
                            text_input="MENU", font=get_font(75), base_color="Green", hovering_color="Green")

        WINSCR_BACK.changeColor(WINSCR_MOUSE_POS)
        WINSCR_BACK.update(WIN)

        # Send back to main menu if clicking on button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WINSCR_BACK.checkForInput(WINSCR_MOUSE_POS):
                    main_menu()

        pygame.display.update()

# Get grid value from cursor position
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Start the program on the main menu
main_menu()
