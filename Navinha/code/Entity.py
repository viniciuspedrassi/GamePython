#!/usr/bin/python
#-*- coding: utf-8 -*-
from abc import ABC

import pygame.image


def abtrasctmethod(args):
    pass


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = pygame.image.load('./asset/' + name + '.png').convert_alpha()
        self.rect = self.surf.get_rect(left= position[0], top=position[1])
        self.speed = 0


    @abtrasctmethod
    def move(self, ):
        pass

