#python vorlage
import pygame
import os
import time
from functions import Button, scrollable_list
import pygame_textinput as pginput
from pgu import gui
import csv
import random as rd
import pandas as pd
from datetime import date, timedelta


#init
pygame.init()
pygame.key.set_repeat(200, 25)
settings=[]
with open("settings.txt", "r") as file:
    settings = eval(file.read())


#root
root = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
WIDTH,HEIGHT = root.get_width(), root.get_height()

#fonts
with open("settings_font.txt", "r") as file:
    current_font = file.readline()

font_h = pygame.font.SysFont(current_font, 70, bold=True)
font_1 = pygame.font.SysFont(current_font, 50, bold=True)
font_2 = pygame.font.SysFont(current_font, 40)
font_3 = pygame.font.SysFont(current_font, 20, italic=True)
font_4 = pygame.font.SysFont(current_font, 30, italic=True)



#colours
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREY = (0, 20, 0)
LIGHT_GREY = (240, 248, 255)
LOW_GREY = (160, 178, 175)
GREEN = (0, 100, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY_1 = (108, 106, 107)
LIGHT_GREEN = (141, 182, 14)
LILA = (124, 15, 102)
RED = (152, 35, 35)

#variables
screen = "homescreen"
current_stack = ""
mode = ""
field = ""
textinput = pginput.TextInputVisualizer(font_object=font_h)
manager = pginput.TextInputManager(validator = lambda input: len(input) <= 25)
listinput = pginput.TextInputVisualizer(manager = manager, font_object=font_1)
manager_2 = pginput.TextInputManager(validator = lambda input: len(input) <= 75)
manager_3 = pginput.TextInputManager(validator = lambda input: len(input) <= 75)
german_input = pginput.TextInputVisualizer(manager = manager_2, font_object=font_2)
english_input = pginput.TextInputVisualizer(manager = manager_3, font_object=font_2)
enter = False
tasks = 0
font_size_german = 40
font_size_english = 40
font_size_name = 50
v_size = 70
e_size = 35
back_color = settings[0]
f = False
selected = 0
test_number = int(settings[1])


#images
background_2 = pygame.transform.scale(pygame.image.load(os.path.join("materials", "background_2.png")), (WIDTH-100, HEIGHT-100))
exit_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "exit.png")), (70, 70))
settings_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "settings.png")), (50, 50))
tasks_back = pygame.transform.scale(pygame.image.load(os.path.join("materials", "tasks_back.png")), (700, 530))
grey_color = pygame.image.load(os.path.join("materials", "background_color_grey.png"))
green_color = pygame.image.load(os.path.join("materials", "background_color_green.png"))
light_green_color = pygame.image.load(os.path.join("materials", "background_color_lightgreen.png"))
lila_color = pygame.image.load(os.path.join("materials", "background_color_lila.png"))
red_color = pygame.image.load(os.path.join("materials", "background_color_red.png"))
arrow_up = pygame.transform.scale(pygame.image.load(os.path.join("materials", "arrow_up.png")), (30, 30))
arrow_down = pygame.transform.scale(pygame.image.load(os.path.join("materials", "arrow_down.png")), (30, 30))

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
WEITER_BUTTON = Button(WIDTH-300, 800, font_2.render("Weiter", True, BLACK), 1)
ADD_LIST_BUTTON = Button(3.56 / 10 * WIDTH, 610, font_2.render("+", True, GREEN), 1.5)
ADD_VOCAB_BUTTON = Button(WIDTH-300, HEIGHT-200, font_2.render("add_vocab", True, GREEN), 1)
NEW_VOCAB_BUTTON = Button(WIDTH-320, HEIGHT-150, font_2.render("add vocab", True, GREEN), 0.8)
CORRECT_BUTTON = Button(WIDTH/2-50, HEIGHT - 100, font_2.render("I knew this", True, BLACK), 1)

# Background Buttons
COLOR_BUTTON_1 = Button(550, 220, grey_color, 0.5)
COLOR_BUTTON_2 = Button(650, 220, green_color, 0.5)
COLOR_BUTTON_3 = Button(750, 220, light_green_color, 0.5)
COLOR_BUTTON_4 = Button(850, 220, lila_color, 0.5)
COLOR_BUTTON_5 = Button(950, 220, red_color, 0.5)

