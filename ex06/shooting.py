import pygame as pg
import sys
import math
import random


img_bg = pg.image.load("fig/sora2.png") #背景画像
img_mafu = pg.image.load("fig/mafu2.png") #player(mafu)画像
img_attack = pg.image.load("fig/sizuku2.png") #player攻撃弾画像

img_enemy = [
    pg.image.load("fig/kaeru.png"),#Enemy画像
    pg.image.load("fig/sun2.png")]#Enemy攻撃弾画像
img_hp = pg.image.load("fig/gauge.png")#体力ゲージ
img_title = pg.image.load("fig/shoot_title.jpg")#タイトル画像

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 243, 82)
BORDEAUX = (108, 39, 45)
GREEN = (185, 208, 139)

bg_x = 0
bg_y = 0
px = 320 #playerのX座標
py = 240 #playerのY座標
bx = 0 #弾のX座標
by = 0 #弾のY座標
t = 0 #タイマー変数

REROAD_TIME = 0
reload_timer = 0
score = 0
lives = 0

BULLET_MAX = 100 #弾の最大値
ENEMY_MAX = 100 #敵の最大数
BULLET_MAX_lv2 = 150 #弾の最大値(lv.2)
ENEMY_MAX_lv2 = 150 #敵の最大数(lv.2)
ENEMY_BULLET=1
bull_n = 0
bull_x =[0]*BULLET_MAX
bull_y =[0]*BULLET_MAX
bull_f =[False]*BULLET_MAX

ebull_n = 0
ebull_x = [0]*ENEMY_MAX
ebull_y = [0]*ENEMY_MAX
ebull_a = [0]*ENEMY_MAX
ebull_f =[False]*ENEMY_MAX
ebull_f2 = [False]*ENEMY_MAX
e_list = [0]*ENEMY_MAX
e_sp = [0]*ENEMY_MAX

p_hp = 100 #HP
p_muteki = 0 #無敵状態の管理

idx = 0 #ゲーム状態の管理

p_damage = None#プレイヤーがダメージを受けた際のSE
p_shoot = None#プレイヤーのショットSE
e_down = None#敵を倒した際のSE


def set_bullet():#弾のスタンバイ
    global bull_n
    bull_f[bull_n] = True
    bull_x[bull_n] = px
    bull_y[bull_n] = py
    bull_n = (bull_n+1)%BULLET_MAX
    

def move_bullet(screen):#弾を飛ばす
    imgsize = [(64,70)]
    random_num = random.choice(imgsize)
    img_attack1 = pg.transform.scale(img_attack,random_num)
    img_attack2 = pg.transform.rotozoom(img_attack1, 0, 1.0)

    for i in range(BULLET_MAX):
        
        if bull_f[i] == True:
            bull_y[i] = bull_y[i] - 10
            screen.blit(img_attack2,[bull_x[i],bull_y[i]])
            
            if bull_y[i] < 0:
                bull_f[i] = False

