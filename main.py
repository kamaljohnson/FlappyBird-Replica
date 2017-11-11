#all the import funtions are here

import pygame
from pygame.locals import *
import menu
import random
import pickle
import time

Time = time.clock()
#initialisations are done here
pygame.init()
pygame.mixer.init()

music = pygame.mixer.Sound("sound5.wav")
FPS = 30
clock = pygame.time.Clock()

#basic colors are initialised here
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screenx,screeny = (700,504)
screen = pygame.display.set_mode((screenx,screeny))
pygame.display.set_caption("Flappy Bird")
screen.fill(BLACK)
menu = menu.Menu(screen,GREEN)

#all the lists for the menus in the game
while True:
    main_menu = ["START","HIGH SCORE","EXIT",]
    running = True

    select = menu.menu_UI(main_menu)
    bird_x_position = int(screenx*(1/4))
    bird_y_position = 10
    bird = pygame.image.load("bird 1.png").convert_alpha()
    layer1 = pygame.image.load("game_layer_1.jpg").convert()
    layer12 = pygame.image.load("game_layer_2.jpg").convert()
    pip_up = pygame.image.load("up pipe.png").convert()
    pip_down = pygame.image.load("down pipe.png").convert()

    points = 0
    pip_list = []
    life = 5
    music_time = time.clock()

    if select == 1:
        file_name = "highscore.pkl"
        file_object = open(file_name,'rb')
        high_score = pickle.load(file_object)
        file_object.close()
        myfont = pygame.font.SysFont("arial", 50)
        label = myfont.render("HIGH SCORE : " + str(high_score), 2, BLACK)
        screen.fill(GREEN)
        screen.blit(label, (screenx // 2 - 200, screeny // 2))
        pygame.display.update()
        pygame.time.delay(2000)


    if select == 0:
        screen.fill(GREEN)
        #the main loop for the game
        up = False
        up_time = 0
        parabolic_time = 20
        pause = False
        start = 0
        game_duration = 1
        flag = 0
        x = .5
        music.play()
        Time = Time - time.clock()
        animation_time = 0
        t = 0
        y = bird_y_position
        justAnotherKey = True
        while running == True:
            animation_time+=1
            if (animation_time<=60 and int(animation_time)%20 == 0)or ((t-1 <= 3) and t-1>0):
                myfont = pygame.font.SysFont("arial", 200)
                t = 4 - animation_time // 20
                label1 = myfont.render(str(t), 2, WHITE)
                screen.blit(label1, (screenx // 2 - 50, screeny // 2 - 130))
            if start == 0 and animation_time>=70:
                bird_y_position = y
                myfont = pygame.font.SysFont("arial",40)
                label1 = myfont.render("click space ",2,WHITE)
                label2 = myfont.render("to start ", 2, WHITE)
                screen.blit(label1,(screenx//2-80,screeny//2-50))
                screen.blit(label2,(screenx//2-50,screeny//2))
            pygame.display.update()
            if ((time.clock() - music_time)>=198):
                Time = time.clock()
                music.stop()
                music.play()
                music_time = time.clock()

            if game_duration%37 == 0:
                if flag == 1 and start != 0:
                    points+=1
                if start == 1:
                    pip_list.append([random.randrange(-20,200),700])
            if start == 1:
                for i in range(len(pip_list)):
                    pip_list[i][1] -= 10
            if len(pip_list) == 2:
                flag = 1
            game_duration += 1
            clock.tick(FPS)
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    start = 1
                    if event.key == K_SPACE:
                        up = True
                        up_time = 0
                        justAnotherKey = False
                    elif event.key == K_ESCAPE:
                        pause = True
                        justAnotherKey = False
                    else:
                        up = False
                        justAnotherKey = True

            #logic
            if animation_time <60:
                start = 0
            if (up == True and start == 1)and animation_time>=20 and t<2:
                x = 1
                if up_time <= parabolic_time:
                    bird_y_position -= (parabolic_time - up_time)
                    up_time+=3
            if (up == False and start == 1) and (animation_time >60):
                x += .1
                up_time += 2*x
                bird_y_position += (parabolic_time + up_time)
            if start == 0 and justAnotherKey == True:
                bird_y_position = screeny//2 -200
            if up_time>=parabolic_time and up == True:
                up = False
                up_time = 0
            if bird_y_position<=-45:
                bird_y_position = -45
            if bird_y_position >= 370:
                bird_y_position = 370
                running = False
            #rendering
            screen.blit(layer1,(-21,0))
            screen.blit(bird,(bird_x_position,bird_y_position))
            myfont = pygame.font.SysFont("arial",50)
            if points%10 == 0 and points !=0:
                label = myfont.render(str(points),2,RED)
            else:
                label = myfont.render(str(points),2,BLACK)
            screen.blit(label,(62,70))
            if animation_time <= 50:
                label1 = myfont.render("x "+str(life), 2, BLACK)
                screen.blit(label1, (340, 70))

            k = 0
            for i in range(len(pip_list)-1,0,-1):
                if bird_y_position >= pip_list[i][0] + 170 and (bird_x_position >= pip_list[i][1]-120 and (bird_x_position <= pip_list[i][1])):
                    running = False
                    break
                if bird_y_position <= pip_list[i][0] - 25 and (bird_x_position >= pip_list[i][1]-120  and (bird_x_position <= pip_list[i][1])):
                    running = False
                    break
                screen.blit(pip_down,(pip_list[i][1],pip_list[i][0]-280))
                screen.blit(pip_up,(pip_list[i][1],pip_list[i][0]+280))
                k+=1
                if k == 4:
                    break

            pygame.display.update()

            #updating
            if (pause == True):
                select = menu.menu_UI(["NEW GAME","CONTINUE","HIGH SCORE","EXIT"])
                if select == 0:
                    life = 5
                    points = 0
                    start = 1
                if select == 3:
                    break
                if select == 2:
                    file_name = "highscore.pkl"
                    file_object = open(file_name,'rb')
                    high_score = pickle.load(file_object)
                    file_object.close()
                    myfont = pygame.font.SysFont("arial",50)
                    label = myfont.render("HIGH SCORE : "+str(high_score),2,BLACK)
                    screen.fill(GREEN)
                    screen.blit(label,(screenx//2-200,screeny//2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                Time = time.clock()
                y = bird_y_position
                pause = False
                start = 0
            if running == False:
                running = True
                bird_y_position = 10
                start = 0
                life -= 1
                animation_time = 0
                if life == 0:
                    screen.blit((layer12),(-20,0))
                    myfont = pygame.font.SysFont("arial", 40)
                    label = myfont.render("GAME OVER ", 2, WHITE)
                    label2 = myfont.render("SCORE : " + str(points), 2, WHITE)
                    screen.blit(label2, (screenx // 2 - 120, screeny // 2 - 15))
                    screen.blit(label, (screenx // 2 - 140, screeny // 2 - 50))
                    pygame.display.update()
                    time.sleep(2)
                    life = 5
                    file_name = "highscore.pkl"
                    file_object = open(file_name,'rb')
                    high_score = pickle.load(file_object)
                    file_object.close()
                    file_object1 = open(file_name, "wb")
                    if high_score <= points:
                        high_score = points
                    pickle.dump(high_score,file_object1)
                    file_object1.close()
                    points = 0
                pip_list = []
                flag = 0
    if select == 3:
        break