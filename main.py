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
Player = pygame.transform.scale(Player, (128, 128))
Player_x = 400
Player_y = 300

#Draw Background
def background():
    
    screen.blit(image, (0, 0))


#Draw Player
def player():
    
    screen.blit(Player,(Player_x,Player_y))



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    background()
    player()
    pygame.display.update()