def move_mafu(screen,key): #playerの移動
    global px, py, p_hp, p_muteki, idx, t ,reload_timer ,REROAD_TIME
    if key[pg.K_UP] == 1:
        py = py - 10
        if py < 20:
            py = 20
    
    if key[pg.K_DOWN] == 1:
        py = py + 10
        if py > 400:
            py = 400
    
    if key[pg.K_LEFT] == 1:
        px = px - 10
        if px < 20:
            px = 20
    
    if key[pg.K_RIGHT] == 1:
        px = px + 10
        if px > 570:
            px = 570
                
    if key[pg.K_SPACE]:
        if  reload_timer > REROAD_TIME:
            set_bullet()
            p_shoot.play()
            reload_timer = 0
        else:
            reload_timer += 1

    if p_muteki %2 == 0:
        screen.blit(img_mafu,[px-16,py-16])

    if p_muteki > 0:
        p_muteki = p_muteki - 1#無敵時は当たり判定を無効にする
        return

    elif idx == 1: #Peacefull mode
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                w = img_enemy[e_list[i]].get_width()
                h = img_enemy[e_list[i]].get_height()
                r = int((w+h)/4+(32+32)/4)
            
                if distance(ebull_x[i],ebull_y[i],px,py) < r*r: #敵及び敵の攻撃に接触
                    # effect(px,py)
                    p_damage.play()
                    p_hp = p_hp - 5 #ダメージを受ける
                    if p_hp <= 0:
                        idx = 2
                        t = 0
                    if p_muteki == 0:
                        p_muteki = 30 #無敵時間
                    ebull_f[i] = False
                    ebull_f2[i] = False
                
                REROAD_TIME = 10

                    
    elif idx == 3: #Hard mode
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                w = img_enemy[e_list[i]].get_width()
                h = img_enemy[e_list[i]].get_height()
                r = int((w+h)/4+(32+32)/4)

                if distance(ebull_x[i],ebull_y[i], px, py) < r*r: #敵及び敵の攻撃に接触
                    # effect(px,py)
                    p_damage.play()
                    p_hp = p_hp - 10 #ダメージを受ける
                    if p_hp <= 0:
                        idx = 2
                        t = 0
                    if p_hp == 0:
                        p_hp = 15 #無敵時間
                    ebull_f[i] = False
                    ebull_f2[i] = False

                REROAD_TIME = 30

    elif idx == 6: #stage lv.2
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                w = img_enemy[e_list[i]].get_width()
                h = img_enemy[e_list[i]].get_height()
                r = int((w+h)/4+(32+32)/4)
                
                if distance(ebull_x[i],ebull_y[i],px,py) < r*r: #敵及び敵の攻撃に接触
                    p_damage.play()
                    p_hp = p_hp - 15 #ダメージを受ける
                    if p_hp <= 0:
                        idx = 2
                        t = 0
                    if p_hp == 0:
                        p_hp = 10 #無敵時間
                    ebull_f[i] = False
                    ebull_f2[i] = False
                
                REROAD_TIME = 50
                
                    
def set_kaeru(x,y,a,enemy,sp): #enemy(kaeru)の設定
    global ebull_n
    while True:
        if ebull_f[ebull_n] == False:
            ebull_f[ebull_n] = True
            ebull_x[ebull_n] = x
            ebull_y[ebull_n] = y
            ebull_a[ebull_n] = a
            e_list[ebull_n] = enemy
            e_sp[ebull_n] = sp
            break
        ebull_n = (ebull_n+1)%ENEMY_MAX


def move_kaeru(screen): #enemyの移動
    global score, idx, t
    for i in range(ENEMY_MAX):
        if ebull_f[i] == True:
            png = e_list[i]
            ebull_x[i] = ebull_x[i] + e_sp[i]*math.cos(math.radians(ebull_a[i]))
            ebull_y[i] = ebull_y[i] + e_sp[i]*math.sin(math.radians(ebull_a[i]))
            
            if e_list[i] == 0 and ebull_y[i] > 100 and ebull_f2[i] == False:#弾を発射
                set_kaeru(ebull_x[i],ebull_y[i],90,1,15)
                ebull_f2[i] = True
            
            if ebull_x[i] < -40 or ebull_x[i] > 680 or ebull_y[i] < -40 or ebull_y[i] > 520:#画面外に敵が消える
                ebull_f[i] = False
                ebull_f2[i] = False

            if e_list[i] !=ENEMY_BULLET:
                w=img_enemy[e_list[i]].get_width()
                h=img_enemy[e_list[i]].get_height()
                r=int((w+h)/4)+8

                for n in range(BULLET_MAX):    
                    if bull_f[n]==True and distance(ebull_x[i]-16,ebull_y[i]-16,bull_x[n],bull_y[n])<r*r:
                        bull_f[n]=False
                        score = score + 10
                        e_down.play()
                        if idx == 1:
                            if score >= 50:
                                idx = 7
                                t = 0

                        if idx == 3:
                            if score >= 1000:
                                idx = 4
                                t = 0 
                        else:
                            if score >= 1000:                            
                                idx = 7
                                t = 0
                        ebull_f[i]=False
                        ebull_f2[i]=False
            
            rz = pg.transform.rotozoom(img_enemy[png],-180,1.0)
            screen.blit(rz,[ebull_x[i]-rz.get_width()/2,ebull_y[i]-rz.get_height()/2])


