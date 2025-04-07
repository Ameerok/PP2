import pygame
import sys
import random

pygame.init()

#Константы
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 10
SPEED = 5
SCORE = 0
LEVEL = 1

#Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

font = pygame.font.SysFont(None, 35)


def draw_snake(snake):
    for cell in snake:
        pygame.draw.rect(screen, 'dark green', pygame.Rect(cell[0], cell[1], CELL_SIZE, CELL_SIZE))

def draw_food(position):
    pygame.draw.rect(screen, 'red', pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE))

#Рестарт кнопка
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, 'lightblue', (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, 'black')
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

    def check_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  #Клик
            if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
                if self.action:
                    self.action() 

#Ресет
def reset_game():
    global snake, direction, food, score, level, speed
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)
    food = spawn_food(snake)
    score = 0
    level = 1
    speed = 10

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
direction = (CELL_SIZE, 0)
food = spawn_food(snake)
restart_button = Button(WIDTH//2 - 75, HEIGHT//2 - 25, 150, 50, "Restart", reset_game)


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

    #Движение змейки
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)

    #Сбор очков
    if head == food:
        food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        SCORE += 1
    else:
        snake.pop()

    if SCORE >= 2 * (LEVEL+1):
        LEVEL += 1
        SPEED = int(SPEED + LEVEL * 1.5)  #Увеличиваем скорость при новом уровне


     #Столкновения с препятствиями
    if ((head[0] < 0) or (head[0] >= WIDTH) or (head[1] < 0) or (head[1] >= HEIGHT) or (head in snake[1:])):
        screen.fill('red')
        game_over = font.render('GAME OVER!', True, 'black')
        screen.blit(game_over, (WIDTH//2-100, HEIGHT//2))
        restart_button.draw()
        restart_button.check_click()
        
    
    screen.fill('white')
    draw_snake(snake)
    draw_food(food)    
    show_score(SCORE, LEVEL)

    direction = next_direction #Я гений

    pygame.display.update()
    pygame.time.Clock().tick(SPEED)  #Скорость