import pygame as pg
import sys
import math
import random
import tkinter.messagebox as tkm
from pygame import mixer


img_bg = pg.image.load("fig/sora2.png")
img_player = pg.image.load("fig/mafu2.png")
img_weapon = pg.image.load("fig/sizuku3.png") #武器(弾)画像
img_enemy = [
    pg.image.load("fig/kaeru.png"), #敵画像
    pg.image.load("fig/sun2.png") #敵の攻撃弾
    ]

img_explode = [
    None, 
    pg.image.load("fig/explosion/explode1.gif"),
    pg.image.load("fig/explosion/explode2.gif"),
    pg.image.load("fig/explosion/explode3.gif"),
    pg.image.load("fig/explosion/explode4.gif"),
    pg.image.load("fig/explosion/explode5.gif"),
    pg.image.load("fig/explosion/explode6.gif"),
    pg.image.load("fig/explosion/explode7.gif")
] # 敵を撃破したときの爆発（成澤）(新垣)

img_hp = pg.image.load("fig/hp.png") #HPゲージ画像（成澤）(佐々木)

#(成澤)(佐々木)(新垣)
player_hp = 100 #最大HP
player_muteki = 0 #無敵状態を管理
idx = 0 #ゲーム状態を管理
score = 0 #スコア計算

#文字の色を変数においておく（成澤）(佐々木)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 243, 82)

bg_x = 0 #背景のx座標
bg_y = 0 #背景のy座標

px = 320 #プレイヤーのX座標
py = 240 #プレイヤーのY座標

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

bull_x =[0] * BULLET_MAX
bull_y =[0] * BULLET_MAX
bull_f =[False] * BULLET_MAX

ebull_n = 0

ebull_x = [0] * ENEMY_MAX
ebull_y = [0] * ENEMY_MAX
ebull_a = [0] * ENEMY_MAX
ebull_f =[False] * ENEMY_MAX
ebull_f2 = [False] * ENEMY_MAX
e_list = [0] * ENEMY_MAX
e_sp = [0] * ENEMY_MAX

#(成澤)
EFFECT_MAX = 100 #エフェクトの最大数
e_n = 0
effect_l = [0] * EFFECT_MAX
effect_x = [0] * EFFECT_MAX #エフェクトのX座標
effect_y = [0] * EFFECT_MAX #エフェクトのY座標


def set_bullet(): #弾のスタンバイ
    global bull_n
    bull_f[bull_n] = True
    bull_x[bull_n] = px - 16
    bull_y[bull_n] = py - 32
    bull_n = (bull_n + 1) % BULLET_MAX


def move_bullet(screen):#弾を飛ばす
    imgsize = [(64,70)]
    random_num = random.choice(imgsize)
    img_attack1 = pg.transform.scale(img_weapon,random_num)
    img_attack2 = pg.transform.rotozoom(img_attack1, 0, 1.0)

    for i in range(BULLET_MAX):
        
        if bull_f[i] == True:

            bull_y[i] = bull_y[i] - 32
            screen.blit(img_attack2, [bull_x[i], bull_y[i]])
            if bull_y[i] < 0:
                bull_f[i] = False



