"""
User selects: even or odd; computer takes the other option
User inputs an integer number from 0 to 10
Computer generates a random integer number from 0 to 10
If the sum of the two numbers is even, 'even' wins, if it is odd, 'odd' wins
"""
import random


print("Let's play the Even or Odd game!")

#enter user option
user_option = ' '
while user_option not in ['e', 'o']:
    user_option = input('Choose your option (e for even, o for odd):')
if user_option == 'e':
    print('Your option is EVEN')
else:
    print('Your option is ODD')

#user enters theyr number
user_number = -1

while not (isinstance(user_number, int)  and user_number in range(0, 11)):
    try:
        user_number = int((input('Choose your number (from 0 to 10):')))
    except ValueError:
        pass

#computer chooses a random number
computer_number = random.randint(0, 10)
print('Computer number is: ', computer_number)

#add numbers and declare winner
total = computer_number + user_number
print('The total is: ', total)

if total % 2:
    if user_option =='o':
        print('Congratulations, you won!')
    else:
        print('I won!')
else:
    if user_option =='e':
         print('Congratulations, you won!')
    else:
         print('I won!')






