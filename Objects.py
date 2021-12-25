import pygame

pygame.init()

# Ветка Егора
class Object(pygame.sprite.Sprite):  # Создание базового объекта
    def __init__(self, path, coords, *args):
        super().__init__(*args)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords

    def reform(self, w, h):  # Изменение размеров отгносительно размеров окна
        self.rect.x *= w / 1920
        self.rect.y *= h / 1080
        self.rect.width *= w / 1920
        self.rect.height *= h / 1080

    def update(self, *args):
        super().update(*args)


# Объекты геймплея. Будут обрабатываться непосредственно во время игры


class Player(Object):
    def __init__(self, path, coords, speed=10, *args):
        super().__init__(path, coords, *args)
        self.speed = speed

    def update(self, events, m_pos, *args):
        super().update(*args)
        if pygame.KEYDOWN in events:
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
