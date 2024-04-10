#!/usr/bin/python
#-*- coding: utf-8 -*-
import pygame
from pygame import Surface

from code.EntifyFactory import EntityFactory
from code.Entity import Entity


class Level:
    def __init__(self, window, name, menu_option):
        self.window :Surface = window
        self.name = name
        self.mode = menu_option # opção do menu, onde o jogador escolheu o modo de jogo (1/2 jogadores)
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))

    def run(self, ):
        while True:
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
            pygame.display.flip()
        pass