# Font Buttons
FONT_BUTTON = Button(300, 350, font_2.render(f"{current_font}                     ", True, BLACK), 1)
FONT_1 = Button(330, 400, pygame.font.SysFont("Arial", 40).render(f"Arial         ", True, BLACK), 1)
FONT_2 = Button(330, 450, pygame.font.SysFont("Calibri", 40).render(f"Calibri       ", True, BLACK), 1)
FONT_3 = Button(330, 500, pygame.font.SysFont("maiandragd", 40).render(f"maiandragd    ", True, BLACK), 1)
FONT_4 = Button(330, 550, pygame.font.SysFont("MV Boli", 40).render(f"MV Boli       ", True, BLACK), 1)

# Words in tests
BUTTON_10 = Button(500, 470, font_2.render("10", True, BLACK), 1)
BUTTON_15 = Button(600, 470, font_2.render("15", True, BLACK), 1)
BUTTON_30 = Button(700, 470, font_2.render("30", True, BLACK), 1)
BUTTON_50 = Button(800, 470, font_2.render("50", True, BLACK), 1)


def show_window():
    global current_stack
    global listinput
    background = pygame.Rect(0, 0, WIDTH, HEIGHT)
    pygame.draw.rect(root, back_color, background)
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
        if stacks.index(element) <= 4:
            spot = 320 + 70 * stacks.index(element)
            BUTTON = Button(2/10*WIDTH-30, spot, font_2.render(f"{element}", True, BLACK), 1)
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
    global font_size_name
    if HOME_BUTTON.draw(root):
        screen="homescreen"
    # Rectangel in background
    pygame.draw.rect(root, WHITE, (1 / 10 * WIDTH, 200, WIDTH * 8 / 10, HEIGHT - 300))
    pygame.draw.rect(root, GREY, (1/10*WIDTH, 200, WIDTH*8/10, HEIGHT-300), width=5)
    # Name of the unit
    rect_name = pygame.Rect(WIDTH / 2 - 210, 250, 400, 100)
    rect_german = pygame.Rect(WIDTH/6-10, 400, german_input.surface.get_width()+10 if german_input.surface.get_width() > 200 else 200, 50)
    rect_english = pygame.Rect(WIDTH/6-10, 600, english_input.surface.get_width()+10 if english_input.surface.get_width() > 200 else 200, 50)
    pygame.draw.rect(root, LIGHT_GREY, (WIDTH/2-210, 250, 400, 100))
    pygame.draw.rect(root, GREY, (WIDTH/2-210, 250, 400, 100), width=4)
    pygame.draw.rect(root, LIGHT_GREY, rect_german)
    pygame.draw.rect(root, GREY, rect_german, width=4)
    pygame.draw.rect(root, LIGHT_GREY, rect_english)
    pygame.draw.rect(root, GREY, rect_english, width=4)
    if listinput.value == "" and field != "name":
        root.blit(font_2.render("Name of the unit", True, LOW_GREY), (WIDTH/2-150, 280))
    root.blit(font_4.render("add question: ", True, BLACK), (WIDTH/6-20, 360))
    root.blit(font_4.render("add answer: ", True, BLACK), (WIDTH/6-20, 560))
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
    font_german = pygame.font.SysFont(current_font, font_size_german)
    font_english = pygame.font.SysFont(current_font, font_size_english)
    font_list = pygame.font.SysFont(current_font, font_size_name, bold=True)

    # If input is too big
    if listinput.surface.get_width() > 400:
        font_size_name -= 5
        listinput.font_object = font_list
    if listinput.surface.get_width() < 100:
        font_size_name = 50
        listinput.font_object = font_list
    if german_input.surface.get_width() > 600:
        font_size_german -= 1
        german_input.font_object = font_german
    if english_input.surface.get_width() > 600:
        font_size_english -= 1
        english_input.font_object = font_english
    if german_input.surface.get_width() < 100:
        font_size_german = 40
        german_input.font_object = font_german
    if english_input.surface.get_width() < 100:
        font_size_english = 40
        german_input.font_object = font_german
    if NEW_VOCAB_BUTTON.draw(root):
        add_vocab()

