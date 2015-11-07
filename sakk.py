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

#t[5][3] = 2

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
    if melyiket == 21:
        f = cel

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

def szamma(oszlop, sor):
    return oszlop * 8 + sor

def szambol(szam):
    return [int(szam / 8), szam % 8]

def ures(oszlop, sor):
    return t[oszlop][sor] == 0

def sotet(oszlop, sor):
    return t[oszlop][sor] >= 10

def vilagos(oszlop, sor):
    ez = t[oszlop][sor]
    return ez >= 1 and ez <= 6

def ide_lephet(oszlop, sor):
    valasz = []
    f = t[oszlop][sor]
    if f == 6: # gyalog
        if sor < 7 and ures(oszlop, sor + 1):
            valasz.append(szamma(oszlop,sor+1))
        if sor == 1 and ures(oszlop, sor + 1) and ures(oszlop, sor + 2):
            valasz.append(szamma(oszlop,sor+2))
    if f == 2 or f == 3: # vezér vagy bástya
        # jobbra meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx < 7 and ures(ittx+1, itty):
            valasz.append(szamma(ittx+1,itty))
            ittx += 1
        if ittx < 7 and sotet(ittx+1, itty):
            valasz.append(szamma(ittx+1,itty))
        # balra meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx > 0 and ures(ittx-1, itty):
            valasz.append(szamma(ittx-1,itty))
            ittx -= 1
        if ittx > 0 and sotet(ittx-1, itty):
            valasz.append(szamma(ittx-1,itty))
        # le meddig tud lépni:
        ittx = oszlop
        itty = sor
        while itty > 0 and ures(ittx, itty-1):
            valasz.append(szamma(ittx,itty-1))
            itty -= 1
        if itty > 0 and sotet(ittx, itty-1):
            valasz.append(szamma(ittx,itty-1))
        # fel meddig tud lépni:
        ittx = oszlop
        itty = sor
        while itty < 7 and ures(ittx, itty+1):
            valasz.append(szamma(ittx,itty+1))
            itty += 1
        if itty < 7 and sotet(ittx, itty+1):
            valasz.append(szamma(ittx,itty+1))
    if f == 2 or f == 4: # vezér vagy futó
        # jobbra-fel meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx < 7 and itty < 7 and ures(ittx+1, itty+1):
            valasz.append(szamma(ittx+1,itty+1))
            ittx += 1
            itty += 1
        if ittx < 7 and itty < 7 and sotet(ittx+1, itty+1):
            valasz.append(szamma(ittx+1,itty+1))
        # balra-fel meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx > 0 and itty < 7 and ures(ittx-1, itty+1):
            valasz.append(szamma(ittx-1,itty+1))
            ittx -= 1
            itty += 1
        if ittx > 0 and itty < 7 and sotet(ittx-1, itty+1):
            valasz.append(szamma(ittx-1,itty+1))
        # balra-le meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx > 0 and itty > 0 and ures(ittx-1, itty-1):
            valasz.append(szamma(ittx-1,itty-1))
            ittx -= 1
            itty -= 1
        if ittx > 0 and itty > 0 and sotet(ittx-1, itty-1):
            valasz.append(szamma(ittx-1,itty-1))
        # jobbra-le meddig tud lépni:
        ittx = oszlop
        itty = sor
        while itty > 0 and ittx < 7 and ures(ittx+1, itty-1):
            valasz.append(szamma(ittx+1,itty-1))
            ittx += 1
            itty -= 1
        if itty > 0 and ittx < 7 and sotet(ittx+1, itty-1):
            valasz.append(szamma(ittx+1,itty-1))
    if f == 5: # huszár
        if sor < 7 and oszlop < 6 and not vilagos(oszlop + 2, sor + 1):
            valasz.append(szamma(oszlop+2,sor+1))
        if sor > 0 and oszlop < 6 and not vilagos(oszlop + 2, sor - 1):
            valasz.append(szamma(oszlop+2,sor-1))
        if sor < 6 and oszlop < 7 and not vilagos(oszlop + 1, sor + 2):
            valasz.append(szamma(oszlop+1,sor+2))
        if sor > 1 and oszlop < 7 and not vilagos(oszlop + 1, sor - 2):
            valasz.append(szamma(oszlop+1,sor-2))
        if sor < 7 and oszlop > 1 and not vilagos(oszlop - 2, sor + 1):
            valasz.append(szamma(oszlop-2,sor+1))
        if sor > 0 and oszlop > 1 and not vilagos(oszlop - 2, sor - 1):
            valasz.append(szamma(oszlop-2,sor-1))
        if sor < 6 and oszlop > 0 and not vilagos(oszlop - 1, sor + 2):
            valasz.append(szamma(oszlop-1,sor+2))
        if sor > 1 and oszlop > 0 and not vilagos(oszlop - 1, sor - 2):
            valasz.append(szamma(oszlop-1,sor-2))
    return valasz

kijelolve = False
lepett = False

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
                    if kijelolve:
                        for lista in lepesek:
                            ide = szambol(lista)
                            idex = ide[0]
                            idey = ide[1]
                            if (egerx == idex) and (egery == idey):
                                # Itt lépünk:
                                t[egerx][egery] = t[innenx][inneny]
                                t[innenx][inneny] = 0
                                # Ha a gyalog belépett az utolsó sorba, akkor vezér lesz:
                                if t[egerx][egery] == 6 and egery == 7:
                                    t[egerx][egery] = 2
                                kijelolve = False
                                lepett = True
                                kirajzol()
                    if not lepett:
                        figura = t[egerx][egery]
                        if (figura >= 1) and (figura <= 6):
                            kirajzol()
                            figurat_rajzol(egerx, egery, 20)
                            lepesek = ide_lephet(egerx, egery)
                            for lista in lepesek:
                                ide = szambol(lista)
                                print "Ide léphet:", ide
                                idex = ide[0]
                                idey = ide[1]
                                figurat_rajzol(idex, idey, 21)
                                kijelolve = True
                            innenx = egerx
                            inneny = egery
                

    pygame.display.flip()

    lepett = False

    ora.tick(30)

