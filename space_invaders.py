"""
Space invaders game in pygame.
Images downloaded from cleanpng.com
Sounds downloaded from pixabay.com
"""
import pygame
import sys
import random
import math
from pygame import mixer

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (127, 127, 127)
WIDTH = 1024
HEIGHT = 770
SPACESHIP_SIZE = (100, 100)
ALIEN_SIZE = (130, 130)
LASER_SIZE = (50, 50)
AIM_SIZE = (50, 50)
LASER_FREQUENCY = 70
SPACESHIP_STEP = 5
LASER_STEP = 10
MIN_SPAWN_Y = -450
MAX_SPAWN_Y = -50
BREAK_TIME = 200


def range_of_movement():
    """
    This function sets range of the movement of the spaceship on the screen.
    """
    if spaceship["rect"].left < scr.left:
        spaceship["rect"].left = scr.left
    if spaceship["rect"].right > scr.right:
        spaceship["rect"].right = scr.right
    if spaceship["rect"].bottom > scr.bottom:
        spaceship["rect"].bottom = scr.bottom
    if spaceship["rect"].top < (HEIGHT / 2):
        spaceship["rect"].top = (HEIGHT / 2)


def summoning_laser():
    """
    This function generate laser and append it to the object list.
    """
    red_laser_beam["surf"] = pygame.image.load(red_laser_beam["file"])
    red_laser_beam["surf"] = pygame.transform.scale(red_laser_beam["surf"],
                                                    LASER_SIZE)
    red_laser_beam["rect"] = red_laser_beam["surf"].get_rect()
    objects.append(red_laser_beam)


def summoning_aim():
    """
    This function sets aim image.
    """
    aim["surf"] = pygame.image.load(aim["file"])
    aim["surf"] = pygame.transform.scale(aim["surf"], AIM_SIZE)
    aim["rect"] = aim["surf"].get_rect()


def shoot():
    """
    This function places laser in front of spaceship and play sound effect.
    """
    summoning_laser()
    red_laser_beam["rect"].midbottom = (spaceship["rect"].centerx,
                                        spaceship["rect"].top + 25)
    mixer.music.play()


def moving_laser():
    """
    This function move laser and sets break between shots.
    """
    global bullet_on_screen
    global wait_to_shoot
    global timer_laser

    if red_laser_beam in objects:
        if bullet_on_screen == "go":
            red_laser_beam["rect"] = \
                red_laser_beam["rect"].move((0, -LASER_STEP))
        # checking if laser is out of screen
        if red_laser_beam["rect"].bottom < scr.top:
            bullet_on_screen = "stop"
            objects.remove(red_laser_beam)

    # laser timer
    if wait_to_shoot == "stop":
        timer_laser += 1
        if (timer_laser % LASER_FREQUENCY) == 0:
            wait_to_shoot = "go"


def collision():
    """
    This function detects collisions of laser and spaceship with alien
    and then move them out of screen.
    """
    global your_score
    if red_laser_beam in objects:
        for alien in aliens:
            if alien["rect"].collidepoint(red_laser_beam["rect"].center):
                alien["rect"].midtop = (WIDTH * 2, HEIGHT)
                red_laser_beam["rect"].centerx = WIDTH * 3
                your_score += vel_y
    for alien in aliens:
        if spaceship["rect"].collidepoint(alien["rect"].center):
            alien["rect"].center = (WIDTH * 2, HEIGHT)
            game_over()


def summoning_spaceship():
    """
    This function displays spaceship in proper position.
    """
    spaceship["surf"] = pygame.image.load(spaceship["file"])
    spaceship["surf"] = pygame.transform.scale(spaceship["surf"],
                                               SPACESHIP_SIZE)
    spaceship["rect"] = spaceship["surf"].get_rect()
    spaceship["rect"].midbottom = scr.midbottom


