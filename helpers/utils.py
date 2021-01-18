import numpy as np
import pygame

import constants.constants as vals
from helpers.core import *


def initialize_screen():
    # Size is the game screen size in pixels
    SIZE = width, height = vals.WIDTH, vals.HEIGHT
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.flip()

    return SCREEN


def add_new_car(cars):
    x = vals.MARGIN + vals.CAR_WIDTH / 2 + vals.LINE_WIDTH
    y = vals.HEIGHT - vals.MARGIN - 2 * vals.CAR_HEIGHT

    car = Enemy_car(x, y)

    cars.append(car)


def move_cars(cars):
    # move_cars calls move method of each car in cars state if the car is active
    for car in cars:
        if car.active:
            car.move()


def deactivate_cars(cars):
    # deactivate_cars checks if a car is outside of map boundaries and deactivates it
    for car in cars:
        # If the enemy_car has reached the bottom of any road line, deactivate it
        if car.y > vals.HEIGHT - vals.MARGIN - vals.CAR_HEIGHT / 2:
            car.active = False


def draw_cars(screen, cars):
    # draw_cars will draw each car from cars array on screen using its icon
    for car in cars:
        screen.blit(
            vals.ENEMY_CAR_ICON, (car.x - car.width / 2, car.y - car.height / 2))


def draw_my_car(screen, my_car):
    # draw_my_car will draw my car on screen using its icon
    screen.blit(vals.MY_CAR_ICON, (my_car.x - my_car.width /
                                   2, my_car.y - my_car.height / 2))


def draw_vertical_lines(screen):
    # draw left vertical line to separate roads
    pygame.draw.rect(screen, vals.GREY,
                     (vals.LINE_WIDTH - vals.ROAD_LINE_WIDTH / 2, 0, vals.ROAD_LINE_WIDTH, vals.HEIGHT))
    # draw right vertical line to separate roads
    pygame.draw.rect(screen, vals.GREY, (vals.LINE_WIDTH *
                                         2 - vals.ROAD_LINE_WIDTH / 2, 0, vals.ROAD_LINE_WIDTH, vals.HEIGHT))


def map_cars_to_lines(cars, my_car):
    # lines will represent 3 arrays corresponsding to 3 vertical road lines
    lines = [[0, 0, 0, 0, 0, 0, 0, 0], [
        0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    for car in cars:
        # 2 is a label for enemy cars
        coord_x = car.x // vals.LINE_WIDTH
        coord_y = car.y // vals.LINE_WIDTH
        try:
            lines[int(coord_x)][int(coord_y)] = 2
        except IndexError:
            pygame.quit()

    # 1 is a label for my car
    my_coord_x = my_car.x // vals.LINE_WIDTH
    my_coord_y = my_car.y // vals.LINE_WIDTH
    lines[int(my_coord_x)][int(my_coord_y)] = 1
    return lines


def find_my_position(my_car):
    # returns index of a line my car is at (0 or 1 or 2)
    # return int(my_car.x // vals.LINE_WIDTH) MYCODE
    return int(my_car.y // vals.CAR_HEIGHT)


def find_enemy_position(cars):
    return int(cars[0].y // vals.CAR_HEIGHT)  # MYCODE


def is_my_car_behind(my_car, enemy_car):  # MYCODE
    if enemy_car - my_car < 0:
        return True
    return False


def are_cars_side_by_side(my_car, enemy_car):  # MYCODE
    if enemy_car - my_car == 0:
        return True
    return False


def find_closest_car(lines, index):
    # Find and return the distance to the first car on a line given by index
    count = -1
    # Loops through each line and finds the number 2 which represents the enemy car
    for i in reversed(lines[index]):
        # When found an enemy car returns a distance from my car to enemy car
        if i == 2:
            return count
        count += 1
    # If there are no cars on the line, returns max possible number ie length of the line
    return count


def find_all_distances(lines):
    # Returns an array of 3 values representing distances to the nearest cars on each road line
    all_distances = []

    distance_0 = find_closest_car(lines, 0)
    all_distances.append(distance_0)

    distance_1 = find_closest_car(lines, 1)
    all_distances.append(distance_1)

    distance_2 = find_closest_car(lines, 2)
    all_distances.append(distance_2)

    return all_distances


def choose_action(cars, my_car):
    # Decide to either go left right or stay at still and Return a tuple of decision, my_position, all_distances
    if not cars:
        return 'left', 14, 12, True, False
    # Find X index of my position
    my_position = find_my_position(my_car)
    # MYCODE
    enemy_position = find_enemy_position(cars)
    is_behind = is_my_car_behind(my_position, enemy_position)
    is_side_by_side = are_cars_side_by_side(my_position, enemy_position)
    if is_behind and not is_side_by_side:
        action = "left"
    elif is_side_by_side:
        action = "stay"
    else:
        action = "right"

    return action, my_position, enemy_position, is_behind, is_side_by_side


def perform_action(action, my_car):
    my_car.move(action)


def check_if_lost(cars, my_car):
    # For all cars on map check if x and y coordinates are equal to my_car's
    for car in cars:
        if car.x == my_car.x and car.y == my_car.y:
            print("Ops! You crashed!")
            return True

    return False


def save_data_row(data, action, is_behind, is_side_by_side):
    # Saves each row into a data array for future data analytics
    action_indices = {
        'left': 0, 'stay': 1, 'right': 2
    }

    data.append([

        #  Is Behind  |   Is Side By Side   |        Action
        int(is_behind), int(is_side_by_side), action_indices[action]
    ])


def predict(input_array, model):
    # Puts input state into neural network and returns an action predicted by model
    # Convert array into model input format
    input_state = np.array([input_array])

    # Pass input through model to get prediction
    action = model.predict_classes(input_state)

    actions = {
        0: 'left', 1: 'stay', 2: 'right'
    }

    return actions[action[0]]


def build_input_state(cars, my_car):
    # Turns all input variables into a single array
    action, my_position, enemy_position, is_behind, is_side_by_side = choose_action(cars, my_car)
    return [int(is_behind), int(is_side_by_side)]


def autopilot(data, cars, my_car):
    # Autopilot will play the game infinitely to collect data
    action, my_position, enemy_position, is_behind, is_side_by_side = choose_action(cars, my_car)
    perform_action(action, my_car)
    save_data_row(data, action, is_behind, is_side_by_side)
    move_cars(cars)


def ai_model(model, cars, my_car):
    # AI will put state into model, predict the action and perform it
    # Build input array for ai model
    input_state = build_input_state(cars, my_car)
    # Pass input through model to find action
    action = predict(input_state, model)
    # Perform the action suggested by ai model
    perform_action(action, my_car)
    move_cars(cars)
