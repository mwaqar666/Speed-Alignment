import pygame
import os

# Rows to add to csv file
DATA_ROWS = 20000

# Frame rate
FRAME_RATE = 20

# My car action perform rate
ACTION_PERFORM_RATE = 1

# Road line width is for two vertical lines
ROAD_LINE_WIDTH = 10

# Margin of the useful map area
MARGIN = 20

# Width of the game screen
WIDTH = 240

# Height of the game screen
HEIGHT = 600

# Width of any car on the map
CAR_WIDTH = 20

# Height of any car on the map
CAR_HEIGHT = 40

# Distance between centers of vertical lines
LINE_WIDTH = 80

# Initial coordinates of my car
MY_CAR_X = MARGIN + CAR_WIDTH / 2
MY_CAR_Y = HEIGHT - MARGIN - CAR_HEIGHT / 2

# Colors in a format accepted by pygame
BLACK = (0, 0, 0)
GREY = (150, 150, 150)

MY_CAR_ICON = pygame.image.load(os.path.abspath("C:/Users/mwaqa/OneDrive/Desktop/racing-game-ai/img/my_car.png"))
ENEMY_CAR_ICON = pygame.image.load(os.path.abspath("C:/Users/mwaqa/OneDrive/Desktop/racing-game-ai/img/enemy_car.png"))
