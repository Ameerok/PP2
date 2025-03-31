import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Red Ball')

player_size = 50
player_x = 30
player_y = 30
player_speed = 5

coin_size = 25
coin_x = random.randint(0, WIDTH-coin_size)
coin_y = random.randint(0, HEIGHT-coin_size)
coins_collected = 0

font = pygame.font.Font(None, 36)

running = True

while running:
    screen.fill('white')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed
    
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)
    if player_rect.colliderect(coin_rect):
        coins_collected += 1
        if coins_collected >= 5:
            running = False
        else:
            coin_x = random.randint(0, WIDTH - coin_size)
            coin_y = random.randint(0, HEIGHT - coin_size)

    pygame.draw.ellipse(screen, 'red', (player_x, player_y, player_size, player_size))
    pygame.draw.ellipse(screen, 'yellow', (coin_x, coin_y, coin_size, coin_size))

    score_text = font.render(f"Score = {coins_collected}/5", True, 'black')
    screen.blit(score_text, (WIDTH-200, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

screen.fill('white')
win_message = font.render("Congrats! You Won!", True, 'black')
screen.blit(win_message, (WIDTH/2-150, HEIGHT/2))
pygame.display.flip()
pygame.time.delay(2000)

pygame.quit()