def distance(x1,y1,x2,y2):
    return((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


def draw_text(screen,x,y,text,size,col):#文字表示の関数
    font = pg.font.SysFont("hg明朝e",size)
    s = font.render(text,True,col)
    x = x - s.get_width()/2
    y = y - s.get_height()/2
    screen.blit(s,[x,y])


def main(): #main関数

    global t, bg_y, idx, p_hp, p_muteki, px, py, score, p_damage, p_shoot, e_down
    pg.init()
    pg.display.set_caption("シューティングゲーム")
    screen = pg.display.set_mode((640,480))
    clock = pg.time.Clock()
    p_damage = pg.mixer.Sound("se/p_damage.mp3")
    p_shoot = pg.mixer.Sound("se/p_shoot.mp3")
    e_down = pg.mixer.Sound("se/enemydown.mp3")

    running = True
    while running:
        t=t+1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        bg_y = (bg_y+16)%480
        screen.blit(img_bg,[0,bg_y-480])
        screen.blit(img_bg,[0,bg_y])
        key = pg.key.get_pressed()

        if idx == 0: #title
            # for event in pygame.event.get():
            img_t = pg.transform.rotozoom(img_title,0,1.0)
            screen.blit(img_t,[0,0])
            draw_text(screen,320,80,"SHOOTING GAME!!!",80,BLACK)
            draw_text(screen,320,200,"PLEASE SELECT MODE",50,BLACK)
            draw_text(screen,320,280,"Peacefull : puth『1』key",50,GREEN)
            draw_text(screen,320,360,"Hard : puth『2』key", 50,BORDEAUX)
            
            if key[pg.K_1] == 1:
                idx = 1
                t = 0
                px = 320
                py = 300
                p_hp = 100
                p_muteki = 0
                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False

            if key[pg.K_2] == 1:
                idx = 3
                t = 0
                px = 320
                py = 300
                p_hp = 100
                p_muteki = 0
                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False

        if idx == 1: #playing #peacefull
            move_mafu(screen,key)
            move_bullet(screen)

            if t%30 == 0:#30フレームにつき敵1体出現
                set_kaeru(random.randint(20,620),-10,90,0,6)
            move_kaeru(screen)

        if idx == 2: #gameover
            draw_text(screen, 320, 240, "GAMEOVER", 100, BORDEAUX)
        # screen.blit(img_gauge,(10,450))#体力ゲージ
        pg.draw.rect(screen,(32,32,32),[10+p_hp*2,450,(100-p_hp)*2,25])#ダメージを受けたら矩形で塗りつぶす
        
        if idx == 3: #playing #hard
            move_mafu(screen,key)
            move_bullet(screen)

            if t%10 == 0:#10フレームにつき敵1体出現
                set_kaeru(random.randint(20,620),-10,90,0,6)
            move_kaeru(screen)

        if idx == 4: #Hardモードからのclear
            draw_text(screen,320,240,"GAMECLEAR",100,YELLOW)
            draw_text(screen,330,320,"NEXT LEVEL:push『3』key",50,BLACK)
            draw_text(screen,385,320,"GAME ESCAPE:push『5』key",55,BLACK)
            if key[pg.K_3] == 1:
                idx = 5
                t = 0
                px = 320
                py = 300
                p_hp = 100
                p_muteki = 0
                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False
            if key[pg.K_5] == 1:
                pg.quit()
                sys.exit()

        if idx == 5: #playing #lv.2　playing準備
            draw_text(screen,320,240,"Level.2",100,YELLOW)
            draw_text(screen,320,320,"CONTINUE:puth『4』key",55,BLACK)
            if key[pg.K_4] == 1:
                idx = 6
                t = 0
                px = 320
                py = 300
                p_hp = 50
                p_muteki = 0
                score = 0
                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False

        if idx == 6: #lv.2 playing
            move_mafu(screen,key)
            move_bullet(screen)
            if t%7 == 0: #7フレームにつき敵1体出現
                set_kaeru(random.randint(20,620),-10,90,0,6)
            move_kaeru(screen)
        
        if idx == 7: #Hardモード以外のclear
            draw_text(screen,320,240,"GAMECLEAR",100,YELLOW)
            draw_text(screen,385,320,"GAME ESCAPE:push『5』key",55,BLACK)
            draw_text(screen,385,400,"GAME RESTART:push『6』key",55,BLACK)
            if key[pg.K_5] == 1:
                pg.quit()
                sys.exit()
            if key[pg.K_6] == 1:
                pg.quit()
                idx = 0
        

        if idx == 1 or idx == 3 or idx == 6:#ゲームプレイ中のみ体力ゲージとスコアを表示する
            screen.blit(img_hp,(10,450))#体力ゲージ
            pg.draw.rect(screen,(32,32,32),[10+p_hp*2,450,(100-p_hp)*2,25])#ダメージを受けたら矩形で塗りつぶす
            draw_text(screen, 580, 20, "SCORE" + str(score), 30, WHITE)
        pg.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
