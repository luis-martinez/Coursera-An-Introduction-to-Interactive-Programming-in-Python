# "Guess the number" mini-project
# http://www.codeskulptor.org/#user38_wF8rSuTziQ5fxIk.py
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

low = 0
high = 100

# helper function to start and restart the game
def new_game():
	# initialize global variables used in your code here
	global secret_number, remaining_guesses
	secret_number = random.randrange(low, high)
	print
	print "New game. Range is from " + str(low) + " to " + str(high)
	remaining_guesses = int(math.ceil(math.log(high - low + 1, 2)))
	print "Number of remaining guesses is", remaining_guesses


# define event handlers for control panel
def range100():
	# button that changes the range to [0,100) and starts a new game 
	global high
	high = 100
	new_game()

def range1000():
	# button that changes the range to [0,1000) and starts a new game     
	global high
	high = 1000
	new_game()

	
def input_guess(guess):
	# main game logic goes here	
	user_number = int(guess)
	print
	print "Guess was", user_number
	global remaining_guesses
	remaining_guesses = remaining_guesses - 1
	print "Number of remaining guesses is", remaining_guesses
	if remaining_guesses > 0:
		if secret_number < user_number:
			print "Lower"
		elif secret_number > user_number:
			print "Higher"
		else:
			print "Correct"
			new_game()
	else:
		if secret_number == user_number:
			print "Correct"
		else:
			print "You ran out of the guesses. The number was", secret_number
		new_game()

	
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)
frame.start()

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric
