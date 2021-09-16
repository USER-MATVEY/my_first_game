import pygame
from pygame import *
from random import randint

FPS = 60
lost_ships = 0
score = 0
Color = (255, 255, 255)

update_level = 1
common_HP = 1
hard_HP = 2
super_HP = 4

flag = True
hard_flag_1 = True
hard_flag_2 = True
final_flag1 = True
final_flag2 = True

reload = False
reload_timer = 0
bullet_counter = 0

Enemy_bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, start_x, start_y, sprite_hight, sprite_weight, hp, sprite_class):
        super().__init__()
        self.sprite_class = sprite_class
        self.HP = hp
        self.sprite_hight = sprite_hight
        self.sprite_weight = sprite_weight
        self.image = transform.scale(image.load(player_image), (self.sprite_hight, self.sprite_weight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.flag = True

    def show_sprite(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move_player(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 10:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < window_weidth - 60:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Enemy_Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 1000 and self.sprite_class == 'Asteroid':
            self.rect.y = randint(-150, -100)
            self.rect.x = randint(50, window_weidth - 100)
            self.speed = 2 + randint(-1, 2)

        if self.rect.y >= 1100:
            self.kill()



class Sphera(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 1000:
            self.kill()

class Enemy(GameSprite):
    def __init__(self, player_image, player_speed, start_x, start_y, sprite_hight, sprite_weight, hp, sprite_class, piu_timer):
        super().__init__(player_image, player_speed, start_x, start_y, sprite_hight, sprite_weight, hp, sprite_class)
        self.piu_timer = piu_timer

    def update(self):
        global lost_ships
        self.rect.y += self.speed
        if self.rect.y >= window_hight:
            self.rect.y = randint(-200, -100)
            self.rect.x = randint(50, window_weidth - 100)
            self.speed = 1 + randint(1, 3)
            lost_ships += 1

    def shot(self):
            bullet = Enemy_Bullet('enemy_bullet.png', 5, self.rect.x + 50, self.rect.y + 100, 10, 20, 0, 'Bullet')
            Enemy_bullets.add(bullet)

    def die(self):
        global score, hard_HP, super_HP
        self.rect.x = randint(50, window_weidth - 100)
        self.rect.y = randint(-200, -100) - 100
        self.speed = 1 + randint(1, 3)
        score += 1

        if self.sprite_class == 'Hard':
            self.HP = hard_HP
            score += 1
            if self.speed >= 2:
                self.speed -= 1

        elif self.sprite_class == 'Super_Hard':
            self.HP = super_HP
            score += 3
            if self.speed >= 3:
                self.speed -= 2

def piu(update_level):
    if update_level == 1:
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 40, player.rect.y-10, 10, 20, 0, 'Bullet'))
    elif update_level == 2:
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 25, player.rect.y-10, 10, 20, 0, 'Bullet'))
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 55, player.rect.y-10, 10, 20, 0, 'Bullet'))
    elif update_level == 3:
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 20, player.rect.y-10, 10, 20, 0, 'Bullet'))
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 40, player.rect.y-25, 10, 20, 0, 'Bullet'))
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 60, player.rect.y-10, 10, 20, 0, 'Bullet'))
    elif update_level >= 4:
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 10, player.rect.y - 25, 10, 20, 0, 'Bullet'))
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 30, player.rect.y-10, 10, 20, 0, 'Bullet'))
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 50, player.rect.y-10, 10, 20, 0, 'Bullet'))
        Bullets.add(Bullet('bullet.png', 5, player.rect.x + 70, player.rect.y - 25, 10, 20, 0, 'Bullet'))

def level_up(score):
    global flag, hard_flag_1, hard_flag_2, final_flag1, final_flag2

    if score >= 20 and flag:
        flag = False
        for i in range(3):
            Enemy_bullets.add(
                Enemy_Bullet('asteroid.png', 2 + randint(-1, 2), randint(50, window_weidth - 100), randint(-150, -100), 50, 50, 0,
                             'Asteroid'))

    elif score >= 50 and hard_flag_1:
        Enemies.append(Hard_enemy1)
        Enemies.append(Hard_enemy2)
        Enemies.append(Hard_enemy3)
        hard_flag_1 = False

    elif score >= 70 and hard_flag_2:
        Enemies.pop(0)
        Enemies.pop(1)
        Enemies.append(super_enemy)
        Enemies.append(super_enemy2)
        hard_flag_2 = False

    elif score >= 120 and final_flag1:
        Enemies.pop(5)
        Enemies.append(shotting_enemy1)
        final_flag1 = False

    elif score >= 190 and final_flag2:
        Enemies.pop(2)
        Enemies.pop(3)
        Enemies.append(shotting_enemy2)
        Enemies.append(shotting_enemy3)
        final_flag2 = False

def reset_game():
    global finish, score, lost_ships, update_level, hard_flag_1, hard_flag_2, final_flag1, final_flag2, bullet_counter, flag
    finish = False
    for enemy in Enemies:
        enemy.rect.x = randint(50, window_weidth - 100)
        enemy.rect.y = randint(-200, -100) - 100
    Bullets.empty()
    Enemy_bullets.empty()
    player.rect.x = 600
    score = 0
    lost_ships = 0
    update_level = 1
    bullet_counter = 0
    flag = True
    hard_flag_1 = True
    hard_flag_2 = True
    final_flag1 = True
    final_flag2 = True
    reload = False
    bullet_counter = 0
    reload_timer = 0
    Enemies.clear()
    for i in range(5):
        Enemies.append(
            Enemy('enemy.png', 1 + randint(1, 3), randint(50, window_weidth - 100), randint(-200, -100), 90, 90, 1, 'Common', 0))


