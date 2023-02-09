import pygame
import random
import math
import sys
from pygame import mixer

WIDTH = 800
HEIGHT = 600
AIM_SIZE = (50, 50)
WHITE = (255, 255, 255)
BLUE = (52, 78, 91)
RED = (255, 0, 0)


def score_text():
    """
    Displays current score
    """
    img = font.render(f'Score:{score}', True, 'white')
    screen.blit(img, (10, 10))


def gameover():
    '''
    Displays text
    '''
    img_gameover = font_gameover.render('GAME OVER', True, 'white')
    screen.blit(img_gameover, (200, 250))


def laser_sound():
    bulletSound = mixer.Sound('laser.wav')
    bulletSound.play()


def summoning_aim():
    """
    This function sets aim image.
    """
    aim["surf"] = pygame.image.load(aim["file"])
    aim["surf"] = pygame.transform.scale(aim["surf"], AIM_SIZE)
    aim["rect"] = aim["surf"].get_rect()


def menu():
    """
    Displays starting menu
    """
    screen.blit(background, (0, 0))
    myfont1 = pygame.font.Font('freesansbold.ttf', 58)
    myfont2 = pygame.font.Font('freesansbold.ttf', 38)
    msg1 = myfont1.render("SPACE INVADERS", True, WHITE)
    msg2 = myfont2.render("press enter to start", True, WHITE)

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    intro = False
        screen.blit(msg1, (140, 120))
        screen.blit(msg2, (210, 400))
        pygame.display.flip()


def options():
    """
    Allows user to choose particular level of difficulty and to set controls
    """
    global no_of_aliens
    global switch
    global alienspeed
    screen.blit(background, (0, 0))
    myfont1 = pygame.font.Font('freesansbold.ttf', 58)
    myfont3 = pygame.font.Font('freesansbold.ttf', 44)
    myfont2 = pygame.font.Font('freesansbold.ttf', 38)
    title = myfont3.render("Pick difficulty: ", True, WHITE)
    title_box = title.get_rect()
    title_box.midtop = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.05)).midbottom
    option1 = myfont2.render("easy", True, WHITE)
    option2 = myfont2.render("normal", True, WHITE)
    option3 = myfont2.render("hard", True, WHITE)
    controls = myfont3.render("Select controls: ", True, WHITE)
    controls_box = controls.get_rect()
    controls_box.center = (WIDTH/2, HEIGHT/2)
    mouse_button = myfont2.render("mouse", True, WHITE)
    keyboard_button = myfont2.render("keyboard", True, WHITE)
    enter = myfont2.render("Press enter to continue ", True, WHITE)
    enter_box = enter.get_rect()
    easy_box = option1.get_rect()
    normal_box = option2.get_rect()
    hard_box = option3.get_rect()
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    intro = False
                if event.key == pygame.K_e:
                    option1 = myfont2.render("easy", True, RED)
                    option2 = myfont2.render("normal", True, WHITE)
                    option3 = myfont2.render("hard", True, WHITE)
                    no_of_aliens = 6
                    alienspeed = 1
                if event.key == pygame.K_n:
                    option1 = myfont2.render("easy", True, WHITE)
                    option2 = myfont2.render("normal", True, RED)
                    option3 = myfont2.render("hard", True, WHITE)
                    no_of_aliens = 8
                    alienspeed = 2
                if event.key == pygame.K_h:
                    option1 = myfont2.render("easy", True, WHITE)
                    option2 = myfont2.render("normal", True, WHITE)
                    option3 = myfont2.render("hard", True, RED)
                    no_of_aliens = 10
                    alienspeed = 2.5
                if event.key == pygame.K_k:
                    mouse_button = myfont2.render("mouse", True, WHITE)
                    keyboard_button = myfont2.render("keyboard", True, RED)

                if event.key == pygame.K_m:
                    mouse_button = myfont2.render("mouse", True, RED)
                    keyboard_button = myfont2.render("keyboard", True, WHITE)
                    switch = "mouse"
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                mouse = pygame.mouse.get_pos()
                if click[0] and easy_box.collidepoint(mouse):
                    option1 = myfont2.render("easy", True, RED)
                    option2 = myfont2.render("normal", True, WHITE)
                    option3 = myfont2.render("hard", True, WHITE)
                    alienspeed = 1
                    no_of_aliens = 6
                if click[0] and normal_box.collidepoint(mouse):
                    option1 = myfont2.render("easy", True, WHITE)
                    option2 = myfont2.render("normal", True, RED)
                    option3 = myfont2.render("hard", True, WHITE)
                    alienspeed = 2
                    no_of_aliens = 8
                if click[0] and hard_box.collidepoint(mouse):
                    option1 = myfont2.render("easy", True, WHITE)
                    option2 = myfont2.render("normal", True, WHITE)
                    option3 = myfont2.render("hard", True, RED)
                    alienspeed = 2.5
                    no_of_aliens = 10
                if click[0] and keyboard_button_box.collidepoint(mouse):
                    mouse_button = myfont2.render("mouse", True, WHITE)
                    keyboard_button = myfont2.render("keyboard", True, RED)
                if click[0] and mouse_button_box.collidepoint(mouse):
                    mouse_button = myfont2.render("mouse", True, RED)
                    keyboard_button = myfont2.render("keyboard", True, WHITE)
                    switch = "mouse"
        easy_box = option1.get_rect()
        easy_box.top = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.15)).bottom
        easy_box.left = WIDTH * 0.42

        normal_box = option2.get_rect()
        normal_box.top = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.25)).bottom
        normal_box.left = WIDTH * 0.42

        hard_box = option2.get_rect()
        hard_box.top = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.35)).bottom
        hard_box.left = WIDTH * 0.42

        keyboard_button_box = keyboard_button.get_rect()
        keyboard_button_box.midright = (controls_box.right - 20, WIDTH * 0.45)

        mouse_button_box = mouse_button.get_rect()
        mouse_button_box.midleft = (controls_box.left + 20, WIDTH * 0.45)

        enter_box.top = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.85)).bottom
        enter_box.left = WIDTH * 0.23

        screen.blit(title, title_box)
        screen.blit(option1, easy_box)
        screen.blit(option2, normal_box)
        screen.blit(option3, hard_box)
        screen.blit(controls, controls_box)
        screen.blit(mouse_button, mouse_button_box)
        screen.blit(keyboard_button, keyboard_button_box)
        screen.blit(enter, enter_box)

        pygame.display.flip()


