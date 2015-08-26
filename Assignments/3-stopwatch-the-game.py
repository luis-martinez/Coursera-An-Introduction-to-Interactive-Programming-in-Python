# "Stopwatch: The Game"
# http://www.codeskulptor.org/#user38_XQe1Io5dkjbHgch.py

import simplegui

# define global variables
interval = 100
time = 0
x = 0
y = 0
running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A = t/600
    B = t%600/100
    C = t%100/10
    D = t%10
    result = str(A) + ":" + str(B) + str(C) + "." +str(D)
    return result

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running
    timer.start()
    running = True

def stop():
    global x, y, running
    timer.stop()
    if running:
        y = y + 1
        if time % 10 == 0:
            x = x + 1
    running = False

def reset():
    global time, running, x, y
    timer.stop()
    time = 0
    running = False
    x = 0
    y = 0


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time = time + 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time), [100,100], 40, "White")
    canvas.draw_text(str(x)+"/"+str(y), [250,30], 20, "White")


# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)

# register event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(interval, timer_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
