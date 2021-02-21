__author__ = 'DWA'

import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x=x
        self.y=y