import pygame
import math
import random
from os import path
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("20221052심규재")
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.2)
running = True
game_over = False
is_Jongang = False

# '종강 만들기!'v.23.12.08 (original: Suika Game <https://suikagame.com/>)

# "모두의 간절한 염원을 담아, 종강을 만들어 봅시다!"" made by 20221052 심규재, special thanks to AndyCheung0211<https://medium.com/@andy456333/make-your-own-suica-game-watermelon-game-using-pygame-1441de42f573 >

# <규칙> 
# 1.같은 크기의 '강' 들은 합쳐집니다.
# 2.'강'이 천장에 닿으면 게임이 종료됩니다.
# 3.개강->녹강(녹화강의)->수강->건강(bad)->건강(good)->서강->송강->종강 의 단계로 합쳐지고 커집니다.

##################################################################################

#중력
gravity = 0.05

#색상
white = (255,255,255)
black = (0,0,0)

#에셋 디렉토리
img_dir = path.join(path.dirname(__file__), 'suika_img')
snd_dir = path.join(path.dirname(__file__), 'suika_snd')

#스크린 사이즈
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

##################################################################################

#'강' 사이즈 별 분류 리스트
balls1 = []
balls2 = []
balls3 = []
balls4 = []
balls5 = []
balls6 = []
balls7 = []
balls8 = []
balls = [balls1, balls2, balls3, balls4, balls5, balls6, balls7, balls8]

#'강' 들의 등장 확률
skwed_probabitity = [0, 0, 0, 0, 0, 0, 1, 0] #[0.7, 0.2, 0.06, 0.03, 0.01, 0, 0, 0]
next_index = 0
index = range(len(balls))
random_int = random.choices(index, weights=skwed_probabitity, k=1)[0]

#'강' 별 점수
score = 0
score_order = [0, 2, 4, 8, 16, 32, 64, 128]

#'강' 지름
radius_order = [80, 95, 110, 125, 140, 200, 300, 500]

#'강' 사이즈 별 합쳐질때 소리 효과
gang_sounds = []
for snd in ['2.mp3','3.mp3','4.mp3','5.mp3','6.mp3','7.mp3','8.mp3']:
    gang_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
#'강' 사이즈 별 이미지
gang_images = []
gang_list = ['1.png','2.png','3.png','4.png','5.png','6.png','7.png','8.png'] 
for img in gang_list:
    gang_images.append(pygame.image.load(path.join(img_dir, img)).convert())

##################################################################################

#'강' 끼리 충돌 감지
def checkcirclecollide(x1, y1, r1, x2, y2, r2):
    distX = x1 - x2
    distY = y1 - y2
    distance = math.sqrt( (distX * distX) + (distY * distY) )
    return (distance <= (r1 + r2))

#'강' 스프라이트 형 클래스
class Gang(pygame.sprite.Sprite):
    def __init__(self, i, x, y, is_dropping):
        pygame.sprite.Sprite.__init__(self)
        self.order = i                          #사이즈 순서 인덱스 받아서 저장
        self.image_orig = gang_images[self.order]#이미지 리스트 인덱스 접근
        self.image_orig = pygame.transform.scale(self.image_orig, (radius_order[self.order],radius_order[self.order]))#크기만큼 리사이즈
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.radius = radius_order[self.order]  #지름 리스트 인덱스 접근
        self.x = x                              #생성시 x좌표는 마우스 좌표 또는 합성위치 를 따름
        self.y = y                              #생성시 y좌표는 기준선 위로 고정됨 또는 합성위치 를 따름
        self.vx = 0
        self.rect = self.image.get_rect()        
        self.is_dropping = is_dropping                        
        if self.is_dropping == True:#낙하시 1정도의 속도
            self.vy = 1
        else:
            self.vy = 0