def move_player(screen, key):
    global px, py, space, player_hp, player_muteki, idx, t, score, reload_timer, REROAD_TIME
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

    #(佐々木)         
    if key[pg.K_SPACE]:
        if  reload_timer > REROAD_TIME:
            set_bullet()
            mixer.music.play(1) #21055 菊池
            reload_timer = 0
        else:
            reload_timer += 1
    #(佐々木)(成澤)
    if player_muteki % 2 == 0: #無敵状態ならプレイヤー画像点滅
        screen.blit(img_player, [px-16, py-16])

    if player_muteki > 0:
        player_muteki = player_muteki - 1 #無敵時は当たり判定を無効にする
        return
    
    #(佐々木)
    elif idx == 1: #Peacefull mode
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                w = img_enemy[e_list[i]].get_width()
                h = img_enemy[e_list[i]].get_height()
                r = int((w+h)/4+(32+32)/4)
                #(佐々木)(成澤)(新垣)
                if distance(ebull_x[i],ebull_y[i],px,py) < r*r: #敵及び敵の攻撃に接触
                    #(成澤)
                    effect_explode(px,py)
                    #(佐々木)(成澤)
                    player_hp = player_hp - 10 #ダメージを受ける
                    score -=5
                    if player_hp <= 0:
                        idx = 2
                        t = 0
                    if player_muteki == 0:
                        player_muteki = 30 #無敵時間
                    ebull_f[i] = False
                    ebull_f2[i] = False
                
                REROAD_TIME = 5

            
    elif idx == 3: #Hard mode
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                w = img_enemy[e_list[i]].get_width()
                h = img_enemy[e_list[i]].get_height()
                r = int((w+h)/4+(32+32)/4)

                if distance(ebull_x[i],ebull_y[i], px, py) < r*r: #敵及び敵の攻撃に接触
                    effect_explode(px,py)
                    player_hp = player_hp - 10 #ダメージを受ける
                    score -= 5
                    if player_hp <= 0:
                        idx = 2
                        t = 0
                    if player_muteki == 0:
                        player_muteki = 15 #無敵時間
                    ebull_f[i] = False
                    ebull_f2[i] = False

                REROAD_TIME = 10

    elif idx == 6: #stage lv.2
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                w = img_enemy[e_list[i]].get_width()
                h = img_enemy[e_list[i]].get_height()
                r = int((w+h)/4+(32+32)/4)
                
                if distance(ebull_x[i],ebull_y[i],px,py) < r*r: #敵及び敵の攻撃に接触
                    effect_explode(px,py)
                    player_hp = player_hp - 10 #ダメージを受ける
                    score -=10
                    if player_hp <= 0:
                        idx = 2
                        t = 0
                    if player_hp == 0:
                        player_hp = 10 #無敵時間
                    ebull_f[i] = False
                    ebull_f2[i] = False
                
                REROAD_TIME = 15

    
def set_enemy(x, y, a, enemy, sp):
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
        ebull_n = (ebull_n + 1) % ENEMY_MAX


def move_enemy(screen): #enemyの移動
    global score, idx, t
    for i in range(ENEMY_MAX):
        if ebull_f[i] == True:
            png = e_list[i]
            ebull_x[i] = ebull_x[i] + e_sp[i]*math.cos(math.radians(ebull_a[i]))
            ebull_y[i] = ebull_y[i] + e_sp[i]*math.sin(math.radians(ebull_a[i]))
            
            if e_list[i] == 0 and ebull_y[i] > 100 and ebull_f2[i] == False:#弾を発射
                set_enemy(ebull_x[i],ebull_y[i],90,1,15)
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
                        #(佐々木)(成澤)
                        score = score +10
                        if idx == 1:
                            if score >= 50:
                                idx = 7
                                t = 0
                        #(佐々木)
                        if idx == 3:
                            if score >= 70:
                                idx = 4
                                t = 0 
                        else:
                            if score >= 100:                            
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

def effect_explode(x, y): #エフェクトを描画する準備（成澤）
    global e_n
    effect_l[e_n] = 1
    effect_x[e_n] = x #エフェクト画像のX座標
    effect_y[e_n] = y #エフェクト画像のY座標


def draw_effect(screen): #エフェクト描画（成澤）
    for i in range(EFFECT_MAX):
        if effect_l[i] > 0:
            rz = pg.transform.rotozoom(img_explode[effect_l[i]], 0, 0.7) #画像を縮小させる
            screen.blit(rz, [effect_x[i] - 15, effect_y[i] - 30])
            effect_l[i] = effect_l[i] + 1
            if effect_l[i] == 8: #使用する爆発エフェクト用画像が7枚
                effect_l[i] = 0


