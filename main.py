import pygame
import random
import string

#============================================================================================================================================
# INITIALISE GAME
#============================================================================================================================================

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

bombe_solved = False      # In this version: means you successfully ACTED on good intel at least once
game_won = False
mode = "explore"
hint_text = ""

#============================================================================================================================================
# ASSETS
#============================================================================================================================================

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

# Clue image (LOAD ONCE, not inside draw loop)
CIPHER_IMG = pygame.image.load("CIPHER.png").convert_alpha()
CIPHER_IMG = pygame.transform.scale(CIPHER_IMG, (400, 400))

#============================================================================================================================================
# ZONES
#============================================================================================================================================

bombe_rect = pygame.Rect(30, 80, 740, 100)
door_rect  = pygame.Rect(790, 240, 30, 120)

# If you draw the radio at (30, 420) scaled to 64x64, make the rect match
radio_rect = pygame.Rect(30, 420, 64, 64)

#============================================================================================================================================
# DRAW BASIC
#============================================================================================================================================

def background():
    screen.blit(image, (0, 0))

def player(x, y):
    screen.blit(Player, (x, y))

def radio():
    screen.blit(Radio, (30, 420))

#============================================================================================================================================
# LIFE COUNTER
#============================================================================================================================================

def life():
    for i in range(3):
        if i < Life:
            screen.blit(Heart, (i * 30, 0))
        else:
            screen.blit(lose, (i * 30, 0))

#============================================================================================================================================
# DEBUGGING
#============================================================================================================================================

def draw_debug_zones():
    pygame.draw.rect(screen, (0, 255, 255), bombe_rect, 2)
    pygame.draw.rect(screen, (255, 255, 0), door_rect, 2)
    pygame.draw.rect(screen, (0, 255, 0), radio_rect, 2)

#============================================================================================================================================
# OVERLAYS
#============================================================================================================================================

def draw_hint(text):
    if text:
        surf = font.render(text, True, (255, 255, 255))
        screen.blit(surf, (20, 20))

def draw_puzzle_overlay():
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    

    title = font.render("BOMBE RUN (ESC to exit)", True, (255, 255, 255))
    screen.blit(title, (260, 170))

    if not intel:
        return

    t1 = font.render(
        f"Cipher: {intel['cipher_type']}   Reliability: {intel['reliability']}   Category: {intel['category']}",
        True,
        (200, 200, 200),
    )
    screen.blit(t1, (60, 220))

    cipher_label = font.render("Intercept:", True, (255, 255, 255))
    screen.blit(cipher_label, (60, 260))

    cipher_text = font.render(intel["ciphertext"], True, (255, 255, 255))
    screen.blit(cipher_text, (170, 260))

    help_text = font.render("Type the DECRYPTED plaintext (spaces allowed), press ENTER", True, (200, 200, 200))
    screen.blit(help_text, (140, 390))

    pygame.draw.rect(screen, (255, 255, 255), (80, 320, 640, 50), 2)
    typed = font.render(player_input, True, (255, 255, 255))
    screen.blit(typed, (90, 335))

    if puzzle_message:
        msg = font.render(puzzle_message, True, (255, 255, 0))
        screen.blit(msg, (250, 420))
        
    if intel["cipher_type"] == "ATBASH":
        hint = font.render("Hint: A ↔ Z, B ↔ Y, C ↔ X", True, (160, 160, 160))
        screen.blit(hint, (60, 300))
        
            
    elif intel["cipher_type"] == "CAESAR":
        hint = font.render("Hint: Letters are shifted along the alphabet", True, (160, 160, 160))
        screen.blit(hint, (60, 300))
        
    else:
        hint = font.render("Hint: Repeating keyword encryption", True, (160, 160, 160))
        screen.blit(hint, (60, 300))
        

def draw_decision_overlay():
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("INTELLIGENCE ASSESSMENT", True, (255, 255, 255))
    screen.blit(title, (235, 160))

    if not intel:
        return

    line1 = font.render(f"Decrypted: {intel['plaintext']}", True, (255, 255, 255))
    screen.blit(line1, (70, 230))

    line2 = font.render(f"Category: {intel['category']}   Reliability: {intel['reliability']}", True, (200, 200, 200))
    screen.blit(line2, (70, 270))

    prompt = font.render("[A] ACT    [I] IGNORE/ARCHIVE    (ESC to return)", True, (255, 255, 0))
    screen.blit(prompt, (70, 340))

    meters = font.render(f"Suspicion: {suspicion}/100   Score: {score}   Missed Critical: {missed_critical}", True, (180, 180, 180))
    screen.blit(meters, (70, 430))

def draw_Locked_zones():
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("Door is Locked, Act on good intel first (ESC to exit)", True, (255, 255, 255))
    screen.blit(title, (160, 280))

def draw_clue():
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("A Clue (press ESC to exit)", True, (255, 255, 255))
    screen.blit(title, (270, 150))

    screen.blit(CIPHER_IMG, (200, 200))
    
def draw_hud():
    hud = font.render(f"Score: {score}   Suspicion: {suspicion}/100   Missed: {missed_critical}", True, (255, 255, 255))
    screen.blit(hud, (20, 35))

