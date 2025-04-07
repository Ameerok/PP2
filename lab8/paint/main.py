import pygame, sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    drawing = False
    current_shape = 'line'
    radius = 15
    color = 'blue'
    start_pos = None
    end_pos = None

    shapes_to_draw = []  # список всех нарисованных фигур

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # выбор цвета
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    color = 'red'
                elif event.key == pygame.K_g:
                    color = 'green'
                elif event.key == pygame.K_b:
                    color = 'blue'
                elif event.key == pygame.K_1:
                    current_shape = 'line'
                elif event.key == pygame.K_2:
                    current_shape = 'rectangle'
                elif event.key == pygame.K_3:
                    current_shape = 'right_triangle'
                elif event.key == pygame.K_4:
                    current_shape = 'equil_triangle'
                elif event.key == pygame.K_5:
                    current_shape = 'rhombus'
                elif event.key == pygame.K_6:
                    current_shape = 'circle'
                elif event.key == pygame.K_0:
                    current_shape = 'eraser'
                elif event.key == pygame.K_o:
                    radius -= 2
                elif event.key == pygame.K_p:
                    radius += 2

            #Начало рисования
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    drawing = True
                    start_pos = event.pos

            #Нарисовка
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    end_pos = event.pos
                    shapes_to_draw.append((current_shape, start_pos, end_pos, radius, color))
                    drawing = False

        #Отображение всех нарисованных фигур
        for shape in shapes_to_draw:
            draw_shape(screen, *shape)

        #Предпросмотр
        if drawing:
            end_pos = pygame.mouse.get_pos()
            draw_shape(screen, current_shape, start_pos, end_pos, radius, color, preview=True)

        pygame.display.flip()
        clock.tick(60)

def get_color(color_mode):
    if color_mode == 'blue':
        return (0, 0, 255)
    elif color_mode == 'red':
        return (255, 0, 0)
    elif color_mode == 'green':
        return (0, 255, 0)
    return (255, 255, 255)

def draw_shape(screen, shape, start, end, width, color_mode, preview=False):
    color = get_color(color_mode)
    if preview:
        temp_surface = screen.copy()
        draw_shape(temp_surface, shape, start, end, width, color_mode)
        screen.blit(temp_surface, (0, 0))
        return

    x1, y1 = start
    x2, y2 = end

    if shape == 'line':
        pygame.draw.line(screen, color, start, end, width)
    elif shape == 'rectangle':
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, color, rect, width)
    elif shape == 'circle':
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        radius = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5 // 2)
        pygame.draw.circle(screen, color, center, radius, width)
    elif shape == 'right_triangle':
        points = [start, (x1, y2), end]
        pygame.draw.polygon(screen, color, points, width)
    elif shape == 'equil_triangle':
        points = [((x1 + x2) // 2, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(screen, color, points, width)
    elif shape == 'rhombus':
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
        pygame.draw.polygon(screen, color, points, width)
    elif shape == 'eraser':
        pygame.draw.line(screen, (0, 0, 0), start, end, width)

main()
