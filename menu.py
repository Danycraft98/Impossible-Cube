import pygame,sys
from pygame.locals import *

class Menu():
    def __init__(self,screen,font):
        self.selected = 0
        self.menu = [' Start ',' Help ',' Quit ']
        self.font = font
        # set pygame options
        self.menuid()

    #handle keys for the menu
    def handlekeys(self,kpd,menuOn,game,help):
        for event in pygame.event.get():
            if kpd[K_LEFT]:
                self.position(-1)
            elif kpd[K_RIGHT]:
                self.position(1)
            if kpd[K_RETURN]:
                menuOn,game,help = self.select(menuOn,game,help)
        return menuOn,game,help

    def menuid(self):
        self.mid= list()
        for n in self.menu:
            text_surface = self.font.render(n,True,(255,255,255))
            self.mid.append(text_surface.get_width())

    def position(self,move):
        self.selected += move
        if self.selected < 0:
            self.selected = 2
        if self.selected > 2:
            self.selected = 0

    def select(self,menuOn,game,help):
        menuOn = False
        if self.selected == 0:
            game = True
        elif self.selected == 1:
            help = True
        else:
            pygame.quit()
            sys.exit()
        return menuOn,game,help

    def comeBack(self):
        self.selected = 0

    def draw(self,screen):
        i = 0
        xpos = 0
        while i <= self.selected:
            xpos -= self.mid[i]
            i += 1
        xpos += self.mid[self.selected]/2
        # draw menus on screen
        arrow = self.font.render('^', True,(255,255,255))
        screen.blit(arrow,(650,550))
        title = self.font.render('Impossible Cube', True,(255,255,255))
        screen.blit(title,(550,100))
        submenu = self.font.render(' Start  Help  Quit ', True,(255,255,255))
        screen.blit(submenu,(650 + xpos,500))
