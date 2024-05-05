import time

import pygame
import json
from os.path import exists
from os import mkdir

# Pygame values DO NOT MODIFY
pygame.init()
pygame_icon = pygame.image.load('./resources/gui/icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("ZeldaNSI")
screen = pygame.display.set_mode((1366, 912)) #, flags=pygame.FULLSCREEN | pygame.NOFRAME)
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
interact_mask = pygame.mask.Mask((115, 115), True)
game_finished = False

back_x = 0
back_y = 0
movement = True

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
SOUND_EFFECTS = {
    "chest": pygame.mixer.Sound("resources/sounds/chest.mp3"),
    "small_chest": pygame.mixer.Sound("resources/sounds/small_chest.mp3"),
    "trumpet": pygame.mixer.Sound("resources/sounds/trumpet.mp3"),
}
for sound in SOUND_EFFECTS.values():
    sound.set_volume(0.5)

TITLE_MUSIC = "resources/music/title_theme.mp3"
DEATH_MUSIC = "resources/music/death.mp3"

PAUSE_MENU_BUTTONS = ((pygame.Rect(screen.get_width() / 2 - 150, 400, 300, 90), "Reprendre"),
                      (pygame.Rect(screen.get_width() / 2 - 150, 550, 300, 90), "Retourner au menu"))

BACKGROUND = pygame.transform.scale_by(pygame.image.load("resources/gui/world.png").convert_alpha(), 4)

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

MASK_SNAKE = pygame.mask.from_surface(SNAKE_TEXTURES[0])

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
    "playerPos": pygame.Vector2(686, 332),
    "playerSpeed": pygame.Vector2(0, 0),
    "life": 12,
    "maxHealth": 12,
    "objects": {"coeur": 0},
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
def showMessageOnScreen(texts, textToShow):
    textToShow.clear()
    for txt in texts:
        textToShow.append((txt, time.time() + 5))


def openChest(id, worldInfos, playerInfos, textToShow):
    if not worldInfos["chests"][worldInfos["worldIndex"]][id][1]:
        if worldInfos["chests"][worldInfos["worldIndex"]][id][0][0] in playerInfos["objects"]:
            playerInfos["objects"][worldInfos["chests"][worldInfos["worldIndex"]][id][0][0]] += \
                worldInfos["chests"][worldInfos["worldIndex"]][id][0][1]
        else:
            playerInfos["objects"][worldInfos["chests"][worldInfos["worldIndex"]][id][0][0]] = \
                worldInfos["chests"][worldInfos["worldIndex"]][id][0][1]
        worldInfos["chests"][worldInfos["worldIndex"]][id][1] = True
        if worldInfos["chests"][worldInfos["worldIndex"]][id][0][0] == "épée":
            showMessageOnScreen(
                ("Vous avez obtenu " + str(worldInfos["chests"][worldInfos["worldIndex"]][id][0][1]) + " " +
                 worldInfos["chests"][worldInfos["worldIndex"]][id][0][0],"Vous pouvez désormais attaquer en appuyant sur ESPACE"), textToShow)
        elif worldInfos["chests"][worldInfos["worldIndex"]][id][0][0] == "bottes":
            showMessageOnScreen(
                ("Vous avez obtenu " + str(worldInfos["chests"][worldInfos["worldIndex"]][id][0][1]) + " " +
                 worldInfos["chests"][worldInfos["worldIndex"]][id][0][0],
                 "Vous pouvez desormais courire en appuyant sur MAJ"), textToShow)
        else:
            showMessageOnScreen(
                ("Vous avez obtenu " + str(worldInfos["chests"][worldInfos["worldIndex"]][id][0][1]) + " " +
                 worldInfos["chests"][worldInfos["worldIndex"]][id][0][0],), textToShow)
        if worldInfos["chests"][worldInfos["worldIndex"]][id][3]:
            SOUND_EFFECTS["small_chest"].play()
        else:
            SOUND_EFFECTS["chest"].play()


def interactChangeMap(screen, world, player, ennemies, args):
    changeMap(screen, world, player, ennemies, args[0], pygame.Vector2(args[1], args[2]), pygame.Vector2(args[3],
                                                                                                         args[4]))


def interactNpc(texts, textToShow, objects, player, condition):
    items = 0
    for object in condition:
        if object in player["objects"]:
            items += 1

    if items == len(condition) and items != 0:
        return True
    else:

        if len(objects) > 0:
            if not objects[0] in player["objects"]:
                player["objects"][objects[0]] = objects[1]
                texts = texts + ("Vous avez obtenu " + str(objects[1]) + " " + objects[0],)
        showMessageOnScreen(texts, textToShow)
        return False


worldInfos_base = {"worldPos": pygame.Vector2(-400, 0),
                   "worldIndex": 27,
                   "music": ("resources/music/spawn_village_theme.mp3",
                             "resources/music/field_theme.mp3",
                             "resources/music/field_theme.mp3",
                             "resources/music/field_theme.mp3",
                             "resources/music/forest.mp3",
                             "resources/music/forest.mp3",
                             "resources/music/forest.mp3",
                             "resources/music/forest.mp3",
                             "resources/music/forest.mp3",
                             "resources/music/forest.mp3",
                             "resources/music/forest.mp3",
                             "resources/music/forest.mp3",
                             "resources/music/forest_village.mp3",
                             "resources/music/forest_village.mp3",
                             "resources/music/forest_village.mp3",
                             "resources/music/forest_village.mp3",
                             "resources/music/cave_theme.mp3",
                             "resources/music/cave_theme.mp3",
                             "resources/music/cave_theme.mp3",
                             "resources/music/cave_theme.mp3",
                             "resources/music/cave_theme.mp3",
                             "resources/music/cave_theme.mp3",
                             "resources/music/cave_theme.mp3",
                             "resources/music/cave_village_theme.mp3",
                             "resources/music/field_theme.mp3",
                             "resources/music/field_theme.mp3",
                             "resources/music/house_theme.mp3",
                             "resources/music/house_theme.mp3"),
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
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest3.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest4.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest5.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest6.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest7.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest8.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest9.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest_village1.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest_village2.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest_village3.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest_village4.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave1.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave2.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave3.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave4.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave5.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave6.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave7.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave_village1.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/yard1.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("resources/map/yard2.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("resources/map/house_princesse.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("resources/map/house_hero.png").convert_alpha(),
                                              (1766, 1177)),
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
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest3_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest4_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest5_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest6_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest7_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest8_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/forest9_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(
                           pygame.image.load("./resources/map/forest_village1_coll.png").convert_alpha(),
                           (1766, 1177)),
                       pygame.transform.scale(
                           pygame.image.load("./resources/map/forest_village2_coll.png").convert_alpha(),
                           (1766, 1177)),
                       pygame.transform.scale(
                           pygame.image.load("./resources/map/forest_village3_coll.png").convert_alpha(),
                           (1766, 1177)),
                       pygame.transform.scale(
                           pygame.image.load("./resources/map/forest_village4_coll.png").convert_alpha(),
                           (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave1_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave2_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave3_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave4_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave5_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave6_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/cave7_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(
                           pygame.image.load("./resources/map/cave_village1_coll.png").convert_alpha(),
                           (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/yard1_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("resources/map/yard2_coll.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(
                           pygame.image.load("resources/map/house_princesse_coll.png").convert_alpha(),
                           (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("resources/map/house_hero_coll.png").convert_alpha(),
                                              (1766, 1177)),
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
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                       pygame.transform.scale(pygame.image.load("./resources/map/empty.png").convert_alpha(),
                                              (1766, 1177)),
                   ),
                   "collisions": [],
                   "ennemiesCleared": [False] * 28,
                   # (Type, Life, Pos, Rect size, Damage, ViewDistance, ReachDistance, TimeToAttack)
                   "ennemiesForMap": ((),  # 0
                                      (),  # 1
                                      (),  # 2
                                      (),  # 3
                                      ((0, 100, (200, 1000), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (800, 950), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1200, 200), (50, 50), 1, 600, 15, 1)),  # 4
                                      ((0, 100, (400, 400), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (400, 900), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (700, 650), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1000, 400), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1000, 900), (50, 50), 1, 600, 15, 1)),
                                      (),
                                      ((0, 100, (1600, 115), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1550, 115), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1500, 115), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1600, 165), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1500, 165), (50, 50), 1, 600, 15, 1)),
                                      ((0, 100, (625, 450), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (725, 450), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (825, 450), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (925, 450), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1025, 450), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1125, 450), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (550, 450), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (725, 650), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (825, 650), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (925, 650), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1025, 650), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1125, 650), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (550, 650), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (550, 650), (50, 50), 1, 600, 15, 1),),
                                      ((0, 100, (800, 550), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (900, 450), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (1000, 550), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (900, 550), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (900, 650), (50, 50), 1, 600, 15, 1),
                                       (0, 100, (900, 750), (50, 50), 1, 600, 15, 1),),
                                      ((0, 500, (880, 546), (50, 50), 2, 600, 60, 0.75),),
                                      (),
                                      (),
                                      (),
                                      (),
                                      (),
                                      ((0, 200, (1180, 260), (50, 50), 1, 600, 30, 0.5),),
                                      ((0, 200, (1110, 770), (50, 50), 1, 600, 30, 0.5),
                                       (0, 200, (1110, 970), (50, 50), 1, 600, 30, 0.5)),
                                      ((0, 150, (1350, 550), (50, 50), 1, 600, 30, 0.5),
                                       (0, 150, (1350, 850), (50, 50), 1, 600, 30, 0.5)),
                                      (),
                                      ((0, 500, (610, 320), (50, 50), 2, 600, 60, 0.75),),
                                      ((0, 100, (570, 560), (50, 50), 1, 600, 30, 0.25),
                                       (0, 100, (1250, 560), (50, 50), 1, 600, 30, 0.25),
                                       (0, 200, (945, 280), (50, 50), 2, 600, 30, 1),
                                       (0, 200, (945, 900), (50, 50), 2, 600, 30, 1),
                                       (0, 600, (945, 560), (50, 50), 4, 600, 60, 2),),
                                      ((0, 500, (1420, 950), (50, 50), 2, 600, 60, 0.75),), #22
                                      (),
                                      (),
                                      (),
                                      (),
                                      ()
                                      ),
                   # tuple of tuples(map index) of tuples (mask, mapIndex, maskX, maskY, destPlayerX, destPlayerY,
                   # destMapX, destMapY)
                   "changeMapTriggers": (
                       ((pygame.mask.Mask((175, 15), True), 1, 635, 10, -1, 870, -1, -265),),  # 0
                       ((pygame.mask.Mask((175, 15), True), 0, 635, 900, -1, 25, -1, 0),  # 1
                        (pygame.mask.Mask((15, 300), True), 2, 1351, 905 / 2 - 250 / 2, 0,
                         -1, 0, -1),
                        (pygame.mask.Mask((15, 300), True), 3, -15, 905 / 2 - 250 / 2, 1300,
                         -1, -400, -1)),
                       ((pygame.mask.Mask((15, 300), True), 1, -15, 905 / 2 - 250 / 2, 1300,
                         -1, -400, -1),),  # 2
                       ((pygame.mask.Mask((15, 300), True), 1, 1351, 905 / 2 - 250 / 2, 0,
                         -1, 0, -1),
                        (pygame.mask.Mask((300, 15), True), 4, 400, 900, -1, 20, -1, 0),
                        (pygame.mask.Mask((1300, 15), True), 24, 25, 0, -1, 875, -1, -250)),  # 3
                       ((pygame.mask.Mask((300, 15), True), 3, 400, 0, -1, 870, -1, -265),
                        (pygame.mask.Mask((900, 15), True), 5, 25, 900, -1, 20, -1, 0)),  # 4
                       ((pygame.mask.Mask((900, 15), True), 4, 25, 0, -1, 870, -1, -265),
                        (pygame.mask.Mask((400, 15), True), 4, 25, 900, 1222, 785, -400, -265),
                        (pygame.mask.Mask((550, 15), True), 7, 700, 900, -1, 20, -1, 0),
                        (pygame.mask.Mask((15, 300), True), 6, 1351, 905 / 2 - 250 / 2, 20,
                         -1, 0, -1)),  # 5
                       ((pygame.mask.Mask((15, 300), True), 5, 10, 905 / 2 - 250 / 2, 1300,
                         -1, -400, -1),),  # 6
                       ((pygame.mask.Mask((550, 15), True), 5, 700, 0, -1, 870, -1, -265),
                        (pygame.mask.Mask((900, 15), True), 4, 325, 900, 1222, 785, -400, -265),
                        (pygame.mask.Mask((15, 300), True), 8, 1351, 905 / 2 - 250 / 2, 15,
                         -1, 0, -1),
                        (pygame.mask.Mask((15, 300), True), 4, 0, 905 / 2 - 250 / 2, 1222, 785, -400, -265)
                        ),  # 7
                       ((pygame.mask.Mask((15, 300), True), 7, 0, 905 / 2 - 250 / 2, 1300,
                         -1, -400, -1),
                        (pygame.mask.Mask((600, 15), True), 4, 450, 900, 1222, 785, -400, -265),
                        (pygame.mask.Mask((15, 300), True), 9, 1351, 905 / 2 - 250 / 2, 15,
                         -1, 0, -1)
                        ),  # 8
                       ((pygame.mask.Mask((15, 300), True), 8, 0, 905 / 2 - 250 / 2, 1300,
                         -1, -400, -1),
                        (pygame.mask.Mask((300, 15), True), 4, 775, 900, 1222, 785, -400, -265),
                        (pygame.mask.Mask((15, 300), True), 4, 1351, 905 / 2 - 250 / 2, 1222, 785, -400, -265),
                        (pygame.mask.Mask((300, 15), True), 10, 650, 0, -1, 900, -1, -265)),  # 9
                       ((pygame.mask.Mask((300, 15), True), 9, 650, 900, -1, 15, -1, 0),
                        (pygame.mask.Mask((15, 300), True), 4, 0, 905 / 2 - 250 / 2, 1222, 785, -400, -265),
                        (pygame.mask.Mask((15, 300), True), 4, 1351, 905 / 2 - 250 / 2, 1222, 785, -400, -265),
                        (pygame.mask.Mask((300, 15), True), 11, 650, 0, -1, 900, -1, -265)),  # 10
                       ((pygame.mask.Mask((300, 15), True), 10, 650, 900, -1, 15, -1, 0),
                        (pygame.mask.Mask((15, 300), True), 12, 1351, 905 / 2 - 250 / 2, 15, -1, 0, -1)),  # 11
                       ((pygame.mask.Mask((15, 300), True), 11, 0, 905 / 2 - 250 / 2, 1300, -1, -400, -1),
                        (pygame.mask.Mask((15, 900), True), 15, 1351, 0, 15, -1, 0, -1),
                        (pygame.mask.Mask((1366, 15), True), 13, 0, 900, -1, 15, -1, 0)),  # 12
                       ((pygame.mask.Mask((1366, 15), True), 12, 0, 0, -1, 895, -1, -265),
                        (pygame.mask.Mask((15, 900), True), 14, 1351, 0, 15, -1, 0, -1)),  # 13
                       ((pygame.mask.Mask((1366, 15), True), 15, 0, 0, -1, 895, -1, -265),
                        (pygame.mask.Mask((15, 900), True), 13, 0, 0, 1300, -1, -400, -1)),  # 14
                       ((pygame.mask.Mask((15, 900), True), 12, 0, 0, 1300, -1, -400, -1),
                        (pygame.mask.Mask((1366, 15), True), 14, 0, 900, -1, 15, -1, 0)),  # 15
                       ((pygame.mask.Mask((200, 15), True), 2, 1200, 875, 1225, 300, -400, -250),
                        (pygame.mask.Mask((15, 1000), True), 17, 1350, 75, 25, -1, 0, -1)),  # 16
                       ((pygame.mask.Mask((15, 1000), True), 16, 0, 75, 1300, -1, -400, -1),
                        (pygame.mask.Mask((1300, 15), True), 18, 0, 900, -1, 25, -1, 0),
                        (pygame.mask.Mask((300, 15), True), 22, 1000, 0, -1, 875, -1, -250)),  # 17
                       ((pygame.mask.Mask((1300, 15), True), 17, 0, 0, -1, 875, -1, -250),
                        (pygame.mask.Mask((15, 500), True), 19, 1350, 400, 25, -1, 0, -1)),  # 18
                       ((pygame.mask.Mask((15, 500), True), 18, 0, 400, 1325, -1, -400, -1),
                        (pygame.mask.Mask((1300, 15), True), 20, 0, 0, -1, 875, -1, -250),),  # 19
                       ((pygame.mask.Mask((1300, 15), True), 19, 0, 900, -1, 25, -1, 0),
                        (pygame.mask.Mask((1300, 15), True), 21, 0, 0, -1, 875, -1, -250)),  # 20
                       ((pygame.mask.Mask((1300, 15), True), 20, 0, 900, -1, 25, -1, 0),
                        (pygame.mask.Mask((15, 200), True), 22, 0, 100, 1325, -1, -400, -1)),  # 21
                       ((pygame.mask.Mask((300, 15), True), 17, 1000, 900, -1, 25, -1, 0),
                        (pygame.mask.Mask((400, 15), True), 23, 500, 0, -1, 875, -1, -250),
                        (pygame.mask.Mask((15, 200), True), 21, 1350, 100, 25, -1, 0, -1)),  # 22
                       ((pygame.mask.Mask((400, 15), True), 22, 500, 900, -1, 25, -1, 0),),  # 23
                       ((pygame.mask.Mask((1300, 15), True), 3, 25, 900, -1, 25, -1, 0),
                        (pygame.mask.Mask((1300, 15), True), 25, 0, 0, -1, 875, -1, -250)),  # 24
                       ((pygame.mask.Mask((1300, 15), True), 24, 0, 900, -1, 50, -1, 0),),  # 25
                       ((pygame.mask.Mask((100, 15), True), 15, 643, 655, 687, 406, -400, 0),),
                       ((pygame.mask.Mask((100, 15), True), 0, 643, 655, 442, 323, 0, 0),)
                   ),
                   "interactables": (  # tuple of tuples(map index) of tuples (mask, action, maskX, maskY, params)
                       ((interact_mask, interactChangeMap, 384, 330, (27, 683, 650, -200, -250)),),
                       ((interact_mask, showMessageOnScreen, 1535, 475, ("Grotte de la solitude: →", "Forêt et "
                                                                                                     "Chateau: ←")),
                        (interact_mask, openChest, 855, 125, 0)),
                       ((interact_mask, interactChangeMap, 1565, 500, (16, 1250, 850, -400, -250)),),
                       ((interact_mask, showMessageOnScreen, 1210, 375, ("Chateau: ↑", "Village de la foret: ↓")),
                        (interact_mask, showMessageOnScreen, 267, 375, ("Enclot du ROI", "Interdiction d'y entrer.")),
                        (interact_mask, openChest, 57, 150, 0)),
                       (),
                       (),
                       ((interact_mask, openChest, 1530, 734, 0),),
                       (),
                       ((interact_mask, openChest, 970, 100, 0),),
                       (),
                       (),
                       ((interact_mask, openChest, 857, 218, 0),),
                       (),
                       (),
                       ((interact_mask, interactNpc, 1300, 720, (("Snif. Snif. Mon ami est mort......",
                                                                  "Oh qui êtes vous? C'est mon père qui vous envoie? Très bien allez chercher mon grimoir.",
                                                                  "Il est dans la seule maison ouverte du village, tout les habitants ont fuient."),
                                                                 (), ())),),  # 14
                       ((interact_mask, interactChangeMap, 1030, 375, (26, 683, 650, -200, -250)),),
                       (),
                       (),
                       (),
                       (),
                       ((interact_mask, openChest, 1590, 92, 0),),
                       (),
                       (),
                       ((interact_mask, interactNpc, 827, 670, ((
                                                                "Qui êtes vous? Que se passe-t-il? Le royaumes est en danger?? C'est mon père qui vous envoie?",
                                                                "Tenez prenez ma pioche mais faites y attention, c'est un héritage de famille qui m'est très précieux."),
                                                                ("pioche sacree", 1), ())),),
                       (),
                       ((interact_mask, interactNpc, 827, 275, ((
                                                                "Vite jeune homme, allez chercher le prince dans la caverne et la princesse dans la foret!!",
                                                                "Le barrage du nord est en train de ceder il me faut absolument la pioche sacrée et le grimoir de magie!!",
                                                                "Ne tardez pas, le sort du royaume dépend de vous."),
                                                                (), ("pioche sacree", "grimoir de magie"))),),
                       ((interact_mask, openChest, 1001, 269, 0),),
                       ()
                   ),
                   "chests": [[],
                              [[("bottes", 2), False, (875, 95), False]],
                              [],
                              [[("épée", 1), False, (77, 120), False]],
                              [],
                              [],
                              [[("coeur", 1), False, (1552, 702), True]],
                              [],
                              [[("coeur", 1), False, (992, 62), True]],
                              [],
                              [],
                              [[("torche", 1), False, (879, 180), True]],
                              [],
                              [],
                              [],
                              [],
                              [],
                              [],
                              [],
                              [],
                              [[("coeur", 1), False, (1612, 54), True]],
                              [],
                              [],
                              [],
                              [],
                              [],
                              [[("grimoir de magie", 1), False, (1023, 231), True]],
                              []
                              ]
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


