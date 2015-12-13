# coding: latin-1
# If you are commenting in icelandic you need the line above.
import os
import pygame
import random
import time
pygame.mixer.init()
gamemusic = pygame.mixer.Sound('sounds/music.wav')
gamemusic.play(-1)
# For points
def text_Objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_to_screen(msg, color):
    textSurface, textRrect = text_Objects(msg, color)
    textRrect.center = (screen_width/2), 10
    screen.blit(textSurface, textRrect)
def message_to_screen_mid(msg, color):
    textSurface, textRrect = text_Objects(msg, color)
    textRrect.center = (screen_width/2), (screen_height/2)
    screen.blit(textSurface, textRrect)
def deathmessage(msg,msg2,msg3,color):
    textSurface, textRrect = text_Objects(msg, color)
    textRrect.center = (screen_width/2), (screen_height/2)-25
    screen.blit(textSurface, textRrect)
    textSurface, textRrect = text_Objects(msg2, color)
    textRrect.center = (screen_width/2), (screen_height/2)
    screen.blit(textSurface, textRrect)
    textSurface, textRrect = text_Objects(msg3, color)
    textRrect.center = (screen_width/2), (screen_height/2)+25
    screen.blit(textSurface, textRrect)
# If we want to use sprites we create a class that inherits from the Sprite class.
# Each class has an associated image and a rectangle.
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid_image
        self.rect = self.image.get_rect()
class Asteroid2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid2_image
        self.rect = self.image.get_rect()
class Asteroid3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid3_image
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.direction = "UP"
    def change_dir(self, direction):
        if direction == "UP":
            self.image = player_image
            self.direction = "UP"
        if direction == "DOWN":
            self.image = player_image_down
            self.direction = "DOWN"
        if direction == "LEFT":
            self.image = player_image_left
            self.direction = "LEFT"
        if direction == "RIGHT":
            self.image = player_image_right
            self.direction = "RIGHT"
    def get_dir(self):
        return self.direction


class Missile(pygame.sprite.Sprite):
    def __init__(self, direct_set):
        pygame.sprite.Sprite.__init__(self)
        if direct_set == "UP":
            self.image = missile_image
        if direct_set == "DOWN":
            self.image = missile_image_down
        if direct_set == "LEFT":
            self.image = missile_image_left
        if direct_set == "RIGHT":
            self.image = missile_image_right
        self.rect = self.image.get_rect()
        self.direction = direct_set

# Lets load the game images and put them into variables
player_image = pygame.image.load('images/player_pad.png')
asteroid_image = pygame.image.load('images/green_ball.png')
missile_image = pygame.image.load('images/missile.png')
asteroid2_image = pygame.image.load('images/reen_ball.png')
asteroid3_image = pygame.image.load('images/asteroid.png')

player_image_left = pygame.image.load('images/player_pad_left.png')
asteroid_image_left = pygame.image.load('images/green_ball_left.png')
missile_image_left = pygame.image.load('images/missile_left.png')

player_image_right = pygame.image.load('images/player_pad_right.png')
asteroid_image_right = pygame.image.load('images/green_ball_right.png')
missile_image_right = pygame.image.load('images/missile_right.png')

player_image_down = pygame.image.load('images/player_pad_down.png')
asteroid_image_down = pygame.image.load('images/green_ball_down.png')
missile_image_down = pygame.image.load('images/missile_down.png')

backround_image = pygame.image.load('images/background.jpg')

blaster = pygame.mixer.Sound('sounds/blaster.wav')
explosion = pygame.mixer.Sound('sounds/explosion.wav')

WHITE = (255, 255, 255)
yellow = (255, 255, 20)
black = (255, 255, 255)

pygame.init()


screen_width = 700
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

title = "Space Invaders II"
pygame.display.set_caption(title)

# Font 
font = pygame.font.SysFont(None, 30)

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
asteroid_list = pygame.sprite.Group()
asteroid_list2 = pygame.sprite.Group()
asteroid_list3 = pygame.sprite.Group()
# Group to hold missiles
missile_list = pygame.sprite.Group()
# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List so missiles dont turn with ship after beeing shot
old_missiles = pygame.sprite.Group()