def main(): #main関数

    global t, bg_y, idx, player_hp, player_muteki, px, py, score
    pg.init()
    pg.display.set_caption("シューティングゲーム")
    screen = pg.display.set_mode((640,480))
    clock = pg.time.Clock()
    mixer.init()#21055 菊池
    mixer.music.load("fig/se_music.mp3")

    
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
        #(佐々木)(成澤)
        if idx == 0: #title
            draw_text(screen,320,80,"SHOOTING GAME!!!",80,BLACK)
            draw_text(screen,320,200,"PLEASE SELECT MODE",50,BLACK)
            draw_text(screen,320,280,"Peacefull : puth『1』key",50,GREEN)
            draw_text(screen,320,360,"Hard : puth『2』key", 50,RED)
            
            if key[pg.K_1] == 1:
                idx = 1
                t = 0
                px = 320
                py = 300
                player_hp = 100
                player_muteki = 0
                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False
                    
            #(佐々木)
            if key[pg.K_2] == 1:
                idx = 3
                t = 0
                px = 320
                py = 300
                player_hp = 100
                player_muteki = 0

                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False

        if idx == 1: #playing #peacefull
            move_player(screen,key)
            move_bullet(screen)

            if t%30 == 0:#30フレームにつき敵1体出現
                set_enemy(random.randint(20,620),-10,90,0,6)
            move_enemy(screen)
        
        #(佐々木)(成澤)(新垣)
        if idx == 2: #gameover
            draw_text(screen, 320, 240, "GAMEOVER", 100, RED)
        
        #(佐々木)-------------------
        if idx == 3: #playing #hard
            move_player(screen,key)
            move_bullet(screen)

            if t%10 == 0:#10フレームにつき敵1体出現
                set_enemy(random.randint(20,620),-10,90,0,6)
            move_enemy(screen)

        if idx == 4: #Hardモードからのclear
            draw_text(screen,320,240,"GAMECLEAR",100,YELLOW)
            draw_text(screen,330,320,"NEXT LEVEL:push『3』key",50,BLACK)
            draw_text(screen,385,400,"GAME ESCAPE:push『5』key",55,BLACK)
            if key[pg.K_3] == 1:
                idx = 5
                t = 0
                px = 320
                py = 300
                player_hp = 100
                player_muteki = 0
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
                player_hp = 50
                player_muteki = 0
                score = 0
                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False

        if idx == 6: #lv.2 playing
            move_player(screen,key)
            move_bullet(screen)
            if t%7 == 0: #7フレームにつき敵1体出現
                set_enemy(random.randint(20,620),-10,90,0,6)
            move_enemy(screen)
        
        if idx == 7: #Hardモード以外のclear
            draw_text(screen,320,240,"GAMECLEAR",100,YELLOW)
            draw_text(screen,385,320,"GAME ESCAPE:push『5』key",55,BLACK)
            draw_text(screen,385,400,"GAME RESTART:push『6』key",55,BLACK)
            if key[pg.K_5] == 1:
                pg.quit()
                sys.exit()
            if key[pg.K_6] == 1:
                #pg.quit()
                idx = 0
                t = 0
                px = 320
                py = 300
                player_hp = 100
                player_muteki = 0
                score = 0


        if idx == 1 or idx == 3 or idx == 6:#ゲームプレイ中のみ体力ゲージとスコアを表示する
            screen.blit(img_hp,(10,450))#体力ゲージ
            pg.draw.rect(screen,(32,32,32),[10+player_hp*2,450,(100-player_hp)*2,25])#ダメージを受けたら矩形で塗りつぶす
            draw_text(screen, 580, 20, "SCORE" + str(score), 30, WHITE)
        #(佐々木)--------------

        #成澤    
        draw_effect(screen)
        
        pg.display.update()
        clock.tick(30)
if __name__ == "__main__":
    main()