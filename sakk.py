#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Sakk
"""

import pygame
import random
import time
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

from pygame.locals import *

negyzet = 70

#keret = pygame.image.load('keret.png')

fig = [[None for i in range(3)] for j in range(6)]

for j in range(1,3):
    fajlnev = 'K' + str(j) + '.png'
    fig[0][j-1] = pygame.image.load(fajlnev)
    print "Betöltöttem a " + fajlnev + " fájlt."
    fajlnev = 'V' + str(j) + '.png'
    fig[1][j-1] = pygame.image.load(fajlnev)
    print "Betöltöttem a " + fajlnev + " fájlt."
    fajlnev = 'B' + str(j) + '.png'
    fig[2][j-1] = pygame.image.load(fajlnev)
    print "Betöltöttem a " + fajlnev + " fájlt."
    fajlnev = 'F' + str(j) + '.png'
    fig[3][j-1] = pygame.image.load(fajlnev)
    print "Betöltöttem a " + fajlnev + " fájlt."
    fajlnev = 'H' + str(j) + '.png'
    fig[4][j-1] = pygame.image.load(fajlnev)
    print "Betöltöttem a " + fajlnev + " fájlt."
    fajlnev = 'Gy' + str(j) + '.png'
    fig[5][j-1] = pygame.image.load(fajlnev)
    print "Betöltöttem a " + fajlnev + " fájlt."

kivalaszt = pygame.image.load("kivalaszt.png")
cel = pygame.image.load("cel.png")
# kivalaszt = cel

t = [[0 for i in range(8)] for j in range(8)]

# Világosak:

t[0][0] = 3
t[1][0] = 5
t[2][0] = 4
t[3][0] = 2
t[4][0] = 1
t[7][0] = 3
t[6][0] = 5
t[5][0] = 4

for i in range(8):
    t[i][1] = 6

# Sötétek:

t[0][7] = 13
t[1][7] = 15
t[2][7] = 14
t[3][7] = 12
t[4][7] = 11
t[7][7] = 13
t[6][7] = 15
t[5][7] = 14

for i in range(8):
    t[i][6] = 16

xplusz = 50
yplusz = 100

sz = negyzet * 8 + 2 * xplusz
m = negyzet * 8 + 2 * yplusz

screen = pygame.display.set_mode((sz, m))

#hatter = pygame.transform.scale(keret, (sz, m))

def figurat_rajzol(oszlop, sor, melyiket):
    if melyiket == 1:
        f = fig[0][0]
    if melyiket == 2:
        f = fig[1][0]
    if melyiket == 3:
        f = fig[2][0]
    if melyiket == 4:
        f = fig[3][0]
    if melyiket == 5:
        f = fig[4][0]
    if melyiket == 6:
        f = fig[5][0]
    if melyiket == 11:
        f = fig[0][1]
    if melyiket == 12:
        f = fig[1][1]
    if melyiket == 13:
        f = fig[2][1]
    if melyiket == 14:
        f = fig[3][1]
    if melyiket == 15:
        f = fig[4][1]
    if melyiket == 16:
        f = fig[5][1]

    if melyiket == 20:
        f = kivalaszt

    if melyiket != 0:
        meretx = f.get_rect().w
        merety = f.get_rect().h
        javitasx = (negyzet-meretx)/2
        javitasy = (negyzet-merety)/2
        screen.blit(f,(oszlop*negyzet+javitasx+xplusz,(7-sor)*negyzet+javitasy+yplusz))

def kirajzol():
    tablaszin = (0,128,0,255)
    pygame.draw.rect(screen, tablaszin, (0,0,sz,m), 0)

    for i in range(8):
        for j in range(8):
            if ((i+j) % 2) == 0:
                mezoszin = (128,128,128,255)
            else:
                mezoszin = (192,192,192,255)
            pygame.draw.rect(screen, mezoszin, (i*negyzet+xplusz,(7-j)*negyzet+yplusz,negyzet,negyzet), 0)
            figurat_rajzol(i, j, t[i][j])

kirajzol()

fut = True

pygame.key.set_repeat(500, 30)

ora = pygame.time.Clock()
ora.tick()

pygame.init()

while fut:

    esemenyek = pygame.event.get()

    for e in esemenyek:
        if e.type == pygame.QUIT:
            fut = False
        if e.type == pygame.KEYDOWN:
            gombok = pygame.key.get_pressed()
            if gombok[K_ESCAPE]:
                fut = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            egergombok = pygame.mouse.get_pressed()
            if egergombok[0]:
                print "Bal egérgomb lenyomva."
                egerhol = pygame.mouse.get_pos()
                egerx = (egerhol[0] - xplusz) / negyzet
                egery = 7 - ((egerhol[1] - yplusz) / negyzet)
                print "Ez a", egerx, egery, "négyzet."
                if (egerx >= 0) and (egerx <= 7) and (egery >=0) and (egery <= 7):
                    figura = t[egerx][egery]
                    if (figura >= 1) and (figura <= 6):
                        figurat_rajzol(egerx, egery, 20)
                

    pygame.display.flip()

    ora.tick(30)

