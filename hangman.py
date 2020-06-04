#Hangman Game
import pygame
import random


pygame.init()
pygame.font.init()
HEIGHT = 480
WIDTH = 700
win = pygame.display.set_mode((WIDTH, HEIGHT))

BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0,)
WHITE = (255,255,255)
BLACK = (0,0,0)
LGT_BLUE = (0,255,255)

button_font = pygame.font.SysFont('comicsans', 20)
guess_font = pygame.font.SysFont('monospace', 24)
loss_font = pygame.font.SysFont('comicsans', 45)

word = ''
buttons = []
guessed = []

hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

guess_count = 0

def redraw_game_window():
    global guessed, hangmanPics, guess_count
    win.fill(LGT_BLUE)
    for i in range(len(buttons)):
        if buttons[i][4]:
            # buttons = [color, x, y, radius, visible, character]
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = button_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width()/2), buttons[i][2] - (label.get_height()/2)))
            
    spaced = spacedOut(word, guessed)
    label = guess_font.render(spaced, 1, BLACK)
    rect = label.get_rect()
    length = rect[2]
    
    win.blit(label, (WIDTH/2 - length/2, 400))
    
    pic = hangmanPics[guess_count]
    win.blit(pic, (WIDTH/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()


def spacedOut(word, guessed=[]):
    spacedWord = '' 
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' ' 
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord

def randomWord(fileName):
    file = open(fileName)
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)
    
    return f[i][:-1]

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False
    
def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]

def end(filename, winner=False):
    global guess_count
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'YOU WIN!!! Press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(RED)
    
    if winner == True:
        label = loss_font.render(winTxt, 1, BLACK)
    else:
        label = loss_font.render(lostTxt, 1, BLACK)
        
    wordTxt = loss_font.render(word.upper(), 1, BLACK)
    wordWas = loss_font.render('The word was: ', 1, BLACK)
    
    win.blit(wordTxt, (WIDTH/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (WIDTH/2 - wordWas.get_width()/2, 245))
    win.blit(label, (WIDTH/2 - label.get_width()/2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
                
    reset(filename)
    
    
def reset(fileName):
    global guess_count, guessed, buttons, word
    for i in range(len(buttons)):
        buttons[i][4] = True
        
    guess_count = 0
    guessed = []
    word = randomWord(fileName)
    
def mainMenu():
    click = False
    while True:
        win.fill(GREEN)
        #font = pygame.font.SysFont('comicsans', 50)
        buttonFont = pygame.font.SysFont('comicsans', 30)
        #title = font.render("Hangman", 1, WHITE)
        title = pygame.image.load("header.jpg")
        win.blit(title, (125 , 0))
        
        posx, posy = pygame.mouse.get_pos()
        
        button1 = pygame.Rect(250, 225, 200, 50)
        pygame.draw.rect(win, RED, button1)
        animalButton = buttonFont.render("Animals", 1, WHITE)
        win.blit(animalButton, (272 + animalButton.get_width()/2, 240))
        button2 = pygame.Rect(250, 300, 200, 50)
        pygame.draw.rect(win, RED, button2)
        regularButton = buttonFont.render("Regular Words", 1, WHITE)
        win.blit(regularButton, (215 + regularButton.get_width()/2, 315))
        button3 = pygame.Rect(250, 375, 200, 50)
        pygame.draw.rect(win, RED, button3)
        hardButton = buttonFont.render("Hard Words", 1, WHITE)
        win.blit(hardButton, (240 + hardButton.get_width()/2, 390))
        if button1.collidepoint(posx, posy):
            if click:
                filename = "animals.txt"
                main(filename)
        if button2.collidepoint(posx, posy):
            if click:
                filename = "words.txt"
                main(filename)
        if button3.collidepoint(posx, posy):
            if click:
                filename = "hardWords.txt"
                main(filename)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()

def main(fileName):
    global guess_count, word
    increase = round(WIDTH / 13)
    for i in range(26):
        if i < 13:
            y = 40
            x = int(25 + (increase * i))
        else:
            x = int(25 + (increase * (i - 13)))
            y = 85
        buttons.append([WHITE, x, y, 20, True, 65 + i]) # ([color, x, y, radius, visible, character])
        #print(buttons)
        
    word = randomWord(fileName)
    run = True
    
    while run:
        redraw_game_window()
        pygame.time.delay(10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                letter = buttonHit(click_pos[0], click_pos[1])
                if letter != None:
                    guessed.append(chr(letter))
                    buttons[letter - 65][4] = False
                    if hang(chr(letter)):
                        if guess_count != 5:
                            guess_count += 1
                        else:
                            end(fileName)
                    else:
                        print(spacedOut(word, guessed))
                        if spacedOut(word, guessed).count('_') == 0:
                            end(fileName, True)
                



mainMenu()



