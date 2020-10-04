import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('assets/bg.png')
pygame.mixer.music.load('assets/background.wav')
pygame.mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('assets/alien.png')
pygame.display.set_icon(icon)

playerImage = pygame.image.load('assets/spacecraft.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemys = 6

for i in range(num_of_enemys):
    enemyImage.append(pygame.image.load('assets/enemy1.png'))
    enemyImage.append(pygame.image.load('assets/enemy2.png'))
    enemyImage.append(pygame.image.load('assets/enemy3.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

bulletImage = pygame.image.load('assets/bulletx.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
game_over = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = game_over.render("GAME OVER :", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = pygame.mixer.Sound("assets/laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemys):
        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemys):
                enemyY[j] = 2000
                game_over_text()
                break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = pygame.mixer.Sound('assets/explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
