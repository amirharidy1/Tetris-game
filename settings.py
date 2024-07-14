import pygame 
from copy import deepcopy
from random import choice , randrange 
FPS=60
TILE_SIZE=50
FIELD_W=10
FIELD_H=20
FIELD_RES = FIELD_W *TILE_SIZE,FIELD_H *TILE_SIZE 
RES=750,950

pygame.init()
sc=pygame.display.set_mode(RES)
game_sc=pygame.display.set_mode(FIELD_RES)
clock=pygame.time.Clock()
grid=[pygame.rect(x * TILE_SIZE, y *TILE_SIZE,TILE_SIZE,TILE_SIZE)for x in range (FIELD_W) for y in range(FIELD_H) ]

TETROMINOES={
    'T':[(0,0),(-1,0),(1,0),(0,-1)],
    'O':[(0,0),(0,-1),(1,0),(1,-1)],
    'J':[(0,0),(-1,0),(0,-1),(0,-2)],
    'L':[(0,0),(1,0),(0,-1),(0,-2)],
    'I':[(0,0),(0,1),(0,-1),(0,-2)],
    'S':[(0,0),(-1,0),(0,-1),(1,-1)],
    'Z':[(0,0),(1,0),(0,-1),(-1,-1)]

}
bg=pygame.image.load('photo.jpg').convert()
bg_game=pygame.image.load('photo2.jpg').convert()

figures=[[pygame.Rect(x+FIELD_W//2,y+1,1,1,1)for x,y in fig_pos]for fig_pos in TETROMINOES]
figure_rect=pygame.Rect(0,0,TILE_SIZE-2,TILE_SIZE-2)
field= [[0 for i in range(FIELD_W) ]for j in range(FIELD_H)]
figure,next_figure=deepcopy(choice(figures)),deepcopy(choice(figures))
anim_count,anim_speed,anim_limit=0,60,2000
score,lines=0,0
scores={0:0,1:100,2:300,3:700,4:1000}

main_font=pygame.font.Font('font/font.ttf',65)
font=pygame.font.Font('font/font.ttf',45)  

title_tetris=main_font.render('tetris',True,pygame.Color('yellow'))
title_score=main_font.render('score',True,pygame.Color('blue'))
title_record=main_font.render('record',True,pygame.Color('orange'))

def check_boarder():
     if figure[i].x <0 or figure[i].x>FIELD_W-1:
          return False
     elif figure[i].y >FIELD_H - 1 or field[figure[i].y][figure[i].x]:
          return False
     return True

def set_record(record,score):
    rec=max(int(record),score)
    with open('record','w') as f:
        f.write (str(rec)) 
    
def get_record():
    try:
      with open ('record') as f:  
          return f.readline()  
    except FileNotFoundError:
     with open ('record','w') as f: 
           f.write ('0')

while True:
    record=get_record()
    dx=0
    sc.blit(bg,(0,0))
    sc.blit(bg_game,(20,20))
    game_sc.blit(bg_game,(0,0))
    for i in range(lines):
        pygame.time.wait(200)
       
    for event in pygame.event.get():
      if event.type == pygame.QUIT or(event.type ==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()
      if event.type==pygame.KEYDOWN:
         if event.key==pygame.K_LEFT:
              dx=-1
         if event.key==pygame.K_RIGHT:
              dx=1   
         if event.key==pygame.K_DOWN:
              anim_limit=100        

    figure_old=deepcopy(figure)             
    for i in range(4): 
         figure[i].x += dx
         if not check_boarder():
              figure=deepcopy(figure_old)
              break
    anim_count+=anim_speed
    if anim_count>anim_limit:
         anim_count=0
         figure_old=deepcopy(figure) 
         for i in range(4): 
           figure[i].y += 1
           if not check_boarder():
              for i in range(4): 
                   field[figure_old[i].y][figure_old[i].x]=pygame.Color('white'),
              figure=next_figure
              next_figure=deepcopy(choice(figures))
              anim_limit=2000
              break

     line , lines = FIELD_H - 1 , 0
    for row in range(FIELD_H-1,-1,-1):
     count=0
     for i in range (FIELD_W):
          if field[row][i]:
               count+=1
               field[line][i]=field[row][i]
               if count<FIELD_W:
                    line-=1
               else:
                   anim_speed+=3
                   lines+=1     
     score+=scores[lines]
     


    [pygame.draw.rect(game_sc,(40,40,40),i_rect,1) for i_rect in grid]      

    for i in range(4):
         figure_rect.x=figure[i].x*TILE_SIZE
         figure_rect.y=figure[i].y*TILE_SIZE
         pygame.draw.rect(game_sc,pygame.color('white'),figure_rect)

     for i in range(4):
         figure_rect.x = next_figure[i].x*TILE_SIZE+380
         figure_rect.y = next_figure[i].y*TILE_SIZE+185
         pygame.draw.rect(game_sc,pygame.color('white'),figure_rect)



     for y,raw in enumerate (field):
          for x , col in enumerate (raw):
               if col:
                    figure_rect.x,figure_rect.y=x*TILE_SIZE,y*TILE_SIZE
                    pygame.draw.rect(game_sc,col,figure_rect)
    

     sc.blit(title_tetris,(485,-10))
     sc.blit(title_score,(535,780))
     sc.blit(font.render(str(score),True,pygame.Color('green')),(580,840))
     sc.blit(title_record,(525,650))
     sc.blit(font.render(record,True,pygame.Color('gold')),(550,710))
    
    for i in range(FIELD_W):
     if field[0][i]:
      set_record(record,score)
      field[[0 for i in range(FIELD_W)]for i in range(FIELD_H)]
      anim_count,anim_speed,anim_limit=0,60,2000
      score=0
      for i_rect in grid:
          pygame.draw.rect(game_sc,get_color(),i_rect)
          sc.blit(game_sc,(20,20))
          pygame.display.flip()
          clock.tick(FPS)



     