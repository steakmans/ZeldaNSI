import time

import pygame
import json
from os.path import exists

# Pygame values DO NOT MODIFY
pygame.init()
pygame_icon = pygame.image.load('./resources/gui/icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("ZeldaNSI")
screen = pygame.display.set_mode((1366, 912))  # , flags=pygame.FULLSCREEN | pygame.NOFRAME)
running = True
clock = pygame.time.Clock()
dt = 0
timer = 0
isInMainMenu = True
isInPauseMenu = False
isPauseKeyPressed = False
titleMusicPlaying = False
timeDelay = 30
fontTitle = pygame.font.SysFont("arial", 75)
fontButton = pygame.font.SysFont("arial", 30)
mouseMask = pygame.mask.Mask((1, 1), True)
pygame.mixer.music.set_volume(0.1)
textToShow = []

# Constants
ICONS = {
    "fullHearth": pygame.transform.scale_by(pygame.image.load("resources/gui/full_heart.png").convert_alpha(), 4),
    "3/4Hearth": pygame.transform.scale_by(pygame.image.load("resources/gui/heart-3.png").convert_alpha(), 4),
    "2/4Hearth": pygame.transform.scale_by(pygame.image.load("resources/gui/heart-2.png").convert_alpha(), 4),
    "1/4Hearth": pygame.transform.scale_by(pygame.image.load("resources/gui/heart-1.png").convert_alpha(), 4),
    "emptyHearth": pygame.transform.scale_by(pygame.image.load("resources/gui/empty_hearth.png").convert_alpha(), 4),
    "bubble": pygame.transform.scale(pygame.image.load("resources/gui/bubble.png").convert_alpha(), (1366, 912 / 4)),
    "chest_closed": pygame.transform.scale_by(pygame.image.load("resources/map/chest_closed.png").convert_alpha(), 4),
    "chest_opened": pygame.transform.scale_by(pygame.image.load("resources/map/chest_opened.png").convert_alpha(), 4)
}
MAIN_MENU = {
    "background": pygame.transform.scale(pygame.image.load("resources/gui/full_heart.png").convert_alpha(),
                                         (1366, 912)),
    "buttons": ((pygame.Rect(1366 / 2 - 150, 912 / 2 + 50, 300, 90), "Nouvelle partie"),
                (pygame.Rect(1366 / 2 - 150, 912 / 2 + 200, 300, 90), "Quitter"),
                (pygame.Rect(1366 / 2 - 150, 912 / 2 - 100, 300, 90), "Reprendre")),
    "text": (("ZeldaNSI", (1366 / 2, 200), True),)
}

TITLE_MUSIC = "resources/music/title_theme.mp3"
DEATH_MUSIC = "resources/music/death.mp3"

PAUSE_MENU_BUTTONS = ((pygame.Rect(screen.get_width() / 2 - 150, 400, 300, 90), "Reprendre"),
                      (pygame.Rect(screen.get_width() / 2 - 150, 550, 300, 90), "Retourner au menu"))

SNAKE_TEXTURES = [
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_idle1.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_idle2.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_idle3.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_idle4.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_walk1.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_walk2.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_walk3.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_walk4.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_attack1.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_attack2.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_attack3.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_attack4.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_attack5.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_attack6.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_hurt1.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_hurt2.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_death1.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_death2.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_death3.png").convert_alpha(), 3),
    pygame.transform.scale_by(pygame.image.load("resources/ennemies/snake/snake_death4.png").convert_alpha(), 3),
]

PLAYER_CONSTS = {
    "playerTextures": (
        pygame.transform.scale_by(pygame.image.load("resources/character/idle down.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load("resources/character/idle up.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load("resources/character/idle left.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/idle right.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk down 1.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load("resources/character/walk up1.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk left1.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk right1.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk down 2.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load("resources/character/walk up2.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk left2.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk right2.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk down 3.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load("resources/character/walk up3.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk left3.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/walk right3.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack down 1.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack up 1.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack left 1.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack right 1.png").convert_alpha(),
                                  2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack down 2.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack up 2.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack left 2.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack right 2.png").convert_alpha(),
                                  2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack down 3.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack up 3.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack left 3.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack right 3.png").convert_alpha(),
                                  2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack down 4.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack up 4.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack left 4.png").convert_alpha(), 2),
        pygame.transform.scale_by(pygame.image.load(
            "resources/character/attack right 4.png").convert_alpha(), 2)
    ),
    "playerCollision": (pygame.mask.Mask((20, 5), True),  # top and bottom collision mask
                        pygame.mask.Mask((5, 5), True)),  # left and right collision mask
    "attackCollider": pygame.Rect((-100, -100), (70, 70))
}

# Gameplay values
playerInfos = {
    "playerPos": pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),
    "playerSpeed": pygame.Vector2(0, 0),
    "life": 12,
    "maxHealth": 12,
    "coins": 0,
    "objects": {},
    "damage": 50,
    "speed": 200,
    "playerXToMove": False,
    "playerYToMove": False,
    "playerDir": 0,  # 0 = down, 1 = up, 2 = left, 3 = right
    "playerAnimIndex": 0,
    "playerAnimTimer": 0,
    "attacking": False,
    "ennemiesHit": [],
    "attackTimer": 0,
}


# World related objects
def showMessageOnScreen(texts):
    global textToShow
    textToShow.clear()
    for txt in texts:
        textToShow.append((txt, time.time() + 5))


def openChest(id):
    global worldInfos, playerInfos
    if not worldInfos["chests"][worldInfos["worldIndex"]][id][1]:
        if worldInfos["chests"][worldInfos["worldIndex"]][id][0][0] in playerInfos["objects"]:
            playerInfos["objects"][worldInfos["chests"][worldInfos["worldIndex"]][id][0][0]] += \
                worldInfos["chests"][worldInfos["worldIndex"]][id][0][1]
        else:
            playerInfos["objects"][worldInfos["chests"][worldInfos["worldIndex"]][id][0][0]] = \
                worldInfos["chests"][worldInfos["worldIndex"]][id][0][1]
        worldInfos["chests"][worldInfos["worldIndex"]][id][1] = True
        showMessageOnScreen(("Vous avez obtenu " + str(worldInfos["chests"][worldInfos["worldIndex"]][id][0][1]) + " " +
                             worldInfos["chests"][worldInfos["worldIndex"]][id][0][0],))


worldInfos_base = {"worldPos": pygame.Vector2(-200, -250),
                   "worldIndex": 0,
                   "music": ("resources/music/spawn_village_theme.mp3",
                             "resources/music/field_theme.mp3",
                             "resources/music/field_theme.mp3",
                             "resources/music/field_theme.mp3",
                             "resources/music/field_theme.mp3"),
                   "background": (
                       pygame.transform.scale(pygame.image.load("./resources/map/spawn.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/map1.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/beach.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest1.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest2.png").convert_alpha(),
                                              (1766, 1177))
                   ),
                   "colliding": (
                       pygame.transform.scale(pygame.image.load("./resources/map/spawn_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/map1_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/beach_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest1_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest2_coll.png").convert_alpha(),
                                              (1766, 1177))
                   ),
                   "foreground": (
                       pygame.transform.scale(pygame.image.load("./resources/map/spawn_fore.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177))
                   ),
                   "collisions": [],
                   "ennemiesCleared": [False, False, False, False, False],
                   # (Type, Life, Pos, Rect size, Damage, ViewDistance, ReachDistance, TimeToAttack)
                   "ennemiesForMap": ((),  # 0
                                      (),  # 1
                                      (),  # 2
                                      (),  # 3
                                      ((0, 100, (200, 1000), (50, 50), 1, 300, 15, 1),
                                       (0, 100, (800, 950), (50, 50), 1, 300, 15, 1),
                                       (0, 100, (1200, 200), (50, 50), 1, 300, 15, 1))  # 4
                                      ),
                   # tuple of tuples(map index) of tuples (mask, mapIndex, maskX, maskY, destPlayerX, destPlayerY, destMapX, destMapY)
                   "changeMapTriggers": (
                   ((pygame.mask.Mask((175, 15), True), 1, 635, 10, 1366 / 2, 870, -230, -265),),  # 0
                   ((pygame.mask.Mask((175, 15), True), 0, 635, 900, 1366 / 2, 0, -230, 0),  # 1
                    (pygame.mask.Mask((15, 300), True), 2, 1351, 905 / 2 - 250 / 2, 0,
                     screen.get_height() / 2, 0, -150),
                    (pygame.mask.Mask((15, 300), True), 3, -15, 905 / 2 - 250 / 2, 1300,
                     screen.get_height() / 2, -400, -100)),
                   ((pygame.mask.Mask((15, 300), True), 1, -15, 905 / 2 - 250 / 2, 1300,
                     screen.get_height() / 2, -400, -150),),  # 2
                   ((pygame.mask.Mask((15, 300), True), 1, 1351, 905 / 2 - 250 / 2, 0,
                     screen.get_height() / 2, 0, -150),
                    (pygame.mask.Mask((300, 15), True), 4, 400, 900, 1366 / 2 - 100, 20, 0, 0)),  # 3
                   ((pygame.mask.Mask((300, 15), True), 3, 400, 0, 1366 / 2 - 100, 870, 0, -265),)),
                   # 4
                   "interactables": (  # tuple of tuples(map index) of tuples (mask, action, maskX, maskY)
                       (), ((pygame.mask.Mask((75, 75), True), showMessageOnScreen, 1555, 475, ("test", "ligne2")),
                            (pygame.mask.Mask((75, 75), True), openChest, 875, 125, 0))),
                   "chests": [[], [[("épée", 1), False, (875, 95)]], [], [], []]
                   }

worldInfos = worldInfos_base.copy()
ennemiesList = []

for item in worldInfos["colliding"]:
    worldInfos["collisions"].append(pygame.mask.from_surface(item))


# functions
def clamp(value, minValue, maxValue):
    if value > maxValue:
        return maxValue
    elif value < minValue:
        return minValue
    return value


def attack(player):
    attack_pos = player["playerPos"].__copy__()
    if player["playerDir"] == 0:
        attack_pos.x -= 30
        attack_pos.y -= 15
    elif player["playerDir"] == 1:
        attack_pos.x -= 30
        attack_pos.y -= 55
    elif player["playerDir"] == 2:
        attack_pos.y -= 40
        attack_pos.x -= 50
    elif player["playerDir"] == 3:
        attack_pos.y -= 40
    PLAYER_CONSTS["attackCollider"].x = attack_pos.x
    PLAYER_CONSTS["attackCollider"].y = attack_pos.y


def changeMap(world, player, ennemies, mapIndex,
              playerPos=pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),
              worldPos=pygame.Vector2(-200, -200), spawnEnnemies=True, forceMusic=False, forceChange=False):
    if world["worldIndex"] == mapIndex and not forceChange:
        return

    if world["music"][world["worldIndex"]] != world["music"][mapIndex] or forceMusic:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(world["music"][mapIndex])
        pygame.mixer.music.play(-1, 0, 0)

    world["worldIndex"] = mapIndex
    ennemies.clear()
    if playerPos.x == screen.get_width() / 2:
        player["playerXToMove"] = False
    else:
        player["playerXToMove"] = True
    if playerPos.y == screen.get_height() / 2:
        player["playerYToMove"] = False
    else:
        player["playerYToMove"] = True
    world["worldPos"] = worldPos
    player["playerPos"] = playerPos
    if spawnEnnemies and not world["ennemiesCleared"][mapIndex]:
        for ennemy in worldInfos["ennemiesForMap"][mapIndex]:
            print("called")
            createEnnemy(ennemies, ennemy[0], ennemy[1], pygame.Rect(ennemy[2], ennemy[3]), ennemy[4], ennemy[5],
                         ennemy[6], ennemy[7])


def createEnnemy(ennemies, type, life, rect, damage=10, viewDistance=100, reachDistance=15, timeToAttack=3):
    attributes = {
        "type": type,
        "life": life,
        "damage": damage,
        "playerDetected": False,
        "viewDistance": viewDistance,
        "reachDistance": reachDistance,
        "rect": rect,
        "animIndex": 0,
        "attackTimer": 0,
        "attacking": False,
        "animTimer": 0,
        "hurtTimer": 0,
        "timeToAttack": timeToAttack
    }
    ennemies.append(attributes)


def manageEnnemies(ennemies, player, world):
    for ennemy in ennemies:
        if player["playerPos"].distance_to(pygame.Vector2(ennemy["rect"].x + ennemy["rect"].width // 2,
                                                          ennemy["rect"].y + ennemy["rect"].height // 2)) <= ennemy[
            "viewDistance"] and not ennemy["playerDetected"]:
            ennemy["playerDetected"] = True
            ennemy["animIndex"] = 0
        if ennemy["playerDetected"]:
            if world["collisions"][world["worldIndex"]].get_at((-world["worldPos"].x + ennemy["rect"].x + ennemy[
                "rect"].width + 10, -world["worldPos"].y + ennemy["rect"].y + ennemy["rect"].height // 2)) == 0:
                ennemy["rect"].x += 100 * dt
            if world["collisions"][world["worldIndex"]].get_at((-world["worldPos"].x + ennemy["rect"].x - 10,
                                                                -world["worldPos"].y + ennemy["rect"].y + ennemy[
                                                                    "rect"].height // 2)) == 0:
                ennemy["rect"].x -= 100 * dt
            if world["collisions"][world["worldIndex"]].get_at((-world["worldPos"].x + ennemy["rect"].x + ennemy[
                "rect"].width // 2, -world["worldPos"].y + ennemy["rect"].y + ennemy["rect"].height + 10)) == 0:
                ennemy["rect"].y += 100 * dt
            if world["collisions"][world["worldIndex"]].get_at((-world["worldPos"].x + ennemy["rect"].x + ennemy[
                "rect"].width // 2, -world["worldPos"].y + ennemy["rect"].y - 10)) == 0:
                ennemy["rect"].y -= 100 * dt
            ennemy["rect"].y += 100 * clamp(player["playerPos"].y - ennemy["rect"].y - ennemy["rect"].height // 2, -1,
                                            1) * dt
            ennemy["rect"].x += 100 * clamp(player["playerPos"].x - ennemy["rect"].x - ennemy["rect"].width // 2, -1,
                                            1) * dt
        if player["playerPos"].distance_to(pygame.Vector2(ennemy["rect"].x + ennemy["rect"].width // 2,
                                                          ennemy["rect"].y + ennemy["rect"].height // 2)) <= ennemy[
            "reachDistance"]:
            ennemy["attackTimer"] += dt
            if ennemy["attackTimer"] >= ennemy["timeToAttack"] - 0.45 and ennemy["type"] == 0:
                ennemy["attacking"] = True
            if ennemy["attackTimer"] >= ennemy["timeToAttack"]:
                ennemy["attackTimer"] = 0
                player["life"] -= ennemy["damage"]
                if player["life"] <= 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(DEATH_MUSIC, "mp3")
                    pygame.mixer.music.play(1, 0, 0)
        else:
            ennemy["attackTimer"] = 0


def manageControls(keys, player):
    if keys[pygame.K_SPACE] and not player["attacking"] and "épée" in player["objects"]:
        player["attacking"] = True
        player["playerAnimIndex"] = 16 + player["playerDir"]
        attack(player)

    if keys[pygame.K_EQUALS]:
        print(player["playerPos"], worldInfos["worldPos"])
        createEnnemy(ennemiesList, 0, 100, pygame.Rect(player["playerPos"].__copy__(), (50, 50)), 2,
                     timeToAttack=1)

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

        playerInfos["playerAnimTimer"] += player["speed"] / 200
    else:
        player["playerSpeed"].x = 0
        player["playerSpeed"].y = 0
        player["attackTimer"] += 1
        if player["attackTimer"] >= 32:
            player["attacking"] = False
            player["ennemiesHit"].clear()
            player["attackTimer"] = 0
            PLAYER_CONSTS["attackCollider"].x = -100
            PLAYER_CONSTS["attackCollider"].y = -100
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

    if world["worldPos"].x < -400:
        world["worldPos"].x = -400
        player["playerXToMove"] = True
        player["playerPos"].x = screen.get_width() / 2 + player["speed"] * 0.017

    if world["worldPos"].y > 0:
        world["worldPos"].y = 0
        player["playerYToMove"] = True
        player["playerPos"].y = screen.get_height() / 2 - player["speed"] * 0.017

    if world["worldPos"].y < -265:
        world["worldPos"].y = -265
        player["playerYToMove"] = True
        player["playerPos"].y = screen.get_height() / 2 + player["speed"] * 0.017

    if abs(player["playerPos"].x - screen.get_width() / 2) < player["speed"] * 0.016:
        player["playerPos"].x = screen.get_width() / 2
        player["playerXToMove"] = False
    if abs(player["playerPos"].y - screen.get_height() / 2) < player["speed"] * 0.016:
        player["playerPos"].y = screen.get_height() / 2
        player["playerYToMove"] = False


def manageDisplay(player, world, ennemies, needFlip):
    global PLAYER_CONSTS
    debug = True
    screen.fill("black")

    screen.blit(world["background"][world["worldIndex"]], world["worldPos"])
    screen.blit(world["colliding"][world["worldIndex"]], world["worldPos"])

    for i in range(len(world["chests"][world["worldIndex"]])):
        if world["chests"][world["worldIndex"]][i][1]:
            screen.blit(ICONS["chest_opened"], (
                world["chests"][world["worldIndex"]][i][2][0] + world["worldPos"][0] - 23,
                world["chests"][world["worldIndex"]][i][2][1] + world["worldPos"][1] - 32))
        else:
            screen.blit(ICONS["chest_closed"], (
                world["chests"][world["worldIndex"]][i][2][0] + world["worldPos"][0] - 23,
                world["chests"][world["worldIndex"]][i][2][1] + world["worldPos"][1]))

    for ennemy in ennemies:
        if ennemy["type"] == 0:
            if ennemy["playerDetected"]:
                index = 0 + ennemy["animIndex"]
                if ennemy["hurtTimer"] > 0:
                    index = 14 + ennemy["animIndex"]
                    if ennemy["animIndex"] > 1:
                        ennemy["animIndex"] = 0
                    if ennemy["hurtTimer"] >= 2:
                        ennemy["hurtTimer"] = 0
                    else:
                        ennemy["hurtTimer"] += dt
                elif ennemy["attacking"]:
                    index = 8 + ennemy["animIndex"]
                    if ennemy["animIndex"] > 5:
                        ennemy["animIndex"] = 0
                        ennemy["attacking"] = False
                elif abs(ennemy["rect"].x - player["playerPos"].x) > 30 or abs(
                        ennemy["rect"].y - player["playerPos"].y) > 30:
                    index = 4 + ennemy["animIndex"]
                    if ennemy["animIndex"] > 3:
                        ennemy["animIndex"] = 0
                elif ennemy["animIndex"] > 3:
                    ennemy["animIndex"] = 0
                if ennemy["rect"].x <= player["playerPos"].x - 20:
                    screen.blit(pygame.transform.flip(SNAKE_TEXTURES[index], True, False),
                                (ennemy["rect"].x - 32, ennemy["rect"].y - 32))
                else:
                    screen.blit(SNAKE_TEXTURES[index], (ennemy["rect"].x - 32, ennemy["rect"].y - 32))
            else:
                screen.blit(SNAKE_TEXTURES[0], (ennemy["rect"].x - 32, ennemy["rect"].y - 32))
        if ennemy["animTimer"] > 8:
            ennemy["animIndex"] += 1
            ennemy["animTimer"] = 0
        ennemy["animTimer"] += 1

    playerPos = player["playerPos"].__copy__()
    playerPos.x -= 30
    playerPos.y -= 80
    screen.blit(PLAYER_CONSTS["playerTextures"][player["playerAnimIndex"]], playerPos)

    screen.blit(world["foreground"][world["worldIndex"]], world["worldPos"])

    for hearts in range(player["maxHealth"] // 4):
        if player["life"] - 4 - 4 * hearts >= 0:
            screen.blit(ICONS["fullHearth"], (15 + 66 * hearts, 15))
        elif player["life"] - 3 - 4 * hearts >= 0:
            screen.blit(ICONS["3/4Hearth"], (15 + 66 * hearts, 15))
        elif player["life"] - 2 - 4 * hearts >= 0:
            screen.blit(ICONS["2/4Hearth"], (15 + 66 * hearts, 15))
        elif player["life"] - 1 - 4 * hearts >= 0:
            screen.blit(ICONS["1/4Hearth"], (15 + 66 * hearts, 15))
        else:
            screen.blit(ICONS["emptyHearth"], (15 + 66 * hearts, 15))

    if len(textToShow) > 0:
        screen.blit(ICONS["bubble"], (0, (3 / 4) * screen.get_height()))
        for i in range(len(textToShow)):
            img = fontButton.render(textToShow[i][0], True, "black")
            screen.blit(img, (35, (3 / 4) * screen.get_height() + 25 + i * 50))

    if debug:
        for maptrig in world["changeMapTriggers"][world["worldIndex"]]:
            pygame.draw.rect(screen, "red", maptrig[0].get_rect(
                topleft=(maptrig[2] * 1.3 + world["worldPos"].x, maptrig[3] * 1.3 + world["worldPos"].y)))

    if needFlip:
        pygame.display.flip()


def manageCollisions(player, world, ennemies):
    global PLAYER_CONSTS
    # top
    if PLAYER_CONSTS["playerCollision"][0].overlap(world["collisions"][world["worldIndex"]], (
            world["worldPos"].x - player["playerPos"].x + 7, world["worldPos"].y - player["playerPos"].y - 10)):
        if player["playerSpeed"].y > 0:
            player["playerSpeed"].y = 0

    # bottom
    if PLAYER_CONSTS["playerCollision"][0].overlap(world["collisions"][world["worldIndex"]], (
            world["worldPos"].x - player["playerPos"].x + 7, world["worldPos"].y - player["playerPos"].y - 20)):
        if player["playerSpeed"].y < 0:
            player["playerSpeed"].y = 0
    # left
    if PLAYER_CONSTS["playerCollision"][1].overlap(world["collisions"][world["worldIndex"]], (
            world["worldPos"].x - player["playerPos"].x + 12, world["worldPos"].y - player["playerPos"].y - 15)):
        if player["playerSpeed"].x > 0:
            player["playerSpeed"].x = 0
    # left
    if PLAYER_CONSTS["playerCollision"][1].overlap(world["collisions"][world["worldIndex"]], (
            world["worldPos"].x - player["playerPos"].x - 12, world["worldPos"].y - player["playerPos"].y - 15)):
        if player["playerSpeed"].x < 0:
            player["playerSpeed"].x = 0

    for ennemy in ennemies[:]:
        if PLAYER_CONSTS["attackCollider"].colliderect(ennemy["rect"]) and ennemy not in player["ennemiesHit"]:
            player["ennemiesHit"].append(ennemy)
            ennemy["life"] -= player["damage"]
            ennemy["hurtTimer"] = 1
            if player["playerDir"] == 0:
                ennemy["rect"].y += 50
            if player["playerDir"] == 1:
                ennemy["rect"].y -= 50
            if player["playerDir"] == 2:
                ennemy["rect"].x -= 50
            if player["playerDir"] == 3:
                ennemy["rect"].x += 50
            if ennemy["life"] <= 0:
                ennemies.remove(ennemy)
                if len(ennemies) == 0:
                    world["ennemiesCleared"][world["worldIndex"]] = True

    for mapTrigger in world["changeMapTriggers"][world["worldIndex"]]:
        if mapTrigger[0].overlap(PLAYER_CONSTS["playerCollision"][0],
                                 (player["playerPos"].x - mapTrigger[2],
                                  player["playerPos"].y - mapTrigger[3])):
            changeMap(world, player, ennemies, mapTrigger[1], pygame.Vector2(mapTrigger[4], mapTrigger[5]),
                      pygame.Vector2(mapTrigger[6], mapTrigger[7]))


def manageMainMenu(menu, world, player, ennemies):
    global isInMainMenu, titleMusicPlaying, timeDelay, isInPauseMenu
    pygame.mouse.set_visible(True)
    screen.fill("black")

    if not titleMusicPlaying:
        pygame.mixer.music.load(TITLE_MUSIC, "mp3")
        pygame.mixer.music.play(-1, 0, 0)
        titleMusicPlaying = True

    screen.blit(menu["background"], (0, 0))
    for button in MAIN_MENU["buttons"]:
        if not button[1] == "Reprendre":
            pygame.draw.rect(screen, "red", button[0])
            img = fontButton.render(button[1], True, "white")
            screen.blit(img, (button[0].x + button[0].width / 2 - img.get_width() / 2,
                              button[0].y + button[0].height / 2 - img.get_height() / 2))
        elif exists("save/save.json"):
            pygame.draw.rect(screen, "red", button[0])
            img = fontButton.render(button[1], True, "white")
            screen.blit(img, (button[0].x + button[0].width / 2 - img.get_width() / 2,
                              button[0].y + button[0].height / 2 - img.get_height() / 2))
        if button[0].topleft[0] <= pygame.mouse.get_pos()[0] <= button[0].bottomright[0] and button[0].topleft[1] <= \
                pygame.mouse.get_pos()[1] <= button[0].bottomright[1] and pygame.mouse.get_pressed()[0]:

            if button[1] == "Nouvelle partie" and timeDelay >= 15:
                global playerInfos, worldInfos, worldInfos_base
                isInMainMenu = False
                isInPauseMenu = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(world["music"][0])
                pygame.mixer.music.play(-1, 0, 0)
                playerInfos = {
                    "playerPos": pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),
                    "playerSpeed": pygame.Vector2(0, 0),
                    "life": 12,
                    "maxHealth": 12,
                    "coins": 0,
                    "objects": {},
                    "damage": 50,
                    "speed": 200,
                    "playerXToMove": False,
                    "playerYToMove": False,
                    "playerDir": 0,  # 0 = down, 1 = up, 2 = left, 3 = right
                    "playerAnimIndex": 0,
                    "playerAnimTimer": 0,
                    "attacking": False,
                    "ennemiesHit": [],
                    "attackTimer": 0,
                }
                worldInfos = worldInfos_base.copy()
                playerInfos["playerPos"] = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                worldInfos["worldPos"] = pygame.Vector2(-200, -250)
                worldInfos[""] = worldInfos_base["chests"].copy()
                #changeMap(worldInfos, playerInfos, ennemies, 0, worldPos=pygame.Vector2(-200, -250), forceChange=True)
                saveGame(worldInfos, playerInfos)

            if button[1] == "Reprendre" and timeDelay >= 15 and exists("save/save.json"):
                isInMainMenu = False
                isInPauseMenu = False
                pygame.mixer.music.stop()
                loadGame()
                pygame.mixer.music.load(world["music"][world["worldIndex"]])
                pygame.mixer.music.play(-1, 0, 0)
                changeMap(world, player, ennemies, world["worldIndex"], worldPos=pygame.Vector2(-200, -250))
            if button[1] == "Quitter" and timeDelay >= 60:
                global running
                running = False

    for text in menu["text"]:
        img = fontTitle.render(text[0], True, "White") if text[2] else fontButton.render(text[0], True, "White")
        screen.blit(img, (text[1][0] - img.get_width() / 2, text[1][1]))

    pygame.display.flip()


def managePauseMenu(player, world, ennemies, buttons):
    manageDisplay(player, world, ennemies, False)

    s = pygame.Surface((screen.get_width(), screen.get_height()),
                       pygame.SRCALPHA)  # Creates a surface with transparent pixels
    s.fill((0, 0, 0, 200))
    screen.blit(s, (0, 0))
    img = fontTitle.render("Jeu en pause", True, "White")
    screen.blit(img, (screen.get_width() / 2 - img.get_width() / 2, 200))

    for button in buttons:
        pygame.draw.rect(screen, "red", button[0])
        img = fontButton.render(button[1], True, "white")
        screen.blit(img, (button[0].x + button[0].width / 2 - img.get_width() / 2,
                          button[0].y + button[0].height / 2 - img.get_height() / 2))
        if button[0].topleft[0] <= pygame.mouse.get_pos()[0] <= button[0].bottomright[0] and button[0].topleft[1] <= \
                pygame.mouse.get_pos()[1] <= button[0].bottomright[1] and pygame.mouse.get_pressed()[0]:
            if button[1] == "Retourner au menu":
                global isInMainMenu, titleMusicPlaying, timeDelay
                isInMainMenu = True
                titleMusicPlaying = False
                timeDelay = 0
                saveGame(world, player)
            if button[1] == "Reprendre":
                global isInPauseMenu
                isInPauseMenu = False

    pygame.display.flip()


def saveGame(world, player):
    try:
        with open("save/save.json", "w") as file:
            dict_prov = player.copy()
            dict_prov["playerPos"] = (player["playerPos"].x, player["playerPos"].y)
            dict_prov["playerSpeed"] = (0, 0)
            dict_prov["worldIndex"] = world["worldIndex"]
            dict_prov["worldPos"] = (world["worldPos"].x, world["worldPos"].y)
            dict_prov["chests"] = worldInfos["chests"]
            dict_prov["ennemiesCleared"] = worldInfos["ennemiesCleared"]
            del dict_prov["ennemiesHit"]
            json.dump(dict_prov, file)
            file.close()
            print("Saved game")
    except FileNotFoundError:
        print("Save file was not found")


def loadGame():
    global playerInfos, worldInfos
    try:
        with open("save/save.json", "r") as file:
            dict_prov = json.loads(file.read())
            worldInfos["worldPos"] = pygame.Vector2(dict_prov["worldPos"][0], dict_prov["worldPos"][1])
            worldInfos["worldIndex"] = dict_prov["worldIndex"]
            worldInfos["chests"] = dict_prov["chests"]
            worldInfos["ennemiesCleared"] = dict_prov["ennemiesCleared"]
            playerInfos = dict_prov.copy()
            playerInfos["playerPos"] = pygame.Vector2(dict_prov["playerPos"][0], dict_prov["playerPos"][1])
            playerInfos["playerSpeed"] = pygame.Vector2(0, 0)
            playerInfos["life"] = dict_prov["life"]
            playerInfos["ennemiesHit"] = []
            del playerInfos["worldIndex"], playerInfos["worldPos"], playerInfos["chests"], playerInfos[
                "ennemiesCleared"]
            file.close()
            changeMap(worldInfos, playerInfos, ennemiesList, dict_prov["worldIndex"], playerInfos["playerPos"],
                      worldInfos["worldPos"], spawnEnnemies=True, forceMusic=True, forceChange=True)
            print("Loaded save file")
    except FileNotFoundError:
        print("Save file was not found")


def manageInteractables(world, player):
    for interactable in world["interactables"][world["worldIndex"]]:
        if interactable[0].overlap(PLAYER_CONSTS["playerCollision"][0],
                                   (player["playerPos"].x - 7 - interactable[2] - world["worldPos"][0],
                                    player["playerPos"].y - interactable[3] + 20 - world["worldPos"][1])):
            interactable[1](interactable[4])


def manageDeath(timer):
    global isInMainMenu, timeDelay
    if timer > 1:
        timer = 0
        black_fade = pygame.Surface((screen.get_width(), screen.get_height()))
        black_fade.set_alpha(10)
        screen.blit(black_fade, (0, 0))
        pygame.mouse.set_visible(True)

        # buttons
        pygame.draw.rect(screen, "red", pygame.Rect(1366 / 2 - 150, 912 / 2 + 50, 300, 90))
        pygame.draw.rect(screen, "red", pygame.Rect(1366 / 2 - 150, 912 / 2 - 100, 300, 90))
        img = fontTitle.render("Vous êtes mort", True, "White")
        screen.blit(img, (1366 / 2 - img.get_width() / 2, 200))
        img = fontButton.render("Reprendre à la", True, "White")
        screen.blit(img, (1366 / 2 - img.get_width() / 2, 912 / 2 - 95))
        img = fontButton.render("dernière sauvegarde", True, "White")
        screen.blit(img, (1366 / 2 - img.get_width() / 2, 912 / 2 - 55))
        img = fontButton.render("Retour au menu", True, "White")
        screen.blit(img, (1366 / 2 - img.get_width() / 2, 912 / 2 + 75))

        if 1366 / 2 - 150 <= pygame.mouse.get_pos()[0] <= 1366 / 2 + 150 and pygame.mouse.get_pressed()[0]:
            if 912 / 2 + 50 <= pygame.mouse.get_pos()[1] <= 912 / 2 + 140:
                isInMainMenu = True
                timeDelay = 0
            if 912 / 2 - 100 <= pygame.mouse.get_pos()[1] <= 912 / 2 - 10:
                loadGame()

        pygame.display.update()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                manageInteractables(worldInfos, playerInfos)

    if pygame.key.get_pressed()[pygame.K_ESCAPE] and not isInMainMenu:
        if not isPauseKeyPressed and playerInfos["life"] > 0:
            isInPauseMenu = not isInPauseMenu
        isPauseKeyPressed = True
    else:
        isPauseKeyPressed = False

    if not isInMainMenu and not isInPauseMenu:
        manageControls(pygame.key.get_pressed(), playerInfos)
        manageAnimations(playerInfos)

    pygame.mouse.set_visible(isInPauseMenu or isInMainMenu)
    if isInPauseMenu:
        dt = 0

    if isInMainMenu:
        manageMainMenu(MAIN_MENU, worldInfos, playerInfos, ennemiesList)
    elif isInPauseMenu:
        managePauseMenu(playerInfos, worldInfos, ennemiesList, PAUSE_MENU_BUTTONS)
    elif playerInfos["life"] <= 0:
        manageDeath(timer)
    else:
        manageCollisions(playerInfos, worldInfos, ennemiesList)
        manageMovement(playerInfos, worldInfos, ennemiesList)
        manageEnnemies(ennemiesList, playerInfos, worldInfos)
        manageDisplay(playerInfos, worldInfos, ennemiesList, True)

    for text in textToShow.copy():
        if text[1] < time.time():
            textToShow.remove(text)
    dt = clock.tick(60) / 1000
    timeDelay += 1
    timer += dt

pygame.quit()
