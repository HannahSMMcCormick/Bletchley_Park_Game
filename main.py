import pygame 


pygame.init()

screen = pygame.display.set_mode((800, 600))


# Name of Game
pygame.display.set_caption("Bletchley Park")

#Icon
icon = pygame.image.load("player.png")
pygame.display.set_icon(icon)

#Background
image = pygame.image.load("background.png")

#Create Player
Player = pygame.image.load("Player.png").convert_alpha()
#Had to scale player image cause too small
Player = pygame.transform.scale(Player, (64, 64))
Player_x = 400
Player_y = 300

max_x = 800 - 64
max_y = 600 - 64

#Draw Background
def background():
    
    screen.blit(image, (0, 0))


#Draw Player
def player(x,y):
    
    screen.blit(Player,(x,y))


walking_speed = 0.1
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Player Movement 
        player_x_change = 0
        player_y_change = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -walking_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = walking_speed
            if event.key == pygame.K_UP:
                player_y_change = -walking_speed
            if event.key == pygame.K_DOWN:
                player_y_change = walking_speed

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_x_change = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                player_y_change = 0
                
    Player_x += player_x_change
    Player_y += player_y_change
    

    Player_x = max(0, min(Player_x, max_x))
    Player_y = max(0, min(Player_y, max_y))
    
        
    background()
    player(Player_x,Player_y)
    pygame.display.update()

