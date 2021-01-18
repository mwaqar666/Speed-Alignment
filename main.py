from tensorflow.keras.models import load_model

import constants.constants as values
from data.data import *
from helpers.utils import *

model = load_model(os.path.abspath("C:/Users/mwaqa/OneDrive/Desktop/racing-game-ai/models/categorical_crossentropy.h5"))

pygame.init()
pygame.display.set_caption('Racing Car AI')

SCREEN = initialize_screen()

# Clock is set to keep track of frames
clock = pygame.time.Clock()

cars = []
data = []

my_car = My_car(values.MY_CAR_X, values.MY_CAR_Y)

# Set ai_mode false if you want to play in autopilot mode to collect data
ai = True

# Set True if you want to collect state at every frame for data analytics
collect_data = not ai

# Decide on amount of rows after which data should be saved
rows = values.DATA_ROWS

# counter = 298
while 1:
    # limit runtime speed to 30 frames/second
    clock.tick(values.FRAME_RATE)
    pygame.event.pump()
    for event in pygame.event.get():

        # Press Escape key to quit game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit

        # Quit the game if the X symbol is clicked
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Build up a black screen as a game background
    SCREEN.fill(values.BLACK)

    # Draw two road separator lines
    draw_vertical_lines(SCREEN)

    # Remove cars that are out of map boundaries
    deactivate_cars(cars)

    # filter out not active cars
    cars = list(filter(lambda x: (x.active != False), cars))

    # Increase a frame counter
    # counter += 1

    # Perform this action every frame
    # if counter % values.ACTION_PERFORM_RATE == 0:
    if ai:
        # Test your ai model's performance
        ai_model(model, cars, my_car)
    else:
        # Collect data by playing autopilot mode
        if cars:
            autopilot(data, cars, my_car)

    # Perform this action every 2 frames
    if not cars:
        add_new_car(cars)

    # Draw cars
    draw_cars(SCREEN, cars)
    # Draw player car
    draw_my_car(SCREEN, my_car)

    if collect_data:
        save_data(data)

    # update display
    pygame.display.flip()
