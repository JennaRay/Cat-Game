import pygame
import player
import background
import object


pygame.init()
#constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 120

#initiate screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat Platformer")
def main():
    playing = menu()
    if playing:
        play()
    pygame.quit()

def menu():
    bg = background.Background("images/ui/menu-bg.png", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    start_button = object.Button(SCREEN_WIDTH/2 - 96, SCREEN_HEIGHT/2 - 110, "images/ui/start-button.png", (192, 96))
    quit_button = object.Button(SCREEN_WIDTH/2 - 96, SCREEN_HEIGHT/2 + 10, "images/ui/quit-button.png", (192, 96))
 
    running = True
    while running:
        screen.fill((0, 0, 0))
        bg.draw(screen)
        start_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                    start_button.image = start_button.pressed
                else:
                    start_button.image = start_button.unpressed
                if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    quit_button.image = quit_button.pressed
                else:
                    quit_button.image = quit_button.unpressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    return True
                if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    return False

def play():
        
    #set up background
    bg = background.Background("images/env/bg.png", 0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT)
    platforms = pygame.sprite.Group()
    platforms.add(object.Object(200, SCREEN_HEIGHT - 100, "images/sprites/dresser.png", (192, 96)))
    platforms.add(object.Object(400, SCREEN_HEIGHT - 200, "images/sprites/shelf.png", (192, 24)))

    #initiate player
    mc = player.Player(10, SCREEN_HEIGHT - 100, 0, 0, "images/sprites/cat-sprite.png")


    #animation variables
    player_action = 0
    player_frame = 0
    last_update = pygame.time.get_ticks()
    jump_start = pygame.time.get_ticks()
    jump_length = 200

    #game loop
    running = True
    while running:
        screen.fill((255, 255, 255))
        bg.draw(screen)
        platforms.draw(screen)
        mc.draw(screen)
    #update animations
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= FPS:
            mc.set_frame(player_frame + 1)
            player_frame = mc.get_frame()
            last_update = current_time
            if player_frame >= len(mc.get_animation()):
                mc.set_frame(0)
                player_frame = mc.get_frame()

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    mc.move_right()
                if event.key == pygame.K_a:
                    mc.move_left()
                if event.key == pygame.K_SPACE:
                    if mc.is_jumping() == False:
                        mc.set_jumping(True)
                        jump_start = pygame.time.get_ticks()
                
            if event.type == pygame.KEYUP:
                pressed = pygame.key.get_pressed()
                if event.key == pygame.K_d:
                    mc.stand_still()
                    if pressed[pygame.K_a]:
                        mc.move_left()
                if event.key == pygame.K_a:
                    mc.stand_still()
                    if pressed[pygame.K_d]:
                        mc.move_right()

        #jump
        current_time = pygame.time.get_ticks()
        if mc.is_jumping():
            mc.move_up()
        if current_time - jump_start >= jump_length and mc.is_jumping():
            mc.set_jumping(False)
            mc.set_falling(True)
        if mc.is_falling():
            if  mc.get_y() < SCREEN_HEIGHT - 100:
                mc.move_down()
                colliders = pygame.sprite.spritecollide(mc, platforms, False)
                if colliders:
                    for collider in colliders:
                        if collider.rect.top >= mc.rect.bottom - 10:
                            mc.set_falling(False)
                            mc.stop_falling()
                            mc.set_y(collider.rect.top - 96)
                            mc.set_on_object(True)
            if  mc.get_y() >= SCREEN_HEIGHT - 100:
                mc.set_falling(False)
                mc.stop_falling()
                mc.set_y(SCREEN_HEIGHT - 100)   
        if mc.is_on_object():
            colliders = pygame.sprite.spritecollide(mc, platforms, False)
            if colliders and not mc.is_jumping():
                for collider in colliders:
                    if collider.rect.top <= mc.get_y():
                        mc.set_falling(True)
                        mc.set_on_object(False)
            if not colliders and not mc.is_jumping():
                mc.set_falling(True)
                mc.set_on_object(False)

        #update player
        mc.update()
        pygame.display.update()

if __name__ == "__main__":
    main()


