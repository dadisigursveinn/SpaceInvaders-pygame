# coding: latin-1
# If you are commenting in icelandic you need the line above.
import pygame
import random

# If we want to use sprites we create a class that inherits from the Sprite class.
# Each class has an associated image and a rectangle.
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid_image
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()

class Missile(pygame.sprite.Sprite):
    def __init__(self, direct_set):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.direction = direct_set

# Lets load the game images and put them into variables
player_image = pygame.image.load('images/player_pad.png')
asteroid_image = pygame.image.load('images/green_ball.png')
missile_image = pygame.image.load('images/missile.png')
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

WHITE = (255, 255, 255)

pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
asteroid_list = pygame.sprite.Group()
# Group to hold missiles
missile_list = pygame.sprite.Group()
# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List so missiles dont turn with ship after beeing shot
old_missiles = pygame.sprite.Group()

for i in range(1):
    block = Asteroid()
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width - 20)
    block.rect.y = random.randrange(screen_height - 160)  # ekki láta asteroid-ana byrja of neðarlega

    asteroid_list.add(block)
    all_sprites_list.add(block)

# Create a player block
player = Player()
player.rect.x = 320
player.rect.y = 355

all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0

# Store direction of ship for missiles direction
player_direction = "UP"

# -------- Main Program Loop -----------
# We need to check out what happens when the player hits the space bar in order to "shoot".
# A new missile is created and gets it's initial position in the "middle" of the player.
# Then this missile is added to the missile sprite-group and also to the all_sprites group.
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player_direction == "UP":
                    shot = Missile("UP")
                if player_direction == "DOWN":
                    shot = Missile("DOWN")
                if player_direction == "LEFT":
                    shot = Missile("LEFT")
                if player_direction == "RIGHT":
                    shot = Missile("RIGHT")
                # shot = Missile()
                shot.rect.x = player.rect.x + 1
                shot.rect.y = player.rect.y - 20
                missile_list.add(shot)
                all_sprites_list.add(shot)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player_direction = "LEFT"
        if player.rect.x < -60:
            player.rect.x = 700
        player.rect.x -= 5
    elif key[pygame.K_RIGHT]:
        player_direction = "RIGHT"
        if player.rect.x > 700:
            player.rect.x = - 60
        player.rect.x += 5
    if key[pygame.K_UP]:
        player_direction = "UP"
        if player.rect.y < -60:
            player.rect.y = 700
        player.rect.y -= 5
    elif key[pygame.K_DOWN]:
        player_direction = "DOWN"
        if player.rect.y > 700:
            player.rect.y = - 60
        player.rect.y += 5

    screen.blit(backround_image, (0, 0))

    # Below is another good example of Sprite and SpriteGroup functionality.
    # It is now enough to see if some missile has collided with some asteroid
    # and if so, they are removed from their respective groups.
    # In other words:  A missile exploded and so did an asteroid.

    # See if the player block has collided with anything.
    pygame.sprite.groupcollide(missile_list, asteroid_list, True, True)

    # Missiles move at a constant speed up the screen, towards the enemy
    for shot in missile_list:
        if shot.direction == "UP":
            shot.rect.y -= 5
        if shot.direction == "DOWN":
            shot.rect.y += 5
        if shot.direction == "LEFT":
            shot.rect.x -= 5
        if shot.direction == "RIGHT":
            shot.rect.x += 5

    # All the enemies move down the screen at a constant speed
    for block in asteroid_list:
        block.rect.y += 1

    # End game if there are no more enemyes
    if len(asteroid_list) <= 0:
        done = True

    # Check if enemy chrases into mothership
    if pygame.sprite.spritecollide(player, asteroid_list, True):
        done = True

    # Draw all the spites
    all_sprites_list.draw(screen)
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()


