import pygame

path_picture = '' #'/data/data/com.socute.ultrapygame/files/app/'

clock = pygame.time.Clock()
FPS = 15

pygame.init()
screen = pygame.display.set_mode((600, 360))#flags=pygame.NOFRAME)
pygame.display.set_caption("Pygame")
icon = pygame.image.load(path_picture + 'pictures/7945099.png')
pygame.display.set_icon(icon)
font = pygame.font.Font(path_picture + 'fonts/JetBrains-Mono.ttf', 40)
font_ui = pygame.font.Font(path_picture + 'fonts/JetBrains-Mono.ttf', 15) 

bg = pygame.image.load(path_picture +'pictures/bg.jpg').convert()


# Player
player_anim_count = 0
bg_x = 0
player_speed = 7
player_x = 150
player_y = 210
is_jump = False
jump_count = 9
walk_backward = [
    pygame.image.load(path_picture +'pictures/player_backward/frame1_mirrror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame1_mirrror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame1_mirrror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame2_mirror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame2_mirror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame2_mirror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame3_mirror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame3_mirror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame3_mirror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame4_mirror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame4_mirror.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_backward/frame4_mirror.png').convert_alpha(),
]
walk_forward = [
    pygame.image.load(path_picture +'pictures/player_forward/frame1.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame1.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame1.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame2.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame2.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame2.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame3.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame3.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame3.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame4.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame4.png').convert_alpha(),
    pygame.image.load(path_picture +'pictures/player_forward/frame4.png').convert_alpha(),
]

# Pinos mrime
minos = pygame.image.load(path_picture +'pictures/enemy/minos.png').convert_alpha()
minos_list_in_game = []

bg_sound = pygame.mixer.Sound(path_picture +'sounds&music/bg_music.mp3')
# bg_sound.play()

minos_timer = pygame.USEREVENT + 1
pygame.time.set_timer(minos_timer, 3000)

text = font.render('You lose!', True, 'White')
restart = font.render('Restart', True, 'White')
restart_rect = restart.get_rect(topleft=(200, 100))

projectiles_left = 7
projectile = pygame.image.load(path_picture +'pictures/projectiles/blyat.png')
projectiles = []


gameplay = True

running = True
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 600, 0))

    if gameplay:

        player_rect = walk_backward[0].get_rect(topleft=(player_x, player_y))
    
        if minos_list_in_game:
            for (i, el) in enumerate(minos_list_in_game):
                screen.blit(minos, el)
                el.x -= 10

                if el.x < -10:
                    minos_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_backward[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_forward[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 0: 
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 590:
            player_x += player_speed 

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -600:
            bg_x = 0

        if projectiles:
            for (i, el) in enumerate(projectiles):
                screen.blit(projectile, (el.x, el.y))
                el.x += 4

                if el.x > 630:
                    projectiles.pop(i)

                if minos_list_in_game:
                    for (index, pinos) in enumerate(minos_list_in_game):
                        if el.colliderect(pinos):
                            minos_list_in_game.pop(index)
                            projectiles.pop(i)
        
        projectiles_count = font_ui.render("Projectiles left: {0}".format(projectiles_left), 1, 'White')
        screen.blit(projectiles_count, (10, 10))
    else:
        screen.blit(text, (200, 30))
        screen.blit(restart, restart_rect)

        mouse = pygame.mouse.get_pos()
        if restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            minos_list_in_game.clear()
            projectiles.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                        
            pygame.quit()
        
        if event.type == minos_timer:
            minos_list_in_game.append(minos.get_rect(topleft=(620, 195)))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and projectiles_left > 0:
            projectiles.append(projectile.get_rect(topleft=(player_x + 10, player_y + 10)))
            projectiles_left -= 1

    clock.tick(FPS)