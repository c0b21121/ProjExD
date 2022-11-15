import pygame as pg
import sys
import math
import random
import tkinter.messagebox as tkm

#C0B21009 新垣颯大==================================================
WIDTH = 640
HEIGHT = 480
#C0B21009 新垣颯大==================================================

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
] # 敵を撃破したときの爆発（成澤）

img_hp = pg.image.load("fig/hp.png") #HPゲージ画像（成澤）

#(成澤)
player_hp = 100 #最大HP
player_muteki = 0 #無敵状態を管理
game_state = 0 #ゲーム状態を管理
score = 0 #スコア計算

#文字の色を変数においておく（成澤）
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

bg_y = 0 #背景のy座標

px = 320 #プレイヤーのX座標
py = 240 #プレイヤーのY座標

t = 0 #タイマー変数
space = 0
BULLET_MAX = 100 #弾の最大値
ENEMY_MAX = 100 #敵の最大数
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
e_speed = [0] * ENEMY_MAX

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
    for i in range(BULLET_MAX):
        if bull_f[i] == True:
            bull_y[i] = bull_y[i] - 32
            screen.blit(img_weapon, [bull_x[i], bull_y[i]])
            if bull_y[i] < 0:
                bull_f[i] = False



def move_player(screen, key):
    global px, py, space, player_hp, player_muteki, game_state, t, score
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

    space = (space + 1) * key[pg.K_SPACE]

    if space % 5 == 1: #5フレーム毎に弾を飛ばす
        set_bullet()

    if player_muteki % 2 == 0: #無敵状態ならプレイヤー画像点滅
        screen.blit(img_player, [px-16, py-16])

    if player_muteki > 0:
        player_muteki = player_muteki - 1 #無敵時は当たり判定を無効にする
        return

    elif game_state == 1:
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                w = img_enemy[e_list[i]].get_width()
                h = img_enemy[e_list[i]].get_height()
                r = int((w + h) / 4 + (32 + 32) / 4)

                if distance(ebull_x[i], ebull_y[i], px, py) < r * r: #敵or敵の攻撃に接触
                    effect_explode(px, py)
                    player_hp = player_hp - 20 #ダメージを受ける
                    score -= 50
                    if player_hp <= 0:
                        game_state = 2
                        t = 0
                    if player_muteki == 0:
                        player_muteki = 30 #無敵時間

                    ebull_f[i] = False
                    ebull_f2[i] = False


    screen.blit(img_player, [px-16, py-16])


def set_enemy(x, y, a, enemy, speed):

    global ebull_n
    while True:
        if ebull_f[ebull_n] == False:
            ebull_f[ebull_n] = True
            ebull_x[ebull_n] = x
            ebull_y[ebull_n] = y
            ebull_a[ebull_n] = a
            e_list[ebull_n] = enemy
            e_speed[ebull_n] = speed
            break
        ebull_n = (ebull_n + 1) % ENEMY_MAX


def move_enemy(screen):
    global score, game_state, t
    for i in range(ENEMY_MAX):
        if ebull_f[i] == True:
            png = e_list[i]
            ebull_x[i] = ebull_x[i] + e_speed[i] * math.cos(math.radians(ebull_a[i]))
            ebull_y[i] = ebull_y[i] + e_speed[i] * math.sin(math.radians(ebull_a[i]))
            if e_list[i] == 0 and ebull_y[i] > 100 and ebull_f2[i] == False:#弾を発射
                set_enemy(ebull_x[i], ebull_y[i], 90, 1, 15)
                ebull_f2[i] = True
                
            if ebull_x[i] < -40 or ebull_x[i] > 680 or ebull_y[i] < -40 or ebull_y[i] > 520: #画面外に敵が消える
                ebull_f[i] = False
                ebull_f2[i] = False

            if e_list[i] != ENEMY_BULLET:
                w = img_enemy[e_list[i]].get_width()
                h = img_enemy[e_list[i]].get_height()
                r = int((w + h) / 4) + 8
                for n in range(BULLET_MAX):
                    if bull_f[n] == True and distance(ebull_x[i] - 16, ebull_y[i] - 16, bull_x[n], bull_y[n])< r * r:
                        bull_f[n] = False
                        effect_explode(ebull_x[i], ebull_y[i]) #エフェクト爆発発生
                        score += 100 #スコア＋１００

                        if score >= 2000:
                            game_state = 3 #ゲームクリア
                            t = 0

                        ebull_f[i] = False
                        ebull_f2[i] = False
            rz = pg.transform.rotozoom(img_enemy[png], -180, 1.0)
            screen.blit(rz, [ebull_x[i] - rz.get_width() / 2, ebull_y[i] - rz.get_height() / 2])


