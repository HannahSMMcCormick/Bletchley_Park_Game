import pygame
import random
import string

player_input = ""
puzzle_message = ""

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bletchley Park")
clock = pygame.time.Clock()

# Font ONCE
font = pygame.font.SysFont(None, 28)

# Icon
icon = pygame.image.load("player.png")
pygame.display.set_icon(icon)

# Background
image = pygame.image.load("background.png")

bombe_solved = False
game_won = False
mode = "explore"
hint_text = ""

# Player
Player = pygame.image.load("Player.png").convert_alpha()
Player = pygame.transform.scale(Player, (64, 64))
Player_x = 400
Player_y = 300
PLAYER_W, PLAYER_H = 64, 64

max_x = 800 - PLAYER_W
max_y = 600 - PLAYER_H

# Radio
Radio = pygame.image.load("Radio.png").convert_alpha()
Radio = pygame.transform.scale(Radio, (64, 64))

# Lives
Heart = pygame.image.load("Heart_life.png").convert_alpha()
lose = pygame.image.load("Heart_Lost.png").convert_alpha()

# Zones
bombe_rect = pygame.Rect(30, 80, 740, 100)
door_rect  = pygame.Rect(790, 240, 30, 120)
radio_rect = pygame.Rect(39,440,50,30)

def background():
    screen.blit(image, (0, 0))

def player(x, y):
    screen.blit(Player, (x, y))

def radio():
    screen.blit(Radio, (30, 420))

def life():
    for i in range(3):
        if i < Life:
            screen.blit(Heart,(i*30,0))
        else:
            screen.blit(lose,(i*30,0))

def draw_hint(text):
    if text:
        surf = font.render(text, True, (255, 255, 255))
        screen.blit(surf, (20, 20))

def draw_puzzle_overlay():
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("PUZZLE MODE (press ESC to exit)", True, (255, 255, 255))
    screen.blit(title, (220, 200))
    
    cipher_label = font.render("Decrypt this:", True, (255, 255, 255))
    screen.blit(cipher_label, (220, 250))

    cipher_text = font.render(puzzle_cipher, True, (255, 255, 255))
    screen.blit(cipher_text, (350, 250))

    help_text = font.render("Type answer, press ENTER", True, (200, 200, 200))
    screen.blit(help_text, (250, 390))

    pygame.draw.rect(screen, (255, 255, 255), (200, 330, 400, 50), 2)
    typed = font.render(player_input, True, (255, 255, 255))
    screen.blit(typed, (210, 345))

    if puzzle_message:
        msg = font.render(puzzle_message, True, (255, 255, 0))
        screen.blit(msg, (250, 410))
        
def draw_Locked_zones():
    
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("Door is Locked, Solve Puzzle (press ESC to exit)", True, (255, 255, 255))
    screen.blit(title, (220, 280))


def draw_clue():
    

    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("A Clue(press ESC to exit)", True, (255, 255, 255))
    screen.blit(title, (270, 150))
    
    cipher = pygame.image.load("CIPHER.png").convert_alpha()
    cipher = pygame.transform.scale(cipher, (400, 400))
    screen.blit(cipher, (200,200))
    
    

def draw_debug_zones():
    pygame.draw.rect(screen, (0, 255, 255), bombe_rect, 2)
    pygame.draw.rect(screen, (255, 255, 0), door_rect, 2)
    pygame.draw.rect(screen,(0, 255,0), radio_rect, 2)

def caesar_encrypt(text, shift):
    out = []
    for ch in text.upper():
        if ch in string.ascii_uppercase:
            idx = ord(ch) - ord('A')
            out.append(chr((idx+shift) % 26 + ord ("A")))
        else:
            out.append(ch)
    return "".join(out)
        

def new_puzzle():
    words = ["BLETCHLEY", "ENIGMA", "BOMBE","ENCRYPT","CIPHER"]
    plaintext = random.choice(words)
    shift = random.randint(1, 9)
    ciphertext = caesar_encrypt(plaintext, shift)
    return plaintext, ciphertext

puzzle_answer, puzzle_cipher = new_puzzle() 
puzzle_active = True

def draw_game_over():
    
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(220)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))
    
    title = font.render("GAME OVER", True, (255,80,80))
    screen.blit(title,(350,250))
    
    sub = font.render("Press R to restart or ESC to quit", True, (255,255,255))
    screen.blit(sub,(245,300))
    
