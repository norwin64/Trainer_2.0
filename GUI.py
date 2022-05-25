#python vorlage
import pygame
import os
import time
from functions import Button
import pygame_textinput as pginput
from pgu import gui
import csv
import random as rd
import pandas as pd
from datetime import date, timedelta


#init
pygame.init()
pygame.key.set_repeat(200, 25)

#root
root = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
WIDTH,HEIGHT = root.get_width(), root.get_height()

#fonts
font_h = pygame.font.SysFont("maiandragd", 70, bold=True)
font_1 = pygame.font.SysFont("maiandragd", 50, bold=True)
font_2 = pygame.font.SysFont("maiandragd", 40)
font_3 = pygame.font.SysFont("maiandragd", 20, italic=True)
font_4 = pygame.font.SysFont("maiandragd", 30, italic=True)



#colours
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREY = (0, 20, 0)
LIGHT_GREY = (240, 248, 255)
GREEN = (0, 100, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#variables
screen = "homescreen"
current_stack = ""
mode = ""
field = ""
textinput = pginput.TextInputVisualizer(font_object=font_h)
manager = pginput.TextInputManager(validator = lambda input: len(input) <= 12)
listinput = pginput.TextInputVisualizer(manager = manager, font_object=font_1)
manager_2 = pginput.TextInputManager(validator = lambda input: len(input) <= 30)
manager_3 = pginput.TextInputManager(validator = lambda input: len(input) <= 30)
german_input = pginput.TextInputVisualizer(manager = manager_2, font_object=font_2)
english_input = pginput.TextInputVisualizer(manager = manager_3, font_object=font_2)
enter = False
tasks = 0
font_size_german = 40
font_size_english = 40

#images
background = pygame.transform.scale(pygame.image.load(os.path.join("materials", "background.png")), (WIDTH, HEIGHT))
background_2 = pygame.transform.scale(pygame.image.load(os.path.join("materials", "background_2.png")), (WIDTH-100, HEIGHT-100))
exit_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "exit.png")), (70, 70))
settings_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "settings.png")), (50, 50))
tasks_back = pygame.transform.scale(pygame.image.load(os.path.join("materials", "tasks_back.png")), (700, 530))


#widgets
EXIT_BUTTON = Button(WIDTH-140, 70, exit_image, 1)
MORE_STACKS_BUTTON = Button(1 / 10 * WIDTH, 700, font_2.render("Click here for more units", True, BLUE), 0.8)
ELIMINATION_MODE_BUTTON = Button(1 / 10 * WIDTH, 470, font_2.render("- Elimination mode", True, BLACK), 1)
TRAINING_MODE_BUTTON = Button(1 / 10 * WIDTH, 580, font_2.render("- Training mode", True, BLACK), 1)
TEST_MODE_BUTTON = Button(1 / 10 * WIDTH, 690, font_2.render("- Test mode", True, BLACK), 1)
HOME_BUTTON = Button(100, 100, font_2.render("Home", True, BLACK), 1)
SETTINGS_BUTTON = Button(75, HEIGHT-120, settings_image, 1)
BACK_BUTTON = Button(300, 100, font_2. render("Back", True, BLACK), 1)
ENTER_BUTTON = Button(WIDTH-300, 690, font_1.render("Enter", True, BLACK), 1)
WEITER_BUTTON = Button(WIDTH-300, 580, font_2.render("Weiter", True, BLACK), 1)
ADD_LIST_BUTTON = Button(3.56 / 10 * WIDTH, 610, font_2.render("+", True, GREEN), 1.5)
ADD_VOCAB_BUTTON = Button(WIDTH-300, HEIGHT-300, font_2.render("add_vocab", True, GREEN), 1)
NEW_VOCAB_BUTTON = Button(WIDTH-100, HEIGHT-100, font_2.render("new_vocab", True, GREEN), 1)


def show_window():
    global current_stack
    global listinput
    root.blit(background, (0, 0))
    root.blit(background_2, (50, 50))
    if EXIT_BUTTON.draw(root):
        quit()
    if screen == "homescreen":
        current_stack = ""
        listinput.value = ""
        homescreen()
    elif screen == "stackscreen":
        stackscreen()
    elif screen == "settings_screen":
        settings_screen()
    elif screen == "vocab_screen":
        vocab_screen()
    elif screen == "edit_screen":
        edit_vocab_screen()

    pygame.display.update()

