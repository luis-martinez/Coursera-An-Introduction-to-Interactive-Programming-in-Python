# Implementation of classic arcade game Pong
# http://www.codeskulptor.org/#user38_wAHaUAbkokH7YC3.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
vel = 15


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    horizontal = random.randrange(120, 240) / 60
    vertical = random.randrange(60, 180) / 60
    
    if direction == RIGHT:
        ball_vel = [horizontal, -vertical]
    else:
        ball_vel = [-horizontal, -vertical]

        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # reset paddles to center
    paddle1_pos = [0 , (HEIGHT / 2) - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH, (HEIGHT / 2) - HALF_PAD_HEIGHT]
    
    # init paddle1_vel, paddle2_vel and scores
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
    # initial direction of the ball
    direction = random.randrange(0,2)
    if direction == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

        
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # left - right - top - bottom
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] >= (paddle1_pos[1] - BALL_RADIUS/2) and ball_pos[1] <= (paddle1_pos[1] + PAD_HEIGHT + BALL_RADIUS/2):
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            spawn_ball(RIGHT)
            score2 += 1
    elif ball_pos[0] >= (WIDTH - (BALL_RADIUS + PAD_WIDTH)):
        if ball_pos[1] >= (paddle2_pos[1] - BALL_RADIUS/2) and ball_pos[1] <= (paddle2_pos[1] + PAD_HEIGHT + BALL_RADIUS/2):
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            spawn_ball(LEFT)
            score1 += 1
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]        
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]    
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    
    # keep paddle on the screen
    if paddle1_pos[1] <= 0:
        paddle1_pos[1] = 0
    if paddle1_pos[1] + PAD_HEIGHT >= HEIGHT:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
    if paddle2_pos[1] <= 0:
        paddle2_pos[1] = 0
    if paddle2_pos[1] + PAD_HEIGHT >= HEIGHT:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT  
    
    # draw paddles
    canvas.draw_line([paddle1_pos[0],paddle1_pos[1]],[paddle1_pos[0],paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH , "White")
    canvas.draw_line([paddle2_pos[0],paddle2_pos[1]],[paddle2_pos[0],paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH , "White")
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 2 - 90, 90], 45, 'White')
    canvas.draw_text(str(score2), [WIDTH / 2 + 90, 90], 45, 'White')

    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += vel


def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel += vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= vel


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', new_game, 200)


# start frame
new_game()
frame.start()