def draw_status():
    if status_timer > 0 and status_text:
        msg = font.render(status_text, True, (255, 255, 0))
        screen.blit(msg, (20, 60))

#===========================================================================================================================================
# CIPHERS
#==========================================================================================================================================

ALPH = string.ascii_uppercase

def caesar_encrypt(text, shift):
    out = []
    for ch in text.upper():
        if ch in ALPH:
            idx = ord(ch) - ord("A")
            out.append(chr((idx + shift) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)

def atbash_encrypt(text):
    # A<->Z, B<->Y ...
    out = []
    for ch in text.upper():
        if ch in ALPH:
            out.append(chr(ord("Z") - (ord(ch) - ord("A"))))
        else:
            out.append(ch)
    return "".join(out)

def vigenere_encrypt(text, key):
    key = "".join([c for c in key.upper() if c in ALPH])
    if not key:
        return text.upper()

    out = []
    ki = 0
    for ch in text.upper():
        if ch in ALPH:
            shift = ord(key[ki % len(key)]) - ord("A")
            out.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)

#===========================================================================================================================================
# CREATE PUZZLES (BOMBE OUTPUT)
#===========================================================================================================================================

MESSAGE_TEMPLATES = [
    ("ROUTINE",  "WEATHER REPORT AT DAWN"),
    ("ROUTINE",  "SUPPLY LOG MOVES TONIGHT"),
    ("CRITICAL", "CONVOY ROUTE CHANGES TODAY"),
    ("CRITICAL", "PATROL SHIFT MOVES EARLY"),
    ("CRITICAL", "RADAR OUTAGE AT MIDNIGHT"),
]

VIG_KEYS = ["HUT", "BOMBE", "CODE", "PARK", "TURING"]

def pick_cipher(difficulty):
    # difficulty: 1..3
    pool = ["CAESAR", "ATBASH"]
    if difficulty >= 2:
        pool += ["VIGENERE"]
    return random.choice(pool)

def generate_intel(difficulty=1):
    category, plaintext = random.choice(MESSAGE_TEMPLATES)

    reliability = random.choice(["LOW", "MED", "HIGH"])
    decoy_chance = {"LOW": 0.35, "MED": 0.20, "HIGH": 0.08}[reliability]
    is_decoy = (random.random() < decoy_chance)

    cipher_type = pick_cipher(difficulty)
    extra = {}

    if cipher_type == "CAESAR":
        shift = random.randint(1, 9 if difficulty == 1 else 15)
        ciphertext = caesar_encrypt(plaintext, shift)
        extra["shift"] = shift

    elif cipher_type == "ATBASH":
        ciphertext = atbash_encrypt(plaintext)

    elif cipher_type == "VIGENERE":
        key = random.choice(VIG_KEYS)
        ciphertext = vigenere_encrypt(plaintext, key)
        extra["key"] = key

    else:
        ciphertext = plaintext

    return {
        "cipher_type": cipher_type,
        "category": category,          # ROUTINE / CRITICAL
        "reliability": reliability,    # LOW/MED/HIGH
        "is_decoy": is_decoy,          # hidden truth for consequences
        "plaintext": plaintext,        # what player must enter (learning quiz)
        "ciphertext": ciphertext,
        "extra": extra,
    }

#===========================================================================================================================================
# CONSEQUENCES (ACT vs IGNORE)
#===========================================================================================================================================
#===========================================================================================================================================
# CONSEQUENCES (ACT vs IGNORE)
#===========================================================================================================================================

def apply_decision(act: bool):
    global suspicion, score, missed_critical, difficulty, bombe_solved, Life
    global status_text, status_timer

    if not intel:
        return

    #====================================================================
    # SUSPICION (PATTERN EXPOSURE)
    #====================================================================

    if act:
        suspicion += {"LOW": 15, "MED": 10, "HIGH": 6}[intel["reliability"]]
    else:
        suspicion -= 2

    suspicion = max(0, min(100, suspicion))

    #====================================================================
    # OUTCOME (VISIBLE FEEDBACK)
    #====================================================================

    if act:
        if intel["is_decoy"]:
            score -= 10
            Life -= 1
            status_text = "ACTED: It was a DECOY! Suspicion rose."
        else:
            score += 20 if intel["category"] == "CRITICAL" else 5
            bombe_solved = True
            status_text = "ACTED: Success! Intel used."
    else:
        if (not intel["is_decoy"]) and intel["category"] == "CRITICAL":
            missed_critical += 1
            score -= 8
            status_text = "IGNORED: Missed CRITICAL intel."
        else:
            score += 1
            status_text = "IGNORED: Good restraint."

    # Show message for ~2 seconds
    status_timer = 120

    # Clamp life
    Life = max(0, Life)

    #====================================================================
    # DIFFICULTY RAMPS WITH SUSPICION
    #====================================================================

    difficulty = 1
    if suspicion >= 70:
        difficulty = 2
    if suspicion >= 90:
        difficulty = 3

    #====================================================================
    # DEBUG (REMOVE LATER)
    #====================================================================

    print("DECISION:", "ACT" if act else "IGNORE")
    print("PLAINTEXT:", intel["plaintext"], "| DECOY:", intel["is_decoy"])
    print("SCORE:", score, "SUSPICION:", suspicion, "LIFE:", Life)