##################################################################################
next_index = 0  #초기 생성 '강'
while running:
    screen.fill(black)# 초기화, 잔상제거
    screen.blit(screen, (screen_width,screen_height))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:          #마우스 클릭으로 새로운 '강' 투하
            if event.pos[0] > 40 and event.pos[0]<560:      #마우스가 해당 범위 안에 있을때만
                g = Gang(next_index,event.pos[0], 40, True) #낙하속도 1로 낙하
                balls[next_index].append(g)                 #인덱스 크기별 그룹화
                score += score_order[next_index]            #점수 계산
                next_index = random.choices(index, weights=skwed_probabitity, k=1)[0]#생성 이후 다음에 내려올 새 랜덤 인덱스 생성
        
        #다음에 올 것 보이게 하기
        mouseX, mouseY = pygame.mouse.get_pos()
        if (mouseX > 40 and mouseX<560) and not game_over:    
            nextBallImg = gang_images[next_index]
            nextBallImg = pygame.transform.scale(nextBallImg, (radius_order[next_index],radius_order[next_index]))
            screen.blit(nextBallImg,(mouseX - radius_order[next_index] / 2, 40))
            
    if not game_over and not is_Jongang:
        for i in range(0,8):#i = 0 1 2 3 4 5 6 7 (8가지)
            if len(balls[i]) == 0:#리스트 내부가 비어있으면 넘김
                    continue
            initalLen = len(balls[i])#동일 크기의 리스트의 원소가 줄어 들었을때 감지

            #최소 한개의 원소는 있는 경우 
            for j in range(0,len(balls[i])):       
                if len(balls[i]) != initalLen:#충돌로 현재 리스트의 크기에 변화가 생겼을 경우
                    #print("---------------balls[i]) != initalLen-----------------")
                    break

                #같은 크기의 공이 두개 이상일때만
                for k in range(j+1, len(balls[i])):
                    if checkcirclecollide(balls[i][j].x,balls[i][j].y,balls[i][j].radius / 2,balls[i][k].x,balls[i][k].y,balls[i][k].radius / 2):
                        #충돌감지                   
                        newball = Gang(i+1, ((balls[i][j].x + balls[i][k].x) / 2), ((balls[i][j].y + balls[i][k].y) / 2),False)
                        balls[i+1].append(newball)      
                        balls[i].remove(balls[i][k])    #합쳐진 기존의 공 제거
                        balls[i].remove(balls[i][j])
                        pygame.mixer.stop()
                        gang_sounds[i].play()           #합쳐질 때 다음 단계의 소리 재생    
                        score += score_order[i + 1]     #새롭게 합쳐져서 등장한 '강'의 점수 추가
                        if(i + 1 == 7):
                            is_Jongang = True
                        break
                        #두개나 리스트에서 지웠기때문에 인덱스에 변동이 있을 수 있다 -> initalLen으로 감지
        
        #사이즈에 관련없이 모든 '강'들을 하나의 ballball 리스트로
        ballball = []
        for i in range(0,8):
            for j in range(0,len(balls[i])):
                balls[i][j].update()#추가
                ballball.append(balls[i][j])

        # 모든 '강'에 대하여
        for i in range (0,len(ballball)):
            box_top = 40
            
            #천장에 '강'이 닿았는지 체크, 게임오버
            if (not ballball[i].is_dropping) and ballball[i].y - ballball[i].radius < box_top:
                if(ballball[i].order == 8):
                    is_Jongang = True
                    break
                else:
                    game_over = True
                    break
            
            #화면에 리스트 상의 '강' 보여주기
            screen.blit(ballball[i].image,(ballball[i].x - ballball[i].radius / 2, ballball[i].y - ballball[i].radius / 2))
            
            #중력 반영
            ballball[i].vy += gravity

            #화면 밖으로 안나가게 하기
            box_bottom = 720 - ballball[i].radius / 2
            box_left = 40 + ballball[i].radius / 2
            box_right = 560 - ballball[i].radius / 2
            if ballball[i].y >= box_bottom:
                ballball[i].y = box_bottom
                ballball[i].vy = 0
            elif ballball[i].y < box_bottom:
                ballball[i].y += ballball[i].vy
            if ballball[i].x < box_left:
                ballball[i].x = box_left + 1
                ballball[i].vx *= -0.5
            elif ballball[i].x > box_right:
                ballball[i].x = box_right - 1
                ballball[i].vx *= -0.5

        #리스트의 서로 다른 두개의 사이즈 다른 '강'들에 대한 충돌 감지
        if len(ballball) >= 2:
            for i in range (0,len(ballball)-1):            
                for j in range (i+1, len(ballball)):
                    if checkcirclecollide(ballball[i].x, ballball[i].y, ballball[i].radius / 2, ballball[j].x, ballball[j].y, ballball[j].radius / 2) & (ballball[i].order != ballball[j].order):
                        dx = ballball[i].x - ballball[j].x
                        dy = ballball[i].y - ballball[j].y
                        distance = math.sqrt(dx **2 + dy **2)
                        overlap = ballball[i].radius/2 + ballball[j].radius/2 - distance
                        dx = dx / distance
                        dy = dy / distance
                        ballball[i].x += dx * overlap / 2
                        ballball[i].y += dy * overlap / 2
                        ballball[j].x -= dx * overlap / 2
                        ballball[j].y -= dy * overlap / 2                     
                        ballball[i].vx = 0 
                        ballball[j].vx = 0
                        ballball[i].vy *= 1
                        ballball[j].vy *= 1
                        ballball[i].is_dropping = False
                        ballball[j].is_dropping = False
        ##################################################################################

        #'강'이 존재할 수 있는 박스 경계선 그리기
        pygame.draw.line(screen, white, (40, 40), (40, 720), 1)
        pygame.draw.line(screen, white, (40, 720), (560, 720), 1)
        pygame.draw.line(screen, white, (560, 720), (560, 40), 1)
        
        # 박스 상부 게임오버 경계선 그리기
        dotted_line_y = 40
        dotted_line_length = 4
        dotted_line_space = 4
        dotted_line_color = (255,0,0)
        for x in range(40, 560, dotted_line_length + dotted_line_space):
            pygame.draw.line(screen, dotted_line_color, (x, dotted_line_y), (x + dotted_line_length, dotted_line_y), 1)
        
        #점수 그리기
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, white)
        screen.blit(score_text, (screen_width /2 - score_text.get_width()/2, 20))

    #종강 시
    if is_Jongang:
        screen.blit(balls[7][0].image,(40, 120))
        Font = pygame.font.Font(None, 36)
        Gimal_over_text_lines = [
            "Dobby is FREE",
            "Your Gimal is OVER",
            "Your Score is: A+",
            "press ESC to Enjoy Winter Vacation"
        ]  
        for i, line in enumerate(Gimal_over_text_lines):
            line_text = Font.render(line, True, white)
            screen.blit(line_text, (screen_width / 2 - line_text.get_width() / 2, screen_height / 2 - line_text.get_height() / 2 + i * line_text.get_height()))
        pygame.display.update()

        #게임종료
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    #게임 오버 시
    elif game_over:
        font = pygame.font.Font(None, 36)
        game_over_text_lines = [
            "GAME OVER",
            "But Your Final EXAM is NOT OVER",
            f"Your Score is: {score}",
            "quit game by pressing ESC"
        ]
        for i, line in enumerate(game_over_text_lines):
            line_text = font.render(line, True, white)
            screen.blit(line_text, (screen_width / 2 - line_text.get_width() / 2, screen_height / 2 - line_text.get_height() / 2 + i * line_text.get_height()))
        pygame.display.update()

        #게임종료
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()