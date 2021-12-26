import pygame
from Objects import *

pygame.init()
settings = {}
sprites_group = pygame.sprite.Group()

with open("settings.txt", "r", encoding="utf-8") as f:
    for i in f.read().split("\n"):
        a, b = i.split(":")
        settings[a] = b.split()

# Здесь будет происходить выгрузка параметров из файла settings.txt
size = list(map(int, settings["size"]))

screen = pygame.display.set_mode(size)
run = True

obj = Object('textures/morgenshtern.jpg', (100, 100))
obj2 = Object('textures/morgenshtern.jpg', (100 + obj.rect.width, 100))
obj.reform(size[0], size[1])
obj2.reform(size[0], size[1])
player = Player('textures/morgenshtern.jpg', (300, 300))
sprites_group.add(obj)
sprites_group.add(obj2)
sprites_group.add(player)

while run:
    screen.fill((0, 0, 0))
    events = [event for event in pygame.event.get()]
    m_pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            break
    sprites_group.draw(screen)
    sprites_group.update(events, m_pos)
    pygame.display.flip()

pygame.quit()
