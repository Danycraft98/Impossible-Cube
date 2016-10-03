import pygame,sys,menu,function
from pygame.locals import *
pygame.init()

#Preset
helpImage = pygame.image.load("help.png")
endImage = pygame.image.load("end.png")
pygame.mixer.music.load("bgMusic.ogg")

loseMsg = ['Sorry but you have lost the game.','please try again next time.']
winMsg = ['Congratz you have won.',"you're welcome to play next time."]

#key = level, value = [sprite start info, wall info, door loc info, door close info, door open info, key info, level end info,enemy info,trapdoor,fake wall info]
lvl = {1:[(610,560),[[(190,60),(900,30)],[(190,160),(410,30)],[(680,160),(410,30)],[(190,60),(30,130)],[(1060,60),(30,130)],[(570,160),(30,500)],[(670,160),(30,500)],[(570,630),(110,30)]],(900,60),(30,100),(100,30),[(230,120)],(1030,90),None,None,None],
       2:[(270,310),[[(190,270),(410,30)],[(700,270),(410,30)],[(190,370),(410,30)],[(700,370),(410,30)],[(570,60),(30,240)],[(670,60),(30,240)],[(570,60),(110,30)],[(570,60),(30,240)],[(670,60),(30,240)],[(570,370),(30,240)],[(670,370),(30,240)],[(570,580),(110,30)],[(190,270),(30,110)],[(1080,270),(30,110)]],(960,270),(30,100),(100,30),[(240,330)],(1050,300),[[(610,120),(50,50),(0,1,2)]],None,None],
       3:[(270,320),[[(190,60),(900,30)],[(190,630),(900,30)],[(190,60),(30,600)],[(1060,60),(30,600)],[(890,60),(200,250)],[(890,380),(200,250)]],(890,280),(30,100),(100,30),[(850,340)],(1030,310),[[(360,120),(30,30),(0,1,2)],[(560,120),(30,30),(0,1,2)],[(760,120),(30,30),(0,1,2)]],[[(460,90),(30,540)],[(660,90),(30,540)]],None],
       4:[(230,240),[[(190,60),(900,30)],[(190,630),(900,30)],[(190,60),(30,600)],[(1060,60),(30,600)],[(190,60),(300,100)],[(590,60),(500,70)],[(290,230),(530,100)],[(890,230),(100,220)],[(190,300),(400,120)],[(690,300),(200,150)],[(190,520),(400,140)],[(690,550),(400,110)]],(320,420),(30,100),(100,30),[(850,280)],(220,450),[[(220,180),(30,30),(1,0,2)],[(625,400),(30,30),(0,1,1)]],[[(450,450),(30,70)],[(800,450),(30,70)]],[[(590,130),(470,30)],[(220,420),(370,30)],[(690,520),(400,30)]]],
       5:[(230,290),[[(190,250),(30,100)],[(570,60),(70,30)],[(570,630),(70,30)],[(990,60),(70,30)],[(570,630),(70,30)],[(990,630),(70,30)],[(190,480),(30,180)],[(390,510),(30,20)],[(390,610),(30,20)],[(1060,480),(30,150)]],(280,520),(30,100),(100,30),[(600,120)],(220,535),[[(570,550),(70,50),(0,1,1)],[(990,100),(70,50),(0,1,1)],[(420,510),(30,20),(1,0,2)],[(720,610),(30,20),(1,0,2)]],[[(500,260),(50,120)],[(650,260),(50,120)],[(575,90),(65,70)],[(600,500),(40,150)],[(750,500),(40,150)],[(870,500),(40,150)],[(480,500),(40,150)],[(980,400),(100,50)],[(980,200),(100,50)]],[[(540,60),(30,100)],[(640,60),(350,30)],[(220,630),(870,30)],[(220,480),(760,30)],[(1060,60),(30,420)],[(190,250),(800,30)],[(190,350),(800,30)],[(540,160),(450,30)],[(960,160),(30,100)],[(960,360),(30,150)]]]}

#Setting
screen = pygame.display.set_mode((1280,720),pygame.FULLSCREEN)
font = pygame.font.SysFont("arial", 40)
menu = menu.Menu(screen,font)

pygame.event.pump()
gameLoop = True
menuOn,game,help, quitted = True,False,False,False
mRedraw = 0

