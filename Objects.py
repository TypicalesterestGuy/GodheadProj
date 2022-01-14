import random as r

import pygame

pygame.init()

with open("settings.txt") as f:
    for i in f.read().split("\n"):
        if "size" in i:
            resolution = list(map(int, i[5:].split(" ")))
        if "FPS" in i:
            FPS = int(i[4:])


# Моя ветка
class Object(pygame.sprite.Sprite):  # Создание базового объекта
    def __init__(self, path, coords, *args):
        super().__init__(*args)

        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        self.coords = coords
        self.rect.x, self.rect.y = coords
        self.reform(*resolution)

    def reform(self, w, h):  # Изменение размеров отгносительно размеров окна
        # (Элес) Я изменил механизм.
        # Мы меняли лишь положение картинки и хитбокс, но непосредственно размер изображения не менялся
        self.image = pygame.transform.scale(self.image,
                                            pygame.rect.Rect(self.rect.x, self.rect.y, self.rect.width * (
                                                    w / 1920),
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
        self.speed = speed
        super().__init__(path, coords, *args)
        self.hp = 100
        self.defense = 10
        self.damage_immune = False
        self.i_frames = 0
        self.damage = 0
        self.knockbacking = 0

    def reform(self, w, h):
        super().reform(w, h)
        self.speed /= FPS

    def update(self, events, m_pos, keys, objs, screen,
               *args):  # Теперь игрок просит список твердых объектов, дабы проверить, где он собсна среди них. Предлагаю сюда посылать только объекты сугубо на экране
        super().update(*args)
        if keys[pygame.K_LEFT]:
            self.rect = self.rect.move(-self.speed,
                                       0)  # Движение поменял на move. Теперь скорость одинакова во все стороны.
            for i in objs.sprites():
                if self.rect.colliderect(i.rect):
                    self.rect.move_ip((self.rect.x - i.rect.x - self.rect.width) * -1, 0)
                    i.player_collide["right"] = True
        if keys[pygame.K_RIGHT]:
            self.rect = self.rect.move(self.speed, 0)
            for i in objs.sprites():
                if self.rect.colliderect(i.rect):
                    self.rect.move_ip((self.rect.x - i.rect.x + i.rect.width) * -1, 0)
                    i.player_collide["left"] = True
        if keys[pygame.K_UP]:
            self.rect = self.rect.move(0, -self.speed)
            for i in objs.sprites():
                if self.rect.colliderect(i.rect):
                    self.rect.move_ip(0, (self.rect.y - i.rect.y - self.rect.height) * -1)
                    i.player_collide["down"] = True
        if keys[pygame.K_DOWN]:
            self.rect = self.rect.move(0, self.speed)
            for i in objs.sprites():
                if self.rect.colliderect(i.rect):
                    self.rect.move_ip(0, (self.rect.y - i.rect.y + i.rect.height) * -1)
                    i.player_collide["top"] = True

        """for i in objs.sprites():
            if self.rect.colliderect(i.rect):
                self.rect.y = i.rect.y - self.rect.height - 1  # Пассивная обработка, которая заставит игрока непрерывно стоять сверху блока. Когда мы доделаем падение, будет весьма полезно
                i.player_collide["top"] = True"""
        if self.i_frames:
            self.i_frames -= 1
            print(f"Фреймы: {self.i_frames}")
            pygame.draw.rect(screen, (255, 255, 255), self.rect, self.i_frames)
        else:
            self.damage_immune = False
        if self.knockbacking:
            self.knockbacking -= 1
            self.rect.x -= 1

    def on_get_hit(self, damage, knockback, crit, enemy):
        if crit:
            damage *= r.randrange(2, 3 + 1)
        if damage >= self.defense:
            damage -= self.defense
        if knockback:
            if enemy.rect.x < self.rect.x:
                self.rect.x += knockback
            else:
                self.rect.x -= knockback
        else:
            damage = 1
        self.hp -= damage
        self.damage_immune = True
        self.i_frames = 30


class SolidObj(Object):
    def __init__(self, path, coords, *args):
        super().__init__(path, coords, *args)
        self.player_collide = {"right": False,
                               "left": False,
                               "top": False,
                               "down": False}  # Здесь информация, с какой стороны игрок толкнул объект. Примеры использования снизу

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
    def __init__(self, path, coords, *args):
        super().__init__(path, coords, *args)
        self.ai_list = [0, 0, 0]
        self.velocity = [0, 0]
        self.on_tile_collide = False
        self.penetration = 0
        self.live_time = -1

    def update(self, *args):
        super().update(*args)
        self.rect = self.rect.move(*self.velocity)
        self.ai()

    def ai(self, *args):
        pass


class NPC(Mob):
    def __init__(self, path, coords, *args):
        super().__init__(path, coords, *args)
        self.friendly = False
        self.hp = 0
        self.knockback = 0
        self.contact_damage = False
        self.damage = 0
        self.damage_resistance = 0
        self.boss = False

    def update(self, tiles, objs, player, *args):
        super().update(*args)
        for object in objs.sprites():
            if self.rect.colliderect(object.rect) and object.__class__.__name__ != "Player":
                self.on_get_hit(object.damage, object.knockback, object.crit, self)
        if not player.damage_immune and player.rect.colliderect(self.rect):
            player.on_get_hit(self.damage, self.knockback, bool(r.randrange(0, 1 + 1)), self)
        if self.hp <= 0:
            self.on_death()

    def on_get_hit(self, damage, knockback, crit):
        if crit:
            damage *= r.randrange(2, 3 + 1)
        if damage >= self.damage_resistance:
            damage -= self.damage_resistance
        else:
            damage = 0
        self.hp -= damage

    def on_death(self):
        self.kill()

    def on_hit(self, target):
        target.on_get_hit(self.damage, self.knockback, r.randrange(0, 1 + 1))


class testEnemy(NPC):
    def __init__(self, coords, *args):
        super().__init__("textures/slizen.png", coords, *args)
        self.velocity = [0, 5]
        self.hp = 1000
        self.knockback = 90

    def ai(self):
        pass


class Item(Object):
    pass


# В долгий ящик. От него будем наследовать хп-бары, диалоговые окна, инвентарь и т.п.
class UI(Object):
    pass
