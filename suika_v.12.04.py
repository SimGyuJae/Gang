import pygame
import math
import random
from os import path
clock = pygame.time.Clock()
FPS = 60
img_dir = path.join(path.dirname(__file__), 'suika_img')
snd_dir = path.join(path.dirname(__file__), 'suika_snd')
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("20221052심규재")
screen_width = 600
screen_height = 800

skwed_probabitity = [0.7, 0.15, 0.05, 0.07, 0.02, 0.01, 0, 0]
screen = pygame.display.set_mode((screen_width, screen_height))
# define scores of each ball
score = 0
score_order = [0, 2, 4, 8, 16, 32, 64, 128]
# define ball speed and redius
radius_order = [65, 80, 95, 110, 125, 140, 200,300]
gravity = 0.05
white = (255,255,255)
black = (0,0,0)

balls1 = []
balls2 = []
balls3 = []
balls4 = []
balls5 = []
balls6 = []
balls7 = []
balls8 = []

balls = [balls1, balls2, balls3, balls4, balls5, balls6, balls7, balls8]

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("20221052심규재")
running = True
gaem_over = False
next_index = 0
index = range(len(radius_order))
random_int = random.choices(index, weights=skwed_probabitity, k=1)[0]

gang_images = []
gang_list = ['1.png','2.png','3.png','4.png','5.png','6.png','7.png','8.png'] 
for img in gang_list:
    gang_images.append(pygame.image.load(path.join(img_dir, img)).convert())

def checkcirclecollide(x1, y1, r1, x2, y2, r2):
    distX = x1 - x2
    distY = y1 - y2
    distance = math.sqrt( (distX * distX) + (distY * distY) )
    return (distance <= (r1 + r2))

def ballcollision(m1, m2, v1, v2):
    v2f = (2*m1*v1 + m2*v2 - m1*v2) / (m1+m2)
    v1f = (m1*v1 + m2*v2 - m2*v2f)/m1
    return v1f, v2f

def separate_balls(ball, other):
    # Get the Opposite direction
    angle = - math.atan2(ball.y - other.y, ball.x - other.x)

    # Calculate distance between both balls
    distX = ball.x - other.x
    distY = ball.y - other.y
    distance = math.sqrt( (distX * distX) + (distY * distY) )
    diffR = ball.radius / 2 + other.radius / 2 - distance# 두 거리의 차

    #diffR *= 1# 0.5 이걸 비율로 줘야 함

    # Separate each ball by half of distance
    ball.x += math.cos(angle) * diffR * (ball.radius / 2) / (ball.radius / 2 + other.radius / 2)
    ball.y += math.sin(angle) * diffR * (ball.radius / 2) / (ball.radius / 2 + other.radius / 2)

    other.x += math.cos(angle) * diffR * (other.radius / 2) / (ball.radius / 2 + other.radius / 2)
    other.y += math.sin(angle) * diffR * (other.radius / 2) / (ball.radius / 2 + other.radius / 2)
    # ball.x += math.cos(angle) * diffR * (other.radius / 2) / (ball.radius / 2 + other.radius / 2)
    # ball.y += math.sin(angle) * diffR * (other.radius / 2) / (ball.radius / 2 + other.radius / 2)

    # other.x -= math.cos(angle) * diffR * (ball.radius / 2) / (ball.radius / 2 + other.radius / 2)
    # other.y -= math.sin(angle) * diffR * (ball.radius / 2) / (ball.radius / 2 + other.radius / 2)

