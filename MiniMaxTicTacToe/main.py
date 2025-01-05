import sys
import pygame
import random
import numpy as np
from button import Button

pygame.init()

#colors
WHITE =  (255, 255, 255)
GREY = (180,180,180)
DGREY = (140,140,140)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
BLACK = (0,0,0)

#proportions and sizes
WIDTH = 500 
HEIGHT = 500
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

MAX_DEPTH = float('inf')


CURR_DIFFICULTY = 0  #0 is hard 1 is easy

#Font
font = pygame.font.SysFont( "minecraftregular", 55)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('game base')
board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines(color=WHITE):
    for i in range(1,BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i))
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)
    
        
def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col*SQUARE_SIZE + (SQUARE_SIZE // 2 ) ) , int(row*SQUARE_SIZE + (SQUARE_SIZE // 2 ) ) ), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2: 
                pygame.draw.line(screen, color, (col* SQUARE_SIZE + SQUARE_SIZE // 4 , row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col* SQUARE_SIZE + SQUARE_SIZE // 4 , row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):  # bros logic in the video makes no sense for this function, i wrote it a lil different lmao
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board = board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
        
    if check_board[2][0] == player and check_board[1][1] == player and check_board[0][2] == player:
        return True
    
    return False
    

def random_move():
    available = []
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] ==0:
                available.append((row, col))
                
    move = random.choice(available)
    
    if not available:
        return False
    
    board[move[0]][move[1]] = 2
    
    return True
    
    
    

            
            
def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
                
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score
    
def best_move():
    best_score = float('-inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
                    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False



def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0
            

def main_menu():
    
    pygame.display.set_caption('main menu')

    while True:
        screen.fill(WHITE)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        # draw_text("Main Menu", font, (BLACK), screen, WIDTH//2, HEIGHT * (1/5))
        PLAY_BUTTON = Button(None, (WIDTH//2, HEIGHT* (3 / 8)), "play", font, RED, GREEN)  # button object test
        OPTIONS_BUTTON = Button(None, (WIDTH//2, HEIGHT* (4 / 8)), "options", font, RED, GREEN)  # button object test
        QUIT_BUTTON = Button(None, (WIDTH//2, HEIGHT* (5 /  8)), "quit", font, RED, GREEN)  # button object test

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):   
                    pygame.quit()
                    sys.exit()
                
                
                
                
                
                
        pygame.display.update()  
    
    
def change_difficulty():
    global CURR_DIFFICULTY
    if CURR_DIFFICULTY == 0:
        CURR_DIFFICULTY = 1
    else:
        CURR_DIFFICULTY = 0
    return 0


def options():
    
    pygame.display.set_caption('options')
    
    
    
    while True:
        screen.fill(GREY)
        
        pygame.draw.rect(screen, DGREY, ((0, 240), (500, 250)))
        
        pygame.draw.rect(screen, (90,90,90), ((0, 425), (500, 250)))
        
        draw_text("Controls: ", font, BLACK, screen, 5, HEIGHT/2)
        draw_text("r = restart", font, BLUE, screen, 5, HEIGHT/2 + 55)
        draw_text("m = main menu", font, BLUE, screen, 5, HEIGHT/2 + 110)
        
        draw_text("made by obi", font, GREY, screen, 5, 445)

        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        if CURR_DIFFICULTY == 0: #currentl y hard
            EASY = Button(None, (WIDTH/4, HEIGHT* (3 / 8)), "easy", font, RED, GREEN)
            HARD = Button(None, (WIDTH/2 + WIDTH/4, HEIGHT* (3 / 8)), "hard", font, RED, GREEN) 
            pygame.draw.rect(screen, BLACK, ((WIDTH/2  + 3*WIDTH/32 , HEIGHT* 5/16), (150, 75)))
        else:
            EASY = Button(None, (WIDTH/4, HEIGHT* (3 / 8)), "easy", font, RED, GREEN)
            HARD = Button(None, (WIDTH/2 + WIDTH/4, HEIGHT* (3 / 8)), "hard", font, RED, GREEN) 
            pygame.draw.rect(screen, BLACK, ((3*WIDTH/32 , HEIGHT* 5/16), (150, 75)))
        
        RETURN_HOME = Button(None, (WIDTH/2, HEIGHT * (1 / 8)), "Main Menu", font, RED, GREEN)

        for button in [EASY, HARD, RETURN_HOME]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if EASY.checkForInput(MENU_MOUSE_POS):
                    change_difficulty()
                if HARD.checkForInput(MENU_MOUSE_POS):
                    change_difficulty()
                if RETURN_HOME.checkForInput(MENU_MOUSE_POS):
                    return 0
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return 0

        pygame.display.update()
            



def play():
    
    pygame.display.set_caption('TicTacToe')
    screen.fill(BLACK)
    draw_lines()
    player = 1
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE
                
                if available_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    
                    if check_win(player):
                        game_over = True
                        
                    player = player % 2 + 1 # 1 to 2 and 2 to 1
                    
                    # minimax move
                    
                    
                    
                    if CURR_DIFFICULTY == 0:
                        if not game_over:
                            if best_move():
                                if check_win(2):
                                    game_over = True
                                player = player % 2 + 1
                    
                    else:
                        
                        if not game_over:
                            if random_move():
                                if check_win(2):
                                    game_over = True
                                player = player % 2 + 1
                        
                    
                    
                    if not game_over:
                        if is_board_full():
                            game_over = True
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    game_over = False
                    player = 1
                if event.key == pygame.K_m:
                    return 0
                    
        if not game_over:
            draw_figures()
        else:
            if check_win(1):
                draw_figures(GREEN)
                draw_lines(GREEN)
            elif check_win(2):
                draw_figures(RED)
                draw_lines(RED)
            else:
                draw_figures(GREY)
                draw_lines(GREY)
        
        pygame.display.update()
    
            
             
            

def main():
    main_menu()
    
            
                
if __name__ == "__main__":
    main()