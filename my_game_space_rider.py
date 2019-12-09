import pygame
import random

pygame.init()
window_width = 1080
window_height = 480
play_width = window_width-100
win = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
pygame.display.set_caption("space rider")
# bg = pygame.image.load("red_space.png")
bg = pygame.image.load("loophole.jpg")
# ship = pygame.image.load('spaceship.png')
ship = pygame.image.load('baseshipb.ico')
enemy_ship1 = pygame.image.load('saucer1b.ico')
enemy_ship2 = pygame.image.load('saucer2b.ico')
enemy_ship3 = pygame.image.load('saucer3b.ico')
enemy_ships = [enemy_ship1,enemy_ship2,enemy_ship3]
bulletSound = pygame.mixer.Sound('shoot.wav')
enemy_killed = pygame.mixer.Sound('invaderkilled.wav')
rider_killed = pygame.mixer.Sound('explosion.wav')
run = True
font = pygame.font.SysFont("comicsans", 30, True)
score = 0
kills = 0
lives = 5


class rider_body(object):
    global keys, ship
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.vel = 5
        self.hitbox = (self.x + 17, self.y + 11, 21, 21)

    def move(self):
        if keys[pygame.K_LEFT] and self.x > 2:
            self.x -= self.vel
            win.blit(ship, (self.x, self.y))
        elif keys[pygame.K_RIGHT] and self.x < play_width - self.width - 2:
            self.x += self.vel
            win.blit(ship, (self.x, self.y))
        elif keys[pygame.K_UP] and self.y > 2:
            self.y -= self.vel
            win.blit(ship, (self.x, self.y))
        elif keys[pygame.K_DOWN] and self.y < window_height - 8:
            self.y += self.vel
            win.blit(ship, (self.x, self.y))
        self.hitbox = (self.x - 3, self.y - 4, 26, 24)


def redrawGameWindow():
    global rider, bullets_shooted, level
    win.blit(bg, (0, 0))
    kill = font.render("kills: " + str(kills), 1, (96, 32, 151))
    total_score = font.render("score: " + str(score), 1, (0, 25, 240))
    total_lives = font.render("Lives: " + str(lives), 1, (255, 0, 0))
    total_bullets = font.render("Bullets : " + str(50-bullets_shooted), 1, (255, 0, 0))
    Reload = font.render("Reload: R ", 1, (255, 0, 0))
    Level = font.render("level: "+str(level), 1, (255, 0, 0))
    win.blit(kill, (window_width - 150, 20))
    win.blit(total_score, (window_width - 150, 40))
    win.blit(total_lives, (window_width - 150, 60))
    win.blit(total_bullets, (window_width - 150, 80))
    win.blit(Level, (window_width - 150, 100))
    if bullets_shooted == 50 :
        win.blit(Reload, (window_width - 150, 120))
    win.blit(ship, (rider.x, rider.y))
    # pygame.draw.rect(win, (120, 0, 0), (rider.x, rider.y, rider.width, rider.height))
    # pygame.draw.rect(win, (0, 0, 0), rider.hitbox, 2)
    for bullet in bullets:
        bullet.draw(win)
    for e in enimes:
        e.draw(win)
    pygame.display.update()


class projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 5

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    global enemy_ships, level
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.vel = 0.5*level
        self.hitbox = (self.x - 3, self.y - 4, 26, 24)
        self.health = 2
        self.enemy_ship = enemy_ships[random.randint(0,len(enemy_ships)-1)]
    def draw(self, win):
        self.hitbox = (self.x - 3, self.y - 4, 26, 24)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)#hit box
        #health bars
        pygame.draw.rect(
            win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)
        )
        pygame.draw.rect(
            win,
            (0, 128, 0),
            (
                self.hitbox[0],
                self.hitbox[1] - 20,
                50 - ((50 / 2) * (2 - self.health)),
                10,
            ),
        )
        # pygame.draw.rect(win, (255, 200, 0), (self.x, self.y, self.width, self.height))
        win.blit(self.enemy_ship, (self.x, self.y))

    def hit(self):
        print("hit")


