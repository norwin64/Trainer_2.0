# Vocab_Trainer
import csv
import pandas as pd
from datetime import date, timedelta
import random
import pygame as pg



def create_list():
    # What name should the list have
    name = input("Wie ist der Name der Liste? ")

    # Create a list with the given name
    df = pd.DataFrame(columns=["german_word", "english_word", "correct_in_a_row", "date_of_next_question"])
    df.to_csv(path_or_buf=rf"C:\Users\Norwi\Desktop\Python\vocab_trainer\Trainer (2.0)\{name}.csv", index=False)
    #Switch to Add vocab function
    add_vocab(name)

def add_vocab(name):
    # Ask for vocabs
    german_vocab = input("Wie lautet die deutsche Vokabel? ")
    if german_vocab == "leave":        # Currently the only way to end the function
        return
    english_vocab = input("Wie lautet die englische Vokabel? ")
    # Add the vocabs to the csv file
    with open(f"{name}.csv", "a") as file:
        writer(file).writerow([german_vocab, english_vocab, 0, date.today()])
    # Repeat the function
    add_vocab(name)

def edit_list(name):
    # Choice between "delete vocab", "Change vocab", "Add vocab"
    choose = input("What would you like to do? (d = delete_vocab, c = change_vocab, a = add_vocab)")
    df = pd.read_csv(f"{name}.csv")
    print(df)
    if choose == "d":       # Delete a vocab
        while True:
            ind = input("type in the index of the vocab, which you would like to delete: ")
            col = input("type in the type of the vocab, which you would like to delete: ")
            if ind == "leave":
                break
            df = df.drop(int(ind))
    if choose == "c":       # Change a vocab
        while True:
            ind = input("type in the index of the vocab, which you would like to change: ")
            col = input("type in the type of the vocab, which you would like to delete: ")
            if ind == "leave":
                break
            new_input = input("What should the word look like?")
            df.at[int(ind), col] = new_input
    if choose == "a":       # Add a vocab
        add_vocab(name)
    df.to_csv(path_or_buf=fr"C:\Users\Norwi\Desktop\Python\vocab_trainer\Trainer (2.0)\{name}.csv", index=False)


def ask_vocab(vocab):
    german = vocab.get("german_word")
    english = vocab.get("english_word")
    answer = input(f"What is the english word for {german}?")
    if answer == english:
        print("yeah")
        return True
    else:
        print("nope")
        return False

def elimination_mode(name):
    wrong = []
    with open(f"{name}.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            wrong.append(row)
    while len(wrong) > 0:
        random_number = random.randint(0, len(wrong)-1)
        random_vocab = wrong[random_number]
        if ask_vocab(random_vocab):
            wrong.remove(random_vocab)

def vocab_test(name):
    list = []
    vocab = 0
    right = []
    with open(f"{name}.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            list.append(row)
    if len(list) > 10:
         while vocab != 10:
             random_number = random.randint(0, len(list) - 1)
             random_vocab = list[random_number]
             if ask_vocab(random_vocab):
                 right.append(random_number)
             list.remove(random_vocab)
             vocab += 1
    else:
        print("Sry, but the chosen Unit is not big enough to create a vocab test")

def karteikarten_system(name):
    df = pd.read_csv(f"{name}.csv")
    list = []
    for index in df.index:
        if df["date_of_next_question"][index] == str(date.today()):
            list.append(index)
    while len(list) != 0:
        random_number = list[random.randint(0, len(list) - 1)]
        random_vocab = df.loc[random_number]
        if ask_vocab(random_vocab):
            df.loc[random_number, "correct_in_a_row"]  = int(df.loc[random_number, "correct_in_a_row"]) + 1
            next_day = int(df.loc[random_number, "correct_in_a_row"]) * 2
            df.loc[random_number, "date_of_next_question"] = date.today() + timedelta(next_day)
        else:
            df.loc[random_number, "correct_in_a_row"] = 0
            df.loc[random_number, "date_of_next_question"] = date.today() + timedelta(1)
    list.remove(random_number)
    df.to_csv(path_or_buf=fr"C:\Users\Norwi\Desktop\Python\vocab_trainer\Trainer (2.0)\{name}.csv", index=False)