if __name__ == "__main__":
    mixer.init()
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Space Invaders Game')

    background = pygame.image.load('space.jpg')
    spaceshipimg = pygame.image.load('spaceship.png')
    bulletimg = pygame.image.load('bullet.png')
    aim = {"file": "aim.png"}

    font = pygame.font.SysFont('Arial', 32, 'bold')
    font_gameover = pygame.font.SysFont('Arial', 64, 'bold')

    alienimg = []
    alienX = []
    alienY = []
    alienspeedX = []
    alienspeedY = []
    no_of_aliens = 6
    alienspeed = 0.5

    score = 0

    check = False
    bulletX = 386
    bulletY = 490

    spaceshipX = 370
    spaceshipY = 480
    changeX = 0
    running = True

    switch = "keys"
    fps = pygame.time.Clock()

    menu()
    options()
    for i in range(no_of_aliens):
        alienimg.append(pygame.image.load('ufo.png'))
        alienX.append(random.randint(0, 736))
        alienY.append(random.randint(30, 240))
        alienspeedX.append(-1)
        alienspeedY.append(40)
    if switch == "mouse":
        summoning_aim()
        pygame.mouse.set_visible(False)

    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if switch == "keys":
                if event.type == pygame.KEYDOWN:
                    """movement of the spaceship"""
                    if event.key == pygame.K_LEFT:
                        changeX = -3
                    if event.key == pygame.K_RIGHT:
                        changeX = 3
                    if event.key == pygame.K_SPACE:
                        if check is False:
                            laser_sound()
                            check = True
                            bulletX = spaceshipX+16

                if event.type == pygame.KEYUP:
                    changeX = 0
            else:
                mouse = pygame.mouse.get_pos()
                spaceshipX = mouse[0] - 32
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if check is False:
                        laser_sound()
                        check = True
                        bulletX = spaceshipX + 16
                aim["rect"].center = mouse
        """make sure that spaceship can't leave the screen"""
        spaceshipX += changeX
        if spaceshipX <= 0:
            spaceshipX = 0
        elif spaceshipX >= 736:
            spaceshipX = 736
        '''when alien gets close to the spaceship,
         the game ends and aliens disapear from the screen'''
        for i in range(no_of_aliens):
            if alienY[i] > 420:
                for j in range(no_of_aliens):
                    alienY[j] = 10000
                gameover()
                break
            '''when alines get close to the boarder thay move a step lower
             and change the direction of the movent'''
            alienX[i] += alienspeedX[i]
            if alienX[i] <= 0:
                alienspeedX[i] = alienspeed
                alienY[i] += alienspeedY[i]
            if alienX[i] >= 736:
                alienspeedX[i] = -alienspeed
                alienY[i] += alienspeedY[i]
            '''checking the distance between alien and bullet,
             and if it is lower the prticular value
             alien removed to the higher part of the screen'''
            distance = math.sqrt(math.pow(bulletX - alienX[i], 2) + math.pow(bulletY - alienY[i], 2))
            if distance < 27:
                explosion = mixer.Sound('explosion.wav')
                explosion.play()
                bulletY = 480
                check = False
                alienX[i] = random.randint(0, 736)
                alienY[i] = random.randint(30, 150)
                score += 1
            screen.blit(alienimg[i], (alienX[i], alienY[i]))
        if bulletY <= 0:
            bulletY = 490
            check = False
        if check:
            screen.blit(bulletimg, (bulletX, bulletY))
            bulletY -= 6
        if switch == "mouse":
            screen.blit(aim["surf"], aim["rect"])
        screen.blit(spaceshipimg, (spaceshipX, spaceshipY))
        score_text()
        pygame.display.update()
        fps.tick(200)