def homescreen():
    global tasks
    global screen
    global current_stack
    global mode
    global field
    tasks = []
    if SETTINGS_BUTTON.draw(root):
        screen = "settings_screen"
    pygame.draw.rect(root, WHITE, (0.7/10*WIDTH, 190, 470, 500))
    pygame.draw.rect(root, GREY, (0.7/10*WIDTH, 190, 470, 500), width = 5)
    root.blit(tasks_back, (4.7 / 10 * WIDTH, 190))
    # "Your stacks"
    root.blit(font_h.render("Your units", True, BLACK), (1/10 * WIDTH, 210))
    root.blit(font_1.render("Your tasks", True, BLACK), (5.8/10 * WIDTH, 300))
    root.blit(font_2.render("Today", True, BLACK), (7/10 * WIDTH, 220))

    if ADD_LIST_BUTTON.draw(root):
        screen = "edit_screen"
        field = ""
        time.sleep(0.2)
    # Stacks
    with open("elements.txt", "r") as file:
        stacks = file.read().splitlines()
    for element in stacks:
        if stacks.index(element) <= 2:
            spot = 340 + 70 * stacks.index(element)
            BUTTON = Button(2 / 10 * WIDTH, spot, font_2.render(f"{element}", True, BLACK), 1)
            if len(check_current_tasks(element)) != 0:
                tasks.append(element)
                BUTTON_TASK = Button(820, 340 + 68  * len(tasks), font_2.render(f"{element}      {len(check_current_tasks(element))} vocabs", True, BLACK), 1)
                if BUTTON_TASK.draw(root):
                    current_stack = element
                    screen = "vocab_screen"
                    mode = "training"
                    textinput.value = ""
                    time.sleep(0.1)
                    set_lists()
            if BUTTON.draw(root):
                current_stack = element
                screen = "stackscreen"
                time.sleep(0.2)
        else:
            if MORE_STACKS_BUTTON.draw(root):
                print("weitere stacks")

def edit_vocab_screen():
    global screen
    global field
    global font_size_german
    global font_size_english
    if HOME_BUTTON.draw(root):
        screen="homescreen"
    # Rectangel in background
    pygame.draw.rect(root, WHITE, (1 / 10 * WIDTH, 200, WIDTH * 8 / 10, HEIGHT - 300))
    pygame.draw.rect(root, GREY, (1/10*WIDTH, 200, WIDTH*8/10, HEIGHT-300), width=5)
    # Name of the unit
    rect_name = pygame.Rect(WIDTH / 2 - 210, 250, 400, 100)
    rect_german = pygame.Rect(WIDTH/6-10, 400-3, german_input.surface.get_width()+10 if german_input.surface.get_width() > 200 else 200, 50)
    rect_english = pygame.Rect(WIDTH/6-10, 600, english_input.surface.get_width()+10 if english_input.surface.get_width() > 200 else 200, 50)
    pygame.draw.rect(root, LIGHT_GREY, (WIDTH / 2 - 210, 250, 400, 100))
    pygame.draw.rect(root, GREY, (WIDTH/2-210, 250, 400, 100), width=4)
    pygame.draw.rect(root, GREY, rect_german, width=4)
    pygame.draw.rect(root, GREY, rect_english, width=4)
    root.blit(font_3.render("name", True, BLACK), (9.5*WIDTH/16, 320))
    root.blit(font_4.render("query box: ", True, BLACK), (WIDTH/6-20, 350))
    root.blit(font_4.render("answer box: ", True, BLACK), (WIDTH/6-20, 550))
    root.blit(listinput.surface, (WIDTH / 2 - listinput.surface.get_width() / 2, 265))
    root.blit(german_input.surface, (WIDTH/6, 400))
    root.blit(english_input.surface, (WIDTH/6, 600))
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if rect_name.collidepoint(pos):
            field = "name"
        elif rect_german.collidepoint(pos):
            field = "german"
        elif rect_english.collidepoint(pos):
            field = "english"
    listinput.cursor_visible = False
    german_input.cursor_visible = False
    english_input.cursor_visible = False
    if field == "name":
        listinput.cursor_visible = True
    if field == "german":
        german_input.cursor_visible = True
    if field == "english":
        english_input.cursor_visible = True
    font_german = pygame.font.SysFont("maiandragd", font_size_german)
    font_english = pygame.font.SysFont("maiandragd", font_size_english)
    # If input is too big
    if german_input.surface.get_width() > 600:
        font_size_german -= 1
        german_input.font_object = font_german
    if english_input.surface.get_width() > 600:
        font_size_english -= 1
        english_input.font_object = font_english
    if NEW_VOCAB_BUTTON.draw(root):
        add_vocab()

def add_vocab():
    with open(f"{listinput.value}.csv", "a") as file:
        print(german_input.value)
        writer = file.write(f"{german_input.value}, {english_input.value}, 0, {date.today()}")




def stackscreen():
    global mode
    global screen
    global field
    if HOME_BUTTON.draw(root):
        screen="homescreen"
    pygame.draw.rect(root, WHITE, (0.7 / 10 * WIDTH, 190, 470, 600))
    pygame.draw.rect(root, GREY, (0.7 / 10 * WIDTH, 190, 470, 600), width=5)
    root.blit(font_h.render(current_stack, True, BLACK), (1 / 10 * WIDTH, 210))
    root.blit(font_3.render("This stack was created by Norwin at ...", True, GREY), (1 / 10 * WIDTH, 300))
    root.blit(font_1.render("Lernmodi:", True, BLACK), (2/15*WIDTH, 400))
    set_lists()
    textinput.value = ""
    enter = False
    if ELIMINATION_MODE_BUTTON.draw(root):
        mode = "elimination"
        screen = "vocab_screen"
    if TRAINING_MODE_BUTTON.draw(root):
        mode = "training"
        screen = "vocab_screen"
        set_lists()
    if TEST_MODE_BUTTON.draw(root):
        if len(unanswered) >= 10:
            mode = "test"
            screen = "vocab_screen"
        else:
            print("Sry, but the dataset is not big enough")
    if ADD_VOCAB_BUTTON.draw(root):
        screen = "edit_screen"
        field = ""
        listinput.value = current_stack