while gameLoop:
    while menuOn:
        kpd = pygame.key.get_pressed()
        menuOn,game,help = menu.handlekeys(kpd,menuOn,game,help)
        if game == True or help == True:
            lvlNum,health = 1,10
            init = True
        screen.fill((43, 60, 28))
        menu.draw(screen)
        pygame.display.update()

    while help:
        kpd = pygame.key.get_pressed()
        help,init = function.menuText(helpImage,help,menuOn,kpd,screen)
        mRedraw = 0

    while init:
        player = function.Player(lvl[lvlNum][0])
        if lvl[lvlNum][7] != None:
            enemyGroup = function.enemy(lvl[lvlNum][7])

        if lvl[lvlNum][8] != None:
            trapGroup = function.trap(lvl[lvlNum][8])

        if lvl[lvlNum][9] != None:
            fakeWallGroup = function.fakeWall(lvl[lvlNum][9])

        wallGroup = function.wall(lvl[lvlNum][1])
        door = function.Door(lvl[lvlNum][2],lvl[lvlNum][3])
        keyGroup = function.key(screen,lvl[lvlNum][5])
        platform = function.Platform(lvl[lvlNum][6],(30,70))
        clock = pygame.time.Clock()
        init,game = False,True

    while game:
        kpd = pygame.key.get_pressed()
        timer = pygame.time.get_ticks()
        clock.tick(100)
        font = pygame.font.Font(None,60)
        life = font.render("Lives: " + str(health),1,(0,0,0))

        for ev in pygame.event.get():
            if kpd[K_ESCAPE]:
                quitted = True
                game = False

        player.handleKeys(1)
        for wall in wallGroup.sprites():
            if player.rect.colliderect(wall.rect) == True:
                player.checkColl(player.rect,wall.rect,-1)

        pygame.sprite.spritecollide(player,keyGroup,True)
        doorOpen = False
        if player.rect.colliderect(door.rect) == True:
            player.checkColl(player.rect,door.rect,-1)

        if platform.rect.colliderect(player.rect) == True:
            game = False

        screen.fill((255,255,255))
        player.draw(screen)
        keyGroup.draw(screen)
        wallGroup.draw(screen)
        if lvl[lvlNum][7] != None:
            enemyGroup.update(screen) #moving of the enemy
            enemyGroup.draw(screen)
            for enemy in enemyGroup:
                if player.rect.colliderect(enemy) == True: #check enemy collision with player
                    player.checkDead(lvl[lvlNum][0])
                    health -= 1
                for wall in wallGroup.sprites():
                    if enemy.rect.colliderect(wall)== True: #check enemy collision with wall
                        enemy.checkCollision()

        if lvl[lvlNum][8] != None:
            #make the trap group
            if (timer//1000)%4==0:
                for trap in trapGroup.sprites():
                    trap.draw(screen)
                    if player.rect.colliderect(trap) == True:
                        player.checkDead(lvl[lvlNum][0])
                        health-=1

        if lvl[lvlNum][9] != None:
            #make the fake group
            for fakeWall in fakeWallGroup.sprites():
                fakeWall.draw(screen)
                if player.rect.colliderect(fakeWall) == True:
                    player.checkDead(lvl[lvlNum][0])
                    health-=1


        if len(keyGroup) == 0:
            #open the door
            door.open(lvl[lvlNum][2],lvl[lvlNum][4])

        door.draw(screen)
        platform.draw(screen)
        screen.blit(life,(10,10))
        pygame.display.update()
        if health == 0:
            game = False
            quitted == True

    if lvlNum == len(lvl) or quitted == True:
        quitted = True
        while quitted:
            kpd = pygame.key.get_pressed()
            quitted,menuOn = function.menuText(endImage,quitted,menuOn,kpd,screen)
            theMsg = winMsg
            if lvlNum != len(lvl):
                theMsg = loseMsg
            for x in range(len(theMsg)):
                msg = font.render(theMsg[x],1,(0,0,0))
                rect = msg.get_rect(center=(640,175+75*x))
                screen.blit(msg,(rect.x,rect.y))
            pygame.display.update()
            mRedraw = 0

    if menuOn == False:# next level
        lvlNum += 1
        init = True
pygame.quit()
