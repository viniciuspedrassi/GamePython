#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import C_YELLOW, MENU_OPTION, EVENT_ENEMY, C_DARKGREY, C_CYAN, \
    EVENT_TIMEOUT
from code.Enemy import Enemy
from code.EntifyFactory import EntityFactory
from code.Entity import Entity
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, menu_option: str, player_score: list[int]):
        self.window: Surface = window
        self.name = name
        self.mode = menu_option  # opção do menu, onde o jogador escolheu o modo de jogo (1/2 jogadores)
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]  # score do player 1
        self.entity_list.append(player)
        if menu_option in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]  # score do player 2
            self.entity_list.append(player)
        pygame.time.set_timer(EVENT_ENEMY, 2000)
        self.timeout = 12000  # 25 SEGUNDOS
        pygame.time.set_timer(EVENT_TIMEOUT, 100)  # 100ms verificar a condição de vitória ou derrota da fase

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(120)
            # for para desenhar todas as entidades
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)  # aqui eu desenho as entidades
                ent.move()
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

                if ent.name == 'Player1':
                    self.level_text(18, f'HP-P1: {ent.health} |', C_DARKGREY, (10, 10))
                    self.level_text(18, f'SCORE: {ent.score}', C_YELLOW, (90, 10))

                if ent.name == 'Player2':
                    self.level_text(18, f'HP-P2: {ent.health} |', C_CYAN, (10, 25))
                    self.level_text(18, f'SCORE: {ent.score}', C_YELLOW, (90, 25))

            #  texto a ser printado na tela
            self.level_text(16, f'{self.name} | {self.timeout / 1000 :.0f} s', C_DARKGREY, (510, 10))
            self.level_text(16, f'{clock.get_fps():.0f} fps', C_YELLOW, (535, 25))

            # atualizar tela
            pygame.display.flip()
            # verificar relacionamentos de entidades
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)
            # conferir eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                # condicao de vitoria
                if event.type == EVENT_TIMEOUT:  # acontece a cada 100ms
                    self.timeout -= 100  # timeout começa com 25000
                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score
                        return True
                # condição de derrota
                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        found_player = True
                if not found_player:
                    return False

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