def summoning_aliens():
    """
    This function summons aliens above the screen and
    protects from overlapping.
    """
    # overlapping protection
    num_aliens = 5
    alien_circles.clear()
    while num_aliens > 0:
        x = random.randint(int(ALIEN_SIZE[0] / 2),
                           WIDTH - int(ALIEN_SIZE[0] / 2))
        y = random.randint(MIN_SPAWN_Y, MAX_SPAWN_Y)
        radius = ALIEN_SIZE[0] * (2 ** 0.5)
        overlap = False
        for alien_circle in alien_circles:
            distance = ((alien_circle[0] - x) ** 2
                        + (alien_circle[1] - y) ** 2) ** 0.5
            if distance < radius:
                overlap = True
                break
        if overlap:
            continue
        alien_circles.append((x, y))
        num_aliens -= 1

    # placing aliens in earlier generated points
    for i, alien in enumerate(aliens):
        alien["origin_surf"] = pygame.image.load(alien["file"])
        alien["origin_surf"] = pygame.transform.scale(alien["origin_surf"],
                                                      ALIEN_SIZE)
        angle = math.atan(vel_x / vel_y)
        alien["angle"] = 180 * math.atan(vel_x / vel_y) / math.pi
        scale = 1 / (math.cos(angle) + math.sin(angle))
        if i % 2 == 0:
            alien["vel"] = [vel_x, vel_y]
            alien["surf"] = pygame.transform.rotozoom(alien["origin_surf"],
                                                      alien["angle"], scale)
        else:
            alien["vel"] = [-vel_x, vel_y]
            alien["surf"] = pygame.transform.rotozoom(alien["origin_surf"],
                                                      -alien["angle"], scale)
        alien["origin_rect"] = alien["origin_surf"].get_rect()
        alien["rect"] = alien["origin_rect"].copy()
        alien["rect"].center = alien["surf"].get_rect().center
        alien["surf"] = alien["surf"].subsurface(alien["rect"]).copy()
        alien["rect"].center = (alien_circles[i][0], alien_circles[i][1])
        objects.append(alien)
        if i == 0:
            print(angle, alien["angle"], scale)


def moving_aliens():
    """
    This function controls movement of all aliens
    and check if alien reached bottom of screen.
    """
    global lives
    global timer_wave

    angle = math.atan(vel_x / vel_y)
    scale = 1 / (math.cos(angle) + math.sin(angle))

    if black_alien or blue_alien or gray_alien \
            or green_alien or purple_alien in objects:
        for alien in aliens:
            alien["rect"] = alien["rect"].move(alien["vel"])
            if alien["rect"].left < scr.left:
                alien["vel"][0] = -alien["vel"][0]
                alien["surf"] = pygame.transform.rotozoom(alien["origin_surf"],
                                                          alien["angle"],
                                                          scale)

            if alien["rect"].right > scr.right:
                alien["vel"][0] = -alien["vel"][0]
                alien["surf"] = pygame.transform.rotozoom(alien["origin_surf"],
                                                          -alien["angle"],
                                                          scale)
            if alien in objects:
                if alien["rect"].top > scr.bottom:
                    objects.remove(alien)
                    if alien["rect"].right < scr.right and \
                            alien["rect"].left > scr.left:
                        lives -= 1
    else:
        timer_wave = "start"


def score():
    """
    This function displays number of wave and remaining lives.
    """
    left_score_text = my_score_font.render(f"Waves: {wave}", True, WHITE)
    right_score_text = my_score_font.render(f"Lives: {lives}", True, WHITE)
    central_score_text = my_score_font.render(f"Score: {your_score}",
                                              True, WHITE)
    window.blit(left_score_text, (20, HEIGHT - 40))
    window.blit(right_score_text, (WIDTH * (27 / 32), HEIGHT - 40))
    window.blit(central_score_text,
                (WIDTH / 2 - central_score_text.get_width() / 2, HEIGHT - 40))


