import pygame
from Objects import *


class Camera:
    def __init__(self, object):
        self.follow = object
        self.offset_x = resolution[0] / 2
        self.offset_y = resolution[1] / 2

    def update(self, screen, objs):
        old_pos = [self.follow.rect.centerx, self.follow.rect.centery]
        if old_pos != [self.offset_x, self.offset_y]:
            self.follow.rect = pygame.rect.Rect(self.offset_x - self.follow.rect.width / 2, self.offset_y + 1 - self.follow.rect.height / 2, self.follow.rect.width, self.follow.rect.height)
            move_x = (old_pos[0] - self.offset_x) * -1
            move_y = (old_pos[1] - self.offset_y) * -1
            for i in objs.sprites():
                if not i is self.follow:
                    i.rect = i.rect.move(move_x, move_y)