def attack(player, PLAYER_CONSTS):
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


def changeMap(screen, world, player, ennemies, mapIndex,
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
        for ennemy in world["ennemiesForMap"][mapIndex]:
            createEnnemy(ennemies, ennemy[0], ennemy[1], pygame.Rect((ennemy[2][0] + world["worldPos"].x, ennemy[2][1] + world["worldPos"].y), ennemy[3]), ennemy[4], ennemy[5],
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


def manageEnnemies(ennemies, player, world, MASK_SNAKE, dt, DEATH_MUSIC):
    for ennemy in ennemies:
        if player["playerPos"].distance_to(pygame.Vector2(ennemy["rect"].x + ennemy["rect"].width // 2,
                                                          ennemy["rect"].y + ennemy["rect"].height // 2)) <= ennemy[
            "viewDistance"] and not ennemy["playerDetected"]:
            ennemy["playerDetected"] = True
            ennemy["animIndex"] = 0
        if ennemy["playerDetected"]:
            y_value = 100 * clamp(player["playerPos"].y - ennemy["rect"].y - ennemy["rect"].height // 2, -1,
                                  1) * dt
            ennemy["rect"].y += y_value
            if MASK_SNAKE.overlap(world["collisions"][world["worldIndex"]], (
                    world["worldPos"].x - ennemy["rect"].x + 32, world["worldPos"].y - ennemy["rect"].y + 32)):
                ennemy["rect"].y -= y_value
            x_value = 100 * clamp(player["playerPos"].x - ennemy["rect"].x - ennemy["rect"].width // 2, -1,
                                  1) * dt
            ennemy["rect"].x += x_value
            if MASK_SNAKE.overlap(world["collisions"][world["worldIndex"]], (
                    world["worldPos"].x - ennemy["rect"].x + 32, world["worldPos"].y - ennemy["rect"].y + 32)):
                ennemy["rect"].x -= x_value

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


def manageControls(keys, player, world, PLAYER_CONSTS):
    if keys[pygame.K_SPACE] and not player["attacking"] and "épée" in player["objects"]:
        player["attacking"] = True
        player["playerAnimIndex"] = 16 + player["playerDir"]
        attack(player, PLAYER_CONSTS)

    if keys[pygame.K_EQUALS]:
        print(player["playerPos"], world["worldPos"], world["worldIndex"])

    if keys[pygame.K_LSHIFT] and "bottes" in player["objects"]:
        player["speed"] = 400
    else:
        player["speed"] = 200
    if not player["attacking"]:
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            player["playerSpeed"].x = player["speed"]
            player["playerDir"] = 2
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player["playerSpeed"].x = -player["speed"]
            player["playerDir"] = 3
        if not (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_q] or keys[pygame.K_LEFT]):
            player["playerSpeed"].x = 0
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            player["playerSpeed"].y = player["speed"]
            player["playerDir"] = 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player["playerSpeed"].y = -player["speed"]
            player["playerDir"] = 0
        if not (keys[pygame.K_z] or keys[pygame.K_UP]) and not (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            player["playerSpeed"].y = 0

    # Makes the player move at the same speed in all directions
    if player["playerSpeed"].length() != 0:
        player["playerSpeed"].clamp_magnitude(player["speed"])


def manageAnimations(player, PLAYER_CONSTS):
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

        player["playerAnimTimer"] += player["speed"] / 200
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


def manageMovement(screen, player, world, ennemies, dt):
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


def manageDisplay(screen, player, world, ennemies, needFlip, SNAKE_TEXTURES, ICONS, dt, PLAYER_CONSTS, textToShow,
                  fontButton):
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

    if world["worldIndex"] in [i for i in range(16, 23)] and not "torche" in player["objects"]:
        screen.fill("black")
        if world["worldIndex"] == 16:
            background = pygame.transform.scale(pygame.image.load("./resources/map/cave1_hidden.png").convert_alpha(),
                                                (1766, 1177))
            coll = pygame.transform.scale(pygame.image.load("./resources/map/cave1_hidden_coll.png").convert_alpha(),
                                          (1766, 1177))
            screen.blit(background, world["worldPos"])
            screen.blit(coll, world["worldPos"])

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

    for interactable in world["interactables"][world["worldIndex"]]:
        if interactable[0].overlap(PLAYER_CONSTS["playerCollision"][0],
                                   (player["playerPos"].x - 7 - interactable[2] - world["worldPos"][0],
                                    player["playerPos"].y - interactable[3] + 20 - world["worldPos"][1])):
            img = fontButton.render("Appuyer sur E pour interagir", True, "black")
            screen.blit(img, (screen.get_width() - img.get_width() - 20, 20))

    if needFlip:
        pygame.display.flip()


def manageCollisions(screen, player, world, ennemies, PLAYER_CONSTS):
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
            player_x = mapTrigger[4]
            player_y = mapTrigger[5]
            world_x = mapTrigger[6]
            world_y = mapTrigger[7]
            if mapTrigger[4] == -1:
                player_x = player["playerPos"].x
            if mapTrigger[5] == -1:
                player_y = player["playerPos"].y
            if mapTrigger[6] == -1:
                world_x = world["worldPos"].x
            if mapTrigger[7] == -1:
                world_y = world["worldPos"].y
            changeMap(screen, world, player, ennemies, mapTrigger[1], pygame.Vector2(player_x, player_y),
                      pygame.Vector2(world_x, world_y))


def manageMainMenu(screen, world, player, ennemies, isInMainMenu, titleMusicPlaying, timeDelay, isInPauseMenu,
                   fontButton, fontTitle, MAIN_MENU, TITLE_MUSIC, worldInfos_base, textToShow, running, BACKGROUND,
                   back_x, back_y, movement, SOUND_EFFECTS):
    pygame.mouse.set_visible(True)
    screen.fill("black")

    if not titleMusicPlaying:
        pygame.mixer.music.load(TITLE_MUSIC, "mp3")
        pygame.mixer.music.play(-1, 0, 0)
        titleMusicPlaying = True

    if movement:
        back_x += 1.25 * 2
        back_y += 1 * 2
        if back_y >= 0:
            movement = False
    else:
        back_x -= 1.25 * 2
        back_y -= 1 * 2
        if back_y <= -1920 * 4 + 1366:
            movement = True

    screen.blit(BACKGROUND, (back_x, back_y))
    s = pygame.Surface((screen.get_width(), screen.get_height()),
                       pygame.SRCALPHA)  # Creates a surface with transparent pixels
    s.fill((0, 0, 0, 100))
    screen.blit(s, (0, 0))

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
                isInMainMenu = False
                isInPauseMenu = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(world["music"][27])
                pygame.mixer.music.play(-1, 0, 0)
                player = {
                    "playerPos": pygame.Vector2(686, 332),
                    "playerSpeed": pygame.Vector2(0, 0),
                    "life": 12,
                    "maxHealth": 12,
                    "objects": {"coeur": 0},
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
                textToShow.clear()
                world = worldInfos_base.copy()
                player["playerPos"] = pygame.Vector2(686, 332)
                world["worldPos"] = pygame.Vector2(-400, 0)
                player["playerXToMove"] = True
                player["playerYToMove"] = True
                for chest in world["chests"]:
                    for i in range(len(chest)):
                        chest[i][1] = False
                saveGame(world, player)
                showMessageOnScreen(("Message du ROI:",
                                     "Vous êtes appelé a venir rencontrer le ROI, ceci n'est pas une demande mais un devoir.",
                                     "Le chateau se trouve au nord ouest du village. Partez sans attendre."),
                                    textToShow)
                SOUND_EFFECTS["trumpet"].play()

            if button[1] == "Reprendre" and timeDelay >= 15 and exists("save/save.json"):
                isInMainMenu = False
                isInPauseMenu = False
                pygame.mixer.music.stop()
                player_prov = loadGame(screen, world, ennemies)
                for keys in player:
                    player[keys] = player_prov[keys]
                pygame.mixer.music.load(world["music"][world["worldIndex"]])
                pygame.mixer.music.play(-1, 0, 0)
                changeMap(screen, world, player, ennemies, world["worldIndex"], worldPos=pygame.Vector2(-200, -250))
            if button[1] == "Quitter" and timeDelay >= 60:
                running = False

    for text in MAIN_MENU["text"]:
        img = fontTitle.render(text[0], True, "White") if text[2] else fontButton.render(text[0], True, "White")
        screen.blit(img, (text[1][0] - img.get_width() / 2, text[1][1]))

    pygame.display.flip()
    return isInMainMenu, titleMusicPlaying, timeDelay, isInPauseMenu, running, back_x, back_y, movement, player, world


def managePauseMenu(screen, player, world, ennemies, buttons, isInMainMenu, titleMusicPlaying, timeDelay, fontTitle,
                    fontButton, SNAKE_TEXTURES, ICONS, dt, PLAYER_CONSTS, textToShow, isInPauseMenu):
    manageDisplay(screen, player, world, ennemies, False, SNAKE_TEXTURES, ICONS, dt, PLAYER_CONSTS, textToShow,
                  fontButton)

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
                isInMainMenu = True
                titleMusicPlaying = False
                timeDelay = 0
                saveGame(world, player)
                return isInMainMenu, titleMusicPlaying, timeDelay, isInPauseMenu
            if button[1] == "Reprendre":
                isInPauseMenu = False
                return isInMainMenu, titleMusicPlaying, timeDelay, isInPauseMenu

    pygame.display.flip()
    return isInMainMenu, titleMusicPlaying, timeDelay, isInPauseMenu


def saveGame(world, player):
    try:
        mkdir("./save")
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
    except OSError:
        print("Save file already exists")
    except FileNotFoundError:
        print("Save file was not found")


def loadGame(screen, worldInfos, ennemiesList):
    try:
        with open("save/save.json", "r") as file:
            dict_prov = json.loads(file.read())
            worldInfos["worldPos"] = pygame.Vector2(dict_prov["worldPos"][0], dict_prov["worldPos"][1])
            worldInfos["worldIndex"] = dict_prov["worldIndex"]
            worldInfos["chests"] = dict_prov["chests"]
            worldInfos["ennemiesCleared"] = dict_prov["ennemiesCleared"]
            player = dict_prov.copy()
            player["playerPos"] = pygame.Vector2(dict_prov["playerPos"][0], dict_prov["playerPos"][1])
            player["playerSpeed"] = pygame.Vector2(0, 0)
            player["life"] = dict_prov["life"]
            player["ennemiesHit"] = []
            del player["worldIndex"], player["worldPos"], player["chests"], player[
                "ennemiesCleared"]
            file.close()
            changeMap(screen, worldInfos, player, ennemiesList, dict_prov["worldIndex"], player["playerPos"],
                      worldInfos["worldPos"], spawnEnnemies=True, forceMusic=True, forceChange=True)
            print("Loaded save file")
            return player
    except FileNotFoundError:
        print("Save file was not found")


def manageInteractables(screen, world, player, ennemies, PLAYER_CONSTS, game_finished):
    for interactable in world["interactables"][world["worldIndex"]]:
        if interactable[0].overlap(PLAYER_CONSTS["playerCollision"][0],
                                   (player["playerPos"].x - 7 - interactable[2] - world["worldPos"][0],
                                    player["playerPos"].y - interactable[3] + 20 - world["worldPos"][1])):
            if interactable[1] is openChest:
                interactable[1](interactable[4], world, player, textToShow)
            elif interactable[1] is interactChangeMap:
                interactable[1](screen, world, player, ennemies, interactable[4])
            elif interactable[1] is interactNpc:
                game_finished = interactable[1](interactable[4][0], textToShow, interactable[4][1], player,
                                                interactable[4][2])
            else:
                interactable[1](interactable[4], textToShow)

    return game_finished


def manageDeath(screen, player, world, ennemies, timer, isInMainMenu, timeDelay, fontTitle, fontButton):
    if timer > 1:
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
                return isInMainMenu, timeDelay
            if 912 / 2 - 100 <= pygame.mouse.get_pos()[1] <= 912 / 2 - 10:
                isInMainMenu = False
                pygame.mixer.music.stop()
                player_prov = loadGame(screen, world, ennemies)
                for keys in player:
                    player[keys] = player_prov[keys]
                pygame.mixer.music.load(world["music"][world["worldIndex"]])
                pygame.mixer.music.play(-1, 0, 0)
                changeMap(screen, world, player, ennemies, world["worldIndex"], worldPos=pygame.Vector2(-200, -250))
                return isInMainMenu, timeDelay

        pygame.display.update()
        return isInMainMenu, timeDelay


def manageWinScreen(screen, timer, isInMainMenu, timeDelay, fontTitle, fontButton):
    if timer > 1:
        black_fade = pygame.Surface((screen.get_width(), screen.get_height()))
        black_fade.set_alpha(10)
        screen.blit(black_fade, (0, 0))
        pygame.mouse.set_visible(True)

        # buttons
        pygame.draw.rect(screen, "red", pygame.Rect(1366 / 2 - 150, 912 / 2 + 50, 300, 90))
        img = fontTitle.render("Bravo vous avez sauvé le royaume!", True, "White")
        screen.blit(img, (1366 / 2 - img.get_width() / 2, 200))
        img = fontButton.render("Vous pouvez maintenat explorer le monde librement.", True, "White")
        screen.blit(img, (1366 / 2 - img.get_width() / 2, 320))
        img = fontButton.render("Retour au menu", True, "White")
        screen.blit(img, (1366 / 2 - img.get_width() / 2, 912 / 2 + 75))

        if 1366 / 2 - 150 <= pygame.mouse.get_pos()[0] <= 1366 / 2 + 150 and pygame.mouse.get_pressed()[0]:
            if 912 / 2 + 50 <= pygame.mouse.get_pos()[1] <= 912 / 2 + 140:
                isInMainMenu = True
                timeDelay = 0
                return isInMainMenu, timeDelay

        pygame.display.update()
        return isInMainMenu, timeDelay


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and not game_finished:
                game_finished = manageInteractables(screen, worldInfos, playerInfos, ennemiesList, PLAYER_CONSTS,
                                                    game_finished)

    if pygame.key.get_pressed()[pygame.K_ESCAPE] and not isInMainMenu:
        if not isPauseKeyPressed and playerInfos["life"] > 0:
            isInPauseMenu = not isInPauseMenu
        isPauseKeyPressed = True
    else:
        isPauseKeyPressed = False

    if not isInMainMenu and not isInPauseMenu:
        manageControls(pygame.key.get_pressed(), playerInfos, worldInfos, PLAYER_CONSTS)
        manageAnimations(playerInfos, PLAYER_CONSTS)

    pygame.mouse.set_visible(isInPauseMenu or isInMainMenu or game_finished)

    #Stops game time when game in pause
    if isInPauseMenu:
        dt = 0

    if isInMainMenu:
        isInMainMenu, titleMusicPlaying, timeDelay, isInPauseMenu, running, back_x, back_y, movement, playerInfos, worldInfos = manageMainMenu(
            screen, worldInfos,
            playerInfos, ennemiesList,
            isInMainMenu,
            titleMusicPlaying,
            timeDelay, isInPauseMenu,
            fontButton, fontTitle,
            MAIN_MENU, TITLE_MUSIC,
            worldInfos_base, textToShow,
            running, BACKGROUND, back_x, back_y, movement, SOUND_EFFECTS)
    elif isInPauseMenu:
        isInMainMenu, titleMusicPlaying, timeDelay, isInPauseMenu = managePauseMenu(screen, playerInfos, worldInfos,
                                                                                    ennemiesList, PAUSE_MENU_BUTTONS,
                                                                                    isInMainMenu, titleMusicPlaying,
                                                                                    timeDelay, fontTitle, fontButton,
                                                                                    SNAKE_TEXTURES, ICONS, dt,
                                                                                    PLAYER_CONSTS, textToShow,
                                                                                    isInPauseMenu)
    elif playerInfos["life"] <= 0:
        isInMainMenu, timeDelay = manageDeath(screen, playerInfos, worldInfos, ennemiesList, timer, isInMainMenu,
                                              timeDelay, fontTitle, fontButton)
    elif game_finished:
        isInMainMenu, timeDelay = manageWinScreen(screen, timer, isInMainMenu, timeDelay, fontTitle, fontButton)
    else:
        manageCollisions(screen, playerInfos, worldInfos, ennemiesList, PLAYER_CONSTS)
        manageMovement(screen, playerInfos, worldInfos, ennemiesList, dt)
        manageEnnemies(ennemiesList, playerInfos, worldInfos, MASK_SNAKE, dt, DEATH_MUSIC)
        manageDisplay(screen, playerInfos, worldInfos, ennemiesList, True, SNAKE_TEXTURES, ICONS, dt, PLAYER_CONSTS,
                      textToShow, fontButton)

    #Make text disappear after a certain time
    for text in textToShow.copy():
        if text[1] < time.time():
            textToShow.remove(text)

    #Add hearts when in inventory
    for i in range(playerInfos["objects"]["coeur"]):
        playerInfos["objects"]["coeur"] -= 1
        playerInfos["life"] += 4
        playerInfos["maxHealth"] += 4

    dt = clock.tick(60) / 1000
    timeDelay += 1
    timer += dt

pygame.quit()