class Gang(pygame.sprite.Sprite):
    def __init__(self, i, x, y, vy):
        pygame.sprite.Sprite.__init__(self)
        self.order = i                      #인덱스 받기
        self.image_orig = gang_images[self.order] #이미지 리스트 인덱스 접근
        self.image_orig = pygame.transform.scale(self.image_orig, (radius_order[self.order],radius_order[self.order]))
        self.image_orig.set_colorkey(black)#black
        self.image = self.image_orig.copy()
        
        self.radius = radius_order[self.order]  #반지름 리스트 인덱스 접근
        self.x = x                              #생성시 x좌표는 마우스 좌표 또는 합성위치 를 따름
        self.y = y                              #생성시 y좌표는 기준선 위로 고정됨 또는 합성위치 를 따름
        self.vx = 0
        
        self.rect = self.image.get_rect()
        self.m = radius_order[self.order]   #아마도 질량???? 일단 추가해 봄
        self.vy = vy                        #낙하시 1정도

        

    def update(self):
        # box_top = 40

            # if ball is not dropping and above the box, game over
        # if (not ball[6]) and ball[1] - self.radius < box_top:
        #     gaem_over = True
        screen.blit(self.image_orig,(self.x,self.y))
        self.vy += gravity
        box_bottom = 720 - self.radius
        box_left = 40 + self.radius
        box_right = 560 - self.radius
        if self.y >= box_bottom:#?????
            self.y = box_bottom
            self.vy = 0 # 추가
        elif self.y < box_bottom:
            self.y += self.vy
            
        if self.x < box_left:
            self.x = box_left + 1
            self.vx *= -0.5
        elif self.x > box_right:
            self.x = box_right - 1
            self.vx *= -0.5
        self.x += self.vx

    def change_attribute(self, x=None, y=None, vx=None, vy=None, radius=None, m=None):
        if x!=None: self.x = x
        if y!=None: self.y = y
        if vx!=None: self.vx = vx
        if vy!=None: self.vy = vy
        if radius!=None: self.radius = radius
        if m!=None: self.m = m

