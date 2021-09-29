#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by Tio Plato
#
# Copyright (c) 2021 Tio Plato. All rights reserved.
#
# This is game main file. Usage: python main.py.

import pygame
import sys

import MofuEngine

class ChessSprite(MofuEngine.Sprite):
    def __init__(self, name, x, y, width, height, is_piece = True, visibility = False):
        # chess has 2 types of sprites: chess piece or winner mark
        self.is_piece = is_piece
        super().__init__(name, x, y, width, height, visibility)

class ChessBoard(MofuEngine.Canvas):
    def __init__(self, background, player1, player2, row_mark, col_mark, diag_mark1, diag_mark2):
        # resources
        self.background = background
        self.player1 = player1
        self.player2 = player2
        self.row_mark = row_mark
        self.col_mark = col_mark
        self.diag_mark1 = diag_mark1
        self.diag_mark2 = diag_mark2
        # it is a 3-order tic-tac-toe game
        self.order = 3
        # two players game, 0 means player1 and 1 means player2
        self.turn = 0
        # board status, -1 means empty position, 0 is player1's piece and 1 is player2's
        self.board = [[-1 for x in range(self.order)] for y in range(self.order)]
        # -1 means no winner
        # 0 ~ order - 1 means one player wins at row i
        # order - 1 ~ order * 2 - 1 means one player wins at col j
        # order * 2 ~ order * 2 + 1 means one player wins at diag 1/2
        self.wintype = -1
        sprites_list = []
        background_sprite = ChessSprite('background', 0, 0, 640, 360, False, True)
        background_sprite.resource = background
        sprites_list.append(background_sprite)
        sprites_list.append(ChessSprite('piece11', 190, 40, 100, 100))
        sprites_list.append(ChessSprite('piece12', 290, 40, 100, 100))
        sprites_list.append(ChessSprite('piece13', 390, 40, 100, 100))
        sprites_list.append(ChessSprite('piece21', 190, 140, 100, 100))
        sprites_list.append(ChessSprite('piece22', 290, 140, 100, 100))
        sprites_list.append(ChessSprite('piece23', 390, 140, 100, 100))
        sprites_list.append(ChessSprite('piece31', 190, 240, 100, 100))
        sprites_list.append(ChessSprite('piece32', 290, 240, 100, 100))
        sprites_list.append(ChessSprite('piece33', 390, 240, 100, 100))
        sprites_list.append(ChessSprite('winner_mark_hor_1', 215, 40, 300, 100, False))
        sprites_list.append(ChessSprite('winner_mark_hor_2', 215, 140, 300, 100, False))
        sprites_list.append(ChessSprite('winner_mark_hor_3', 215, 240, 300, 100, False))
        sprites_list.append(ChessSprite('winner_mark_ver_1', 190, 60, 100, 300, False))
        sprites_list.append(ChessSprite('winner_mark_ver_2', 290, 60, 100, 300, False))
        sprites_list.append(ChessSprite('winner_mark_ver_3', 390, 60, 100, 300, False))
        sprites_list.append(ChessSprite('winner_mark_diag_1', 215, 60, 300, 300, False))
        sprites_list.append(ChessSprite('winner_mark_diag_2', 215, 60, 300, 300, False))
        # sprites list, stores the sprite we need in the game
        super().__init__('tic_tac_toe', 640, 360, sprites_list)

    def CheckClick(self, x, y):
        # stop the game if one of the player has won
        if self.wintype >= 0:
            return False # invlaid click, don't check winner

        index = 0
        piece_pos = {'x': int(-1), 'y': int(-1)}
        for sprite in self.sprites:
            if sprite.is_piece and \
               x > sprite.x and x < sprite.x + sprite.width and \
               y > sprite.y and y < sprite.y + sprite.height:
                piece_pos['x'] = int((index - 1) % self.order)
                piece_pos['y'] = int((index - 1) / self.order)
                break
            index += 1

        # place a piece if this area is empty
        if piece_pos['x'] >= 0 and piece_pos['y'] >= 0 and \
           self.board[piece_pos['y']][piece_pos['x']] < 0:
            self.board[piece_pos['y']][piece_pos['x']] = self.turn
            return True # valid, check winner then
        return False

    def CheckWintype(self):
        if self.wintype >= 0:
            return

        for i in range(self.order):
            win_flag = True
            for j in range(self.order - 1):
                if self.board[i][j] < 0 or self.board[i][j] != self.board[i][j + 1]:
                    win_flag = False
                    break
            if win_flag:
                self.wintype = i # win at row i
                break
        for j in range(self.order):
            win_flag = True
            for i in range(self.order - 1):
                if self.board[i][j] < 0 or self.board[i][j] != self.board[i + 1][j]:
                    win_flag = False
                    break
            if win_flag:
                self.wintype = self.order + j # win at column j
                break
        win_flag = True
        for i in range(self.order - 1):
            if self.board[i][i] < 0 or self.board[i][i] != self.board[i + 1][i + 1]:
                win_flag = False
                break
        if win_flag:
            self.wintype = self.order * 2 # win at diagonal type 1
        win_flag = True
        for i in range(self.order - 1):
            if self.board[i][self.order - i - 1] < 0 or \
               self.board[i][self.order - i - 1] != self.board[i + 1][self.order - i - 2]:
                win_flag = False
                break
        if win_flag:
            self.wintype = self.order * 2 + 1 # win at diagonal type 2

    def TurnFinish(self):
        self.turn = 1 - self.turn

    def UpdatePieceSprite(self):
        for i in range(self.order):
            for j in range(self.order):
                if self.board[i][j] < 0:
                    continue
                elif self.board[i][j] == 0:
                    self.sprites[i * self.order + j + 1].resource = self.player1
                elif self.board[i][j] == 1:
                    self.sprites[i * self.order + j + 1].resource = self.player2
                self.sprites[i * self.order + j + 1].visibility = True

    def UpdateWinnerMark(self):
        if self.wintype < 0:
            return

        if self.wintype >= 0 and self.wintype < self.order:
            self.sprites[self.order * self.order + self.wintype + 1].resource = self.row_mark
        elif self.wintype >= self.order and self.wintype < self.order * 2:
            self.sprites[self.order * self.order + self.wintype + 1].resource = self.col_mark
        elif self.wintype == self.order * 2:
            self.sprites[self.order * self.order + self.wintype + 1].resource = self.diag_mark1
        elif self.wintype == self.order * 2 + 1:
            self.sprites[self.order * self.order + self.wintype + 1].resource = self.diag_mark2
        self.sprites[self.order * self.order + self.wintype + 1].visibility = True