def add_vocab():
    global current_stack
    if german_input.value and english_input.value:
        with open("elements.txt", "r") as file:
            stacks = file.read().splitlines()
        if current_stack:
            with open(f"{listinput.value}.csv", "a") as file:
                file.write(f"{german_input.value},{english_input.value},0,{date.today()}")
                file.write("\n")
            # Change list name
            if listinput.value != current_stack:
                stacks[stacks.index(current_stack)] = listinput.value
                with open("elements.txt", "w") as w:
                    for element in stacks:
                        w.writelines(f"{element}\n")
        else:
            # if stack name does not exist
            if listinput.value not in stacks:
                # if stack name is != 0
                if listinput.value != 0:
                    with open("elements.txt", "a") as file:
                        file.write(listinput.value)
                        file.write("\n")
                        df = pd.DataFrame(columns=["german_word", "english_word", "correct_in_a_row", "date_of_next_question"])
                        df.to_csv(path_or_buf=rf"C:\Users\Norwi\Desktop\Python\vocab_trainer\Trainer (2.0)\{listinput.value}.csv", index=False)
                        current_stack = listinput.value
                        add_vocab()
            else:
                current_stack = listinput.value
                german_input.value = ""
                english_input.value = ""
                field = "german"




def stackscreen():
    global mode
    global screen
    global field
    global enter
    if HOME_BUTTON.draw(root):
        screen="homescreen"
    pygame.draw.rect(root, WHITE, (0.7 / 10 * WIDTH, 190, 470, 600))
    pygame.draw.rect(root, GREY, (0.7 / 10 * WIDTH, 190, 470, 600), width=5)
    root.blit(font_h.render(current_stack, True, BLACK), (1 / 10 * WIDTH, 210))
    root.blit(font_3.render(f"This stack was created by has 100 elements", True, GREY), (0.9 / 10 * WIDTH, 300))
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
        if len(unanswered) >= test_number:
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
        if df["date_of_next_question"][index] <= str(date.today()):
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
    global answer
    global v_size
    global e_size
    vocab = ""
    if HOME_BUTTON.draw(root):
        screen = "homescreen"
    if BACK_BUTTON.draw(root):
        screen = "stackscreen"
    font_v = pygame.font.SysFont(current_font, v_size, bold=True)
    vocab = font_v.render(random_vocab.get("german_word"), True, BLACK)
    if vocab.get_width() >= WIDTH-100:
        v_size -= 10
    root.blit(vocab, (WIDTH / 2 - vocab.get_width() / 2, 300))
    root.blit(textinput.surface, (WIDTH / 2 - textinput.surface.get_width() / 2, 540))
    if enter == False:
        if ENTER_BUTTON.draw(root):
            answer = True
            if textinput.value != random_vocab.get("english_word"):
                answer = False
                wrong.append(random_vocab)
            unanswered.remove(random_vocab)
            enter = True
    if enter:
        if mode != "test":
            if answer:
                root.blit(font_h.render("richtig", True, GREEN), (250, HEIGHT*3/4))
            else:
                root.blit(font_h.render("false", True, RED), (250, HEIGHT*3/4))
                font_e = pygame.font.SysFont(current_font, e_size)
                english_vocab = font_e.render(random_vocab.get("english_word"), True, GREEN)
                root.blit(english_vocab, (WIDTH/2-english_vocab.get_width()/2, 470))
                if CORRECT_BUTTON.draw(root):
                    answer = True
        else:
            check_test()
        if WEITER_BUTTON.draw(root):
            if mode == "elimination":
                check_elimination()
                v_size = 70
            elif mode == "training":
                check_training(answer)
                v_size = 70

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
    if number_vocabs < test_number:
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


