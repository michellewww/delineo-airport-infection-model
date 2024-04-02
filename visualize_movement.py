import pygame
import sys
import json
import os
import random

# (-5000,  -6500), (5000, -6500), (5000,-1300), (-5000,-1300)
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Passenger Movement Visualization")

background_color = (255, 255, 255)

map_min_x, map_min_y = -5000, -6500
map_max_x, map_max_y = 5000, -900

scale_x = screen_width / (map_max_x - map_min_x)
scale_y = screen_height / (map_max_y - map_min_y)

def get_json_file_names(directory):
    return sorted([f for f in os.listdir(directory) if f.endswith('.json')], key=lambda x: int(x.split('.')[0]))

def parse_json_file(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def draw_passenger(x, y, color):
    screen_x = int((x - map_min_x) * scale_x)
    screen_y = int((y - map_min_y) * scale_y)
    pygame.draw.circle(screen, color, (screen_x, screen_y), 5)

def generate_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

json_files = get_json_file_names('data')
color_map = {}

running = True
file_index = 0

while running and file_index < len(json_files):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)

    current_data = parse_json_file(os.path.join('data', json_files[file_index]))
    
    for passenger in current_data["Passenger"]:
        if passenger != {}:
            if passenger["ID"] not in color_map:
                color_map[passenger["ID"]] = generate_random_color()
            
            draw_passenger(passenger["X"], passenger["Y"], color_map[passenger["ID"]])

    pygame.display.flip()
    pygame.time.wait(500)
    file_index += 1

pygame.quit()
sys.exit()