enimes = []
bullets = []
bullets_shooted = 0
shoot_interval = 0
enemy_interval = 0
level = 1
# run game
rider = rider_body(play_width - (play_width // 2), window_height - 10)
maxkills = 40

def reset():
    global bullets, enimes, rider, lives, kills, score, enemy_interval, shoot_interval, bullets_shooted, level, maxkills
    bullets = []
    enimes = []
    rider.x = play_width - play_width/2
    rider.y = window_height - 10
    enemy_interval = 0
    shoot_interval = 0
    bullets_shooted = 0
    lives = 5
    kills = 0
    score = 0
    level = 1
    maxkills = 40

def restart():
    # font1 = pygame.font.SysFont('comicsans', 100)
    text = font.render('Restart', 1, (255, 0, 0))
    Press = font.render('Y/N', 1, (255, 0, 0))
    win.blit(text, (window_width - (text.get_width()+5), 200))
    win.blit(Press, (window_width - (Press.get_width()+ 5), 220))
    pygame.display.update()
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if  keys[pygame.K_n]:
            pygame.quit()
        elif keys[pygame.K_y]:
            reset()
            break
def pause():
    # font1 = pygame.font.SysFont('comicsans', 100)
    continue_y = font.render('Continue - y', 1, (255, 0, 0))
     # = font.render('Y/N', 1, (255, 0, 0))
    exit = font.render('Exit - N', 1, (255, 0, 0))
    win.blit(continue_y, (window_width - (continue_y.get_width()+5), 200))
    win.blit(exit, (window_width - (exit.get_width()+5), 220))
    pygame.display.update()
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if  keys[pygame.K_n]:
            pygame.quit()
        elif keys[pygame.K_y]:
            break
while run:
    keys = pygame.key.get_pressed()
    clock.tick(30)
    if shoot_interval > 0:
        shoot_interval += 1
    if shoot_interval > 5:
        shoot_interval = 0
    if enemy_interval > 0:
        enemy_interval += 1
    if enemy_interval > 15:
        enemy_interval = 0
    if kills> maxkills :
        level +=1
        maxkills = maxkills*level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if keys[pygame.K_ESCAPE]:
        pause()
    for bullet in bullets:
        if bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    if keys[pygame.K_r]:
        bullets_shooted = 0
    if keys[pygame.K_SPACE] and not shoot_interval:
        for e in enimes:
            for bullet in bullets:

                if (
                    bullet.y - bullet.radius < e.hitbox[1] + e.hitbox[3]
                    and bullet.y + bullet.radius > e.hitbox[1]
                ):
                    if (
                        bullet.x + bullet.radius > e.hitbox[0]
                        and bullet.x - bullet.radius < e.hitbox[0] + e.hitbox[2]
                    ):
                        score += 10
                        if e.health > 1:
                            e.health -= 1
                            e.hit()
                        else:
                            enemy_killed.play()
                            kills += 1
                            bullets.pop(bullets.index(bullet))
                            if e in enimes:
                                enimes.pop(enimes.index(e))
        if bullets_shooted < 50:
            bulletSound.play()
            bullets_shooted += 1
            shoot_interval = 1
            bullets.append(
                projectile(
                    round(rider.x + rider.width // 2),
                    round(rider.y + rider.height // 2),
                    6,
                    (0, 0, 255),
                )
            )

    if len(enimes) < 5*level and not enemy_interval:
        enemy_interval = 1
        x = random.randint(1, play_width - 200)

        enimes.append(enemy(x, 0))
    for e in enimes:
        inter = random.randint(-1, 1)
        if e.y < window_height:
            e.y += e.vel
            x = e.x + inter
            if 2 < x < play_width:
                e.x = x
        else:
            enimes.pop(enimes.index(e))
            if lives > 1:
                lives -= 1
            else:
                restart()

    rider.move()
    for e in enimes:
        if (
            rider.y - rider.height < e.hitbox[1] + e.hitbox[3]
            and rider.y + rider.height > e.hitbox[1]
        ):
            if (
                rider.x + rider.width > e.hitbox[0]
                and rider.x - rider.width < e.hitbox[0] + e.hitbox[2]
            ):
                rider_killed.play()
                restart()
    redrawGameWindow()

pygame.quit()
