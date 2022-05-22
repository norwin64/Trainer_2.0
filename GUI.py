#python vorlage
import pygame
import os
import time
from functions import Button
import pygame_textinput as pginput
import main

#init
pygame.init()
#root
root = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
WIDTH,HEIGHT = root.get_width(), root.get_height()

#fonts
font_h = pygame.font.SysFont("maiandragd", 70, bold=True)
font_1 = pygame.font.SysFont("maiandragd", 50, bold=True)
font_2 = pygame.font.SysFont("maiandragd", 40)
font_3 = pygame.font.SysFont("maiandragd", 20, italic=True)


#colours
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREY = (0, 50, 0)

#variables
screen = "homescreen"
current_stack = ""
mode = ""
textinput = pginput.TextInputVisualizer(font_object=font_h)

#images
background = pygame.transform.scale(pygame.image.load(os.path.join("materials", "background.png")), (WIDTH, HEIGHT))
background_2 = pygame.transform.scale(pygame.image.load(os.path.join("materials", "background_2.png")), (WIDTH-100, HEIGHT-100))
exit_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "exit.png")), (70, 70))
settings_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "settings.png")), (50, 50))
#widgets
EXIT_BUTTON = Button(WIDTH-140, 70, exit_image, 1)
MORE_STACKS_BUTTON = Button(1 / 10 * WIDTH, 700, font_2.render("Click here for more units", True, BLUE), 0.8)
ELIMINATION_MODE_BUTTON = Button(1 / 10 * WIDTH, 470, font_2.render("- Elimination mode", True, BLACK), 1)
TRAINING_MODE_BUTTON = Button(1 / 10 * WIDTH, 580, font_2.render("- Training mode", True, BLACK), 1)
TEST_MODE_BUTTON = Button(1 / 10 * WIDTH, 690, font_2.render("- Test mode", True, BLACK), 1)
HOME_BUTTON = Button(100, 100, font_2.render("Home", True, BLACK), 1)
SETTINGS_BUTTON = Button(75, HEIGHT-120, settings_image, 1)
BACK_BUTTON = Button(300, 100, font_2. render("Back", True, BLACK), 1)



def show_window():
    root.blit(background, (0, 0))
    root.blit(background_2, (50, 50))
    if EXIT_BUTTON.draw(root):
        quit()
    if screen == "homescreen":
        homescreen()
    elif screen == "stackscreen":
        stackscreen()
    elif screen == "settings_screen":
        settings_screen()
    elif screen == "vocab_screen":
        vocab_screen()
    pygame.display.update()

def homescreen():
    global screen
    global current_stack
    if SETTINGS_BUTTON.draw(root):
        screen = "settings_screen"

    # "Your stacks"
    root.blit(font_h.render("Your stacks:", True, BLACK), (1 / 10 * WIDTH, 210))
    # Stacks
    with open("elements.txt", "r") as file:
        stacks = file.read().splitlines()
    for element in stacks:
        if stacks.index(element) <= 2:
            spot = 360 + 110 * stacks.index(element)
            BUTTON = Button(1 / 10 * WIDTH, spot, font_2.render(f"*  {element}", True, BLACK), 1)
            if BUTTON.draw(root):
                current_stack = element
                screen = "stackscreen"
                time.sleep(0.1)
        else:
            if MORE_STACKS_BUTTON.draw(root):
                print("weitere stacks")

def stackscreen():
    global mode
    global screen
    if HOME_BUTTON.draw(root):
        screen="homescreen"
    root.blit(font_h.render(current_stack, True, BLACK), (1 / 10 * WIDTH, 210))
    root.blit(font_3.render("This stack was created by Norwin at ...", True, GREY), (1 / 10 * WIDTH, 300))
    root.blit(font_1.render("Lernmodi:", True, BLACK), (2/15*WIDTH, 400))
    if ELIMINATION_MODE_BUTTON.draw(root):
        mode = "elimination"
        screen = "vocab_screen"
    if TRAINING_MODE_BUTTON.draw(root):
        mode = "training"
        screen = "vocab_screen"
    if TEST_MODE_BUTTON.draw(root):
        mode = "test"
        screen = "vocab_screen"

def vocab_screen():
    global screen
    if HOME_BUTTON.draw(root):
        screen = "homescreen"
    if BACK_BUTTON.draw(root):
        screen = "stackscreen"
    vocab = font_h.render("german", True, BLACK)
    root.blit(vocab, (WIDTH/2-vocab.get_width()/2, 300))
    root.blit(textinput.surface, (WIDTH/2 - textinput.surface.get_width()/2, 540))

def settings_screen():
    global screen
    if HOME_BUTTON.draw(root):
        screen = "homescreen"



def quit():
    pygame.display.quit()
    exit()

def main():
    run = True
    while run:
        pygame.time.Clock().tick(FPS)
        textinput.update(pygame.event.get())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        show_window()
    quit()

if __name__ == "__main__":
    main()