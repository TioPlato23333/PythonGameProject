#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by Tio Plato
#
# Copyright (c) 2021 Tio Plato. All rights reserved.
#
# Sprite is a changable unit in game display. It shows the content of
# its resource.

import pygame

class Sprite:
    def __init__(self, name, x, y, width, height, visibility = False):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.resource = pygame.Surface([width, height])
        self.visibility = visibility