def game_over():
    """
    This function displays end game screen.
    """
    global work
    my_over_font = pygame.font.Font('freesansbold.ttf', 70)
    over_text = my_over_font.render("GAME OVER", True, RED)
    your_score_text = \
        my_score_font.render(f"Your Final Score: {your_score}", True, WHITE)
    text_placement = (WIDTH / 2 - over_text.get_width() / 2, HEIGHT / 3)
    your_score_placement = (WIDTH / 2 - your_score_text.get_width() / 2,
                            HEIGHT / 2)
    window.blit(over_text, text_placement)
    window.blit(your_score_text, your_score_placement)
    pygame.display.update()
    pygame.time.delay(4000)
    work = False


def intro_screen():
    """
    This function displays intro screen with
    controls instructions.
    """

    text = "Press enter to start"
    title = my_title_font.render("SPACE INVADERS", True, RED)
    title_box = title.get_rect()
    title_box.midtop = pygame.Rect(0, 0, WIDTH, (HEIGHT / 4)).midbottom

    msg = my_intro_font.render(text, True, WHITE)
    msg_box = msg.get_rect()
    msg_box.center = scr.center

    bg_intro_im = pygame.image.load("space.png")
    bg_intro_im = pygame.transform.scale(bg_intro_im, (WIDTH, HEIGHT))

    summoning_aim()

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                mouse = pygame.mouse.get_pos()
                if click[0] and msg_box.collidepoint(mouse):
                    intro = False

        aim["rect"].center = pygame.mouse.get_pos()

        window.blit(bg_intro_im, scr)
        window.blit(msg, msg_box)
        window.blit(title, title_box)
        window.blit(aim["surf"], aim["rect"])

        pygame.display.flip()


