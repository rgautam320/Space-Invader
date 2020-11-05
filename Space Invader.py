import pygame as pg
import random
import math
from pygame import mixer

# Initialize PyGame
pg.init()

# Create the Screen
screen = pg.display.set_mode((800, 600))

# Setting the Title Window
pg.display.set_caption('Space Invater')  # Setting up Title
logo = pg.image.load('ufo.png')  # Setting up Icon for the window
pg.display.set_icon(logo)

# for Background
background = pg.image.load('back.png')

# Background Music
mixer.music.load('background.mp3')
mixer.music.play(-1)

# Creating and Positioning the Player
playerImg = pg.image.load('player.png')
playerX = 368
playerY = 480
playerX_change = 0
playerY_change = 0

# Creating and Positioning the Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10
for i in range(no_of_enemies):
    enemyImg.append(pg.image.load('enemy.png'))
    enemyX.append(random.randint(10, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(32)

# Creating and Positioning the Bullet
bulletImg = pg.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
# Ready - Bullet is ready to fire
# Fire - Bullet is currently moving
bullet_state = "Ready"

# Score Showing
score = 0
fire = 0
font = pg.font.Font('freesansbold.ttf', 32)

score_X = 20
score_Y = 20
fire_X = 20
fire_Y = 64

# Game Over text
over_font = pg.font.Font('freesansbold.ttf', 72)


def score_show(x, y):
    score_value = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def fire_count(x, y):
    f_count = font.render("Fire Count : " + str(fire), True, (255, 255, 255))
    screen.blit(f_count, (x, y))


def game_over():
    over_text = font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y - 16))


def isCollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt(math.pow(bulletX - enemyX, 2) + math.pow(bulletY - enemyY, 2))
    if distance <= 10:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # For The Background
    screen.fill((120, 120, 120))
    screen.blit(background, (0, 0))

    # Writing code for Exit Button
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # If keystroke is pressed, check whether it's left, right or space
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = - 2
            if event.key == pg.K_RIGHT:
                playerX_change = 2
            if event.key == pg.K_SPACE:
                if bullet_state == "Ready":
                    fire += 1
                    # Getting the current state of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        # If keystroke is released
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0

    # Moving the player and enemy in X-axis
    # Setting up Boundary for the spaceship and calling
    playerX += playerX_change
    if playerX <= 10:
        playerX = 10
    elif playerX >= 726:
        playerX = 726
    player(playerX, playerY)

    # Setting up Boundary for the enemy and calling
    for i in range(no_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(no_of_enemies):
                enemyY[j] = 600
            game_over()
            break

        # Moving the enemy
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 10:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 726:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            bulletY = 480
            bullet_state = "Ready"
            score += 1
            enemyX[i] = random.randint(10, 736)
            enemyY[i] = random.randint(50, 150)
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
        enemy(enemyX[i], enemyY[i], i)

    # Firing a bullet
    if bulletY <= 10:
        bulletY = 480
        bullet_state = "Ready"

    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Showing the text
    score_show(score_X, score_Y)
    fire_count(fire_X, fire_Y)

    # Updating everything
    pg.display.update()
