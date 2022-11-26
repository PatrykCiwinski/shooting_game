import time

import pygame
import math


pygame.init()
fps = 60
timer=pygame.time.Clock()
font= pygame.font.Font("assets/font/myFont.ttf", 32)
WIDTH=900
HEIGHT=800
screen=pygame.display.set_mode([WIDTH, HEIGHT])
#backgrounds on each level
bgs=[]
#banners on each level
banners=[]
#guns on each level
guns=[]
target_images=[[],[],[]]
targets={1:[10, 5, 3],
         2:[12,8, 5],
         3:[15, 12, 8, 3]}
level=1
points=0
shoot=False
total_shoots=0
mode=0
ammo=0
for i in range(1,4):
    bgs.append(pygame.image.load(f'assets/bgs/{i}.png'))
    banners.append(pygame.image.load(f'assets/banners/{i}.png'))
    guns.append(pygame.transform.scale(pygame.image.load(f'assets/guns/{i}.png'), (100,100)))
    if i <3:
        for j in range(1,4):
            target_images[i-1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120-(j*18), 80 - (j*12))))
    else:
        for j in range (1,5):
            target_images[i-1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120-(j*18), 80 - (j*12))))
def draw_gun():
    mouse_pos=pygame.mouse.get_pos()
    gun_point=(WIDTH/2, HEIGHT-200)
    lasers=['red', 'purple', 'green']
    clicks=pygame.mouse.get_pressed()
    if mouse_pos[0] != gun_point[0]:
        slope =(mouse_pos[1]-gun_point[1])/(mouse_pos[0]-gun_point[0])
    else:
        slope=-100000
    angle=math.atan(slope)
    rotation=math.degrees(angle)
    if mouse_pos[0]<WIDTH/2:
        gun =pygame.transform.flip(guns[level -1], True, False)
        if mouse_pos[1]<600:
            screen.blit(pygame.transform.rotate(gun, 90 - rotation), (WIDTH/2-90, HEIGHT-250))
            if clicks[0]:
                pygame.draw.circle(screen, lasers[level-1], mouse_pos, 5)
    else:
        gun=guns[level-1]
        if mouse_pos[1]<600:
            screen.blit(pygame.transform.rotate(gun, 270 -rotation), (WIDTH/2-30,HEIGHT-250))


def draw_level(coords):
    if level==1 or level==2:
        target_rects=[[],[],[]]
    else:
        target_rects=[[],[],[],[]]

    for i in range (len(coords)):
        for j in range (len(coords[i])):
            target_rects[i].append(pygame.rect.Rect((coords[i][j][0] +30, coords[i][j][1]),
                                   (60 - i*12, 60 - i*12)))
            screen.blit(target_images[level-1][i], coords[i][j])
    return target_rects
#initialize enemy coords
one_coords=[[],[],[]]
two_coords=[[],[],[]]
three_coords=[[],[],[],[]]

for i in range(3):
    my_list=targets[1]
    for j in range(my_list[i]):
        one_coords[i].append((WIDTH//(my_list[i])*j, 300 - (i*150)+ 30*(j%2)))


for i in range(3):
    my_list=targets[2]
    for j in range(my_list[i]):
        two_coords[i].append((WIDTH//(my_list[i])*j, 300 - (i*150)+ 30*(j%2)))

for i in range(4):
    my_list=targets[3]
    for j in range(my_list[i]):
        three_coords[i].append((WIDTH//(my_list[i])*j, 300 - (i*100)+ 30*(j%2)))


run = True


def move_level(coords):
    if level ==1 or level ==2:
        max_val=3
    else:
        max_val=4
    for i in range(max_val):
        for j in range(len(coords[i])):
            my_coords=coords[i][j]
            if my_coords[0]<-150:
                coords[i][j]=(WIDTH, my_coords[1])
            else:
                coords[i][j]=(my_coords[0]-2**i, my_coords[1])
    return coords

def check_shoot(targets, coords):
    global points
    mouse_pos=pygame.mouse.get_pos()
    for i in range(len(targets)):
        for j in range(len(targets[i])):
            if targets[i][j].collidepoint(mouse_pos):
                coords[i].pop(j)
                points+=10+10*(i**2)
    return coords


def draw_score():
    points_text=font.render(f'Point: {points}', True, 'black')
    screen.blit(points_text, (320,660))


while run:
    timer.tick(fps)

    screen.fill("black")
    screen.blit(bgs[level-1], (0,0))
    screen.blit(banners[level-1], (0, HEIGHT-200))
    if level ==1:
        target_boxes=draw_level(one_coords)
        one_coords=move_level(one_coords)
        if shoot:
            one_coords = check_shoot(target_boxes,one_coords)
            shoot=False
    elif level == 2:
        target_boxes=draw_level(two_coords)
        two_coords=move_level(two_coords)
        if shoot:
            two_coords=check_shoot(target_boxes,two_coords)
            shoot=False
    elif level == 3:
        target_boxes=draw_level(three_coords)
        three_coords=move_level(three_coords)
        if shoot:
            three_coords=check_shoot(target_boxes,three_coords)
            shoot=False
    if level>0:
        draw_gun()
        draw_score()

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            move_position=pygame.mouse.get_pos()
            if (0<move_position[0]<WIDTH) and (0<move_position[1],HEIGHT-200):
                shoot=True
                total_shoots+=1
                if mode==1:
                    ammo-=1
    if level>0:
        if target_boxes ==[[],[],[]] and level<3:
            level+=1


    pygame.display.flip()
pygame.quit()