def options():
    """
    This function displays option screen and sets difficulty mode and controls.
    """
    global difficulty_up_frequency
    global lives
    global switch

    my_option_font = pygame.font.Font('freesansbold.ttf', 35)
    my_selected_font = pygame.font.Font('freesansbold.ttf', 40)
    text = "CHOOSE DIFFICULTY"
    easy = my_option_font.render("1. Easy", True, WHITE)
    easy_box = easy.get_rect()
    normal = my_option_font.render("2. Normal", True, WHITE)
    normal_box = normal.get_rect()
    hard = my_option_font.render("3. Hard", True, WHITE)
    hard_box = hard.get_rect()
    mouse_button = my_option_font.render("Mouse", True, WHITE)
    mouse_button_box = mouse_button.get_rect()
    keyboard_button = my_option_font.render("Keyboard", True, WHITE)
    keyboard_button_box = keyboard_button.get_rect()

    title = my_intro_font.render(text, True, GRAY)
    title_box = title.get_rect()
    title_box.midtop = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.05)).midbottom

    controls = my_intro_font.render("SELECT CONTROLS", True, GRAY)
    controls_box = controls.get_rect()
    controls_box.center = scr.center

    play = my_title_font.render("PLAY", True, WHITE)
    play_box = play.get_rect()
    play_box.midbottom = (scr.centerx, 0.85 * HEIGHT)

    bg_intro_im = pygame.image.load("space.png")
    bg_intro_im = pygame.transform.scale(bg_intro_im, (WIDTH, HEIGHT))

    summoning_aim()

    blockade1 = False
    blockade2 = False
    option = True
    while option:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_1:
                    lives = 15
                    difficulty_up_frequency = 5
                    easy = my_selected_font.render("1. Easy", True, RED)
                    normal = my_option_font.render("2. Normal", True, WHITE)
                    hard = my_option_font.render("3. Hard", True, WHITE)
                    blockade1 = True
                if event.key == pygame.K_2:
                    lives = 10
                    difficulty_up_frequency = 4
                    easy = my_option_font.render("1. Easy", True, WHITE)
                    normal = my_selected_font.render("2. Normal", True, RED)
                    hard = my_option_font.render("3. Hard", True, WHITE)
                    blockade1 = True
                if event.key == pygame.K_3:
                    lives = 5
                    difficulty_up_frequency = 3
                    easy = my_option_font.render("1. Easy", True, WHITE)
                    normal = my_option_font.render("2. Normal", True, WHITE)
                    hard = my_selected_font.render("3. Hard", True, RED)
                    blockade1 = True
                if event.key == pygame.K_m:
                    switch = "mouse"
                    mouse_button = my_selected_font.render("Mouse", True, RED)
                    keyboard_button = my_option_font.render("Keyboard",
                                                            True, WHITE)
                    blockade2 = True
                if event.key == pygame.K_k:
                    switch = "keys"
                    mouse_button = my_option_font.render("Mouse",
                                                         True, WHITE)
                    keyboard_button = my_selected_font.render("Keyboard",
                                                              True, RED)
                    blockade2 = True
                if event.key == pygame.K_RETURN and blockade1 and blockade2:
                    option = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                mouse = pygame.mouse.get_pos()
                if click[0] and easy_box.collidepoint(mouse):
                    lives = 15
                    difficulty_up_frequency = 5
                    easy = my_selected_font.render("1. Easy", True, RED)
                    normal = my_option_font.render("2. Normal", True, WHITE)
                    hard = my_option_font.render("3. Hard", True, WHITE)
                    blockade1 = True
                if click[0] and normal_box.collidepoint(mouse):
                    lives = 10
                    difficulty_up_frequency = 4
                    easy = my_option_font.render("1. Easy", True, WHITE)
                    normal = my_selected_font.render("2. Normal", True, RED)
                    hard = my_option_font.render("3. Hard", True, WHITE)
                    blockade1 = True
                if click[0] and hard_box.collidepoint(mouse):
                    lives = 5
                    difficulty_up_frequency = 3
                    easy = my_option_font.render("1. Easy", True, WHITE)
                    normal = my_option_font.render("2. Normal", True, WHITE)
                    hard = my_selected_font.render("3. Hard", True, RED)
                    blockade1 = True
                if click[0] and mouse_button_box.collidepoint(mouse):
                    switch = "mouse"
                    mouse_button = my_selected_font.render("Mouse", True, RED)
                    keyboard_button = my_option_font.render("Keyboard",
                                                            True, WHITE)
                    blockade2 = True
                if click[0] and keyboard_button_box.collidepoint(mouse):
                    switch = "keys"
                    mouse_button = my_option_font.render("Mouse", True, WHITE)
                    keyboard_button = my_selected_font.render("Keyboard",
                                                              True, RED)
                    blockade2 = True
                if click[0] and play_box.collidepoint(mouse) \
                        and blockade1 and blockade2:
                    option = False

        easy_box = easy.get_rect()
        easy_box.top = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.15)).bottom
        easy_box.left = WIDTH * 0.37

        normal_box = normal.get_rect()
        normal_box.top = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.25)).bottom
        normal_box.left = WIDTH * 0.37

        hard_box = hard.get_rect()
        hard_box.top = pygame.Rect(0, 0, WIDTH, (HEIGHT * 0.35)).bottom
        hard_box.left = WIDTH * 0.37

        mouse_button_box = mouse_button.get_rect()
        mouse_button_box.midleft = (controls_box.left + 20, WIDTH * 0.45)

        keyboard_button_box = keyboard_button.get_rect()
        keyboard_button_box.midright = (controls_box.right - 20, WIDTH * 0.45)

        aim["rect"].center = pygame.mouse.get_pos()

        window.blit(bg_intro_im, scr)

        window.blit(easy, easy_box)
        window.blit(normal, normal_box)
        window.blit(hard, hard_box)
        window.blit(title, title_box)
        window.blit(play, play_box)
        window.blit(controls, controls_box)
        window.blit(mouse_button, mouse_button_box)
        window.blit(keyboard_button, keyboard_button_box)
        window.blit(aim["surf"], aim["rect"])

        pygame.display.flip()


