# implementation of card game - Memory
# http://www.codeskulptor.org/#user38_k0lmT574Xte8ePV.py

import simplegui
import random

# helper function to initialize globals
def new_game():
    global numbers, exposed, card_position, state, cards_flipped, turns, label
    state = 0
    turns = 0
    label.set_text("Turns = " + str(turns))
    cards_flipped = []
    numbers = []
    numbers.extend(range(8))
    numbers.extend(range(8))
    random.shuffle(numbers)
    exposed = []
    for x in range(16):
        exposed.append(False)
    card_position = []
    start = 4
    end = 49 - 5
    for x in range(16):
        card_position.append([start, end])
        start += 50
        end += 50

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, cards_flipped, label, turns
    c = 0
    for n in range(16):
        if ((card_position[c][0] <= pos[0]) and (pos[0] <= card_position[c][1])):
            card_number = n
            if not exposed[card_number]:
                exposed[card_number] = True
                if state == 0:
                    state = 1
                    cards_flipped.append(card_number)
                elif state == 1:
                    state = 2
                    turns += 1
                    label.set_text("Turns = " + str(turns))
                    cards_flipped.append(card_number)
                else:
                    state = 1
                    if numbers[cards_flipped[0]] != numbers[cards_flipped[1]]:
                        exposed[cards_flipped[0]] = False
                        exposed[cards_flipped[1]] = False
                    cards_flipped.pop()
                    cards_flipped.pop()
                    cards_flipped.append(card_number)
        c += 1

                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    pos = 0
    for n in range(16):
        if exposed[n]:
            canvas.draw_text(str(numbers[n]),[10+pos,70],65,"White")
        else:
            rectangle = [ [5+pos,5], [45+pos,5], [45+pos,95], [5+pos,95] ]
            canvas.draw_polygon(rectangle, 5, "Green", "Green")  
        pos += 50
        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
