import pygame
import sys
import random
import time

pygame.init()

#Константы
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 10
SPEED = 5
SCORE = 0
LEVEL = 1
MAX_FOOD = 5

#Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

font = pygame.font.SysFont(None, 35)


def draw_snake(snake):
    for cell in snake:
        pygame.draw.rect(screen, 'dark green', pygame.Rect(cell[0], cell[1], CELL_SIZE, CELL_SIZE))

def draw_food(food_list):
    for food in food_list:
        pygame.draw.rect(screen, 'red', pygame.Rect(food['position'][0], food['position'][1], food['size'], food['size']))

def spawn_food(snake_body): #Ищем свободную от змейки клетку
    all_cells = [
        (x * CELL_SIZE, y * CELL_SIZE)
        for x in range(WIDTH // CELL_SIZE)
        for y in range(HEIGHT // CELL_SIZE)
    ]
    free_cells = list(set(all_cells) - set(snake_body))
    return random.choice(free_cells) #Выбираем случайную свободную клетку

def show_score(score, level):
    score_text = font.render(f"Score: {score} Level: {level}", True, 'black')
    screen.blit(score_text, (10, 10))


#Настройки
snake = [(100, 100), (80, 100), (60, 100)]
food_list = []
direction = (CELL_SIZE, 0)
food = spawn_food(snake)
food_timer = time.time()


#Разрешаем ходить
next_direction = direction

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Мувмент
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                next_direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                next_direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                next_direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                next_direction = (CELL_SIZE, 0)

    if((len(food_list) < MAX_FOOD) and (time.time() - food_timer >= random.randint(2,6))):
        food_position = spawn_food(snake)
        food_points = random.randint(1,3)
        food_size = food_points * 5
        food_lifetime = time.time() + random.randint(5, 10)
        food_list.append({
            'position': food_position,
            'size': food_size,
            'points': food_points,
            'lifetime': food_lifetime
        })
        food_timer = time.time()
    
    food_list = [food for food in food_list if food['lifetime'] > time.time()]
    
    #Движение змейки
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)
    food_eaten = False
    #Сбор очков
    for food in food_list[:]:
        if head == food['position']:
            SCORE += food['points']
            food_list.remove(food)
            food_eaten = True
    if not food_eaten:
        snake.pop()
    if SCORE >= 5 * LEVEL:
        LEVEL += 1
        SPEED = int(SPEED + LEVEL * 1.5)  #Увеличиваем скорость при новом уровне


     #Столкновения с препятствиями
    if ((head[0] < 0) or (head[0] >= WIDTH) or (head[1] < 0) or (head[1] >= HEIGHT) or (head in snake[1:])):
        screen.fill('red')
        game_over = font.render('GAME OVER!', True, 'black')
        screen.blit(game_over, (WIDTH//2-100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(2000)
        snake = [(100, 100), (80, 100), (60, 100)] 
        direction = (CELL_SIZE, 0) 
        next_direction = direction
        food_list = []
        LEVEL = 1
        SCORE = 0
        SPEED = 5
    
    screen.fill('white')
    draw_snake(snake)
    draw_food(food_list)    
    show_score(SCORE, LEVEL)

    direction = next_direction #Я гений

    pygame.display.update()
    pygame.time.Clock().tick(SPEED)  #Скорость