# difficulty increases gradualy
difficulty = 1

def spawn_enemys(diffi):
    # increase difficulty each round
    diffi += 1
    for i in range(2 * difficulty):
        block = Asteroid()
        # Set a random location for the block
        block.rect.x = random.randrange(screen_width - 40)
        block.rect.y = random.randrange(screen_height - 60) - screen_height  # ekki láta asteroid-ana byrja of neðarlega

        asteroid_list.add(block)
        all_sprites_list.add(block)
    for i in range(difficulty):
        block = Asteroid2()
        # Set a random location for the block
        block.rect.x = random.randrange(screen_width - 40)
        block.rect.y = random.randrange(screen_height - 60) - screen_height  # ekki láta asteroid-ana byrja of neðarlega

        asteroid_list2.add(block)
        all_sprites_list.add(block)
    for i in range(difficulty):
        block = Asteroid3()
        # Set a random location for the block
        block.rect.x = random.randrange(screen_width - 30) - screen_width
        block.rect.y = random.randrange(screen_height - 30)  # ekki láta asteroid-ana byrja of neðarlega

        asteroid_list3.add(block)
        all_sprites_list.add(block)

    return diffi

# Create a player block
player = Player()
player.rect.x = screen_width/2
player.rect.y = screen_height-50

all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0

h = screen_height
x = 0
y = 0

x1 = 0
y1 = -h

starting = True 
restarting = False 


