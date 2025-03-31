import pygame
from pygame import mixer

mixer.init()
pygame.init()

screen = pygame.display.set_mode((500,300))


volume = 0.5
pygame.mixer.music.set_volume(volume)

queue = ['music.mp3', 'sample_1.mp3', 'sample_2.mp3']
now_song = 0

def load_song(now_song):
    pygame.mixer.music.load(queue[now_song])
    pygame.mixer.music.play()

def next_song():
    global now_song
    now_song = (now_song + 1) % len(queue)
    load_song(now_song)

def prev_song():
    global now_song
    now_song = (now_song - 1) % len(queue)
    load_song(now_song)

def volume_up():
    global volume
    if(volume <= 0.9):
        volume += 0.1
    pygame.mixer.music.set_volume(volume)

def volume_down():
    global volume
    if(volume >= 0.1):
        volume -= 0.1
    pygame.mixer.music.set_volume(volume)

def go_forward():
    pygame.mixer.music.set_pos(pygame.mixer.music.get_pos() + 5)

def go_back():
    pygame.mixer.music.set_pos(pygame.mixer.music.get_pos() - 5)

def toggle_play():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

running = True
load_song(now_song)
print('Left arrow - seek back\nRight arrow - seek forward\nSpace - Pause, Unpause\n')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_play()
            if event.key == pygame.K_RIGHT:
                go_forward()
            if event.key == pygame.K_LEFT:
                go_back()
            if event.key == pygame.K_UP:
                volume_up()
            if event.key == pygame.K_DOWN:
                volume_down()
    
    screen.fill('white')
    pygame.display.flip()
pygame.quit()