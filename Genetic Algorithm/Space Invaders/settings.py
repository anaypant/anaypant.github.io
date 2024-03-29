#Game Settings
GAME_WIDTH = 600
GAME_HEIGHT = 600
FPS = 30
ALIEN_SPAWN_DELAY = FPS/1.5

#Player Settings
SHIP_W = 40
SHIP_H = 60
SHIP_START_X = (GAME_WIDTH / 2) - (SHIP_W / 2)
SHIP_START_Y = GAME_HEIGHT - (SHIP_H * 1.5)
PLAYER_SPEED = 14
FIRE_DELAY = FPS / 6 # 2 shots check per second

#Laser Settings
LASER_W = 8
LASER_H = 20
LASER_SPEED = 14

#Enemy Settings
ALIEN_W = 30
ALIEN_H = 20
ALIEN_SPEED = 3
NUM_SPAWN_POINTS = GAME_WIDTH/ALIEN_W - 1

#GEN ALG Settings
NUM_POP = 20
NUM_ELITES = int(0.2 * NUM_POP)
NUM_MUTATIONS = int(NUM_POP * 0.1)
MUTATE_RATE = 0.4
NUM_GENERATIONS = 10000
STATIC_INC = 0.01
SCORE_INC = 10

#Pygame Alg Settings
PYGAME_ENABLED = True
PYGAME_LOOK_AFTER_GEN = 1000

#AI Settings
NUM_INPUTS = 4
NUM_OUTPUTS = 5
LAYERS = [NUM_INPUTS, 12, 12, 10, 10, 8, 8, 6, NUM_OUTPUTS]
MOVE_THRESH = 0.55
FIRE_THRESH = 0.55
