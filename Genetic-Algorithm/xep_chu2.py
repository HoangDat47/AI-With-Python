import random
import datetime

#Từ điển tiếng Anh
import nltk

#GUI
import tkinter as tk

# Download the words dataset
#nltk.download('words')

from nltk.corpus import words

geneSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

def get_random_word(starting_letter):
    filtered_words = [word for word in words.words() if word.startswith(starting_letter)]
    return random.choice(filtered_words)

def gen_parent(length):
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    return ''.join(genes)

def get_fitness(guess): return sum(1 for expected, actual in zip(target, guess) if expected == actual)

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

random.seed()
original_counter = 0

while True:
    # Get user input for the initial word
    initial_word = input("Enter a word: ").lower()
    if len(initial_word) < 2 and initial_word != "e":
        print("Please enter a word with at least 2 letter")
        continue
    elif initial_word not in words.words():
        print("Please enter a valid word")
        continue
    elif initial_word == "e":
        print("Exiting...")
        break
    elif original_counter > 0:
        # check if the last letter of the word found is the same as the start letter of the user input
        if last_letter != initial_word.lower():
            print("You lose!")
            break
        elif initial_word == "e":
            print("Exiting...")
            break

    # Use the last letter of the user input to choose a random word from the NLTK words corpus
    last_letter = initial_word[-1].lower()
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

    print("Word found: {}".format(child))
    #save the last letter of the word found to use as the starting letter for the next word
    last_letter = child[-1].lower()
    print("last letter: {}".format(last_letter))
    original_counter += 1
    print("Original counter: {}".format(original_counter))