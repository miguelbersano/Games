"""
Warm-up project #1: Game of `Stop` - version 1
•	Computer will play against one player
•	The game will have 5 categories, selected by the player from a menu at the start of each round
•	The player will say when a round stops
•	Computer will tally the results of each play and keep the scores for the round
•	Player can define ‘difficulty level’: 100 is top difficulty level, 0 is minimum difficulty level
•	Computer will randomly select the letter for each play; computer will take care that letters are
    not repeated for a particular game
•	On each play, player will input their choice and computer will show its choice
•	Game will end when player wishes, or when all letters have already been used
•	Computer will show the score for each player at the end of the game
"""
from google import genai
from google.genai import types
genai_client = genai.Client(api_key='AIzaSyDsl2fK1of0JPCnI30oDoEYDIDWBC-_w80')

import string
import os
import random


#function to select a word from category
def select_word(catg_no, letter, dif_level):
    no_options = len(words_of_catg[(catg_no, letter)])
    extra_null_options = round((100 - dif_level)/100 * no_options)
    word_index = random.randint(0, no_options + extra_null_options -1)
#   print(word_index)
    if word_index >= no_options:
        return ''
    else:
        return words_of_catg[(catg_no, letter)][word_index]

#Creating data tables

categories = {1 :'Name', 2 : 'Brand', 3 : 'Country', 4 : 'Fruit', 5 :'Colour', 6 : 'Flower',
              7 : 'Train Station', 8 : 'Animal',9 : 'City'}
no_of_catg = len(categories)

alphabet = list(string.ascii_lowercase)
used_letters = []

words_of_catg = {}
for i in range(1, 10):
    for l in alphabet:
        words_of_catg[(i, l)] = []
#print(words_of_catg)

os.chdir('C:\\Users\\lenovo-miguel\\OneDrive\\Python_100_days_course')

for catg_no in range(1, 10):
    file = open(str(catg_no) + '_' + categories[catg_no] + '.txt')

    # ignore lines beginning with '*', '\n'
    # extract word from all other lines and insert in categories dictionary

    while True:
        file_line = file.readline()
        if len(file_line) == 0:
            break

        if file_line[0] == '*' or file_line[0] == '\n':
            continue

        initial_letter = file_line.index(' ') + 1
        final_letter = file_line.index('\n')
        word = ''

        for j in range(initial_letter, final_letter):
            word += file_line[j]

        words_of_catg_key = (catg_no, word[0].lower())
        #print(f'{words_of_catg_key} : {word}')

        words_of_catg[words_of_catg_key].append(word)

        #print(f'({catg_no}, {word[0].lower()}) : {words_of_catg[(catg_no, word[0].lower())]}')

    file.close()

#Starting a new round

answer = input('Hi, would you like to play STOP with me? ')

if answer != 'yes':
    print('\nOK, see you later')
    exit()

print("\nOK, let's play!")

print('First you have to select the number of categories you want for this round')

n_cat_round = 0

while (n_cat_round > 5) or (n_cat_round < 1):
    print(f'\nNumber of categories must be between 1 and 5')
    n_cat_round = int(input('How many categories do you want for this round? '))

#print(n_cat_round)

order = {1:'first', 2:'second', 3:'third', 4:'fourth', 5:'fifth'}
selected_catgs = []

print('\nThe available categories are:')
for i in range(1, no_of_catg + 1):
    print(f'{i}. {categories[i]}')

i = 1
while i <= n_cat_round:
    j = int(input(f'\nEnter {order[i]} category: '))
    if j < 0 or j > no_of_catg:
        print(f'Category number must be between 1 and {no_of_catg}')
        continue
    selected_catgs.append(j)
    i += 1

print('\nSelected categories are:')
for i in range(0, n_cat_round):
    print(categories[selected_catgs[i]])


print('\nNow you have to select the level of difficulty you want for this round.')

difficulty_level = -1

while (difficulty_level < 0 or difficulty_level > 100):
    print('\nDifficulty level must be between 0 and 100')
    difficulty_level = int(input('Please enter level of difficulty: '))

#print(difficulty_level)

input('\nOK, we are all set. Press ENTER to start playing')

user_score = 0
computer_score = 0
stop = False

while not stop:

    # select letter for this play
    letter_for_play = alphabet[random.randint(0, 25)]
    #letter_for_play = 'a'
    if letter_for_play in used_letters:
        continue
    used_letters.append(letter_for_play)
    print(f'\nLetter for this play is: {letter_for_play}')

    # enter user's words and define computer's words

    list_of_user_words = []
    list_of_computer_words = []

    for i in range(0, n_cat_round):

        while True:
            current_category = categories[selected_catgs[i]]
            user_word = input(f"\nEnter your word for category '{current_category}' : ")
            if user_word == '':
                break
            if list(user_word)[0].lower() == letter_for_play:
                break
            print(f"Your word must begin with '{letter_for_play}' !")

        #check if user word is valid for the category (integration with Gemini)
        if user_word != '':
            print(f'Computer will check if {user_word} is a valid {current_category}; '
                  f'it can take some time, please wait...')
            gemini_response = genai_client.models.generate_content(
                model='gemini-2.0-flash',
                contents=types.Part.from_text(text='is '
                                                    + user_word
                                                    + ' a valid '
                                                    + current_category
                                                    + '?'
                                              ),
                config=types.GenerateContentConfig(
                    temperature=0,
                    top_p=0.95,
                    top_k=20,
                ),
            )

            if gemini_response.text[0:3] != 'Yes':
                print(f'{user_word} is not a valid {current_category}')
                user_word = ''
            else:
                print(f'{user_word} is OK')

        list_of_user_words.append(user_word)

        computer_word = select_word(selected_catgs[i], letter_for_play, difficulty_level)
        list_of_computer_words.append(computer_word)
        print(f"Computer word for category '{current_category}' is: {computer_word}")

        # calculate scores for this category and add to total scores
        if user_word != computer_word:
            if user_word != '':
                user_score += 10
            if computer_word != '':
                computer_score += 10
        else:
            if user_word != '':
                user_score += 5
            if computer_word != '':
                computer_score += 5

    stop = bool(input(f"\nPress 'enter' to continue round, 's' to finish round "))

print(f'\nRound is finished\nUser score is {user_score}\nComputer score is {computer_score}')

if user_score == computer_score:
    print("\nIt's a draw!")
else:
    if user_score > computer_score:
        print('\nCongratulations, you won!')
    else:
        print('\nI won, play better next time!')
        










    


















