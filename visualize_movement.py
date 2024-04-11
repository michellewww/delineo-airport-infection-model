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
facility_color = (0, 255, 0)
text_color = (0, 0, 0)
font_size = 15
font = pygame.font.Font(None, font_size)

map_min_x, map_min_y = -5000, -6500
map_max_x, map_max_y = 5000, -900

scale_x = screen_width / (map_max_x - map_min_x)
scale_y = screen_height / (map_max_y - map_min_y)

def get_json_file_names(directory):
    return sorted([f for f in os.listdir(directory) if f.endswith('.json')], key=lambda x: int(x.split('.')[0]))

def parse_json_file(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)
    
def draw_facility(name, minX, minY, maxX, maxY, color):
    # Scale and translate the facility coordinates
    topLeftX = (minX - map_min_x) * scale_x
    topLeftY = (minY - map_min_y) * scale_y
    bottomRightX = (maxX - map_min_x) * scale_x
    bottomRightY = (maxY - map_min_y) * scale_y
    width = bottomRightX - topLeftX
    height = bottomRightY - topLeftY
    pygame.draw.rect(screen, color, pygame.Rect(topLeftX, topLeftY, width, height), 2)
    text_surface = font.render(name, True, text_color)
    screen.blit(text_surface, (topLeftX + 5, topLeftY + height + 5))


def draw_passenger(x, y, color):
    screen_x = int((x - map_min_x) * scale_x)
    screen_y = int((y - map_min_y) * scale_y)
    pygame.draw.circle(screen, color, (screen_x, screen_y), 5)

def generate_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

facility_data = parse_json_file('UEAirportFacilityList.json')
json_files = get_json_file_names('data')
color_map = {}

running = True
file_index = 0

while running and file_index < len(json_files):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)

    for facility in facility_data["floor_1"]:
        draw_facility(facility["ID"],facility["minX"], facility["minY"], facility["maxX"], facility["maxY"], facility_color)

    current_data = parse_json_file(os.path.join('data', json_files[file_index]))
    
    for passenger in current_data["Passenger"]:
        if passenger != {} and passenger["Z"] < 200:
            if passenger["ID"] not in color_map:
                color_map[passenger["ID"]] = generate_random_color()
            
            draw_passenger(passenger["X"], passenger["Y"], color_map[passenger["ID"]])

    pygame.display.flip()
    pygame.time.wait(500)
    file_index += 1

pygame.quit()
sys.exit()