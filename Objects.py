import pygame

pygame.init()


# Моя ветка
class Object(pygame.sprite.Sprite):  # Создание базового объекта
    def __init__(self, path, coords, *args):
        super().__init__(*args)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.coords = coords
        self.rect.x, self.rect.y = coords

    def reform(self, w, h):  # Изменение размеров отгносительно размеров окна
        # (Элес) Я изменил механизм.
        # Мы меняли лишь положение картинки и хитбокс, но непосредственно размер изображения не менялся
        self.image = pygame.transform.scale(self.image,
                                            pygame.rect.Rect(self.rect.x, self.rect.y, self.rect.width * (w / 1920),
                                                             self.rect.height * (h / 1080)).size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords
        self.rect.x *= w / 1920
        self.rect.y *= h / 1080

    def update(self, *args):
        super().update(*args)


# Объекты геймплея. Будут обрабатываться непосредственно во время игры


class Player(Object):
    def __init__(self, path, coords, speed=10, *args):
        super().__init__(path, coords, *args)
        self.speed = speed

    def update(self, events, m_pos, *args):
        super().update(*args)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.rect.x -= 20
                if event.key == pygame.K_RIGHT:
                    self.rect.x += 20
                if event.key == pygame.K_UP:
                    self.rect.y -= 20
                if event.key == pygame.K_DOWN:
                    self.rect.y += 20


class SolidObj(Object):
    pass


class Mob(Object):
    pass


class Item(Object):
    pass


# В долгий ящик. От него будем наследовать хп-бары, диалоговые окна, инвентарь и т.п.
class UI(Object):
    pass
