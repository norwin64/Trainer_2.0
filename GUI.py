#python vorlage
import pygame
import os
from Button import Button

#init
pygame.init()
#root
root = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
WIDTH,HEIGHT = root.get_width(), root.get_height()

#fonts
font_h = pygame.font.SysFont("maiandragd", 70, bold=True)
font_2 = pygame.font.SysFont("maiandragd", 40)


#colours
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)

#variables
screen = "homescreen"
current_stack = ""

#images
background = pygame.transform.scale(pygame.image.load(os.path.join("materials", "background.png")), (WIDTH, HEIGHT))
background_2 = pygame.transform.scale(pygame.image.load(os.path.join("materials", "background_2.png")), (WIDTH-100, HEIGHT-100))
exit_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "exit.png")), (70, 70))

#widgets
EXIT_BUTTON = Button(WIDTH-140, 70, exit_image, 1)
more_stacks = Button(1/10 * WIDTH, 700, font_2.render("Click here for more units", True, BLUE), 0.8)



def show_window():
    root.blit(background, (0, 0))
    root.blit(background_2, (50, 50))
    if EXIT_BUTTON.draw(root):
        quit()
    if screen == "homescreen":
        homescreen()
    elif screen == "stackscreen":
        stackscreen()

    pygame.display.update()

def homescreen():
    global screen
    global current_stack
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
        else:
            if more_stacks.draw(root):
                print("weitere stacks")

def stackscreen():
    pass

def quit():
    pygame.display.quit()
    exit()

def main():
    run = True
    while run:
        pygame.time.Clock().tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        show_window()
    quit()

if __name__ == "__main__":
    main()