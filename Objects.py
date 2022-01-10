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
    def __init__(self, path, coords, speed=500, *args):
        super().__init__(path, coords, *args)
        self.speed = speed

    def reform(self, w, h, FPS):
        super().reform(w, h)
        self.speed /= FPS

    def update(self, events, m_pos, keys, objs,
               *args):  # Теперь игрок просит список твердых объектов, дабы проверить, где он собсна среди них. Предлагаю сюда посылать только объекты сугубо на экране
        super().update(*args)
        if keys[pygame.K_LEFT]:
            self.rect = self.rect.move(-self.speed,
                                       0)  # Движение поменял на move. Теперь скорость одинакова во все стороны.
            for i in objs.sprites():
                if self.rect.colliderect(i.rect):
                    self.rect.x = i.rect.x + i.rect.width
                    i.player_collide["right"] = True
        if keys[pygame.K_RIGHT]:
            self.rect = self.rect.move(self.speed, 0)
            for i in objs.sprites():
                if self.rect.colliderect(i.rect):
                    self.rect.x = i.rect.x - self.rect.width
                    i.player_collide["left"] = True
        if keys[pygame.K_UP]:
            self.rect = self.rect.move(0, -self.speed)
            for i in objs.sprites():
                if self.rect.colliderect(i.rect):
                    self.rect.y = i.rect.y + i.rect.height
                    i.player_collide["down"] = True
        if keys[pygame.K_DOWN]:
            self.rect = self.rect.move(0, self.speed)
            for i in objs.sprites():
                if self.rect.colliderect(i.rect):
                    self.rect.y = i.rect.y - self.rect.height
                    i.player_collide["top"] = True

        for i in objs.sprites():
            if self.rect.colliderect(i.rect):
                self.rect.y = i.rect.y - self.rect.height - 1  # Пассивная обработка, которая заставит игрока непрерывно стоять сверху блока. Когда мы доделаем падение, будет весьма полезно
                i.player_collide["top"] = True


class SolidObj(Object):
    def __init__(self, path, coords, *args):
        super().__init__(path, coords, *args)
        self.player_collide = {"right": False,
                               "left": False,
                               "top": False,
                               "down": False}  # Здесь информация, с какой стороны игрок толкнул объект. Примеры использования снизу

    def reform(self, w, h):
        super().reform(w, h)

    def update(self, *args):
        super().update(*args)
        if self.player_collide["top"]:
            print("На мне стоят")
        if self.player_collide["left"]:
            print("Меня толкнули слева")
        if self.player_collide["right"]:
            print("Меня толкнули справа")
        if self.player_collide["down"]:
            print("Меня толкнули снизу")

        self.player_collide = {"right": False,
                               "left": False,
                               "top": False,
                               "down": False}

    def on_collide(self):  # Этот метод следует заменить на on_player_collide
        pass


class Mob(Object):
    pass


class Item(Object):
    pass


# В долгий ящик. От него будем наследовать хп-бары, диалоговые окна, инвентарь и т.п.
class UI(Object):
    pass
