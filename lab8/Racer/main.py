import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0 #Обнуляем счетчик монет
LIVES = 3

font = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 20)
game_over = font.render("Game Over", True, 'black')

background = pygame.image.load("AnimatedStreet.png")

screen = pygame.display.set_mode((400,600))
screen.fill('white')
pygame.display.set_caption("Racer")

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-SPEED, 0)
        if self.rect.right < WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(SPEED, 0)
        if self.rect.bottom < HEIGHT: #Движение вниз
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 0: #Движение вверх
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -SPEED)

class Coin(pygame.sprite.Sprite): #Класс для монетки
    def __init__(self): #Задаём характеристики монетке: цвет, тип, создаем рект монетки
        super().__init__()
        self.image = pygame.Surface((20,20))
        pygame.draw.circle(self.image, 'yellow', (10,10), 10)
        self.rect = self.image.get_rect()
        self.spawn(P1)
    def spawn(self, player):
        while True:
            self.rect.center = (random.randint(20, WIDTH - self.rect.width), random.randint(20, HEIGHT - self.rect.height)) #Спавним монетку в случайном месте экрана
            if not self.rect.colliderect(player.rect): #Проверяем чтобы монетка не появилась на месте игрока (мгновенный сбор монет)
                break
    def move(self):
        pass #В основном цикле этот класс должен исполнять метод move(), поэтому напишем пустой метод

P1 = Player()
E1 = Enemy()
coin = Coin() #Создаём объект монетки

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:      
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    screen.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, 'black')
    screen.blit(scores, (10,10))
    coins = font_small.render(f"Coins = {COINS}", True, 'black') #Текст счётчика монеток
    screen.blit(coins, (10, WIDTH - 100)) #Выводим текст на экран
    lives = font_small.render(f"Lives = {LIVES}", True, 'red')
    screen.blit(lives, (WIDTH//2, HEIGHT - 20))
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)
        
    if pygame.sprite.spritecollideany(P1, enemies):
        if LIVES == 1: #Если осталась 1 жизнь то заканчиваем игру при столкновении
            pygame.mixer.Sound('crash.wav').play()
            time.sleep(1)
            
            screen.fill('red')
            screen.blit(game_over, (30,250))
            
            pygame.display.update()
            for entity in all_sprites:
                    entity.kill() 
            time.sleep(2)
            pygame.quit()
            sys.exit()
        else: #Если жизней больше одной, то начинаем сначала
            E1.rect.center = (random.randint(40, WIDTH - 40), 0)
            P1.rect.center = (160, 520)
            LIVES -= 1
            SPEED = 5

    if P1.rect.colliderect(coin.rect): #Проверяем если игрок собрал монетку
        COINS += 1 #Увеличиваем счётчик на 1 монету
        coin.spawn(P1) #Спавним новую монету

    pygame.display.update()
    pygame.time.Clock().tick(60)