#===========================================================================================================================================
# OUTCOMES
#===========================================================================================================================================

def draw_game_over():
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("GAME OVER", True, (255, 80, 80))
    screen.blit(title, (350, 250))

    sub = font.render("Press R to restart or ESC to quit", True, (255, 255, 255))
    screen.blit(sub, (245, 300))

def draw_game_won():
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font.render("You Win", True, (255, 80, 80))
    screen.blit(title, (360, 250))

    sub = font.render("Press R to restart or ESC to quit", True, (255, 255, 255))
    screen.blit(sub, (245, 300))

#===========================================================================================================================================
# GAME LOOP
#===========================================================================================================================================

speed = 5
running = True

Life = 3

intel = None
difficulty = 1

suspicion = 0
score = 0
missed_critical = 0

status_text = ""
status_timer = 0  

while running:
    clock.tick(60)
    
    if status_timer > 0:
        status_timer -= 1

    # Build player rect each frame
    player_rect = pygame.Rect(Player_x, Player_y, PLAYER_W, PLAYER_H)
    near_bombe = player_rect.colliderect(bombe_rect)
    near_door = player_rect.colliderect(door_rect)
    near_radio = player_rect.colliderect(radio_rect)

    # Hint text (DO NOT change modes here!)
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

            #====================================================================
            # RESTART / QUIT SCREENS
            #====================================================================

            if mode == "game_over":
                if event.key == pygame.K_r:
                    Life = 3
                    bombe_solved = False
                    game_won = False
                    mode = "explore"
                    player_input = ""
                    puzzle_message = ""
                    intel = None
                    difficulty = 1
                    suspicion = 0
                    score = 0
                    missed_critical = 0
                    Player_x, Player_y = 400, 300
                elif event.key == pygame.K_ESCAPE:
                    running = False
                continue

            if mode == "game_won":
                if event.key == pygame.K_r:
                    Life = 3
                    bombe_solved = False
                    game_won = False
                    mode = "explore"
                    player_input = ""
                    puzzle_message = ""
                    intel = None
                    difficulty = 1
                    suspicion = 0
                    score = 0
                    missed_critical = 0
                    Player_x, Player_y = 400, 300
                elif event.key == pygame.K_ESCAPE:
                    running = False
                continue

            #====================================================================
            # GLOBAL ESC (back out of overlays)
            #====================================================================

            if event.key == pygame.K_ESCAPE:
                if mode in ("puzzle", "Locked", "clue", "decision"):
                    mode = "explore"
                    player_input = ""
                    puzzle_message = ""
                else:
                    running = False
                continue

            #====================================================================
            # DECISION MODE (ACT / IGNORE)
            #====================================================================

            if mode == "decision":
                if event.key == pygame.K_a:
                    apply_decision(True)
                    intel = None
                    mode = "explore"
                elif event.key == pygame.K_i:
                    apply_decision(False)
                    intel = None
                    mode = "explore"

                # If life dropped to 0 because of a bad ACT call
                if Life <= 0:
                    mode = "game_over"
                continue

            #====================================================================
            # PUZZLE MODE (TYPE PLAINTEXT)
            #====================================================================

            if mode == "puzzle":
                if event.key == pygame.K_RETURN:
                    guess = player_input.strip().upper()
                    if intel and guess == intel["plaintext"]:
                        puzzle_message = "Decryption verified."
                        mode = "decision"
                    else:
                        puzzle_message = "Incorrect plaintext."
                        Life -= 1
                        Life = max(0, Life)
                        if Life <= 0:
                            mode = "game_over"
                    player_input = ""

                elif event.key == pygame.K_BACKSPACE:
                    player_input = player_input[:-1]

                else:
                    # IMPORTANT: allow spaces, because plaintext contains spaces
                    ch = event.unicode.upper()
                    if (ch.isalpha() or ch == " ") and len(player_input) < 40:
                        player_input += ch
                continue

            #====================================================================
            # EXPLORE INTERACT (E)
            #====================================================================

            if event.key == pygame.K_e and mode == "explore" and not game_won:

                if near_bombe and not bombe_solved:
                    mode = "puzzle"
                    player_input = ""
                    puzzle_message = ""
                    intel = generate_intel(difficulty=difficulty)

                elif near_door:
                    if bombe_solved:
                        mode = "game_won"
                    else:
                        mode = "Locked"
                        hint_text = "Locked! Act on good intel first."

                elif near_radio:
                    mode = "clue"

    #====================================================================
    # MOVEMENT (ONLY IN EXPLORE)
    #====================================================================

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

    #====================================================================
    # DRAW
    #====================================================================

    background()
    radio()
    life()
    draw_debug_zones()      # shows bombe/door/radio rectangles
    player(Player_x, Player_y)
    draw_hint(hint_text)
    draw_hud()
    draw_status()

    if mode == "puzzle":
        draw_puzzle_overlay()

    if mode == "decision":
        draw_decision_overlay()

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
