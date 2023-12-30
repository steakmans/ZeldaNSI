import pygame
import numpy as np

#Pygame values DO NOT MODIFY
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
running = True
clock = pygame.time.Clock()
dt = 0

#Gameplay values
playerInfos = {
    "playerPos": pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),
          "playerSpeed": pygame.Vector2(0,0),
          "life": 100,
          "speed": 200,
          "playerXToMove": False,
          "playerYToMove": False,
          "playerDir": 0, # 0 = down, 1 = up, 2 = left, 3 = right
          "playerAnimIndex": 0,
          "playerAnimTimer": 0,
          "attacking": False,
          "attackTimer": 0,
          "playerTextures": [pygame.transform.scale_by(pygame.image.load("./resources/idle down.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/idle up.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/idle left.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/idle right.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk down 1.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk up1.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk left1.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk right1.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk down 2.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk up2.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk left2.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk right2.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk down 3.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk up3.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk left3.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/walk right3.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack down 1.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack up 1.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack left 1.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack right 1.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack down 2.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack up 2.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack left 2.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack right 2.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack down 3.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack up 3.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack left 3.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack right 3.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack down 4.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack up 4.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack left 4.png").convert_alpha(), 2),
              pygame.transform.scale_by(pygame.image.load("./resources/attack right 4.png").convert_alpha(), 2)
],
          "playerCollision": [pygame.mask.Mask((20, 5), True), #top and bottom collision mask
                              pygame.mask.Mask((5, 5), True)], #left and right collision mask
          "attackCollider": pygame.Rect((-100, -100), (70, 70))
    }
worldInfos = {"worldPos": pygame.Vector2(-215, -195),
              "worldIndex": 0,
              "background": [pygame.transform.scale_by(pygame.image.load("./resources/carte2.png").convert_alpha(), 2.5),
                             pygame.transform.scale_by(pygame.image.load("./resources/carte2.png").convert_alpha(), 2.5)],
              "foreground": [pygame.transform.scale_by(pygame.image.load("./resources/coll.png").convert_alpha(), 2.5),
                             pygame.transform.scale_by(pygame.image.load("./resources/coll.png").convert_alpha(), 2.5)],
              "collisions": [],
              "ennemiesForMap": [],
              "changeMapTriggers": []
    }
ennemiesList = []

for item in worldInfos["foreground"]:
    worldInfos["collisions"].append(pygame.mask.from_surface(item))

#functions
def attack(player):
    attackPos = player["playerPos"].__copy__()
    if player["playerDir"] == 0:
        attackPos.x -= 30
        attackPos.y -= 15
    elif player["playerDir"] == 1:
        attackPos.x -= 30
        attackPos.y -= 55
    elif player["playerDir"] == 2:
        attackPos.y -= 40
        attackPos.x -= 50
    elif player["playerDir"] == 3:
        attackPos.y -= 40
    player["attackCollider"].x = attackPos.x
    player["attackCollider"].y = attackPos.y
    
def createEnnemy(ennemies, life, rect, sprite, damage = 10, viewDistance = 100, reachDistance = 15, timeToAttack = 3):
    attributes = {
            "life": life,
            "damage": damage,
            "playerDetected": False,
            "viewDistance": viewDistance,
            "reachDistance": reachDistance,
            "rect": rect,
            "sprite": sprite,
            "attackTimer": 0,
            "timeToAttack": timeToAttack
        }
    ennemies.append(attributes)
    
