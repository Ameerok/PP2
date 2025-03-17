import pygame
import datetime
import math

pygame.init()

width = 400
height = 300 
screen = pygame.display.set_mode((width, height))

running = True

background = pygame.image.load("lab7\\bg_clock.jpg")
background = pygame.transform.scale(background, (width, height))

min_hand = pygame.image.load("lab7\\right_hand.png")
min_hand = pygame.transform.scale(min_hand, (150,150))

sec_hand = pygame.image.load("lab7\\left_hand.png")
sec_hand = pygame.transform.scale(sec_hand, (200,200))

center_x = width // 2
center_y = height // 2

def clock_rotation(surface, image, pos, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = pos)
        surface.blit(rotated_image, new_rect.topleft)

clock = pygame.time.Clock()

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
        now = datetime.datetime.now()
        minute = now.minute
        second = now.second

        minute_angle = -6 * minute - 0.1 * second
        second_angle = -6 * second

        screen.blit(background, (0,0))
        
        clock_rotation(screen, min_hand, (center_x, center_y), minute_angle)
        clock_rotation(screen, sec_hand, (center_x, center_y), second_angle)
        
        pygame.display.flip()

        clock.tick(60)

pygame.quit()
        