while running:
    screen.fill(black)# 초기화
    screen.blit(screen, (screen_width,screen_height))
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > 40 and event.pos[0]<560:# draw a ball when mouse is clicked
                next_index = random.choices(index, weights=skwed_probabitity, k=1)[0]
                g = Gang(next_index,event.pos[0], 40, 1)#낙하속도 1
                balls[next_index].append(g)#인덱스 크기별 그룹화
                g.update()
        
        
        #다음에 올 것 보이게 하기
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX > 40 and mouseX<560:    
            nextBallImg = gang_images[next_index]
            nextBallImg = pygame.transform.scale(nextBallImg, (radius_order[next_index],radius_order[next_index]))
            screen.blit(nextBallImg,(mouseX,40))
            
            
    if not gaem_over:
        
        for i in range(0,8):#i = 0 1 2 3 4 5 6 7 (8가지)
            
            if len(balls[i]) == 0:#리스트 내부가 비어있으면 넘김
                    continue
            initalLen = len(balls[i])#동일 크기의 리스트의 원소가 줄어 들었을때 감지용
            for j in range(0,len(balls[i])):#최소 한개의 원소는 있는 경우
                #print("debug:[",i,"]:",len(balls[i]),"\n")
                #print("initalLen:[",initalLen,"]\n")
                
                if len(balls[i]) != initalLen:#충돌로 현재 리스트의 크기에 변화가 생겼을 경우
                    #print("---------------balls[i]) != initalLen-----------------")
                    break
                #balls[i][j].update() 일단 빼 봤음


                for k in range(j+1, len(balls[i])):#같은 크기의 공이 두개 이상일때만
                    if checkcirclecollide(balls[i][j].x,balls[i][j].y,balls[i][j].radius / 2,balls[i][k].x,balls[i][k].y,balls[i][k].radius / 2):
                        #print("collide x1: ", balls[i][j].x," y1: ",balls[i][j].y, " x2:",balls[i][k].x," y2:",balls[i][k].y)
                        #print("radius:", balls[i][j].radius, "radius:", balls[i][k].radius, "\n")                    
                        newball = Gang(i+1, ((balls[i][j].x + balls[i][k].x) / 2), ((balls[i][j].y + balls[i][k].y) / 2),(balls[i][j].vy + balls[i][k].vy)/2)
                        balls[i+1].append(newball)
                        balls[i].remove(balls[i][k])
                        balls[i].remove(balls[i][j])
                        newball.update()
                        break#두개나 리스트에서 지웠기때문에 인덱스에 변동이 있을 수 있다
        
        ballball = []
        for i in range(0,8):
            for j in range(0,len(balls[i])):
                balls[i][j].update()#추가
                ballball.append(balls[i][j])

        #ballball set에 대하여
        for i in range (0,len(ballball)-1): 
            for j in range (i+1, len(ballball)):
                if checkcirclecollide(ballball[i].x, ballball[i].y, ballball[i].radius / 2, ballball[j].x, ballball[j].y, ballball[j].radius / 2):
                    # if ballball[i].y < ballball[j].y:# i 기준 1사분면
                    #     if ballball[i].x < ballball[j].x:
                    #         distX = ballball[i].x - ballball[j].x
                    #         distY = ballball[i].y - ballball[j].y
                    #         distance = math.sqrt( (distX * distX) + (distY * distY) )
                    #         diffR = ballball[i].radius / 2 + ballball[j].radius / 2 - distance# 두 거리의 차
                    #         sin = distY / diffR
                    #         cos = distX / diffR
                    #         ballball[i].x = ballball[i].x * 
                    #         balls[i][j].update()
                        


                    new_v1x, new_v2x = ballcollision(ballball[i].m, ballball[j].m, ballball[i].vx, ballball[j].vx)
                    new_v1y, new_v2y = ballcollision(ballball[i].m, ballball[j].m, ballball[i].vy, ballball[j].vy)

                    # Save current position
                    originalX = ballball[i].x
                    originalY = ballball[i].y

                    # Calculate a hint of next position
                    lookAheadX = ballball[i].x + ballball[i].vx
                    lookAheadY = ballball[i].y + ballball[i].vy

                    # Push hint position
                    ballball[i].change_attribute(x = lookAheadX, y = lookAheadY)

                    # Separate both balls from each other
                    separate_balls(ballball[i], ballball[j])

                    # Pop hint position to original one
                    ballball[i].change_attribute(x = originalX, y = originalY)

                    ballball[i].change_attribute(vx = new_v1x, vy = new_v1y)
                    ballball[j].change_attribute(vx = new_v2x, vy = new_v2y)
        
                ballball[i].change_attribute(x = ballball[i].x+ballball[i].vx, y = ballball[i].y+ballball[i].vy)

                    
            
        # draw 3 lines to make a rectangle with upper side open
        pygame.draw.line(screen, white, (40, 40), (40, 720), 1)
        pygame.draw.line(screen, white, (40, 720), (560, 720), 1)
        pygame.draw.line(screen, white, (560, 720), (560, 40), 1)
        # draw a warning line at top of box with red dotted line
        dotted_line_y = 40
        dotted_line_length = 4
        dotted_line_space = 4
        # grey color dotted line
        dotted_line_color = (128,128,128)
        for x in range(40, 560, dotted_line_length + dotted_line_space):
            pygame.draw.line(screen, dotted_line_color, (x, dotted_line_y), (x + dotted_line_length, dotted_line_y), 1)
        
        
        # draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, white)
        screen.blit(score_text, (screen_width /2 - score_text.get_width()/2, 20))
        #pygame.display.update() 이건 잘 모르겠음

    if gaem_over:
        font = pygame.font.Font(None, 36)
        game_over_text_lines = [
            "GAME OVER",
            f"Your Score is: {score}",
            "restart by pressing SPACE",
            "quit game by pressing ESCAPE"
        ]
        for i, line in enumerate(game_over_text_lines):
            line_text = font.render(line, True, white)
            screen.blit(line_text, (screen_width / 2 - line_text.get_width() / 2, screen_height / 2 - line_text.get_height() / 2 + i * line_text.get_height()))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # reset gaem when space is pressed
                    balls.clear()
                    score = 0
                    gaem_over = False
                elif event.key == pygame.K_ESCAPE:
                    # quit game when esc is pressed
                    running = False
    
    pygame.display.flip() # 이건 지우면 아무것도 안나옴
    clock.tick(FPS)
pygame.quit()