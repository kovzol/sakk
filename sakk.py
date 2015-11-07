#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Sakk
"""

import pygame
import random
import time
import os
import copy
import sys

os.environ['SDL_VIDEO_CENTERED'] = '1'

from pygame.locals import *

negyzet = 70
xplusz = 50
yplusz1 = 370
yplusz2 = 30

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

for i in range(8):
    t[i][6] = 16

sz = negyzet * 8 + 2 * xplusz
m = negyzet * 8 + yplusz1 + yplusz2

screen = pygame.display.set_mode((sz, m))

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

def kedvszin():
    e = tablaertek()
    if e > 900:
        return [255,255,255]
    if e > 10:
        return [192,192,192]
    if e > 3:
        return [0,192,0]
    if e < -2:
        return [0,64,0]
    if e < -10:
        return [64,64,64]
    if e < -900:
        return [16,16,16]
    return [0,128,0]

def robotkirajzolas(kedv):
    robotx = robot.get_rect().w
    roboty = robot.get_rect().h
    pygame.draw.rect(screen, (kedv[0],kedv[1],kedv[2],255), (0,0,sz,roboty), 0)
    screen.blit(robot,((sz-robotx)/2,0))

def kirajzol():
    tablaszin = (0,128,0,255)
    pygame.draw.rect(screen, tablaszin, (0,0,sz,m), 0)

    robotkirajzolas(kedvszin())

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

def ide_lephet(oszlop, sor):
    """Egy bizonyos helyről hová léphet valamelyik játékos. Esetleg sakkba is léphet."""
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

def figuranev(f):
    nevek = {
        1: "K",
        2: "V",
        3: "B",
        4: "F",
        5: "H",
        6: str("")
        }
    if f > 6:
        f -= 10
    return nevek.get(f,"?")

def lepesinfo(x1,y1,x2,y2):
    f = figuranev(t[x1][y1])
    x = str("")
    if t[x2][y2] > 0:
        x = "x"
        if f == "": # gyalognál az induló oszlop
            f = str(chr(x1+ord('a')))
    return f + x + str(chr(x2+ord('a'))) + str(y2+1)

def ide_lephet_de_nincs_sakkban(oszlop,sor):
    """Egy bizonyos helyről hová léphet valamelyik játékos. Sakkba nem léphet."""
    f = t[oszlop][sor]
    if vilagos(oszlop, sor):
        plusz = 0
    else:
        plusz = 10

    valasz = ide_lephet(oszlop,sor)
    # Megnézzük, hogy a lehetséges lépések között van-e olyan,
    # ami sakkba lépést jelentene.
    tabla_mentes = copy.deepcopy(t) # megjegyezzük, hogy mi az állás
    torlendo = []
    for l in valasz:
        global t
        info = lepesinfo(oszlop,sor,l[0],l[1])
        # print "Sakkba lépünk-e a",info,"lépéssel?"
        meglepi(oszlop,sor,l[0],l[1]) # kipróbáljuk, mi lenne, ha ezt lépnénk
        tabla_mentes2 = copy.deepcopy(t)
        # Megnézzük, hogy erre a lépésre az ellenfél miket tud lépni
        for o in range(8):
            for s in range(8):
                if ellenkezo(o,s,plusz):
                    for ellenfel_lepes in ide_lephet(o,s):
                        info = lepesinfo(o,s,ellenfel_lepes[0],ellenfel_lepes[1])
                        meglepi(o,s,ellenfel_lepes[0],ellenfel_lepes[1])
                        ertek_ez = tablaertek()
                        if ertek_ez < -500 or ertek_ez > 500: # valamelyik félnek le lehetne ütni a királyát
                            # print "Igen, mert az ellenfél",info,"lépésére a tábla értéke",ertek_ez
                            if not (l in torlendo):
                                torlendo.append(l) # ez a lépés nem szabályos, töröljük
                        t = copy.deepcopy(tabla_mentes2) # visszacsináljuk az ellenfél lépésést
        t = copy.deepcopy(tabla_mentes) # visszacsináljuk a próbalépésünket
    for l in torlendo:
        valasz.remove(l)
    return valasz

def sotet_nyer():
    pygame.mixer.music.fadeout(0)
    # http://www.clanb2k.com/cstrike12/sound/zombie_plague/survivor1.wav
    pygame.mixer.music.load("sotet_nyer.wav")
    pygame.mixer.music.play(0)
    time.sleep(5)
    pygame.quit()
    sys.exit()

def vilagos_nyer():

    for i in range(1000):
        # 0 -> 16, 128 -> 16, 0 -> 16
        kedv = kedvszin()
        honnanr = kedv[0]
        honnang = kedv[1]
        honnanb = kedv[2]
        robotkirajzolas([honnanr - (honnanr - 16)*i/1000,honnang - (honnang-16)*i/1000,honnanb - (honnanb-16)*i/1000])
        pygame.display.flip()

    pygame.mixer.quit()
    film = pygame.movie.Movie('explosion.mpg')
    robotx = robot.get_rect().w
    film_screen = pygame.Surface((robotx,robot.get_rect().h))

    film.set_display(film_screen)
    film.play()

    a = 0
    FPS = 60

    lejatszas = True

    while lejatszas and (a < 400):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                film.stop()
                lejatszas = False
        screen.blit(film_screen,((sz-robotx)/2,0))

        pygame.display.update()
        ora.tick(FPS)
        a += 1
    pygame.quit()
    sys.exit()

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

def also_fele_lep(innen_lehetseges, ide_lehetseges):
    return 0
    # return int(szamuk/2)

def okosan_lep(innen_lehetseges, ide_lehetseges):
    szamuk = len(ide_lehetseges)
    global t
    tabla_mentes = copy.deepcopy(t) # megjegyezzük, hogy mi az állás
    legjobb_tablaertek = -2000 # ennél biztosan csak jobb lehet
    for l in range(szamuk):
        t = copy.deepcopy(tabla_mentes)
        proba_innen = innen_lehetseges[l]
        proba_ide = ide_lehetseges[l]
        meglepi(proba_innen[0], proba_innen[1], proba_ide[0], proba_ide[1])
        ertek_ez = tablaertek()
        if ertek_ez > legjobb_tablaertek:
            legjobb_lepes = l
            legjobb_tablaertek = ertek_ez
        if ertek_ez == legjobb_tablaertek and random.randint(1,6) <= 1:
            legjobb_lepes = l
    t = copy.deepcopy(tabla_mentes)
    return legjobb_lepes

def nagyon_okosan_lep(innen_lehetseges, ide_lehetseges):
    szamuk = len(ide_lehetseges)
    global t
    tabla_mentes = copy.deepcopy(t) # megjegyezzük, hogy mi az állás
    legjobb_tablaertek = -2000 # ennél csak jobb lehet (minimax)
    for l in range(szamuk):
        t = copy.deepcopy(tabla_mentes)
        proba_innen = innen_lehetseges[l]
        proba_ide = ide_lehetseges[l]
        meglepi(proba_innen[0], proba_innen[1], proba_ide[0], proba_ide[1]) # sötét tervezett saját lépése
        tabla_mentes2 = copy.deepcopy(t)
        # Megnézzük, hogy milyen válaszlépéseket tud adni a világos:
        vilagos_legkellemetlenebb_valasza = 2000
        for i in range(8):
            for j in range(8):
                if vilagos(i,j):
                    ide = ide_lephet_de_nincs_sakkban(i,j)
                    for ide_lehet in ide:
                        meglepi(i,j,ide_lehet[0],ide_lehet[1])
                        ertek_ez = tablaertek()
                        if ertek_ez < vilagos_legkellemetlenebb_valasza:
                            vilagos_legkellemetlenebb_valasza = ertek_ez
                        t = copy.deepcopy(tabla_mentes2)
        if vilagos_legkellemetlenebb_valasza > legjobb_tablaertek:
            legjobb_tablaertek = vilagos_legkellemetlenebb_valasza
            legjobb_lepes = l
        if vilagos_legkellemetlenebb_valasza == legjobb_tablaertek and random.randint(1,6) <= 1:
            legjobb_lepes = l
    t = copy.deepcopy(tabla_mentes)
    return legjobb_lepes

def butan_lep(innen_lehetseges, ide_lehetseges):
    szamuk = len(ide_lehetseges)
    veletlen = random.randint(0,szamuk-1)
    return veletlen

kijelolve = False
lepett = False
lepes = 1
jatszma = ""

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
                                info = lepesinfo(innenx,inneny,egerx,egery)
                                jatszma += str(lepes) + ". " + info + " "
                                print "Játszma:", jatszma
                                meglepi(innenx,inneny,egerx,egery)
                                kijelolve = False
                                lepett = True
                                kirajzol()
                                # lepes += 1
                                if lepes % 4 == -1:
                                    sotet_nyer()
                    if not lepett:
                        figura = t[egerx][egery]
                        if (figura >= 1) and (figura <= 6):
                            kirajzol()
                            figurat_rajzol(egerx, egery, 20)
                            lepesek = ide_lephet_de_nincs_sakkban(egerx, egery)
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
                    ide = ide_lephet_de_nincs_sakkban(i,j)
                    for ide_lehet in ide:
                        ide_lehetseges.append(ide_lehet)
                        innen_lehetseges.append([i,j])

        szamuk = len(ide_lehetseges)
        print "Sötét lehetséges lépései:", szamuk, "db"
        if szamuk == 0:
            vilagos_nyer()

        # ezt_lepi = butan_lep(innen_lehetseges, ide_lehetseges)
        # ezt_lepi = okosan_lep(innen_lehetseges, ide_lehetseges)
        ezt_lepi = nagyon_okosan_lep(innen_lehetseges, ide_lehetseges)

        gep_ide = ide_lehetseges[ezt_lepi]
        gep_innen = innen_lehetseges[ezt_lepi]
        # Itt lép:
        innenx = gep_innen[0]
        inneny = gep_innen[1]
        figurat_rajzol(innenx,inneny,20)
        pygame.display.flip()
        time.sleep(0.5)
        egerx = gep_ide[0]
        egery = gep_ide[1]
        figurat_rajzol(egerx,egery,21)
        pygame.display.flip()
        time.sleep(0.5)
        info = lepesinfo(innenx,inneny,egerx,egery)
        jatszma += info + " "
        print "Játszma:", jatszma
        meglepi(innenx,inneny,egerx,egery)
        kirajzol()

        pygame.display.flip()

        # Megnézzük, mattot kapott-e a világos:
        matt = True
        for i in range(8):
            for j in range(8):
                if vilagos(i,j):
                    if ide_lephet_de_nincs_sakkban(i,j) <> []:
                        matt = False
        if matt:
            sotet_nyer()

        lepes += 1

        print "A tábla értéke:", tablaertek()

    lepett = False


    ora.tick(30)

