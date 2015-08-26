# implementation of Spaceship - program template for RiceRocks
# http://www.codeskulptor.org/#user38_xwqGoqdYm6j7nQc.py

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
angle = 0
c = 0.1
rocks = 12
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan+20
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if not self.thrust:            
            canvas.draw_image(self.image,self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
    def update(self):
        
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0]*1.2
            self.vel[1] += forward[1]*1.2
        
        self.angle += self.angle_vel
        self.vel[0] *= (1-c)
        self.vel[1] *= (1-c)
        #update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
    def rotate(self,direction):
        if direction == "left":
            self.angle_vel = -0.1
        elif direction == "right":
            self.angle_vel = 0.1
            
    def stop_rotate(self):
        self.angle_vel = 0
        
    def move(self):
        self.thrust = True
        ship_thrust_sound.play()
        
    def not_move(self):
        self.thrust = False
        ship_thrust_sound.pause()
        ship_thrust_sound.rewind()
        
    def shoot(self):
        global missile_group
        missile_sound.play()        
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 5 * forward[0], self.vel[1] + 5 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]], self.image_size, 
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT  
        
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True
        
    def collide(self, other_object):
        if dist(self.get_position(), other_object.get_position()) <= self.get_radius() + other_object.get_radius():
            return True
        else:
            return False
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    
def group_collide(group, other_object):
    collision_num = 0
    removeEls = set([])
    for sprite in group:
        if sprite.collide(other_object):
            explosion_group.add(Sprite(sprite.pos, [0, 0], 0, 0, explosion_image, explosion_info))
            explosion_sound.rewind()
            explosion_sound.play()
            removeEls.add(sprite)
            collision_num += 1
    if(len(removeEls) > 0):
        group.difference_update(removeEls)
    return collision_num

def group_group_collide(group1, group2):
    collision_num = 0
    removeEls = set([])
    for sprite in group1:
        if group_collide(group2, sprite) > 0:
            removeEls.add(sprite)
            collision_num += 1
    if(len(removeEls) > 0):
        group1.difference_update(removeEls)
    return collision_num    
            
           
def draw(canvas):
    global time, lives,started,score,rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('Lives ', (50, 50), 30, 'White')
    canvas.draw_text(str(lives), (50, 80), 30, 'White')
    canvas.draw_text('Score ', (700, 50), 30, 'White')
    canvas.draw_text(str(score) , (700, 80), 30, 'White')
    # draw ship and sprites
    my_ship.draw(canvas)
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    process_sprite_group(canvas,rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    #a_missile.update()
    
    if group_collide(rock_group, my_ship) > 0:
        lives -= 1
    if lives == 0:
        started = False
        soundtrack.pause()
        rock_group = set([])
    score += group_group_collide(rock_group, missile_group)
    if group_collide(rock_group, my_ship) > 0:
        lives -= 1
    if lives == 0:
        started = False
        soundtrack.pause()
        rock_group = set([])
    score += group_group_collide(rock_group, missile_group)

 
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())        

#keydown and key up

def keydown(key):
     if key==simplegui.KEY_MAP["left"]:
       my_ship.rotate("left")
     elif key==simplegui.KEY_MAP["right"]:
       my_ship.rotate("right")
     elif key==simplegui.KEY_MAP["up"]:
       my_ship.move()
     elif key==simplegui.KEY_MAP["space"]:
       my_ship.shoot()
                    
        
        
        
def keyup(key):
    if key==simplegui.KEY_MAP["left"]:        
        my_ship.stop_rotate()        
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.stop_rotate()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.not_move()
        
def click(pos):
    global started, score, lives, ROCK_MAX
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        ship_thrust_sound.rewind()
        explosion_sound.rewind()
        missile_sound.rewind()
        soundtrack.rewind()
        soundtrack.play()
        score = 0
        lives = 3
        ROCK_MAX = 12
        
        
def rock_spawner():
    global rock_group,my_ship
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random()*0.8-0.4, random.random()*0.8-0.4,]
    rock_angle_vel = random.random()*0.2 - 0.1
    if started:
        if len(rock_group) < rocks:
            if dist(rock_pos, my_ship.get_position()) > asteroid_info.get_radius() + my_ship.get_radius():
                rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_angle_vel, asteroid_image, asteroid_info))


def process_sprite_group(canvas, group):
    removeEls = set([])
    it_group = set(group)    
    for sprite in it_group:
        sprite.draw(canvas)
        sprite.update()
        if sprite.update():
            removeEls.add(sprite)
    if(len(removeEls) > 0):
        group.difference_update(removeEls)

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
