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
xplusz = 50
yplusz1 = 370
yplusz2 = 30

#keret = pygame.image.load('keret.png')

fig = [[None for i in range(3)] for j in range(6)]

for j in range(1,3):
    fajlnev = 'K' + str(j) + '.png'
    fig[0][j-1] = pygame.image.load(fajlnev)
    fajlnev = 'V' + str(j) + '.png'
    fig[1][j-1] = pygame.image.load(fajlnev)
    fajlnev = 'B' + str(j) + '.png'
    fig[2][j-1] = pygame.image.load(fajlnev)
    fajlnev = 'F' + str(j) + '.png'
    fig[3][j-1] = pygame.image.load(fajlnev)
    fajlnev = 'H' + str(j) + '.png'
    fig[4][j-1] = pygame.image.load(fajlnev)
    fajlnev = 'Gy' + str(j) + '.png'
    fig[5][j-1] = pygame.image.load(fajlnev)

kivalaszt = pygame.image.load("kivalaszt.png")
cel = pygame.image.load("cel.png")
robot = pygame.image.load("robot.png")

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


sz = negyzet * 8 + 2 * xplusz
m = negyzet * 8 + yplusz1 + yplusz2

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
        screen.blit(f,(oszlop*negyzet+javitasx+xplusz,(7-sor)*negyzet+javitasy+yplusz1))

def kirajzol():
    tablaszin = (0,128,0,255)
    pygame.draw.rect(screen, tablaszin, (0,0,sz,m), 0)

    # Robotkirajzolás:
    robotx = robot.get_rect().w
    screen.blit(robot,((sz-robotx)/2,0))

    for i in range(8):
        for j in range(8):
            if ((i+j) % 2) == 0:
                mezoszin = (128,128,128,255)
            else:
                mezoszin = (192,192,192,255)
            pygame.draw.rect(screen, mezoszin, (i*negyzet+xplusz,(7-j)*negyzet+yplusz1,negyzet,negyzet), 0)
            figurat_rajzol(i, j, t[i][j])

kirajzol()

fut = True

pygame.key.set_repeat(500, 30)

ora = pygame.time.Clock()
ora.tick()

pygame.init()

def ures(oszlop, sor):
    return t[oszlop][sor] == 0

def sotet(oszlop, sor):
    return t[oszlop][sor] >= 10

def vilagos(oszlop, sor):
    ez = t[oszlop][sor]
    return ez >= 1 and ez <= 6

def ellenkezo(oszlop, sor, p):
    if p == 0: # a világos ellenkezőjét keressük
        return sotet(oszlop, sor)
    return vilagos(oszlop, sor)

def azonos(oszlop, sor, p):
    if p == 0: # a világossal azonosat keressük
        return vilagos(oszlop, sor)
    return sotet(oszlop, sor)

def tablaertek():
    ertek = 0
    for i in range(8):
        for j in range(8):
            f = t[i][j]
            ertekek = {
                1: -1000,
                2: -9,
                3: -5,
                4: -3,
                5: -2,
                6: -1,
                11: 1000,
                12: 9,
                13: 5,
                14: 3,
                15: 2,
                16: 1
                }
            ertek += ertekek.get(f, 0)
    return ertek

