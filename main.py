import pygame

pygame.init()
settings = {}

with open("settings.txt", "r", encoding="utf-8") as f:
    for i in f.read().split("\n"):
        a, b = i.split(":")
        settings[a] = b

# Здесь будет происходить выгрузка параметров из файла settings.txt
size = list(map(int, settings["size"]))

screen = pygame.display
screen.set_mode(size)
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    pygame.display.flip()

pygame.quit()
