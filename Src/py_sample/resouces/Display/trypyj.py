# -*- coding:utf-8 -*-
import pygame
from pygame.locals import*
import sys

(w,h)=(640,480)
rect=Rect(0,0,w,h)
(TATE,YOKO)=(15,20)	#マップサイズ
GS=32	#一ますのサイズ

map=[	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]

def image(filename):
    image=pygame.image.load(filename).convert_alpha()
    return image

def split(image):
    imageList=[]
    for i in range(0,96,GS):	#GSは32
        surface=pygame.Surface((GS,GS))
        surface.blit(image,(0,0),(i,0,GS,GS))
        surface.set_colorkey(000000)
        surface.convert_alpha()
        imageList.append(surface)
    return imageList

def draw_map(screen):
    for i in range(TATE):	#縦回繰り返す
        for ix in range(YOKO):
            if map[i][ix]==0:
                screen.blit(MapImg,(ix*GS,i*GS))

pygame.init()
screen=pygame.display.set_mode((w,h))
pygame.display.set_caption("マップを作成")
 
MapImg=image("d.png")
ImgList=split(image("c.png"))

(x,y)=(0,0)
anime=24
frame=0

clock=pygame.time.Clock()

while(1): 
    clock.tick(60)

    frame+=1
    Img=ImgList[frame//anime%3]

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_LEFT]:
        x-=1
    if pressed_keys[K_RIGHT]:
        x+=1
    if pressed_keys[K_UP]:
        y-=1
    if pressed_keys[K_DOWN]:
        y+=1
    if y < 0:
        y = 0
    if x < 0:
        x = 0
    if x >= YOKO:
        x = YOKO - 1
    if y >= TATE:
        y = TATE - 1

    Img_rect=(x*GS,y*GS,GS,GS)

    draw_map(screen)
    screen.blit(Img,Img_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==QUIT:
            sys.exit()