def effect_explode(x, y): #エフェクトを描画する準備（成澤）
    global e_n
    effect_l[e_n] = 1
    effect_x[e_n] = x #エフェクト画像のX座標
    effect_y[e_n] = y #エフェクト画像のY座標
    #e_no = (e_n + 1) % EFFECT_MAX


def draw_effect(screen): #エフェクト描画（成澤）
    for i in range(EFFECT_MAX):
        if effect_l[i] > 0:
            rz = pg.transform.rotozoom(img_explode[effect_l[i]], 0, 0.7) #画像を縮小させる
            screen.blit(rz, [effect_x[i] - 15, effect_y[i] - 30])
            effect_l[i] = effect_l[i] + 1
            if effect_l[i] == 8: #使用する爆発エフェクト用画像が7枚
                effect_l[i] = 0


#2点間の距離を計算
def distance(x1, y1, x2, y2):
    return((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


#テキスト表示（成澤）
def draw_text(screen, x, y, text, size, color):
    font = pg.font.Font(None, size)
    s = font.render(text, True, color)
    x = x - s.get_width() / 2
    y = y - s.get_height() / 2
    screen.blit(s, [x, y])


def main():

    global t, bg_y,  game_state, score, px, py, player_hp, player_muteki
    pg.init()
    pg.display.set_caption("シューティングゲーム")
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()

    while True:
        t = t + 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        bg_y = (bg_y + 16) % 480
        screen.blit(img_bg, [0, bg_y - 480])
        screen.blit(img_bg, [0, bg_y])
        key = pg.key.get_pressed()

        #(game_state成澤)
        if game_state == 0: #タイトル画面
            draw_text(screen, 320, 240, "PRESS ENTER", 80, WHITE)
            if key[pg.K_RETURN] == 1:
                game_state = 1
                t = 0
                score = 0
                px = 320
                py = 300
                player_hp = 100
                player_muteki = 0
                for i in range(BULLET_MAX):
                    bull_f[i] = False
                for i in range(ENEMY_MAX):
                    ebull_f[i] = False

        if game_state == 1: #ゲームプレイ中
            move_player(screen,key)
            move_bullet(screen)
            if t % 30 == 0: #30フレームにつき敵1体出現
                set_enemy(random.randint(20, 620), -10, 90, 0, 6)
            move_enemy(screen)

            screen.blit(img_hp, (10, 450)) #HPゲージ
            pg.draw.rect(screen, (32, 32, 32), [10 + player_hp * 2, 450, (100 - player_hp) * 2, 25]) #ダメージを受けたら単系で塗りつぶす
            draw_text(screen, 60, 20, "score: " + str(score), 30, GREEN)

        if game_state == 2: #ゲームオーバー
            draw_text(screen, 320, 240, "GAMEOVER", 100, RED)
            if t == 100:
                game_state = 0
                t = 0

        if game_state == 3: #ゲームクリア
            draw_text(screen, 320, 240, "GAME CLEAR! Congrats!", 70, WHITE)
            if t == 100:
                game_state = 0
                t = 0

        draw_effect(screen)
        pg.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()