def manageEnnemies(ennemies, player, world):
    for ennemy in ennemies:
        if player["playerPos"].distance_to(pygame.Vector2(ennemy["rect"].x + ennemy["rect"].width // 2, ennemy["rect"].y + ennemy["rect"].height // 2)) <= ennemy["viewDistance"]:
            ennemy["playerDetected"] = True
        if ennemy["playerDetected"]:
            if world["collisions"][world["worldIndex"]].get_at((-world["worldPos"].x + ennemy["rect"].x + ennemy["rect"].width + 10, -world["worldPos"].y + ennemy["rect"].y + ennemy["rect"].height // 2)) == 0:
                ennemy["rect"].x += 100 * dt
            if world["collisions"][world["worldIndex"]].get_at((-world["worldPos"].x + ennemy["rect"].x - 10, -world["worldPos"].y + ennemy["rect"].y + ennemy["rect"].height // 2)) == 0:
                ennemy["rect"].x -= 100 * dt
            if world["collisions"][world["worldIndex"]].get_at((-world["worldPos"].x + ennemy["rect"].x + ennemy["rect"].width // 2, -world["worldPos"].y + ennemy["rect"].y + ennemy["rect"].height + 10)) == 0:
                ennemy["rect"].y += 100 * dt
            if world["collisions"][world["worldIndex"]].get_at((-world["worldPos"].x + ennemy["rect"].x + ennemy["rect"].width // 2, -world["worldPos"].y + ennemy["rect"].y - 10)) == 0:
                ennemy["rect"].y -= 100 * dt
            ennemy["rect"].y += 100 * np.clip(player["playerPos"].y - ennemy["rect"].y - ennemy["rect"].height // 2, -1, 1) * dt
            ennemy["rect"].x += 100 * np.clip(player["playerPos"].x - ennemy["rect"].x - ennemy["rect"].width // 2, -1, 1) * dt
        if player["playerPos"].distance_to(pygame.Vector2(ennemy["rect"].x + ennemy["rect"].width // 2, ennemy["rect"].y + ennemy["rect"].height // 2)) <= ennemy["reachDistance"]:
            ennemy["attackTimer"] += dt
            if ennemy["attackTimer"] >= ennemy["timeToAttack"]:
                ennemy["attackTimer"] = 0
                player["life"] -= ennemy["damage"]
    
def manageControls(keys, player):
    if keys[pygame.K_SPACE] and not player["attacking"]:
        player["attacking"] = True
        player["playerAnimIndex"] = 16 + player["playerDir"]
        attack(player)
    
    if keys[pygame.K_EQUALS]:
        createEnnemy(ennemiesList, 100, pygame.Rect(player["playerPos"].__copy__(), (50, 50)), "TODO", 100, 100)

    if keys[pygame.K_LSHIFT]:
        player["speed"] = 400
    else:
        player["speed"] = 200
    if not player["attacking"]:
        if keys[pygame.K_q]:
            player["playerSpeed"].x = player["speed"]
            player["playerDir"] = 2
        if keys[pygame.K_d]:
            player["playerSpeed"].x = -player["speed"]
            player["playerDir"] = 3
        if not keys[pygame.K_d] and not keys[pygame.K_q]:
            player["playerSpeed"].x = 0
        if keys[pygame.K_z]:
            player["playerSpeed"].y = player["speed"]
            player["playerDir"] = 1
        if keys[pygame.K_s]:
            player["playerSpeed"].y = -player["speed"]
            player["playerDir"] = 0
        if not keys[pygame.K_z] and not keys[pygame.K_s]:
            player["playerSpeed"].y = 0
            
    if player["playerSpeed"].length() != 0:
        player["playerSpeed"].clamp_magnitude(player["speed"])

def manageAnimations(player):
    if not player["attacking"]:
        
        if player["playerAnimIndex"] % 4 == player["playerDir"]:
            if player["playerAnimTimer"] > 10:
                player["playerAnimTimer"] = 0
                player["playerAnimIndex"] += 4
                if player["playerAnimIndex"] > 15:
                    player["playerAnimIndex"] = player["playerDir"]
        else:
            player["playerAnimIndex"] = player["playerDir"]
        
        if player["playerSpeed"].length() == 0:
            player["playerAnimIndex"] = player["playerDir"]
    else:
        player["playerSpeed"].x = 0
        player["playerSpeed"].y = 0
        player["attackTimer"] += 1
        if player["attackTimer"] >= 32:
            player["attacking"] = False
            player["attackTimer"] = 0
            player["attackCollider"].x = -100
            player["attackCollider"].y = -100
        elif player["attackTimer"] % 8 == 0:
            player["playerAnimIndex"] += 4
            
def manageMovement(player, world, ennemies):
    if not player["playerXToMove"]:
        world["worldPos"].x += player["playerSpeed"].x * dt
        for ennemy in ennemies:
            ennemy["rect"].x += player["playerSpeed"].x * dt
    else:
        player["playerPos"].x -= player["playerSpeed"].x * dt
        
    if not player["playerYToMove"]:
        world["worldPos"].y += player["playerSpeed"].y * dt
        for ennemy in ennemies:
            ennemy["rect"].y += player["playerSpeed"].y * dt
    else:
        player["playerPos"].y -= player["playerSpeed"].y * dt
    
    if world["worldPos"].x > 0:
        world["worldPos"].x = 0
        player["playerXToMove"] = True
        player["playerPos"].x = screen.get_width() / 2 - player["speed"] * 0.017

    if world["worldPos"].x < -434:
        world["worldPos"].x = -434
        player["playerXToMove"] = True
        player["playerPos"].x = screen.get_width() / 2 + player["speed"] * 0.017
        
    if world["worldPos"].y > 0:
        world["worldPos"].y = 0
        player["playerYToMove"] = True
        player["playerPos"].y = screen.get_height() / 2 - player["speed"] * 0.017

    if world["worldPos"].y < -407:
        world["worldPos"].y = -407
        player["playerYToMove"] = True
        player["playerPos"].y = screen.get_height() / 2 + player["speed"] * 0.017

        
    if abs(player["playerPos"].x - screen.get_width() / 2) < player["speed"] * 0.016:
        player["playerPos"].x = screen.get_width() / 2
        player["playerXToMove"] = False
    if abs(player["playerPos"].y - screen.get_height() / 2) < player["speed"] * 0.016:
        player["playerPos"].y = screen.get_height() / 2
        player["playerYToMove"] = False
        
def manageDisplay(player, world, ennemies):
    screen.fill("black")
            
    screen.blit(world["background"][world["worldIndex"]], world["worldPos"])
    screen.blit(world["foreground"][world["worldIndex"]], world["worldPos"])
    
    for ennemy in ennemies:
        pygame.draw.rect(screen, (255, 0, 0), ennemy["rect"])
    
    playerPos = player["playerPos"].__copy__()
    playerPos.x -= 30
    playerPos.y -= 80
    screen.blit(player["playerTextures"][player["playerAnimIndex"]], playerPos)
    pygame.display.flip()
    
def manageCollisions(player, world, ennemies):
    
    #top
    if player["playerCollision"][0].overlap(world["collisions"][world["worldIndex"]], (world["worldPos"].x - player["playerPos"].x + 7, world["worldPos"].y - player["playerPos"].y - 10)):
        if player["playerSpeed"].y > 0:
            player["playerSpeed"].y = 0
        
    #bottom
    if player["playerCollision"][0].overlap(world["collisions"][world["worldIndex"]], (world["worldPos"].x - player["playerPos"].x + 7, world["worldPos"].y - player["playerPos"].y - 20)):
        if player["playerSpeed"].y < 0:
            player["playerSpeed"].y = 0
    #left
    if player["playerCollision"][1].overlap(world["collisions"][world["worldIndex"]], (world["worldPos"].x - player["playerPos"].x + 12, world["worldPos"].y - player["playerPos"].y - 15)):
        if player["playerSpeed"].x > 0:
            player["playerSpeed"].x = 0
    #left
    if player["playerCollision"][1].overlap(world["collisions"][world["worldIndex"]], (world["worldPos"].x - player["playerPos"].x - 12, world["worldPos"].y - player["playerPos"].y - 15)):
        if player["playerSpeed"].x < 0:
            player["playerSpeed"].x = 0
            
    for ennemy in ennemies[:]:
        if player["attackCollider"].colliderect(ennemy["rect"]):
            ennemy["life"] -= 50
            if player["playerDir"] == 0:
                ennemy["rect"].y += 200
            if player["playerDir"] == 1:
                ennemy["rect"].y -= 200
            if player["playerDir"] == 2:
                ennemy["rect"].x -= 200
            if player["playerDir"] == 3:
                ennemy["rect"].x += 200
            if ennemy["life"] <= 0:
                ennemies.remove(ennemy)
                
        
createEnnemy(ennemiesList, 10, pygame.Rect((-100, 50), (50, 50)), "TODO", 100, 500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False 
    
    manageControls(pygame.key.get_pressed(), playerInfos)
    manageAnimations(playerInfos)   
    manageCollisions(playerInfos, worldInfos, ennemiesList)
    manageMovement(playerInfos, worldInfos, ennemiesList)
    manageEnnemies(ennemiesList, playerInfos, worldInfos)
    manageDisplay(playerInfos, worldInfos, ennemiesList)

    dt = clock.tick(60) / 1000
    playerInfos["playerAnimTimer"] += 1
    
pygame.quit()