def enter_input():
    global field
    global enter
    global answer

    if field == "name":
        field = "german"
    elif field == "german":
        field = "english"
    elif field == "english":
        add_vocab()
        field = "german"
        german_input.value = ""
        english_input.value = ""
    elif screen == "vocab_screen" and enter == False:
        answer = True
        if textinput.value != random_vocab.get("english_word"):
            answer = False
            wrong.append(random_vocab)
        unanswered.remove(random_vocab)
        enter = True
    elif screen == "vocab_screen" and enter:
        if mode == "elimination":
            check_elimination()
        elif mode == "test":
            check_test()
        elif mode == "training":
            check_training(answer)



def settings_screen():
    global screen
    global back_color
    global f
    global current_font
    global selected
    if HOME_BUTTON.draw(root):
        screen = "homescreen"
    root.blit(font_2.render("Words in Test: ", True, BLACK), (150, 470))
    if BUTTON_10.draw(root):
        settings[1] = 10
    if BUTTON_15.draw(root):
        settings[1] = 15
    if BUTTON_30.draw(root):
        settings[1] = 30
    if BUTTON_50.draw(root):
        settings[1] = 50
    if settings[1] == 10:
        pygame.draw.line(root, GREEN, (500, 530), (545, 530), width = 10)
    elif settings[1] == 15:
        pygame.draw.line(root, GREEN, (600, 530), (645, 530), width = 10)
    elif settings[1] == 30:
        pygame.draw.line(root, GREEN, (700, 530), (745, 530), width = 10)
    elif settings[1] == 50:
        pygame.draw.line(root, GREEN, (800, 530), (845, 530), width = 10)
    root.blit(font_2.render("background color: ", True, BLACK), (150, 230))
    if COLOR_BUTTON_1.draw(root):
        back_color = GREY_1
        settings[0] = GREY_1
    if COLOR_BUTTON_2.draw(root):
        back_color = GREEN
        settings[0] = GREEN
    if COLOR_BUTTON_3.draw(root):
        back_color = LIGHT_GREEN
        settings[0] = LIGHT_GREEN
    if COLOR_BUTTON_4.draw(root):
        back_color = LILA
        settings[0] = LILA
    if COLOR_BUTTON_5.draw(root):
        back_color = RED
        settings[0] = RED
    pygame.draw.rect(root, LIGHT_GREY, pygame.Rect(295, 350, 403, 50))
    pygame.draw.rect(root, GREY, pygame.Rect(295, 350, 403, 50), width = 2)
    root.blit(font_2.render("font: ", True, BLACK), (150, 350))
    root.blit(arrow_down, (657, 360))
    if FONT_BUTTON.draw(root):
        f = (True if f == False else False)
    if f:
        pygame.draw.rect(root, WHITE, pygame.Rect(295, 400, 403, 260))
        pygame.draw.rect(root, GREY, pygame.Rect(295, 400, 403, 260), width=1)
        root.blit(arrow_up, (657, 360))
        root.blit(font_3.render("Please Restart the game", True, RED), (350, HEIGHT - 290))
        root.blit(font_3.render("to see the new font", True, RED), (355, HEIGHT-275))
        if FONT_1.draw(root):
            with open("settings_font.txt", "w") as file:
                writer = file.write("Arial")
                selected = 1
        if FONT_2.draw(root):
            with open("settings_font.txt", "w") as file:
                writer = file.write("Calibri")
                selected = 2
        if FONT_3.draw(root):
            with open("settings_font.txt", "w") as file:
                writer = file.write("maiandragd")
                selected = 3
        if FONT_4.draw(root):
            with open("settings_font.txt", "w") as file:
                writer = file.write("MV Boli")
                selected = 4
        if selected == 1:
            pygame.draw.circle(root, BLACK, (310, 425), 8)
        elif selected == 2:
            pygame.draw.circle(root, BLACK, (310, 475), 8)
        elif selected == 3:
            pygame.draw.circle(root, BLACK, (310, 525), 8)
        elif selected == 4:
            pygame.draw.circle(root, BLACK, (310, 575), 8)


def quit():
    with open("settings.txt", "w") as file:
        file.writelines(str(settings))
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
                    enter_input()
        show_window()
    quit()

if __name__ == "__main__":
    main()