def ide_lephet(oszlop, sor):
    valasz = []
    f = t[oszlop][sor]
    if vilagos(oszlop, sor):
        plusz = 0
    else:
        plusz = 10

    if f == 6: # világos gyalog
        if sor < 7 and ures(oszlop, sor + 1):
            valasz.append([oszlop,sor+1])
        if sor == 1 and ures(oszlop, sor + 1) and ures(oszlop, sor + 2):
            valasz.append([oszlop,sor+2])
        # jobbra ütés:
        if sor < 7 and oszlop < 7 and ellenkezo(oszlop+1,sor+1,plusz):
            valasz.append([oszlop+1,sor+1])
        # balra ütés:
        if sor < 7 and oszlop > 0 and ellenkezo(oszlop-1,sor+1,plusz):
            valasz.append([oszlop-1,sor+1])
    if f == 16: # sötét gyalog
        if sor > 0 and ures(oszlop, sor - 1):
            valasz.append([oszlop,sor-1])
        if sor == 6 and ures(oszlop, sor - 1) and ures(oszlop, sor - 2):
            valasz.append([oszlop,sor-2])
        # jobbra ütés:
        if sor > 0 and oszlop < 7 and ellenkezo(oszlop+1,sor-1,plusz):
            valasz.append([oszlop+1,sor-1])
        # balra ütés:
        if sor > 0 and oszlop > 0 and ellenkezo(oszlop-1,sor-1,plusz):
            valasz.append([oszlop-1,sor-1])
    if f == 2 + plusz or f == 3 + plusz: # vezér vagy bástya
        # jobbra meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx < 7 and ures(ittx+1, itty):
            valasz.append([ittx+1,itty])
            ittx += 1
        if ittx < 7 and ellenkezo(ittx+1, itty,plusz):
            valasz.append([ittx+1,itty])
        # balra meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx > 0 and ures(ittx-1, itty):
            valasz.append([ittx-1,itty])
            ittx -= 1
        if ittx > 0 and ellenkezo(ittx-1, itty,plusz):
            valasz.append([ittx-1,itty])
        # le meddig tud lépni:
        ittx = oszlop
        itty = sor
        while itty > 0 and ures(ittx, itty-1):
            valasz.append([ittx,itty-1])
            itty -= 1
        if itty > 0 and ellenkezo(ittx, itty-1,plusz):
            valasz.append([ittx,itty-1])
        # fel meddig tud lépni:
        ittx = oszlop
        itty = sor
        while itty < 7 and ures(ittx, itty+1):
            valasz.append([ittx,itty+1])
            itty += 1
        if itty < 7 and ellenkezo(ittx, itty+1,plusz):
            valasz.append([ittx,itty+1])
    if f == 2 + plusz or f == 4 + plusz: # vezér vagy futó
        # jobbra-fel meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx < 7 and itty < 7 and ures(ittx+1, itty+1):
            valasz.append([ittx+1,itty+1])
            ittx += 1
            itty += 1
        if ittx < 7 and itty < 7 and ellenkezo(ittx+1, itty+1,plusz):
            valasz.append([ittx+1,itty+1])
        # balra-fel meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx > 0 and itty < 7 and ures(ittx-1, itty+1):
            valasz.append([ittx-1,itty+1])
            ittx -= 1
            itty += 1
        if ittx > 0 and itty < 7 and ellenkezo(ittx-1, itty+1,plusz):
            valasz.append([ittx-1,itty+1])
        # balra-le meddig tud lépni:
        ittx = oszlop
        itty = sor
        while ittx > 0 and itty > 0 and ures(ittx-1, itty-1):
            valasz.append([ittx-1,itty-1])
            ittx -= 1
            itty -= 1
        if ittx > 0 and itty > 0 and ellenkezo(ittx-1, itty-1,plusz):
            valasz.append([ittx-1,itty-1])
        # jobbra-le meddig tud lépni:
        ittx = oszlop
        itty = sor
        while itty > 0 and ittx < 7 and ures(ittx+1, itty-1):
            valasz.append([ittx+1,itty-1])
            ittx += 1
            itty -= 1
        if itty > 0 and ittx < 7 and ellenkezo(ittx+1, itty-1,plusz):
            valasz.append([ittx+1,itty-1])
    if f == 5 + plusz: # huszár
        if sor < 7 and oszlop < 6 and not azonos(oszlop + 2, sor + 1,plusz):
            valasz.append([oszlop+2,sor+1])
        if sor > 0 and oszlop < 6 and not azonos(oszlop + 2, sor - 1,plusz):
            valasz.append([oszlop+2,sor-1])
        if sor < 6 and oszlop < 7 and not azonos(oszlop + 1, sor + 2,plusz):
            valasz.append([oszlop+1,sor+2])
        if sor > 1 and oszlop < 7 and not azonos(oszlop + 1, sor - 2,plusz):
            valasz.append([oszlop+1,sor-2])
        if sor < 7 and oszlop > 1 and not azonos(oszlop - 2, sor + 1,plusz):
            valasz.append([oszlop-2,sor+1])
        if sor > 0 and oszlop > 1 and not azonos(oszlop - 2, sor - 1,plusz):
            valasz.append([oszlop-2,sor-1])
        if sor < 6 and oszlop > 0 and not azonos(oszlop - 1, sor + 2,plusz):
            valasz.append([oszlop-1,sor+2])
        if sor > 1 and oszlop > 0 and not azonos(oszlop - 1, sor - 2,plusz):
            valasz.append([oszlop-1,sor-2])
    if f == 1 + plusz: # király
        if sor < 7 and oszlop < 7 and not azonos(oszlop + 1, sor + 1,plusz):
            valasz.append([oszlop+1,sor+1])
        if sor > 0 and oszlop < 7 and not azonos(oszlop + 1, sor - 1,plusz):
            valasz.append([oszlop+1,sor-1])
        if sor < 7 and oszlop > 0 and not azonos(oszlop - 1, sor + 1,plusz):
            valasz.append([oszlop-1,sor+1])
        if sor > 0 and oszlop > 0 and not azonos(oszlop - 1, sor - 1,plusz):
            valasz.append([oszlop-1,sor-1])
        if oszlop < 7 and not azonos(oszlop + 1, sor,plusz):
            valasz.append([oszlop+1,sor])
        if sor < 7 and not azonos(oszlop, sor + 1,plusz):
            valasz.append([oszlop,sor+1])
        if oszlop > 0 and not azonos(oszlop - 1, sor,plusz):
            valasz.append([oszlop-1,sor])
        if sor > 0 and not azonos(oszlop, sor - 1,plusz):
            valasz.append([oszlop,sor-1])
    return valasz

