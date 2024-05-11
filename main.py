# Import Modules
import pygame
from pygame import mixer
import math
import random
# Initialize PyGame
pygame.init()
# Create Screen
screen = pygame.display.set_mode((800, 600))
# Backgrounds
background_game = pygame.image.load("background.png")
background_extra = pygame.image.load("space.gif")
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# Player
player_img = pygame.image.load("player.png")
player_x = 370
player_y = 480
player_x_change = 0
# Enemy
enemy_images_list = [
    pygame.image.load("enemy1.png"),
    pygame.image.load("enemy2.png"),
    pygame.image.load("enemy3.png")
]
enemy_number = 0
enemy_number_ll = 3
enemy_number_ul = 5
enemy_img = []
enemy_x = []
enemy_y = []
enemy_dx = []
enemy_dx_ll = 2
enemy_dx_ul = 4
enemy_dy = []
enemy_dy_ll = 30
enemy_dy_ul = 40


def enemy_creation():
    global enemy_number
    enemy_number = random.randint(enemy_number_ll, enemy_number_ul)
    enemy_img.clear()
    enemy_x.clear()
    enemy_y.clear()
    enemy_dx.clear()
    enemy_dy.clear()
    for j in range(enemy_number):
        enemy_img.append(enemy_images_list[random.randint(0, len(enemy_images_list) - 1)])
        enemy_x.append(random.randint(0, 735))
        enemy_y.append(random.randint(50, 150))
        enemy_dx.append(random.randint(enemy_dx_ll, enemy_dx_ul))
        enemy_dy.append(random.randint(enemy_dy_ll, enemy_dy_ul))


# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_in_motion = False
# Score and Level
score_value = 0
level_value = 0
# Fonts
normal_font = pygame.font.Font("Asap-Regular.ttf", 32)
large_font = pygame.font.Font("Asap-Bold.ttf", 64)


# Draw Score and Level
def show_progress():
    score_text = normal_font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    level_text = normal_font.render("Level: " + str(level_value), True, (0, 0, 0))
    screen.blit(level_text, (680, 10))


# Draw Game Over
def show_over():
    over_text = large_font.render("GAME OVER!", True, (50, 50, 50))
    screen.blit(over_text, (200, 250))
    exit_text = normal_font.render("Press the SpaceBar to exit", True, (150, 150, 150))
    screen.blit(exit_text, (200, 500))


# Draw Menu
def menu_text():
    title_text = large_font.render("Space Invaders", True, (50, 50, 50))
    screen.blit(title_text, (170, 230))
    play_text = normal_font.render("PRESS THE SPACEBAR TO PLAY!", True, (150, 150, 150))
    screen.blit(play_text, (160, 400))


# Draw Player
def player(x, y):
    screen.blit(player_img, (x, y))


# Draw Enemy
def enemy(x, y, a):
    screen.blit(enemy_img[a], (x, y))


# Draw Bullet
def fire_bullet(x, y):
    global bullet_in_motion
    bullet_in_motion = True
    screen.blit(bullet_img, (x + 16, y + 10))


# Check if Enemy and Bullet Collided
def collision(x1, y1, x2, y2):
    distance = math.hypot(x1 - x2, y1 - y2)
    if distance < 27:
        return True
    else:
        return False


# Menu Music
mixer.music.load("menu.mp3")
mixer.music.play(-1)
# Menu Screen
game_running = False
over_running = False
menu_running = True
while menu_running:
    # Menu Background
    screen.fill((0, 0, 0))
    screen.blit(background_extra, (0, 0))
    # Display Text
    menu_text()
    for event in pygame.event.get():
        # Game Closer
        if event.type == pygame.QUIT:
            menu_running = False
            game_running = False
            over_running = False
        # If SpaceBar Pressed, Start the Game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu_running = False
                game_running = True
    # Update Display
    pygame.display.update()


# Background Main Game Music
mixer.music.stop()
mixer.music.load("background.wav")
mixer.music.play(-1)
# Main Game
enemy_creation()
while game_running:
    # Display Background
    screen.fill((0, 0, 0))
    screen.blit(background_game, (0, 0))
    # Event Handler
    for event in pygame.event.get():
        # Game Closer
        if event.type == pygame.QUIT:
            game_running = False
            over_running = False
        # Player Controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if not bullet_in_motion:
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    # Prevents Player from going off Screen
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736
    for i in range(enemy_number):
        # Checks If Game Over
        if enemy_y[i] > 440:
            game_running = False
            over_running = True
            lose = mixer.Sound("lose.wav")
            lose.play()
            break
        # Enemy Movement + Prevents Enemy going off Screen
        enemy_x[i] += enemy_dx[i]
        if enemy_x[i] <= 0:
            enemy_dx[i] = abs(enemy_dx[i])
            enemy_y[i] += enemy_dy[i]
        if enemy_x[i] >= 736:
            enemy_dx[i] = -enemy_dx[i]
            enemy_y[i] += enemy_dy[i]
        # Checks if Bullet hits
        if collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_in_motion = False
            score_value += 1
            # Controls LevelUp and Increases Difficulty
            if score_value % 10 == 0:
                level_value += 1
                enemy_number_ll += 1
                enemy_number_ul += 1
                enemy_dx_ll += 1
                enemy_dx_ul += 1
                enemy_dy_ll += 1
                enemy_dy_ul += 1
                # Stabilise Difficulty at a Certain Point
                if enemy_number_ll >= 10 and enemy_number_ul >= 12:
                    enemy_number_ll = 10
                    enemy_number_ul = 12
                if enemy_dx_ll >= 6 and enemy_dx_ul >= 8:
                    enemy_dx_ll = 6
                    enemy_dx_ul = 8
                if enemy_dy_ll >= 40 and enemy_dy_ul >= 50:
                    enemy_dy_ll = 40
                    enemy_dy_ul = 50
                enemy_creation()
                break
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)
    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_in_motion = False
    if bullet_in_motion:
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    # Display Player and Score
    player(player_x, player_y)
    show_progress()
    # Update Display
    pygame.display.update()


mixer.music.stop()
mixer.music.load("menu.mp3")
mixer.music.play(-1)
# High Score Management
scores_file = open("scores.txt", "r")
high_score = max(scores_file.readlines())
scores_file = open("scores.txt", "a")
scores_file.write("\n" + str(score_value))
scores_file.close()
# Game Over Screen
while over_running:
    # Display Background
    screen.fill((0, 0, 0))
    screen.blit(background_extra, (0, 0))
    # Display Game Over
    show_over()
    # Display HighScore
    high_score_text1 = normal_font.render("Your Score: " + str(score_value) + "  High Score: " + high_score, True, (150, 150, 150))
    screen.blit(high_score_text1, (180, 350))
    if score_value >= int(high_score):
        high_score_text2 = normal_font.render("Congratulations, You got the High Score!", True, (150, 150, 150))
        screen.blit(high_score_text2, (100, 425))
    # Game Closer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                over_running = False
    # Update Display
    pygame.display.update()