mixer.init()
mixer.music.load('fon_space.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()
shot = mixer.Sound('shot.ogg')
enemy_shot = mixer.Sound('enemy_shot.ogg')
shot.set_volume(0.2)
enemy_shot.set_volume(0.2)

window_hight = 1000
window_weidth = 1300

main_win = display.set_mode((window_weidth, window_hight))
display.set_caption('Шутер')
background = transform.scale(image.load('background.jpg'), (window_weidth, window_hight))

font.init()
font1 = font.Font(None, 40)
lose_font = font.Font(None, 75)

lose_text = lose_font.render('YOU LOSE! Press "spase" to restart.', True, (255, 0, 0))
reload_text = font1.render('///Reloading! Please wait///', True, Color)

player = Player('hero.png', 6, 600, 850, 90, 90, 1, 'Player')

Enemies = []
Asteroides = []
Bullets = sprite.Group()
Spheres = sprite.Group()

for i in range(5):
    Enemies.append(Enemy('enemy.png', 1 + randint(1, 3), randint(50, window_weidth - 100), randint(-200, -100), 90, 90, 1, 'Common', 0))

Hard_enemy1 = Enemy('enemy_2.png', 1 + randint(0, 1), randint(50, window_weidth - 100), randint(-400, -200), 110, 110, 2, 'Hard', 0)
Hard_enemy2 = Enemy('enemy_2.png', 1 + randint(0, 1), randint(50, window_weidth - 100), randint(-400, -200), 110, 110, 2, 'Hard', 0)
Hard_enemy3 = Enemy('enemy_2.png', 1 + randint(0, 1), randint(50, window_weidth - 100), randint(-400, -200), 110, 110, 2, 'Hard', 0)

super_enemy = Enemy('enemy_3.png', 1, randint(50, window_weidth - 100), randint(-600, -300), 140, 140, 4, 'Super_Hard', 0)
super_enemy2 = Enemy('enemy_3.png', 1, randint(50, window_weidth - 100), randint(-600, -300), 140, 140, 4, 'Super_Hard', 0)

shotting_enemy1 = Enemy('enemy_4.png', 1, randint(50, window_weidth - 100), randint(-600, -300), 100, 100, 4, 'Can_piu_piu', 0)
shotting_enemy2 = Enemy('enemy_4.png', 1, randint(50, window_weidth - 100), randint(-600, -300), 100, 100, 4, 'Can_piu_piu', 0)
shotting_enemy3 = Enemy('enemy_4.png', 1, randint(50, window_weidth - 100), randint(-600, -300), 100, 100, 4, 'Can_piu_piu', 1000)

#Enemy_Bullet('enemy_bullet.png', 5, self.rect.x + 50, self.rect.y + 100, 10, 20, 0, 'Bullet')

clock = pygame.time.Clock()
piu_timer = 0

game = True
finish = False

while game:
    keys_pressed = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
           game = False
        if e.type == MOUSEBUTTONDOWN:
            if reload == False:
                piu(update_level)
                shot.play()
                bullet_counter += 1

    if finish != True:
        lose = font1.render('Пропущено: ' + str(lost_ships), True, Color)
        score_text = font1.render('Счёт: ' + str(score), True, Color)

        level_up(score)

        main_win.blit(background, (0,0))
        main_win.blit(score_text, (50, 50))
        main_win.blit(lose, (50, 75))

        player.move_player()
        player.show_sprite()

        for enemy in Enemies:
            enemy.update()
            enemy.show_sprite()

        for asteroid in Asteroides:
            asteroid.update()
            asteroid.show_sprite()

        Bullets.draw(main_win)
        Bullets.update()
        Enemy_bullets.draw(main_win)
        Enemy_bullets.update()


        Spheres.draw(main_win)
        Spheres.update()

        for enemy in Enemies:
            if enemy.piu_timer >= 2000:
                enemy.piu_timer = 0
                enemy.shot()
                enemy_shot.play()

        for enemy in Enemies:
            for bullet in Bullets:

                if sprite.collide_rect(enemy, bullet) and enemy.HP == 1:
                    sphere_drop_rate = randint(1, 1000)
                    sphere_class = randint(1, 4)

                    if sphere_drop_rate >= 950:
                        sphere = Sphera('sphere_DAM_up.png', 1, enemy.rect.x, enemy.rect.y, 30, 30, 1, 'sphere')
                        Spheres.add(sphere)

                    bullet.kill()
                    enemy.die()

                elif sprite.collide_rect(enemy, bullet):
                    enemy.HP -= 1
                    bullet.kill()

            if sprite.collide_rect(enemy, player):
                finish = True
                main_win.blit(lose_text, (200, 450))

        for sphere in Spheres:
            if sprite.collide_rect(player, sphere):
                sphere.kill()
                update_level += 1

        for en_bul in Enemy_bullets:
            if sprite.collide_rect(player, en_bul):
                finish = True
                main_win.blit(lose_text, (200, 450))

        if bullet_counter >= 10:
            reload = True
            reload_timer += clock.get_time()
            main_win.blit(reload_text, (450, 950))

        if reload_timer >= 3000:
            reload = False
            bullet_counter = 0
            reload_timer = 0

        clock.tick(FPS)
        display.update()
        for enemy in Enemies:
            if enemy.sprite_class == 'Can_piu_piu':
                enemy.piu_timer += clock.get_time()

    if finish == True and keys_pressed[K_SPACE]:
        reset_game()