if __name__ == '__main__':
    # init pygame settings and load resources
    pygame.init()
    # load resources
    chess = ChessBoard(
        background = pygame.image.load('resources/blackboard.png'),
        player1 = pygame.image.load('resources/player1.png'),
        player2 = pygame.image.load('resources/player2.png'),
        row_mark = pygame.image.load('resources/row.png'),
        col_mark = pygame.image.load('resources/column.png'),
        diag_mark1 = pygame.image.load('resources/diagonal1.png'),
        diag_mark2 = pygame.image.load('resources/diagonal2.png')
    )
    # add a clock for fps control
    clock = pygame.time.Clock()

    # render the game window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # check mouse click
        click_valid = False
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0]:
            mouse_pos = pygame.mouse.get_pos()
            click_valid = chess.CheckClick(mouse_pos[0], mouse_pos[1])

        if click_valid:
            chess.UpdatePieceSprite()
            # check winner
            chess.CheckWintype()
            if chess.wintype >= 0:
                chess.UpdateWinnerMark()
            chess.TurnFinish()
        chess.UpdateCanvas()

        pygame.display.flip()

        # can also get the real time cost for 60 FPS and do something more e.g.:
        # dt = clock.tick(60)
        # player.position.x += player.xSpeed * dt
        # player.position.y += player.ySpeed * dt
        clock.tick(60)
