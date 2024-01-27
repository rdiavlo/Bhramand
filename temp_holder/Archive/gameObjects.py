"""
Classes:
    1. GameHandler
    2. Player
"""
import pygame
import time
import math


class GameHandler:
    def __init__(self, entities=None):
        self.pressed_keys = {}
        self.entities = entities

        self.keys_constraint = {"player": {"k_up": [0.01, -1], "k_down": [0.01, -1], "k_left": [0.01, -1], "k_right": [0.01, -1],
                                           "k_space": [0.01, -1], "k_s": [0.01, -1]}}

        pass

    def check_constraint(self, obj, param):
        constraint_data = self.keys_constraint[obj.type][param]
        time_to_wait, start_time = constraint_data[0], constraint_data[1]
        if start_time == -1:
            self.keys_constraint[obj.type][param][1] = time.time()
            return True
        elif time.time() - start_time > time_to_wait:
            # update time constraint
            self.keys_constraint[obj.type][param][1] = time.time()
            return True
        else:
            return False

    def entity_event_handler(self, entity):
        if entity.type == "player":
            velocity_increment = 0.05
            wheel_angle_increment = 0.05
            if self.pressed_keys[pygame.K_UP]:
                if self.check_constraint(entity, "k_up"):
                    new_vel = entity.velocity + velocity_increment
                    entity.change_player_parameter("velocity", new_vel)
            elif self.pressed_keys[pygame.K_DOWN]:
                if self.check_constraint(entity, "k_down"):
                    new_vel = entity.velocity - velocity_increment
                    entity.change_player_parameter("velocity", new_vel)
            elif self.pressed_keys[pygame.K_LEFT]:
                if self.check_constraint(entity, "k_left"):
                    new_angle = entity.current_wheel_angle + wheel_angle_increment
                    entity.change_player_parameter("wheel_angle", new_angle)
            elif self.pressed_keys[pygame.K_RIGHT]:
                if self.check_constraint(entity, "k_right"):
                    new_angle = entity.current_wheel_angle - wheel_angle_increment
                    entity.change_player_parameter("wheel_angle", new_angle)

            elif self.pressed_keys[pygame.K_SPACE]:
                if self.check_constraint(entity, "k_space"):
                    entity.change_player_parameter("velocity", 0)
                    entity.change_player_parameter("current_wheel_angle", 0)
                    entity.change_player_parameter("plane_angle", entity.default_position)
            elif self.pressed_keys[pygame.K_s]:
                if self.check_constraint(entity, "k_s"):
                    entity.change_player_parameter("velocity", 0)
                    entity.change_player_parameter("current_wheel_angle", 0)
                    entity.change_player_parameter("plane_angle", 0)
                    entity.change_player_parameter("plane_angle", entity.default_position)
            pass

    def update_entities(self):
        for entity in self.entities:
            # use handler to update entities from top level
            self.entity_event_handler(entity)
            # tell entities to update themselves on unit level
            entity.update()

    def blit_entities_to_surface(self, surf):
        for entity in self.entities:
            if entity.type == "player":
                pygame.draw.circle(surf, "red", entity.position, 4)

                plane_angle = round(entity.plane_angle, 1)
                wheel_angle = round(entity.current_wheel_angle, 1)
                font = pygame.font.Font('freesansbold.ttf', 32)
                text_p_ang = font.render(str(plane_angle), True, "white")
                text_w_ang = font.render(str(wheel_angle), True, "white")

                surf_dim_x, surf_dim_y = 40, 40
                textrect_p, textrect_w = text_p_ang.get_rect(), text_w_ang.get_rect()
                textrect_p.center, textrect_w.center = (surf_dim_x // 2, surf_dim_y // 2), \
                    (surf_dim_x // 2, surf_dim_y // 2)
                surf_wheel_angle = pygame.surface.Surface((surf_dim_x, surf_dim_y))
                surf_plane_angle = pygame.surface.Surface((surf_dim_x, surf_dim_y))
                surf.blit(text_p_ang, [100, 100])
                surf.blit(text_w_ang, [200, 100])

        pass

    def update(self, pressed_keys_dict, surface):
        self.pressed_keys = pressed_keys_dict
        self.update_entities()
        self.blit_entities_to_surface(surface)


class Plane:

    def __init__(self, default_position=(0, 0)):
        self.type = "player"
        self.position = default_position

        self.max_wheel_angle = 0.5
        self.current_wheel_angle = 0
        self.plane_angle = 90
        self.velocity = 0

        self.default_position = default_position

    def return_player_parameter(self, parameter):
        if parameter == "position":
            return self.position
        elif parameter == "wheel_angle":
            return self.current_wheel_angle
        elif parameter == "plane_angle":
            return self.plane_angle
        return None

    def change_player_parameter(self, parameter, value):
        if parameter == "velocity":
            self.velocity = value
            print(value)
        elif parameter == "position":
            self.position = value
        elif parameter == "wheel_angle":
            if -self.max_wheel_angle < value < self.max_wheel_angle:
                self.current_wheel_angle = value
        elif parameter == "plane_angle":
            self.plane_angle = value

    def move_player(self):
        self.plane_angle = self.plane_angle + self.current_wheel_angle
        if self.plane_angle >= 360:
            self.plane_angle = self.plane_angle % 360

        def get_velocity_components():
            angle, magnitude = self.plane_angle, self.velocity
            x_vel_component, y_vel_component = magnitude * math.cos(math.radians(angle)), \
                magnitude * math.sin(math.radians(angle))
            x_vel_component, y_vel_component = round(x_vel_component, 2), round(y_vel_component, 2)
            return [x_vel_component, y_vel_component]

        x_velocity, y_velocity = get_velocity_components()
        self.position = [self.position[0] + x_velocity, self.position[1] + y_velocity]

    def update(self):
        self.move_player()


""" """



pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = (720, 440)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


plane_1 = Plane([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
game_handler = GameHandler([plane_1])

clock = pygame.time.Clock()
game_run_state = True
while game_run_state:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run_state = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_run_state = False
            break

    pressed_keys_dict = pygame.key.get_pressed()
    game_handler.update(pressed_keys_dict, screen)

    pygame.display.flip()
    screen.fill("black")

    clock.tick(30)

pygame.quit()