def check_current_tasks(stacks):
    df = pd.read_csv(f"{stacks}.csv")
    to_do = []
    for index in df.index:
        if df["date_of_next_question"][index] == str(date.today()):
            to_do.append(index)
    return to_do




def set_lists():
    global unanswered
    global wrong
    global number_vocabs
    global screen
    global mode
    unanswered = []
    wrong = []
    number_vocabs = 1
    with open(f"{current_stack}.csv", "r") as file:
        reader = csv.DictReader(file)
        if mode != "training":
            for row in reader:
                unanswered.append(row)
                set_vocab()
        else:
            for row in reader:
                if row.get("date_of_next_question") == str(date.today()):
                    unanswered.append(row)
            if len(unanswered) == 0:
                screen = "all_finished"
                mode = None
            else:
                set_vocab()

def set_vocab():
    global random_vocab
    random_vocab = unanswered[rd.randint(0, len(unanswered) - 1)]

def vocab_screen():
    global wrong
    global unanswered
    global screen
    global enter
    vocab = ""
    if HOME_BUTTON.draw(root):
        screen = "homescreen"
    if BACK_BUTTON.draw(root):
        screen = "stackscreen"
    vocab = font_h.render(random_vocab.get("german_word"), True, BLACK)
    root.blit(vocab, (WIDTH / 2 - vocab.get_width() / 2, 300))
    root.blit(textinput.surface, (WIDTH / 2 - textinput.surface.get_width() / 2, 540))
    if ENTER_BUTTON.draw(root):
        global answer
        answer = True
        if textinput.value != random_vocab.get("english_word"):
            answer = False
            wrong.append(random_vocab)
        unanswered.remove(random_vocab)
        enter = True
    if enter:
        if answer:
            root.blit(font_h.render("richtig", True, GREEN), (WIDTH-300, HEIGHT/2))
        else:
            root.blit(font_h.render("false", True, RED), (WIDTH-300, HEIGHT/2))
        if WEITER_BUTTON.draw(root):
            if mode == "elimination":
                check_elimination()
            elif mode == "test":
                check_test()
            elif mode == "training":
                check_training(answer)

def check_training(answer):
    global random_vocab
    global unanswered
    global enter
    global screen
    df = pd.read_csv(f"{current_stack}.csv")
    textinput.value = ""
    enter = False
    index_vocabs = df[df["german_word"] == random_vocab.get("german_word")].index.values.tolist()
    if len(unanswered) != 0:
        set_vocab()
    else:
        screen = "endscreen"
    for index_vocab in index_vocabs:
        if answer:
            df.loc[index_vocab, "correct_in_a_row"] = int(df.loc[index_vocab, "correct_in_a_row"]) + 1
            next_day = int(df.loc[index_vocab, "correct_in_a_row"]) * 2
            df.loc[index_vocab, "date_of_next_question"] = date.today() + timedelta(next_day)
        else:
            df.loc[index_vocab, "correct_in_a_row"] = 0
            df.loc[index_vocab, "date_of_next_question"] = date.today() + timedelta(1)
    df.to_csv(path_or_buf=fr"C:\Users\Norwi\Desktop\Python\vocab_trainer\Trainer (2.0)\{current_stack}.csv", index=False)



def check_test():      # What is next => unanswered vocab, end mode
    global unanswered
    global wrong
    global enter
    global screen
    global number_vocabs
    if number_vocabs < 10:
        set_vocab()
        number_vocabs +=1
    else:
        screen = "auswertung_test"        # wrong liste enthält alle falschen Vokabeln
    textinput.value = ""
    enter = False

def check_elimination():   # What is next => unanswered vocab, wrong vocabs or back to homescreen
    global unanswered
    global wrong
    global enter
    global screen
    global random_vocab
    if len(unanswered) > 0:
        set_vocab()
    elif len(wrong) > 0:
        unanswered = [x for x in wrong]
        wrong = []
        set_vocab()
    else:
        screen = "stackscreen"
    textinput.value = ""
    enter = False


def enter():
    global field
    if field == "name":
        field = "german"
    elif field == "german":
        field = "english"
    elif field == "english":
        add_vocab()

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
        events = pygame.event.get()

        textinput.update(events)
        if field == "name":
            listinput.update(events)
        if field == "german":
            german_input.update(events)
        if field == "english":
            english_input.update(events)

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enter()
        show_window()
    quit()

if __name__ == "__main__":
    main()