# -------- Main Program Loop -----------
# We need to check out what happens when the player hits the space bar in order to "shoot".
# A new missile is created and gets it's initial position in the "middle" of the player.
# Then this missile is added to the missile sprite-group and also to the all_sprites group.
while not done:
    
    while starting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                starting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    starting = False
        message_to_screen_mid("Press SPACE to start the game you can pause at any time with P", WHITE)
        # Draw all the spites
        all_sprites_list.draw(screen)
        # Limit to 60 frames per second
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        pygame.display.update()
        #print("Game paused press any key to continue.")
    print(restarting)
    while restarting:

        # This is a list of 'sprites.' Each block in the program is
        # added to this list. The list is managed by a class called 'Group.'
        asteroid_list = pygame.sprite.Group()
        asteroid_list2 = pygame.sprite.Group()
        asteroid_list3 = pygame.sprite.Group()
        # Group to hold missiles
        missile_list = pygame.sprite.Group()
        # This is a list of every sprite.
        # All blocks and the player block as well.
        all_sprites_list = pygame.sprite.Group()

        # List so missiles dont turn with ship after beeing shot
        old_missiles = pygame.sprite.Group()

        # difficulty increases gradualy
        difficulty = 1

        player = Player()
        player.rect.x = screen_width/2
        player.rect.y = screen_height-50

        all_sprites_list.add(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                restarting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restarting = False
        deathmessage("You died!", "Points: " + str(score), "Press SPACE to play again", WHITE)
        # Draw all the spites
        all_sprites_list.draw(screen)
        # Limit to 60 frames per second
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        pygame.display.update()
        #print("Game paused press any key to continue.")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                blaster.play()
                if player.get_dir() == "UP":
                    shot = Missile("UP")
                    shot.rect.x = player.rect.x 
                    shot.rect.y = player.rect.y - 20
                if player.get_dir() == "DOWN":
                    shot = Missile("DOWN")
                    shot.rect.x = player.rect.x 
                    shot.rect.y = player.rect.y + 20
                if player.get_dir() == "LEFT":
                    shot = Missile("LEFT")
                    shot.rect.x = player.rect.x - 23
                    shot.rect.y = player.rect.y - 1
                if player.get_dir() == "RIGHT":
                    shot = Missile("RIGHT")
                    shot.rect.x = player.rect.x + 23
                    shot.rect.y = player.rect.y - 1
                missile_list.add(shot)
                all_sprites_list.add(shot)
            if event.key == pygame.K_p:
                paused = True
                while paused:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            done = True
                            paused = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                paused = False
                    message_to_screen_mid("Game paused press P to resume", yellow)
                    # Draw all the spites
                    all_sprites_list.draw(screen)
                    # Limit to 60 frames per second
                    clock.tick(60)
                    # Go ahead and update the screen with what we've drawn.
                    pygame.display.flip()
                    pygame.display.update()
                    #print("Game paused press any key to continue.")

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.change_dir("LEFT")
        if player.rect.x < -60:
            player.rect.x = screen_width
        player.rect.x -= 5
    elif key[pygame.K_RIGHT]:
        player.change_dir("RIGHT")
        if player.rect.x > screen_width:
            player.rect.x = - 60
        player.rect.x += 5
    if key[pygame.K_UP]:
        player.change_dir("UP")
        if player.rect.y < -60:
            player.rect.y = screen_height
        if player.rect.y > 0:
            player.rect.y -= 5
    elif key[pygame.K_DOWN]:
        player.change_dir("DOWN")
        if player.rect.y > screen_height:
            player.rect.y = - 60
        if player.rect.y < screen_height - 40:
            player.rect.y += 5

    

    #screen.blit(backround_image, (0, 0))
    y1 += 0.5
    y += 0.5
    screen.blit(backround_image,(x,y))
    screen.blit(backround_image,(x1,y1))
    if y > h:
        y = -h
    if y1 > h:
        y1 = -h

    

    # Below is another good example of Sprite and SpriteGroup functionality.
    # It is now enough to see if some missile has collided with some asteroid
    # and if so, they are removed from their respective groups.
    # In other words:  A missile exploded and so did an asteroid.

    # See if the player block has collided with anything.
    if pygame.sprite.groupcollide(missile_list, asteroid_list, True, True):
        explosion.play()
        score += 10
    if pygame.sprite.groupcollide(missile_list, asteroid_list2, True, True):
        explosion.play()
        score += 20
    if pygame.sprite.groupcollide(missile_list, asteroid_list3, True, True):
        explosion.play()
        score += 2

    # Missiles move at a constant speed up the screen, towards the enemy
    for shot in missile_list:
        if shot.direction == "UP":
            shot.rect.y -= 8
        if shot.direction == "DOWN":
            shot.rect.y += 8
        if shot.direction == "LEFT":
            shot.rect.x -= 8
        if shot.direction == "RIGHT":
            shot.rect.x += 8

    # All the enemies move down the screen at a constant speed
    for block in asteroid_list:
        randomdir = random.randrange(1, 10)
        if randomdir > 5:
            block.rect.x += 1
        elif randomdir < 5:
            block.rect.x -= 1
        block.rect.y += 1.5

    for block in asteroid_list2:
        randomdir2 = random.randrange(1, 10)
        if randomdir2 > 5:
            block.rect.x += 3
        elif randomdir2 < 5:
            block.rect.x -= 3
        block.rect.y += 2.5

    for block in asteroid_list3:
        block.rect.x += 2

    # Start next round if there are no more enemyes
    if len(asteroid_list) <= 0:
        difficulty = spawn_enemys(difficulty)

    # Check if enemy chrases into mothership
    if pygame.sprite.spritecollide(player, asteroid_list, True):
        explosion.play()
        all_sprites_list.remove(player)
        restarting = True
    if pygame.sprite.spritecollide(player, asteroid_list2, True):
        explosion.play()
        all_sprites_list.add(remove)
        restarting = True
    if pygame.sprite.spritecollide(player, asteroid_list3, True):
        explosion.play()
        score -= 10

    # If enemy escapes lose points and kill enemy
    for enemy in asteroid_list: 
        if enemy.rect.y == screen_height + 40:
            score -= 100
            enemy.rect.y = -40
            #asteroid_list.remove(enemy)
    for enemy in asteroid_list2:
        if enemy.rect.y == screen_height + 40:
            score -= 100
            enemy.rect.y = -40
            #asteroid_list2.remove(enemy)
    for asteroid in asteroid_list3:
        if asteroid.rect.x == screen_width + 30:
            asteroid_list2.remove(asteroid)

    message_to_screen("Points: " + str(score), WHITE)

    # Draw all the spites
    all_sprites_list.draw(screen)
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    pygame.display.update()
pygame.quit()