if __name__ == "__main__":
    while True:
        # configuration
        pygame.init()
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        scr = window.get_rect()
        pygame.display.set_caption("Space Invaders")
        pygame.mouse.set_visible(False)
        fps = pygame.time.Clock()
        pygame.key.set_repeat(50, 10)

        # sound effect
        mixer.init()
        mixer.music.load("blaster.mp3")
        mixer.music.set_volume(0.2)

        # all objects
        spaceship = {"file": "spaceship.png"}
        red_laser_beam = {"file": "red-laser-beam-pixel-art.png"}
        blue_alien = {"file": "blue_alien.png"}
        green_alien = {"file": "green_alien.png"}
        purple_alien = {"file": "purple_alien.png"}
        black_alien = {"file": "black_alien.png"}
        gray_alien = {"file": "gray_alien.png"}
        aim = {"file": "aim.png"}

        aliens = [blue_alien, green_alien, purple_alien,
                  black_alien, gray_alien]
        alien_circles = []
        objects = [spaceship]

        # background image
        bg_img = pygame.image.load("space2.png")
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        my_score_font = pygame.font.Font('freesansbold.ttf', 30)
        my_intro_font = pygame.font.Font('freesansbold.ttf', 50)
        my_title_font = pygame.font.Font('freesansbold.ttf', 80)

        # variables
        work = True
        wait_to_shoot = "go"
        bullet_on_screen = "stop"
        timer_wave = "stop"
        time = 0
        wave = 1
        lives = 0
        timer_laser = 0
        difficulty_up_frequency = 5
        vel_x = 1
        vel_y = 1
        your_score = 0
        switch = "keys"

        intro_screen()
        options()
        summoning_spaceship()
        summoning_aliens()
        if switch == "mouse":
            summoning_aim()

        # main loop
        while work:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_ESCAPE]:
                        sys.exit()

                    # controls
                if switch == "keys":
                    if keys[pygame.K_LEFT]:
                        spaceship["rect"] = \
                            spaceship["rect"].move((-SPACESHIP_STEP, 0))
                    if keys[pygame.K_RIGHT]:
                        spaceship["rect"] = \
                            spaceship["rect"].move((SPACESHIP_STEP, 0))
                    if keys[pygame.K_UP]:
                        spaceship["rect"] = \
                            spaceship["rect"].move((0, -SPACESHIP_STEP))
                    if keys[pygame.K_DOWN]:
                        spaceship["rect"] = \
                            spaceship["rect"].move((0, SPACESHIP_STEP))
                    if keys[pygame.K_SPACE]:
                        if wait_to_shoot == "go":
                            shoot()
                            bullet_on_screen = "go"
                            wait_to_shoot = "stop"
                            timer_laser = 0
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = pygame.mouse.get_pressed()
                        if click[0]:
                            if wait_to_shoot == "go":
                                shoot()
                                bullet_on_screen = "go"
                                wait_to_shoot = "stop"
                                timer_laser = 0

                    mouse = pygame.mouse.get_pos()
                    spaceship["rect"].center = (mouse[0],
                                                scr.bottom -
                                                SPACESHIP_SIZE[0] / 2)
                    aim["rect"].center = mouse

            range_of_movement()

            moving_laser()

            moving_aliens()

            collision()

            # break before next wave
            if timer_wave == "start":
                time += 1
                if time % BREAK_TIME == 0:
                    if wave % difficulty_up_frequency == 0:
                        vel_y += 1
                    summoning_aliens()
                    timer_wave = "stop"
                    wave += 1

            if len(objects) == 1:
                timer_wave = "start"

            # drawing images
            window.blit(bg_img, scr)
            if lives == 0:
                game_over()

            for item in objects:
                window.blit(item["surf"], item["rect"])
            score()
            if switch == "mouse":
                window.blit(aim["surf"], aim["rect"])
            pygame.display.flip()
            fps.tick(100)
