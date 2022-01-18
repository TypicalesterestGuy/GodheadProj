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
        """Аргументы: path - путь к изображению спрайта, coords - коордтнаты на поле"""
        super().__init__(*args)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        self.coords = coords
        self.rect.x, self.rect.y = coords
        self.reform(*resolution)

    def reform(self, w, h):
        """Изменение размеров спрайта относительно размеров окна
        w, h - размеры окна"""
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
    """Класс Игрока"""
    def __init__(self, path, coords, speed=500, *args):
        """path - путь к спрайту, coords - расположение, speed - скорость перемещения в пикселях в секунду, по умолчанию 500"""
        self.speed = speed
        super().__init__(path, coords, *args)
        self.hp = 100
        self.fly = False
        self.defense = 10
        self.damage_immune = False
        self.i_frames = 0
        self.damage = 0
        self.knockbacking = 0
        self.fall_speed = 5

    def reform(self, w, h):
        """w, h - размеры окна, изменяет спрайт"""
        super().reform(w, h)
        self.speed /= FPS

    def update(self, events, m_pos, keys, objs, screen,
               *args):
        """Обновление покадрово, events - список событий pygame, keys - нажатые клавиши, objs - объекты на экране, screen - полотно игрока"""
        super().update(*args)
        if keys[pygame.K_LEFT]:
            self.rect = self.rect.move(-self.speed,
                                       0)
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

        for i in objs.sprites():
            if self.rect.colliderect(i.rect):
                self.rect.move_ip(0, (
                            self.rect.y - i.rect.y + i.rect.height - 3) * -1)  # Пассивная обработка, которая заставит игрока непрерывно стоять сверху блока. Когда мы доделаем падение, будет весьма полезно
                i.player_collide["top"] = True
        if self.i_frames:
            self.i_frames -= 1
            print(f"Фреймы: {self.i_frames}")
            pygame.draw.rect(screen, (255, 255, 255), self.rect, self.i_frames)
        else:
            self.damage_immune = False
        if self.knockbacking:
            self.knockbacking -= 1
            self.rect.move(self.knockbacking, 0)
        if not self.fly:
            if not self.rect.collidelist([i.rect for i in objs.sprites()]):
                self.rect.move_ip(0, self.fall_speed * -1)
                print("ok")
                self.fall_speed **= 2
            else:
                self.fall_speed = 5

    def on_get_hit(self, damage, knockback, crit, enemy):
        """Вызывается при получении игроком урона. damage - урон, knockback - отбрасывание, crit - был ли нанесён крит, enemy - источник урона"""
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
        """Твёрдый объект. path - путь к текстуре, coords - координаты на поле"""
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

    def on_collide(self):
        """Вызывается при столкновении чего либо с блоком"""
        pass


class Mob(Object):
    def __init__(self, path, coords, *args):
        """Нестатичный объект. path - путь к текстуре, coords - координаты на поле"""
        super().__init__(path, coords, *args)
        self.ai_list = [0, 0, 0]
        self.velocity = [0, 0]
        self.on_tile_collide = False
        self.penetration = 0
        self.live_time = -1

    def update(self, *args):
        super().update(*args)
        if any(self.velocity):
            self.rect = self.rect.move(*self.velocity)
        self.ai()

    def ai(self, *args):
        """Внутренний ИИ. Вызывается при каждом обновлении"""
        pass


class NPC(Mob):
    def __init__(self, path, coords, screen, *args):
        """Класс НПС. path - путь к текстуре, coords - координаты на поле"""
        super().__init__(path, coords, *args)
        self.screen = screen
        self.friendly = False
        self.hp = 0
        self.knockback = 0
        self.contact_damage = False
        self.damage = 0
        self.damage_resistance = 0
        self.boss = False

    def update(self, tiles, objs, player, *args):
        """Обновление, вызывается каждый такт. tiles - группа SolidObj-спрайтов, objs - общие объекты, player - игрок"""
        super().update(*args)
        for object in objs.sprites():
            if self.rect.colliderect(object.rect) and object.__class__.__name__ != "Player":
                self.on_get_hit(object.damage, object.knockback, object.crit, self)
        if not player.damage_immune and player.rect.colliderect(self.rect):
            player.on_get_hit(self.damage, self.knockback, bool(r.randrange(0, 1 + 1)), self)
        if self.hp <= 0:
            self.on_death()

    def on_get_hit(self, damage, knockback, crit):
        """Вызывается при получении урона мобом. damage - полученный урон, knockback - отбрасывание"""
        if crit:
            damage *= r.randrange(2, 3 + 1)
        if damage >= self.damage_resistance:
            damage -= self.damage_resistance
        else:
            damage = 0
        self.hp -= damage

    def on_death(self):
        """Вызывается при смерти"""
        self.kill()

    def on_hit(self, target):
        """Вызывается при нанесении удара. target - тот, кому удар был нанесён"""
        target.on_get_hit(self.damage, self.knockback, r.randrange(0, 1 + 1))


class testEnemy(NPC):
    """Простой враг"""

    def __init__(self, coords, screen, *args):
        """Текстуру указывать при создании класса не нужно"""
        super().__init__("textures/slizen.png", coords, screen, *args)
        self.velocity = [0, 0]
        self.hp = 1000
        self.knockback = 10
        self.contact_damage = True
        self.player_pos = (0, 0)
        self.flag = False
        self.radius = 0

    def update(self, tiles, objs, player, *args):
        """при обновлении"""
        super().update(tiles, objs, player, *args)
        self.player_pos = player.rect.centerx, player.rect.centery

    def ai(self):
        self.ai_list[0] += 1
        if self.ai_list[0] >= 600:
            self.on_death()
            self.contact_damage = False

    def on_death(self):
        self.ai_list[1] += 1
        if self.ai_list[1] < 60:
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect, self.ai_list[1])
        else:
            super().on_death()


class Item(Object):
    pass


# В долгий ящик. От него будем наследовать хп-бары, диалоговые окна, инвентарь и т.п.
class UI(Object):
    pass
