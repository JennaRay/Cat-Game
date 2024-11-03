import pygame
import spritesheet
import constants

class Player(pygame.sprite.Sprite):
    #Animation code from Coding with Russ tutorial
    #https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s

    animation_list = [] #will hold all animation frames
    animation_steps = [] #used to set up animation frames for each action--number coordinates with number of frames in each animation
    current_frame = 0 #current animation frame for character display
    current_action = 0 
    position = [0, 0] #coordinates of character on screen
    velocity = [0, 0] #controls how quickly character moves and in what direction 
    SPEED = .15
    JUMP_SPEED = .5 #controls how quickly character moves --- used in when changing velocity
    FALL_SPEED = .5
    jumping = False
    falling = False
    on_object = False
    
    def __init__(self, x, y, velocity_x, velocity_y, image_path):

        pygame.sprite.Sprite.__init__(self)
        #load sprite sheet
        sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
        #create spritesheet object
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
       
        #load animation frames
        frame_0 = sprite_sheet.get_image(0, 0, 48)
        animation_list = []
        animation_steps = [1,4,4]
        step_counter = 0

        for animation in animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 48, 2))
                step_counter += 1
            animation_list.append(temp_img_list)
        
        self.animation_list = animation_list
        self.animation_steps = animation_steps
        self.image = self.animation_list[0][0]
        self.velocity = [velocity_x, velocity_y]
        self.position = [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
#-----------------------------------------------getters---------------------------------------
    def get_frame(self):
        return self.current_frame
    
    def get_action(self):
        return self.current_action
    
    def get_animation(self):
        return self.animation_list[self.current_action]
    
    def get_animation_frame(self):
        return self.animation_list[self.current_action][self.current_frame]
    
    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]
    
    def is_jumping(self):
        return self.jumping
    
    def is_falling(self):
        return self.falling
    
    def is_on_object(self):
        return self.on_object
#-----------------------------------------------setters---------------------------------------
    def set_frame(self, frame):
        self.current_frame=frame

    def set_action(self, action):
        self.current_action=action

    
    def set_velocity_x(self, x, y):
        self.velocity = [x, y]

    def set_y(self, y):
        self.position[1] = y

    def set_speed(self, num):
        self.SPEED = num

    def set_jump_speed(self, num):
        self.JUMP_SPEED = num

    def set_jumping(self, bool):
        self.jumping = bool

    def set_falling(self, bool):
        self.falling = bool

    def set_on_object(self, bool):
        self.on_object = bool
    
    #Updates position of the player using velocity
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        screen_scroll = [0, 0]
        if self.position[1] < constants.SCROLL_THRESH:
            screen_scroll[1] = constants.SCROLL_THRESH - self.position[1]
            self.position[1] = constants.SCROLL_THRESH

        self.image = self.get_animation_frame()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.mask = pygame.mask.from_surface(self.image)

        return screen_scroll

    #put character on screen
    def draw(self, surface):
        surface.blit(self.get_animation_frame(), self.position)

#---------------------------------------------------------movement functions----------------------------------
    def move_left(self):
        # change velocity x value
        self.velocity[0] = -(self.SPEED)
        #set animation to left facing walking animation
        self.set_action(2)
        self.set_frame(0)
    
    def move_right(self):
        #change velocity x value
        self.velocity[0] = (self.SPEED)
        #set animation to right facing walking animation
        self.set_action(1)
        self.set_frame(0)
    
    def move_up(self):
        #change velocity y value
        self.velocity[1] = -(self.JUMP_SPEED)
        #set animation to jumping animation
    def move_down(self):
        #change velocity y value
        self.velocity[1] = (self.FALL_SPEED)

    #Character goes back to idle and stops moving
    def stand_still(self):
        #change velocity
        self.velocity[0] = 0
        self.velocity[1] = 0
        #set to idle animation
        self.set_action(0)
        self.set_frame(0)
    
    def stop_falling(self):
        self.velocity[1] = 0