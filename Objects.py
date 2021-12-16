import pygame
pygame.init()

class Object:
    def __init__(self, spritepath, hitbox=('n', 'n'), coords=('n', 'n')):
        self.sprite = pygame.image.load(spritepath)
        if 'n' in hitbox + coords:
            self.hitbox = self.sprite.get_rect()
        else:
            self.hitbox = pygame.rect.Rect(coords, hitbox)
        self.layer = 0


# Объекты геймплея. Будут обрабатываться непосредственно во время игры
class Player(Object):
    pass


class SolidObj(Object):
    pass


class Mob(Object):
    pass


class Item(Object):
    pass


 # В долгий ящик. От него будем наследовать хп-бары, диалоговые окна, инвентарь и т.п.
class UI(Object):
    pass