def sotet_nyer():
    pygame.mixer.music.fadeout(0)
    # http://www.clanb2k.com/cstrike12/sound/zombie_plague/survivor1.wav
    pygame.mixer.music.load("sotet_nyer.wav")
    pygame.mixer.music.play(0)

def meglepi(honnanx, honnany, hovax, hovay):
    """Meglépi a táblán a honnan mezőről a hova mezőre a lépést."""
    t[hovax][hovay] = t[honnanx][honnany]
    t[honnanx][honnany] = 0
    # Ha a világos gyalog belépett az utolsó sorba, akkor vezér lesz:
    if t[hovax][hovay] == 6 and hovay == 7:
        t[hovax][7] = 2
    # Ha a sötét gyalog belépett az utolsó sorba, akkor vezér lesz:
    if t[hovax][hovay] == 16 and hovay == 0:
        t[hovax][0] = 12

def okosan_lep(innen_lehetseges, ide_lehetseges):
    tabla_mentes = t # megjegyezzük, hogy mi az állás
    return 0

def butan_lep(innen_lehetseges, ide_lehetseges):
    szamuk = len(ide_lehetseges)
    veletlen = random.randint(0,szamuk-1)
    return veletlen

kijelolve = False
lepett = False
lepes = 0

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
                egerhol = pygame.mouse.get_pos()
                egerx = (egerhol[0] - xplusz) / negyzet
                egery = 7 - ((egerhol[1] - yplusz1) / negyzet)
                if (egerx >= 0) and (egerx <= 7) and (egery >=0) and (egery <= 7):
                    if kijelolve:
                        for lista in lepesek:
                            idex = lista[0]
                            idey = lista[1]
                            if (egerx == idex) and (egery == idey):
                                # Itt lépünk:
                                meglepi(innenx,inneny,egerx,egery)
                                kijelolve = False
                                lepett = True
                                kirajzol()
                                lepes += 1
                                if lepes % 4 == -1:
                                    sotet_nyer()
                    if not lepett:
                        figura = t[egerx][egery]
                        if (figura >= 1) and (figura <= 6):
                            kirajzol()
                            figurat_rajzol(egerx, egery, 20)
                            lepesek = ide_lephet(egerx, egery)
                            for lista in lepesek:
                                idex = lista[0]
                                idey = lista[1]
                                figurat_rajzol(idex, idey, 21)
                                kijelolve = True
                            innenx = egerx
                            inneny = egery

    pygame.display.flip()

    if lepett: # most a gép lép
        ide_lehetseges = []
        innen_lehetseges = []
        for i in range(8):
            for j in range(8):
                if sotet(i,j):
                    ide = ide_lephet(i,j)
                    for ide_lehet in ide:
                        ide_lehetseges.append(ide_lehet)
                        innen_lehetseges.append([i,j])

        szamuk = len(ide_lehetseges)
        print "Sötét lehetséges lépései:", szamuk, "db"

        ezt_lepi = butan_lep(innen_lehetseges, ide_lehetseges) 

        gep_ide = ide_lehetseges[ezt_lepi]
        gep_innen = innen_lehetseges[ezt_lepi]
        # Itt lép:
        innenx = gep_innen[0]
        inneny = gep_innen[1]
        egerx = gep_ide[0]
        egery = gep_ide[1]
        meglepi(innenx,inneny,egerx,egery)
        kirajzol()

        lepes += 1

        print "A tábla értéke:", tablaertek()


    lepett = False


    ora.tick(30)

