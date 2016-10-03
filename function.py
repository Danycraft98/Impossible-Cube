import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self,loc): #Init the player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill((0,180,0))
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

    def handleKeys(self,checker): #Keys to movement
        kpd = pygame.key.get_pressed()
        dist=2*checker
        if kpd[K_DOWN] or kpd[K_s]:
            self.rect.y += dist
        elif kpd[K_UP] or kpd[K_w]:
            self.rect.y -= dist
        if kpd[K_RIGHT] or kpd[K_d]:
            self.rect.x += dist
        elif kpd[K_LEFT] or kpd[K_a]:
            self.rect.x -= dist

    def draw(self,surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))

    def checkColl(self,sprite1,sprite2,checker):#"checkColl" is short for check collision
        if sprite1.colliderect(sprite2) == True:
            Player.handleKeys(self,checker)

    def checkDead(self,loc):
        self.rect.x = loc[0]
        self.rect.y = loc[1]

class Enemy(pygame.sprite.Sprite):#creates the "ennemy" squares, the red ones
    def __init__(self,loc,size,move):#the sprite has its own "loc" tuple, as well as another tuple for its size and another for how it moves
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)#uses the tuple for its size to make its size
        self.image.fill((255,0,0))# makes the colour red
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]#uses the "loc" to determine its posotion
        self.rect.y = loc[1]
        self.dir_x = move[0]#the "move" tuple will have 3 parts lets say:(x,y,z), x will be its x coordinate posotion
        self.dir_y = move[1]#the y will be its y coordinate posotion
        self.speed = move[2]# the z will not be a position, but rather the speed of the ennemy sprite
        self.rect.move_ip(self.speed*self.dir_x,self.speed*self.dir_y)#multiplies the x and y coordinate values by the speed so we can increase/decrease it if necessary

    def update(self,surface):#checks to see if the sprite will collide with the screen, in which case it will change directions
        if self.rect.left < 0 or self.rect.right >= surface.get_width():
            self.dir_x *= -1
        if self.rect.top < 0 or self.rect.bottom >= surface.get_height():
            self.dir_y *= -1
        self.rect.move_ip(self.speed*self.dir_x,self.speed*self.dir_y)

    def checkCollision(self):#checks to see if the sprite collides with a black wall, in which case it will go the opposite direction
        self.dir_x *= -1
        self.dir_y *= -1
        self.rect.move_ip(self.speed*self.dir_x,self.speed*self.dir_y)

    def draw(self, surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))#makes the sprite visible

class Key(pygame.sprite.Sprite):#This is the little yellow square you need to get to open the door
    def __init__(self,screen,loc):#"loc" varible is used the same way as before
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((251,133,0))#makes the colour more orange
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

    def draw(self,surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))#makes the sprite visible

class Door(pygame.sprite.Sprite):
    def __init__(self,loc,size):#"loc" and "size" is used the same way as before
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill((251,133,0))
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

    def open(self,loc,size):#"open" is for making the door "open" after the player touches the key to let the player touch the blue part to end the level
        self.image = pygame.Surface(size)
        self.image.fill((251,133,0))
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]#places the opendoor in its new posotion
        self.rect.y = loc[1]

    def draw(self, surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))#draws the door

class Wall(pygame.sprite.Sprite):#makes black rectanges that will be walls, which neither the players or ennemies can pass
    def __init__(self,loc,size):#"loc" and "size" used same as before
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

    def draw(self,surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))

class Platform(pygame.sprite.Sprite):#the "platform" is the blue rectange behind the orange door, touch it to end your level and move on to the next one
    def __init__(self,loc,size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

    def draw(self,surface):#draws the platform
        surface.blit(self.image,(self.rect.x,self.rect.y))

class Trap(pygame.sprite.Sprite): #traps are the light blue platforms that turn "on" and "off"
    def __init__(self,loc,size):#What makes them "tick" is in the acuactl game file, not this file full of classes and functions
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill((0,200,200))
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class fakeWalls(pygame.sprite.Sprite):#makes pink walls that cause the player to "die" making them loose a life and going back to their starting posotion
    def __init__(self,location,size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size).convert()
        self.image.fill((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]

    def draw(self, surface):#draws the image
        surface.blit(self.image, (self.rect.x, self.rect.y))

#------------------------------Helper Functions---------------------------------
def wall(info):
    wall_group = pygame.sprite.Group()
    for element in info:
        wall_group.add(Wall(element[0],element[1]))
    return wall_group

def enemy(info):
    enemy_group = pygame.sprite.Group()
    for element in info:
        enemy_group.add(Enemy(element[0],element[1],element[2]))
    return enemy_group

def key(screen,info):
    key_group = pygame.sprite.Group()
    for element in info:
        key_group.add(Key(screen,element))
    return key_group

def trap(trap_info):
    trap_group= pygame.sprite.Group()
    for element in trap_info:
        trap_group.add(Trap(element[0],element[1]))
    return trap_group

def fakeWall(fakeWall_info):
    fakeWall_group= pygame.sprite.Group()
    for element in fakeWall_info:
        fakeWall_group.add(fakeWalls(element[0],element[1]))
    return fakeWall_group

def menuText(image,boolean,menuOn,kpd,surface):
    rect = image.get_rect(center=(640,360))
    surface.blit(image, (rect.x, rect.y))
    pygame.display.update()
    for ev in pygame.event.get():
        if kpd[K_SPACE]:
            boolean = False
            menuOn = True
    return boolean,menuOn