def draw_game_won():
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(220)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))
    
    title = font.render("You Win", True, (255,80,80))
    screen.blit(title,(350,250))
    
    sub = font.render("Press R to restart or ESC to quit", True, (255,255,255))
    screen.blit(sub,(245,300))
    


speed = 5  
running = True
Life = 3

while running:
    clock.tick(60)

    # Build player rect each frame 
    player_rect = pygame.Rect(Player_x, Player_y, PLAYER_W, PLAYER_H)
    near_bombe = player_rect.colliderect(bombe_rect)
    near_door = player_rect.colliderect(door_rect)
    near_radio = player_rect.colliderect(radio_rect)

    # Hint text
    if mode == "explore" and not game_won:
        if near_bombe and not bombe_solved:
            hint_text = "Press E to use the Bombe"
        elif near_door:
            hint_text = "Press E to open the door"
        elif near_radio:
            hint_text = "Press E to hear hint"
        else:
            hint_text = ""
    else:
        hint_text = ""


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            
            if mode == "game_over":
                if event.key == pygame.K_r:
            
                    Life = 3
                    bombe_solved = False
                    game_won = False
                    mode = "explore"
                    player_input = ""
                    puzzle_message = ""
                    puzzle_answer, puzzle_cipher = new_puzzle()
                    puzzle_active = True
                    Player_x, Player_y = 400, 300
                    
                
                elif event.key == pygame.K_ESCAPE:
                    running = False
                continue
                    
                      
            elif mode == "game_won":
                    if event.key == pygame.K_r:
                        Life = 3
                        bombe_solved = False
                        game_won = False
                        mode = "explore"
                        player_input = ""
                        puzzle_message = ""
                        puzzle_answer, puzzle_cipher = new_puzzle()
                        puzzle_active = True
                        Player_x, Player_y = 400, 300
                
                                    
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    continue

            elif mode == "puzzle" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mode = "explore"
                    player_input = ""
                    puzzle_message = ""
                    continue

                elif event.key == pygame.K_RETURN:
                    guess = player_input.strip().upper()
                    if guess == puzzle_answer:
                        bombe_solved = True
                        puzzle_message = "Correct! Bombe solved."
                        mode = "explore"
                        puzzle_active = False
                    else:
                        puzzle_message = "Wrong. Try again."
                        Life -= 1
                        
                        if Life <= 0:
                            mode  = "game_over"
                    
                        
                    player_input = ""

                elif event.key == pygame.K_BACKSPACE:
                    player_input = player_input[:-1]

                else:
                    ch = event.unicode.upper()
                    if ch.isalpha() and len(player_input) < 20:
                        player_input += ch

            
        
            if event.key == pygame.K_ESCAPE:
                if mode in ("puzzle", "Locked", "clue"):
                    mode = "explore"
                    player_input = ""
                    puzzle_message = ""
                else:
                    running = False
                continue
            if event.key == pygame.K_e and mode == "explore" and not game_won:
                if near_bombe and not bombe_solved:
                    mode = "puzzle"
                    player_input = ""
                    puzzle_message = ""

                elif near_door:
                    if bombe_solved:
                        mode = "game_won"
                    else:
                        mode = "Locked"
                        hint_text = "Locked! Solve the Bombe first."
                elif near_radio:
                    mode = "clue"

    # Smooth movement (NOT event-based)
    if mode == "explore":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            Player_x -= speed
        if keys[pygame.K_RIGHT]:
            Player_x += speed
        if keys[pygame.K_UP]:
            Player_y -= speed
        if keys[pygame.K_DOWN]:
            Player_y += speed

        Player_x = max(0, min(Player_x, max_x))
        Player_y = max(0, min(Player_y, max_y))

    # Draw everything, then update ONCE
    background()
    radio()
    life()
    draw_debug_zones()      # shows bombe/door rectangles
    player(Player_x, Player_y)
    draw_hint(hint_text)

    
        
    if mode == "puzzle":
        draw_puzzle_overlay()
            
    if mode == "Locked":
        draw_Locked_zones()
            
    if mode == "clue":
        draw_clue()
        
    if mode == "game_over":
        draw_game_over()
    if mode == "game_won":
        draw_game_won()        



    pygame.display.update()
pygame.quit()


