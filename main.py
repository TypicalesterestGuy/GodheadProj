import pygame
from Objects import *

pygame.init()
settings = {}
sprites_group = pygame.sprite.Group()
solids_objs = pygame.sprite.Group()
mob_group = pygame.sprite.Group()

with open("settings.txt", "r", encoding="utf-8") as f:
    for i in f.read().split("\n"):
        a, b = i.split(":")
        settings[a] = b.split()

# Здесь будет происходить выгрузка параметров из файла settings.txt
size = list(map(int, settings["size"]))
FPS = int(*settings["FPS"])

screen = pygame.display.set_mode(size)
run = True

obj = SolidObj('textures/morgenshtern.jpg', (100, 400))
obj.reform(size[0], size[1])
player = Player('textures/morgenshtern.jpg', (300, 300))
player.reform(size[0], size[1], FPS)
solids_objs.add(obj)
sprites_group.add(player)

mob = Mob('textures/morgenshtern.jpg', (600, 400))
mob.velocity = [-10, -10]
mob_group.add(mob)

clock = pygame.time.Clock()
while run:
    screen.fill((0, 0, 0))
    events = [event for event in pygame.event.get()]
    m_pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            break

    mob_group.draw(screen)
    mob_group.update()

    sprites_group.draw(screen)

    solids_objs.draw(screen)
    solids_objs.update()
    sprites_group.update(events, m_pos, pygame.key.get_pressed(), solids_objs)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
