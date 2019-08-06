import pygame
import sys
import myplane
import enemy
import bullet
import supply
import pickle
from easygui import enterbox
from pygame.locals import *
from random import *



__version__ = 'v2.1'
__author__ = 'ietar'

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700  # 为操作界面尺寸
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption(r'打飞机是男人的浪漫! {}'.format(__version__))

background = pygame.image.load(r'images\background_double.png').convert()
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GOLDEN = (205, 255, 0)

# 载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)
cheatonsound = pygame.mixer.Sound(r'sound\cheaton.wav')
cheatonsound.set_volume(0.5)
cheatoffsound = pygame.mixer.Sound(r'sound\cheatoff.wav')
cheatoffsound.set_volume(0.5)
get_life_sound = pygame.mixer.Sound(r'sound\joinme.wav')
get_life_sound.set_volume(0.3)
theworld_sound = pygame.mixer.Sound(r'sound\theworldtick.wav')
theworld_sound.set_volume(1.7)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def increase_speed(target, increase):
    for each in target:
        each.speed += increase


def writeline(
        text='',
        font=r'font\fs.ttf',
        color_367=WHITE,
        bold=False,
        size=24,
        alter_x=None,
        alter_y=0):
    writeline_font = pygame.font.Font(font, size)
    if bold:
        writeline_font.set_bold(True)
    writeline_text = writeline_font.render(text, True, color_367)
    if alter_x is None:
        length = -len(text)
        for i in text:
            if i.isascii():
                length += 0.5
        alter_x = length / 2 * size
    screen.blit(writeline_text, (width // 2 + alter_x, height // 2 + alter_y))


def main():
    pygame.mixer.music.play(-1)

    # 得分先出
    score = 0
    score_font = pygame.font.Font(r'font\font.ttf', 32)

    # 标志是否暂停
    paused = False
    paused_nor_image = pygame.image.load(
        r'images\pause_nor.png').convert_alpha()
    paused_pressed_image = pygame.image.load(
        r'images\pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load(
        r'images\resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load(
        r'images\resume_pressed.png').convert_alpha()
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = paused_nor_image

    # 标志声音播放/静音
    silence = False
    volume_on_image = pygame.image.load(
        r'images\volume_on.png').convert_alpha()
    volume_off_image = pygame.image.load(
        r'images\volume_off.png').convert_alpha()
    volume_rect = volume_on_image.get_rect()
    volume_rect.left, volume_rect.top = width - paused_rect.width - 10, 65
    volume_image = volume_on_image

    # 设置难度
    level = 1
    target_rate = [0.1, 0.2, 0.3]

    # 全屏炸弹
    bomb_image = pygame.image.load(r'images\bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font(r'font\font.ttf', 48)
    bomb_num = 3

    supply_gap = 18
    bullet2_duration = 18
    bullet3_duration = 30
    theworld_duration = 300

    # 每(supply_gap)s补给包
    bullet_supply = supply.BulletSupply(bg_size)
    bomb_supply = supply.BombSupply(bg_size)
    life_supply = supply.LifeSupply(bg_size)
    theworld_supply = supply.TheworldSupply(bg_size)
    supply_time = USEREVENT
    pygame.time.set_timer(supply_time, supply_gap * 1000)

    # 尝试修复暂停时补给间隔直接重置的bug
    # 时间相关
    count_second = 0  # 记录非暂停时间(秒)
    supply_count_second = 0  # 记录上次发补给的时刻(秒)
    bullet2_count_second = 0
    bullet3_count_second = 0
    delay = 0  # 记录已绘制帧数 到100则归零
    supply_time2 = USEREVENT + 1
    pygame.time.set_timer(supply_time2, 1000)  # 每1000毫秒触发一次time2事件
    
    # pep8 fixes
    enemy_hit = None
    bullets = None
    write_info = None

    # 生成我方飞机
    me = myplane.Myplane(bg_size)
    is_double_bullet = False
    is_super_bullet = False
    is_theworld = False
    rpcount_second = 0

    # 生成敌方飞机
    enemies = pygame.sprite.Group()
    # 小飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # 中飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 6)

    # 大飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 4
    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 生成双子弹
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 8
    for i in range(bullet2_num // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    # 生成超级子弹
    bullet3 = []
    bullet3_index = 0
    bullet3_num = 16
    for i in range(bullet3_num // 4):
        bullet3.append(bullet.Bullet3((me.rect.centerx - 63, me.rect.centery)))
        bullet3.append(bullet.Bullet3((me.rect.centerx - 23, me.rect.centery)))
        bullet3.append(bullet.Bullet3((me.rect.centerx + 23, me.rect.centery)))
        bullet3.append(bullet.Bullet3((me.rect.centerx + 63, me.rect.centery)))

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 逃窜率初始化
    kill = [0, 0, 0]
    enemy.miss = [0, 0, 0]
    enemy.create = [2, 6, 15]

    # 详细信息开关
    info = False
    miss_rate = [enemy.miss[0] / enemy.create[1],
                 enemy.miss[1] / enemy.create[1],
                 enemy.miss[2] / enemy.create[2]]

    clock = pygame.time.Clock()

    running = True
    bg_posy = -700

    levelup_score = [50000, 300000, 600000, 1000000]
    # levelup_score = [5000,10000,20000,30000]
    target_score = levelup_score[-1]
    bonus_level = 0

    while running:
        # 暂停控制 背景音乐静音控制
        if paused or silence or is_theworld:
            # pygame.time.set_timer(supply_time,0)
            pygame.mixer.music.pause()
        else:
            # pygame.time.set_timer(supply_time,supply_gap * 1000)
            pygame.mixer.music.unpause()
            # pygame.mixer.unpause

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = paused_pressed_image

                if event.button == 1 and volume_rect.collidepoint(
                        event.pos):  # 鼠标在静音框内左键
                    silence = not silence
                    if silence:
                        volume_image = volume_off_image
                    else:
                        volume_image = volume_on_image

            elif event.type == MOUSEMOTION:  # 鼠标移动
                if paused_rect.collidepoint(event.pos):  # 鼠标在暂停框内
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = paused_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = paused_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_o:  # cheating code###
                    me.wudi = not me.wudi
                    if me.wudi:
                        if not paused and not silence:
                            cheatonsound.play()
                        is_double_bullet = True
                    else:
                        if not paused and not silence:
                            cheatoffsound.play()
                        bullet2_count_second = count_second
                if event.key == K_ESCAPE:  # 立刻结束
                    running = False

                if event.key == K_z:  # 调试用
                    print('level=', level)
                    print('双弹夹:', is_double_bullet)
                    print('四弹夹:', is_super_bullet)
                    print('补给间隔=', supply_gap)
                    print(
                        'current supply gap=',
                        count_second -
                        supply_count_second)
                    print('target_rate=', target_rate)

                    '''print('kill=',kill)
                    print('miss=',enemy.miss)
                    print('create',enemy.create)
                    miss_rate = [enemy.miss[0]/enemy.create[1],\
                                enemy.miss[1]/enemy.create[1],\
                                enemy.miss[2]/enemy.create[2]]
                    miss_rate_str = [str(x*100)+r'%' for x in miss_rate]
                    print('逃窜率:',miss_rate_str)'''

                # 详细信息启动开关 i
                if event.key == K_i:
                    info = not info  # 尝试实时显示
                    if not paused and not silence:
                        cheatoffsound.play()

                    # make_info()
                    miss_rate = [enemy.miss[0] / enemy.create[1],
                                 enemy.miss[1] / enemy.create[1],
                                 enemy.miss[2] / enemy.create[2]]
                    miss_rate_str = ['%.1f' %
                                     (x * 100) + r'%' for x in miss_rate]
                    target_rate_str = ['%.1f' %
                                       (x * 100) + r'%' for x in target_rate]

                    killinfo = 'kill={} {} {}'.format(
                        kill[0], kill[1], kill[2])
                    missinfo = 'miss={} {} {}'.format(
                        enemy.miss[0], enemy.miss[1], enemy.miss[2])
                    targetinfo = 'target={} {} {}'.format(
                        target_rate_str[0], target_rate_str[1], target_rate_str[2])
                    rateinfo = 'rate={} {} {}'.format(
                        miss_rate_str[0], miss_rate_str[1], miss_rate_str[2])
                    # bonuslevelinfo ='bonus={}'.format(bonus_level)

                    def write_info():
                        writeline(
                            text=killinfo,
                            size=12,
                            alter_x=25,
                            alter_y=-345)
                        writeline(
                            text=missinfo,
                            size=12,
                            alter_x=25,
                            alter_y=-330)
                        writeline(
                            text=rateinfo,
                            size=12,
                            alter_x=25,
                            alter_y=-315)
                        writeline(
                            text=targetinfo,
                            size=12,
                            alter_x=25,
                            alter_y=-300)
                        writeline(
                            text='bonus={}'.format(bonus_level),
                            size=12,
                            alter_x=25,
                            alter_y=-285)

                    '''#make_info#
                    miss_rate = [enemy.miss[0]/enemy.create[1],\
                            enemy.miss[1]/enemy.create[1],\
                            enemy.miss[2]/enemy.create[2]]
                    miss_rate_str = ['%.1f'%(x*100)+r'%' for x in miss_rate]

                    killinfo='kill={} {} {}'.format(kill[0],kill[1],kill[2])
                    missinfo='miss={} {} {}'.format(enemy.miss[0],enemy.miss[1],enemy.miss[2])
                    createinfo='create={} {} {}'.format(enemy.create[0],enemy.create[1],enemy.create[2])
                    rateinfo='rate={} {} {}'.format(miss_rate_str[0],miss_rate_str[1],miss_rate_str[2])'''

                # 空格发射全屏炸弹
                if event.key == K_SPACE and not paused:
                    if bomb_num:
                        if me.wudi:
                            bomb_num += 2
                        bomb_num -= 1
                        if not paused and not silence:
                            bomb_sound.play()
                        for each in enemies:
                            if each not in big_enemies:  # 大飞机可炸不动 要慢慢打
                                if each.rect.bottom > 0:
                                    each.active = False

            # 非暂停时才计时count_second
            elif event.type == supply_time2 and not paused:  # 1000毫秒触发1次的事件
                count_second += 1

                if level == 5:
                    if miss_rate[0] > target_rate[0] or miss_rate[1] > target_rate[1]\
                       or miss_rate[2] > target_rate[2]:  # 逃窜率检定未通过
                        running = False
                        print('逃窜率检定未通过')  # test

                if info:

                    # info为True时 每秒更新1次info
                    # make_info()
                    miss_rate = [enemy.miss[0] / enemy.create[1],
                                 enemy.miss[1] / enemy.create[1],
                                 enemy.miss[2] / enemy.create[2]]
                    miss_rate_str = ['%.1f' %
                                     (x * 100) + r'%' for x in miss_rate]
                    target_rate_str = ['%.1f' %
                                       (x * 100) + r'%' for x in target_rate]

                    killinfo = 'kill={} {} {}'.format(
                        kill[0], kill[1], kill[2])
                    missinfo = 'miss={} {} {}'.format(
                        enemy.miss[0], enemy.miss[1], enemy.miss[2])
                    targetinfo = 'target={} {} {}'.format(
                        target_rate_str[0], target_rate_str[1], target_rate_str[2])
                    rateinfo = 'rate={} {} {}'.format(
                        miss_rate_str[0], miss_rate_str[1], miss_rate_str[2])
                    # bonuslevelinfo ='bonus={}'.format(bonus_level)

                if rpcount_second == 0:
                    me.rebornprotect = False
                else:
                    rpcount_second -= 1

                if count_second - supply_count_second == supply_gap:  # 补给间隔到了
                    if not paused and not silence:
                        supply_sound.play()
                    supply_count_second = count_second
                    randsupply = randint(0, 3)
                    if randsupply == 0:
                        bomb_supply.reset()
                    elif randsupply == 1:
                        life_supply.reset()
                    elif randsupply == 2:
                        bullet_supply.reset()
                    else:
                        theworld_supply.reset()

                if count_second - bullet2_count_second ==\
                   bullet2_duration:  # 双子弹持续时间结束
                    if not me.wudi:
                        is_double_bullet = False

                if count_second - bullet3_count_second == bullet3_duration:
                    # 超级子弹持续时间结束
                    is_super_bullet = False

        screen.blit(background, (0, bg_posy))

        # 根据得分提升难度
        if level == 1 and score > levelup_score[0]:
            level = 2
            supply_count_second = count_second
            supply_gap -= 4
            if not paused and not silence:
                upgrade_sound.play()
            # 小+3 中+2 大+1
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            # 小 加速
            increase_speed(small_enemies, 1)
        elif level == 2 and score > levelup_score[1]:
            level = 3
            supply_count_second = count_second
            supply_gap -= 4
            if not paused and not silence:
                upgrade_sound.play()
            # 小+5 中+3 大+2
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 小中 加速
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)
        elif level == 3 and score > levelup_score[2]:
            level = 4
            supply_count_second = count_second
            supply_gap -= 3
            if not paused and not silence:
                upgrade_sound.play()
            # 小+5 中+3 大+2
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 小中 加速
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)
        elif level == 4 and score > levelup_score[3]:
            level = 5
            supply_count_second = count_second
            supply_gap -= 2
            if not paused and not silence:
                upgrade_sound.play()
            # 小+5 中+3 大+2
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 小中 加速
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)

        elif level == 5:

            if score - target_score >= 100000:  # 额外关卡
                bonus_level += 1
                target_score += 100000
                target_rate[0] *= 0.9
                target_rate[1] *= 0.9
                target_rate[2] *= 0.9

                if not paused and not silence:
                    upgrade_sound.play()

        if not paused:

            # theworld逻辑
            if is_theworld:
                theworld_duration -= 1
                if not theworld_duration:
                    theworld_duration = 300
                    is_theworld = False

            # 检测键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveup()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.movedown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveleft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveright()

            # 尝试使背景循环移动 worked well
            if bg_posy >= 0:
                bg_posy = -700
            bg_posy += .5

            # 依次渲染 背景-大中小敌机-本体
            # 背景
            screen.blit(background, (0, bg_posy))

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                if not is_theworld:
                    bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    if not paused and not silence:
                        get_bomb_sound.play()
                    if bomb_num < 6:  # 设置最大全屏炸弹数量为6
                        bomb_num += 1
                    bomb_supply.active = False

            # 绘制双子弹补给并检测是否获得
            if bullet_supply.active:
                if not is_theworld:
                    bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    if not paused and not silence:
                        get_bullet_sound.play()
                    if is_double_bullet:
                        is_super_bullet = True
                        bullet_supply.active = False
                        bullet3_count_second = count_second
                    else:
                        is_double_bullet = True
                        bullet_supply.active = False
                        bullet2_count_second = count_second

            # 绘制生命+1补给并检测是否获得
            if life_supply.active:
                if not is_theworld:
                    life_supply.move()
                screen.blit(life_supply.image, life_supply.rect)
                if pygame.sprite.collide_mask(life_supply, me):
                    if not paused and not silence:
                        get_life_sound.play()
                    if me.life < 6:  # 设置最大备用生命数量为6
                        me.life += 1
                    life_supply.active = False

            # 绘制theworld补给并检测是否获得
            if theworld_supply.active:
                if not is_theworld:
                    theworld_supply.move()
                screen.blit(theworld_supply.image, theworld_supply.rect)
                if pygame.sprite.collide_mask(theworld_supply, me):
                    if not paused and not silence:
                        theworld_sound.play()
                    is_theworld = True
                    theworld_supply.active = False
                    # 补给 重生保护 相应增加5秒
                    supply_count_second += 5
                    rpcount_second += 5
                    bullet2_count_second += 5
                    bullet3_count_second += 5

            # 发射子弹
            if not delay % 10:
                if not paused and not silence and not is_theworld:
                    bullet_sound.play()

                if is_super_bullet:
                    bullets = bullet3
                    bullets[bullet3_index].reset(
                        (me.rect.centerx - 63, me.rect.centery))
                    bullets[bullet3_index +
                            1].reset((me.rect.centerx - 23, me.rect.centery))
                    bullets[bullet3_index +
                            2].reset((me.rect.centerx + 23, me.rect.centery))
                    bullets[bullet3_index +
                            3].reset((me.rect.centerx + 63, me.rect.centery))
                    bullet3_index = (bullet3_index + 4) % bullet3_num
                elif is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset(
                        (me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index +
                            1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num

            # 子弹命中检测
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(
                        b, enemies, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        e.energy -= 1
                        e.hit = True
                        if e.energy == 0:
                            e.active = False

            # 大敌机
            for each in big_enemies:
                if not each.active:
                    # 毁灭
                    if e3_destroy_index == 0:
                        if not paused and not silence:
                            enemy3_down_sound.play()
                    if not (delay % 3):
                        screen.blit(
                            each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            kill[0] += 1
                            each.reset()

                else:
                    if not is_theworld:
                        each.move()
                    if not delay % 5:
                        each.hit = False
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                    else:
                        if delay // 5 % 2:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(
                        screen,
                        BLACK,
                        (each.rect.left,
                         each.rect.top - 5),
                        (each.rect.right,
                         each.rect.top - 5),
                        2)
                    # 当生命大于20% 绿色 否则红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(
                        screen,
                        energy_color,
                        (each.rect.left,
                         each.rect.top -
                         5),
                        (each.rect.left +
                         each.rect.width *
                         energy_remain,
                         each.rect.top -
                         5),
                        2)

                    # 即将出现时播放提醒音效
                    if each.rect.bottom == -50:
                        if not paused and not silence:
                            enemy3_fly_sound.play(-1)

            # 中敌机
            for each in mid_enemies:
                if not each.active:
                    # 毁灭
                    if e2_destroy_index == 0:
                        if not paused and not silence:
                            enemy2_down_sound.play()
                    if not (delay % 3):
                        screen.blit(
                            each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            kill[1] += 1
                            each.reset()

                else:
                    if not is_theworld:
                        each.move()
                    if not delay % 5:
                        each.hit = False
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        # each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    # 绘制血槽
                    pygame.draw.line(
                        screen,
                        BLACK,
                        (each.rect.left,
                         each.rect.top - 5),
                        (each.rect.right,
                         each.rect.top - 5),
                        2)
                    # 当生命大于20% 绿色 否则红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(
                        screen,
                        energy_color,
                        (each.rect.left,
                         each.rect.top -
                         5),
                        (each.rect.left +
                         each.rect.width *
                         energy_remain,
                         each.rect.top -
                         5),
                        2)

            # 小敌机
            for each in small_enemies:
                if not each.active:
                    # 毁灭
                    if e1_destroy_index == 0:
                        if not paused and not silence:
                            enemy1_down_sound.play()
                    if not (delay % 3):
                        screen.blit(
                            each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            kill[2] += 1
                            each.reset()

                else:
                    if not is_theworld:
                        each.move()
                    screen.blit(each.image, each.rect)

            # 检测我方飞机是否撞了
            enemies_down = pygame.sprite.spritecollide(
                me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down:
                if not me.wudi and not me.rebornprotect:  # cheating line###
                    me.active = False
                for e in enemies_down:
                    e.active = False

            # 本体
            # 渲染本体时切换尾气有无 每5tick切换1次
            if me.active:
                if not me.rebornprotect:
                    if delay // 5 % 2:
                        screen.blit(me.image1, me.rect)
                    else:
                        screen.blit(me.image2, me.rect)
                else:
                    if delay % 10 < 7:  # 绘制7帧 空白3帧 人造闪烁
                        screen.blit(me.image1, me.rect)
            else:
                # 毁灭
                if not (delay % 3):
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        me.reset()
                        me.rebornprotect = True
                        rpcount_second = 3
                        me.life -= 1
                        if me.life == 0:
                            me.active = False
                            print('Game over')  # test
                            running = False  # test
        # 绘制炸弹库存
        bomb_text = bomb_font.render(' x {}'.format(bomb_num), True, WHITE)
        screen.blit(bomb_image, (10, height - bomb_rect.height - 10))
        screen.blit(
            bomb_text,
            (10 +
             bomb_rect.width,
             height -
             bomb_rect.height -
             13))

        # 绘制剩余生命数量
        if me.life:
            for i in range(me.life):
                screen.blit(me.life_image,
                            (width - 10 - (i + 1) * me.life_rect.width,
                             height - 10 - me.life_rect.height))
        # 绘制得分
        score_text = score_font.render('Score : {}'.format(score), True, WHITE)
        screen.blit(score_text, (10, 5))

        # 绘制详细信息

        if info:
            write_info()

            '''print('kill=',kill)
                    print('miss=',enemy.miss)
                    print('create',enemy.create)
                    miss_rate = [enemy.miss[0]/enemy.create[1],\
                                enemy.miss[1]/enemy.create[1],\
                                enemy.miss[2]/enemy.create[2]]
                    miss_rate_str = [str(x/100)+r'%' for x in miss_rate]
                    print('逃窜率:',miss_rate_str)'''
        # 暂停按钮
        screen.blit(paused_image, paused_rect)
        # 音乐开关
        screen.blit(volume_image, volume_rect)

        delay += 1
        if delay == 100:
            delay = ACTIVEEVENT

        pygame.display.flip()

        clock.tick(60)

    # 结束后 按q退出 按r重开 60秒后退出
    # 搞个前10的记录
    # 绘制结束界面

    '''
    ending_font = pygame.font.Font(r'font\fs.ttf',24)
    ending_font.set_bold(True)
    ending_text1 = ending_font.render('游戏结束',True,WHITE)
    ending_text2 = ending_font.render('按r重新开始',True,WHITE)
    ending_text3 = ending_font.render('按q结束',True,WHITE)

    screen.blit(ending_text1,(width//2-48,height//2-150))
    screen.blit(ending_text2,(width//2-72,height//2-120))
    screen.blit(ending_text3,(width//2-48,height//2-90))

    writeline(text='游戏结束',bold=True,size=24,alter_y=-150)
    writeline(text='按r重新开始',bold=True,size=24,alter_y=-120)
    writeline(text='按q结束',bold=True,size=24,alter_y=-90)
    writeline(text='按t显示排行榜',bold=True,size=24,alter_y=80)
    '''

    ranking = False

    def mixblit():
        # 渲染队列
        screen.blit(background, (0, bg_posy))
        for b_367 in bullets:
            if b_367.active:
                screen.blit(b_367.image, b_367.rect)
        for each_367 in enemies:
            if each_367.active:
                screen.blit(each_367.image, each_367.rect)
        screen.blit(me.destroy_images[3], me.rect)
        screen.blit(bomb_image, (10, height - bomb_rect.height - 10))
        screen.blit(
            bomb_text,
            (10 +
             bomb_rect.width,
             height -
             bomb_rect.height -
             13))
        for i_367 in range(me.life):
            screen.blit(me.life_image,
                        (width - 10 - (i_367 + 1) * me.life_rect.width,
                         height - 10 - me.life_rect.height))
        screen.blit(score_text, (10, 5))
        # screen.blit(paused_image,paused_rect)

    # 定义游戏结束界面
    def shift_to_gameover():

        mixblit()

        writeline(text='游戏结束', bold=True, size=36, alter_y=-200)
        writeline(text='按r重新开始', bold=True, size=36, alter_y=-150)
        writeline(text='按t查看排行榜', bold=True, size=36, alter_y=-100)
        writeline(text='按q结束', bold=True, size=36, alter_y=+100)

    # 定义排行榜界面

    def shift_to_toplist():
        screen.blit(background, (0, bg_posy))
        screen.blit(score_text, (10, 5))
        writeline(text='排名 ', color_367=WHITE, alter_x=-200, alter_y=-200)
        writeline(text='英雄名', color_367=WHITE, alter_x=-80, alter_y=-200)
        writeline(text='分数', color_367=WHITE, alter_x=100, alter_y=-200)
        mark_me = 0
        for i_367 in range(len(new_record)):
            if new_record[i_367][0] == username and new_record[i_367][1] == score and not mark_me:
                writeline(
                    text='NO.{} '.format(
                        i_367 + 1),
                    color_367=GOLDEN,
                    alter_x=-200,
                    alter_y=-150 + 30 * i_367)
                writeline(
                    text=str(
                        new_record[i_367][0]),
                    color_367=GOLDEN,
                    alter_x=-80,
                    alter_y=-150 + 30 * i_367)
                writeline(
                    text=str(
                        new_record[i_367][1]),
                    color_367=GOLDEN,
                    alter_x=100,
                    alter_y=-150 + 30 * i_367)
                mark_me = 1
            else:
                writeline(
                    text='NO.{} '.format(
                        i_367 + 1),
                    alter_x=-200,
                    alter_y=-150 + 30 * i_367)
                writeline(
                    text=str(
                        new_record[i_367][0]),
                    alter_x=-80,
                    alter_y=-150 + 30 * i_367)
                writeline(
                    text=str(
                        new_record[i_367][1]),
                    alter_x=100,
                    alter_y=-150 + 30 * i_367)
        writeline(text='按b返回上级菜单', bold=True, size=36, alter_y=200)
        writeline(text='按c清空排行榜', bold=True, size=36, alter_y=250)

    # 读取排行榜记录
    with open(r'record.txt', 'rb') as f:
        try:
            record_list = pickle.load(f)
        except EOFError:
            record_list = []
            for i in range(10):
                record_list.append(['you know who', 1000])

    shift_to_gameover()

    if score > record_list[-1][1]:  # 如果比最后1名分高
        ranking = True
        writeline(text='成绩不错,入榜了哦', bold=True, size=24, alter_y=50)
        username = 'you know who'
        pygame.display.flip()

        username = enterbox(msg='英雄大名:', title='万古流芳!', default='you know who')
        while username and len(username) > 12:
            username = enterbox(
                msg=r'英雄名有点长,不太好记啊(12字符以内应该记得住):',
                title='必须万古流芳!',
                default='you know who')
        if not username:
            username = 'you know who'
        # 用easygui.enterbox代替改造的轮子进行输入

        record_list.append([username, score])
        record_list.sort(reverse=True, key=lambda x: x[1])
        if len(record_list) > 10:
            new_record = record_list[0:10]
        else:
            new_record = record_list
        print(new_record)  # test
        with open(r'record.txt', 'wb') as f:
            pickle.dump(new_record, f)
    else:
        new_record = record_list

    if not ranking:
        shift_to_gameover()
    else:
        shift_to_toplist()

    tempcount = 0
    while tempcount < 1800:

        if not ranking:  # 在游戏结束界面
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_t:
                    ranking = True
                    shift_to_toplist()
                if event.type == KEYDOWN and event.key == K_r:
                    main()
                if event.type == KEYDOWN and event.key == K_q:
                    print('user quit with K_q')  # test
                    pygame.quit()
                    sys.exit()

        elif ranking:  # 在排行榜界面
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_b:
                    ranking = False
                    shift_to_gameover()
                if event.type == KEYDOWN and event.key == K_c:
                    # 按c清空排行榜
                    new_record = []
                    for i in range(10):
                        new_record.append(['you know who', 1000])
                    with open(r'record.txt', 'wb') as f:
                        pickle.dump(new_record, f)
                    cheatonsound.play()
                    shift_to_toplist()

        tempcount += 1

        pygame.display.flip()
        clock.tick(30)

    if tempcount == 1800:
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    '''try:
        main()

    except SystemExit:
        pass
    except BaseException:
        traceback.print_exc()
        pygame.quit()
        input()'''
    main()
