#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by Tio Plato
#
# Copyright (c) 2021 Tio Plato. All rights reserved.
#
# Canvas is the game window where we draw sprites and other components.

import pygame

class Canvas:
    def __init__(self, name, width, height, sprites):
        self.name = name
        self.width = width
        self.height = height
        self.sprites = sprites
        self.display = pygame.display.set_mode([width, height])

    def UpdateCanvas(self):
        for sprite in self.sprites:
            if sprite.visibility:
                self.display.blit(sprite.resource, [sprite.x, sprite.y])
