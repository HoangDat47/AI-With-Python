import random
import datetime
from tkinter import *

import nltk
from nltk.corpus import words

geneSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
original_counter = 0

def get_random_word(starting_letter):
    filtered_words = [word for word in words.words() if word.startswith(starting_letter)]
    return random.choice(filtered_words)

def gen_parent(length):
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    return ''.join(genes)

def get_fitness(guess):
    return sum(1 for expected, actual in zip(target, guess) if expected == actual)

def mutate(parent):
    index = random.randrange(0, len(parent))
    childGenes = list(parent)
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    return ''.join(childGenes)

def display(guess):
    timeDiff = datetime.datetime.now() - startTime
    fitness = get_fitness(guess)
    print("{}\t{}\t{}".format(guess, fitness, timeDiff))
    label_result.config(text="{}\t{}\t{}".format(guess, fitness, timeDiff))

def get_input():
    initial_word = entry_word.get().lower()
    return initial_word

def reset_game():
    global original_counter, last_letter, target, startTime
    original_counter = 0
    last_letter = ''
    target = ''
    startTime = None
    label_result.config(text="")
    label_last_letter.config(text="")
    entry_word.delete(0, 'end')

def submit_word():
    global original_counter, last_letter, target, startTime

    user_input = get_input()

    if len(user_input) <= 1:
        label_result.config(text="Please enter a word with at least 2 letters.")
        return
    elif user_input not in words.words():
        label_result.config(text="Please enter a valid word.")
        return
        '''elif user_input == "e":
            label_result.config(text="Exiting...")
            return'''
    elif original_counter > 0 and last_letter != user_input[0].lower():
        label_result.config(text="You lose!")
        return

    last_letter = user_input[-1].lower()
    target = get_random_word(last_letter)

    startTime = datetime.datetime.now()
    bestParent = gen_parent(len(target))
    bestFitness = get_fitness(bestParent)
    display(bestParent)

    generation_count = 1
    while True:
        child = mutate(bestParent)
        childFitness = get_fitness(child)
        if bestFitness >= childFitness:
            continue
        display(child)
        if childFitness >= len(bestParent):
            break
        bestFitness = childFitness
        bestParent = child

        generation_count += 1

    label_result.config(text=format(child))
    entry_word.delete(0, 'end')  # Clear entry_word
    last_letter = child[-1].lower()
    label_last_letter.config(text=format(last_letter))
    original_counter += 1

# GUI
master = Tk()
master.title("Word Game")
#master.geometry("320x90")

Label(master, text='Enter a word:').grid(row=0, column=0)
entry_word = Entry(master)
entry_word.grid(row=0, column=1)
#bind the enter key to the submit function
master.bind('<Return>', lambda event=None: button_submit.invoke())

Label(master, text='Word found:').grid(row=1, column=0)
label_result = Label(master, text="")
label_result.grid(row=1, column=1)

Label(master, text='Last letter:').grid(row=2, column=0)
label_last_letter = Label(master, text="")
label_last_letter.grid(row=2, column=1)

button_submit = Button(master, text="Submit", command=submit_word, fg='blue')
button_submit.grid(row=0, column=3)
#bind the 1 key to the submit function
master.bind('1', lambda event=None: button_submit.invoke())

button_clear = Button(master, text="Clear", command=lambda: entry_word.delete(0, 'end'), fg='blue')
button_clear.grid(row=1, column=3)
#bind the 2 key to the clear function
master.bind('2', lambda event=None: button_clear.invoke())

button_play_again = Button(master, text="Restart", command=reset_game, fg='blue')
button_play_again.grid(row=2, column=3)
#bind the 3 key to the restart function
master.bind('3', lambda event=None: button_play_again.invoke())

master.mainloop()
