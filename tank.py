# import bhramand as brm
from bhramand import Node, Line, Polygon, Object, Plane, Camera, World, GameWorld, game
import random
import pygame
import time
import math


class CodeEngine(Object):
    def __init__(self, object_params):
        self.parent_object = None
        super().__init__(object_params)
        self.time_constraint = {"movement": [time.time(), 0.05], "c_1": [time.time(), 1], "color_change": [time.time(), 0.2]}

    def respond_to_events(self, key_pressed_dict, mouse_object):
        # let object respond to event
        if self.check_time_constraint("movement"):
            if key_pressed_dict[pygame.K_x] and key_pressed_dict[pygame.K_UP]:
                # rotate_about_cartesian_axis(axis_type="X")
                self.rotate_about_axis(axis_to_rotate_around="X")
            elif key_pressed_dict[pygame.K_y] and key_pressed_dict[pygame.K_UP]:
                self.rotate_about_axis(axis_to_rotate_around="Y")
            elif key_pressed_dict[pygame.K_z] and key_pressed_dict[pygame.K_UP]:
                self.rotate_about_axis(axis_to_rotate_around="Z")

            elif key_pressed_dict[pygame.K_PAGEUP]:
                self.move_about_your_axis(axis="y_axis", direction="forward")
            elif key_pressed_dict[pygame.K_PAGEDOWN]:
                self.move_about_your_axis(axis="y_axis", direction="reverse")
            # elif key_pressed_dict[pygame.K_UP]:
            #     self.move_about_your_axis(axis="longitudinal", direction="forward")
            # elif key_pressed_dict[pygame.K_DOWN]:
            #     self.move_about_your_axis(axis="longitudinal", direction="reverse")
            elif key_pressed_dict[pygame.K_LEFT]:
                self.move_about_your_axis(axis="x_axis", direction="forward")
            elif key_pressed_dict[pygame.K_RIGHT]:
                self.move_about_your_axis(axis="x_axis", direction="reverse")
        if self.check_time_constraint("color_change"):
            letter_keys = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g,
                       pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n,
                       pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u,
                       pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z]
            for letter in letter_keys:
                if key_pressed_dict[letter]:
                    for surf in self.surfaces:
                        if surf.color == "red":
                            surf.color = "blue"
                        else:
                            surf.color = "red"

    @staticmethod
    def generate_code_engine():
        core_cube_params = World.object_generator(type_of_object="cube", center_pos=[60, 60, 50], object_name="corecube",
                                                  mode="return_params")
        core_cube = CodeEngine(core_cube_params)
        core_cube.type = "CodeEngine"
        input_cube_params = World.object_generator(type_of_object="cube", center_pos=[60, 120, 90], object_name="inputcube",
                                                   mode="return_params")
        input_cube = CodeEngine(input_cube_params)
        input_cube.type = "CodeEngine Input"
        input_cube.parent_object = [core_cube]

        output_cube_params = World.object_generator(type_of_object="cube", center_pos=[60, 120, 10], object_name="outputcube",
                                             mode="return_params")
        output_cube = CodeEngine(output_cube_params)
        output_cube.type = "CodeEngine Output"
        output_cube.parent_object = [core_cube]

        core_cube.child_objects = [input_cube, output_cube]

        plane_1 = TankCam([core_cube, input_cube, output_cube], cam_orientation="XY")
        w_object_list = [core_cube, input_cube, output_cube]

        return [w_object_list, plane_1]


class TankCam(Camera):
    def __init__(self, objects_to_project, cam_orientation):
        super().__init__(objects_to_project, cam_orientation)
        self.type = "Tank Camera"
        self.god_mode = True

        self.game_object = None

    def get_rotation_axis_based_on_mouse_position(self, mouse_position):
        x_dim, y_dim = self.plane_dimensions[0], self.plane_dimensions[1]
        trim_param = 15
        x_margin, y_margin = x_dim // trim_param, y_dim // trim_param

        x_min, x_max = x_margin, x_dim - x_margin
        y_min, y_max = y_margin, y_dim - y_margin

        if not (x_min < mouse_position[0] < x_max):
            if x_min > mouse_position[0]:
                return "Z"
            else:
                return "-Z"
        if self.god_mode:
            if not (y_min < mouse_position[1] < y_max):
                if y_min > mouse_position[1]:
                    return "X"
                else:
                    return "-X"
        return None

    def respond_to_events(self, key_pressed_dict, mouse_object):
        # let object respond to event
        if self.check_time_constraint("movement"):
            if self.god_mode:
                if key_pressed_dict[pygame.K_PAGEUP]:
                    self.move_about_your_axis(axis="longitudinal", direction="forward")
                elif key_pressed_dict[pygame.K_PAGEDOWN]:
                    self.move_about_your_axis(axis="longitudinal", direction="reverse")

            rotate_axis = self.get_rotation_axis_based_on_mouse_position(mouse_object.get_pos())
            # if key_pressed_dict[pygame.K_x] and key_pressed_dict[pygame.K_UP]:
            #     # rotate_about_cartesian_axis(axis_type="X")
            #     self.rotate_about_axis(axis_to_rotate_around="X")
            if rotate_axis is not None:
                self.rotate_about_axis(axis_to_rotate_around=rotate_axis, angle_to_rotate_by=5)

            elif key_pressed_dict[pygame.K_UP]:
                self.move_about_your_axis(axis="y_axis", direction="reverse")
            elif key_pressed_dict[pygame.K_DOWN]:
                self.move_about_your_axis(axis="y_axis", direction="forward")
            elif key_pressed_dict[pygame.K_LEFT]:
                self.move_about_your_axis(axis="x_axis", direction="forward")
            elif key_pressed_dict[pygame.K_RIGHT]:
                self.move_about_your_axis(axis="x_axis", direction="reverse")
            # else:
            #     for node_o in self.nodes:
            #         node_o.rotate_yourself(self.rotation_rate, axis_override=True, axis=self.axis_line)

        # let each node respond to event [Ex: rotate yourself]
        for node in self.nodes:
            node.update(key_pressed_dict)

    def draw_yourself(self, cam_surface, active_object):
        super().draw_yourself(cam_surface, active_object)


class Tank(Object):
    def __init__(self, object_params):
        super().__init__(object_params)

    def move_to_position(self, position_to_move_to):
        # move yourself
        self.center_node.relative_position = position_to_move_to


class TankWorld(World):
    def __init__(self):
        self.object_list = None
        self.grid_object = None
        self.cam = None
        self.tank = None
        # self.crawler_object = None

        self.initialize_yourself()
        super().__init__(self.cam, self.object_list)

        # bp_coordinate = self.get_a_random_coordinate_on_base_plane()
        # plane_nodes = self.get_plane_nodes_based_on_base_plane_coordinate(bp_co_ordinate=bp_coordinate)
        # self.projected_point = self.get_projected_position_on_plane_with_plane_nodes(plane_nodes=plane_nodes, bp_co_ordinate=bp_coordinate)

    def initialize_yourself(self):

        # cylinder_1_params = generate_cylinder(center_pos=[60, 60, 60], object_name="cylinder1")
        # cylinder_1 = Object(cylinder_1_params)
        # cube_1.child_objects = [cylinder_1]

        w_object_list = []
        grid = self.create_grid()
        w_object_list.append(grid)
        # city_object_list = self.create_city_block()
        # w_object_list += city_object_list

        # plane_1 = TankCam([cube_1, cube_2], cam_orientation="XZ")
        plane_2 = TankCam(w_object_list, cam_orientation="XZ")
        plane_2.move_about_your_axis("longitudinal", direction="forward")
        plane_2.game_object = self

        self.cam = plane_2
        self.grid_object = grid

        random_position = self.get_a_random_coordinate_on_base_plane()
        random_position = [random_position[0], random_position[1], random_position[2]]
        parent_node = self.grid_object.nodes[0]
        parent_node_position = parent_node.get_your_position()
        relative_x, relative_y, relative_z = random_position[0] - parent_node_position[0]\
            , random_position[1] - parent_node_position[1]\
            , random_position[2] - parent_node_position[2]
        cube_1 = World.object_generator(type_of_object="cube", center_pos=[relative_x, relative_y, relative_z], object_name="cube1", parent_node=parent_node)
        self.tank = cube_1
        # cube_2 = World.object_generator(type_of_object="cube", center_pos=[120, 120, 10], object_name="cube2")
        # cube_1.child_objects = [cube_2]

        w_object_list.append(cube_1)
        self.object_list = w_object_list

    def get_a_random_coordinate_on_base_plane(self):
        # get the lowest grid node
        z_min = None
        for node_obj in self.grid_object.nodes:
            position = node_obj.get_your_position()
            if z_min is None:
                z_min = position[2]
            else:
                if position[2] < z_min:
                    z_min = position[2]

        start_pos, end_pos = self.grid_object.nodes[0].get_your_position(), self.grid_object.nodes[-1].get_your_position()
        x_min, y_min = start_pos[0], start_pos[1]
        x_max, y_max = end_pos[0], end_pos[1]

        x_random, y_random = random.randint(x_min, x_max), random.randint(y_min, y_max)
        return x_random, y_random, z_min

    def get_plane_nodes_based_on_base_plane_coordinate(self, bp_co_ordinate):
        node_list = self.grid_object.nodes
        grid_dimension = round(len(node_list)**0.5)

        node_nested_list = []
        for i in range(grid_dimension):
            row_start_index = i * grid_dimension
            row = node_list[row_start_index:row_start_index + grid_dimension]
            node_nested_list.append(row)
            assert len(row) == grid_dimension
        assert len(node_nested_list) == grid_dimension

        for i in range(grid_dimension - 1):
            for ii in range(grid_dimension - 1):
                node_a_obj, node_b_obj, node_c_obj, node_d_obj = node_nested_list[i][ii], node_nested_list[i][ii + 1],\
                    node_nested_list[i + 1][ii], node_nested_list[i + 1][ii + 1]
                node_a, node_b, node_c, node_d = node_a_obj.get_your_position(), node_b_obj.get_your_position(), \
                    node_c_obj.get_your_position(), node_d_obj.get_your_position()

                if node_a[1] <= bp_co_ordinate[1] <= node_b[1]:
                    if node_b[0] < bp_co_ordinate[0] < node_c[0]:
                        return [node_a_obj, node_c_obj, node_d_obj, node_b_obj]
        return None

    @staticmethod
    def get_projected_position_on_plane_with_plane_nodes(plane_nodes, bp_co_ordinate):

        def reduce_position_to_2d(position):
            return [position[0], position[1], bp_co_ordinate[2]]

        # input plane_nodes in form [A, B, C, D]
        a, b, c, d = plane_nodes[0], plane_nodes[1], plane_nodes[2], plane_nodes[3]
        a, b, c, d = a.get_your_position(), b.get_your_position(), c.get_your_position(), d.get_your_position()
        bp_a, bp_b, bp_c, bp_d = reduce_position_to_2d(a), reduce_position_to_2d(b), reduce_position_to_2d(c), \
            reduce_position_to_2d(d)
        # print("Node coordinates: ", a, b, c, d)
        # print("Node base plane coordinates: ",bp_a, bp_b, bp_c, bp_d)

        def get_distance_between_points(point_a, point_b):
            x_diff, y_diff, z_diff = point_b[0] - point_a[0], point_b[1] - point_a[1], point_b[2] - point_a[2]
            dist = math.sqrt((x_diff ** 2) + (y_diff ** 2) + (z_diff ** 2))
            dist = round(dist, 2)
            return dist

        def project_point_on_line():
            pass

        # project on 2 vertical lines ['Y' co-ordinate remains constant, 'Z' remains 0]
        bp_projected_a = [bp_a[0], bp_co_ordinate[1], bp_co_ordinate[2]]
        bp_projected_b = [bp_b[0], bp_co_ordinate[1], bp_co_ordinate[2]]

        # get fraction of vertical length of projection
        base_vertical_dist = get_distance_between_points(bp_a, bp_d)
        projected_a_dist = get_distance_between_points(bp_a, bp_projected_a)
        projected_b_dist = get_distance_between_points(bp_b, bp_projected_b)
        assert projected_a_dist == projected_b_dist
        move_fraction = projected_a_dist/base_vertical_dist

        # move along top edge by move_fraction
        d_x, d_y, d_z = d[0] - a[0], d[1] - a[1], d[2] - a[2]
        up_projected_a = [a[0] + (d_x * move_fraction), a[1] + (d_y * move_fraction), a[2] + (d_z * move_fraction)]
        d_x, d_y, d_z = c[0] - b[0], c[1] - b[1], c[2] - b[2]
        up_projected_b = [b[0] + (d_x * move_fraction), b[1] + (d_y * move_fraction), b[2] + (d_z * move_fraction)]

        # move by move_fraction_2 along top projection connection edge
        all_length = bp_b[0] - bp_a[0]
        fractional_length = get_distance_between_points(bp_projected_a, bp_co_ordinate)
        move_fraction_2 = round(fractional_length / all_length, 2)
        d_x, d_y, d_z = up_projected_b[0] - up_projected_a[0], up_projected_b[1] - up_projected_a[1], \
            up_projected_b[2] - up_projected_a[2]
        center_projected_point = [up_projected_a[0] + (d_x * move_fraction), up_projected_a[1] + (d_y * move_fraction), up_projected_a[2] + (d_z * move_fraction)]

        return center_projected_point

    @staticmethod
    def create_city_block(grid_dimension=3, center=(50, 50, 50)):
        object_name = "terrain"
        center_node = Node(center, "white", 2, object_name=object_name)

        city_obj_list = []
        # create buildings
        building_width = 60
        building_spacing = 20
        for i in range(grid_dimension):
            for ii in range(grid_dimension):
                c_x, c_y, c_z = center[0], center[1], center[2]
                increment = (building_width * 1.5) + building_spacing
                building_name = "building" + str(i) + str(ii)

                x, y, z = (random.randrange(60, 80, 5), random.randrange(60, 80, 5), random.randrange(60, 180, 5))
                position = [(i * increment), (ii * increment), 0]
                position = [position[0] + center[0], position[1] + center[1], position[2], + center[2]]

                building_obj = World.object_generator(type_of_object="cube", center_pos=position, object_name=building_name,dimensional_vals=[x,y,z])
                city_obj_list.append(building_obj)

        # create reference plane
        scale_factor = 1
        grid_width = (building_width + building_spacing)*(grid_dimension**2) * scale_factor
        node_a = Node([(grid_width / 2), (grid_width/2), 0],
                      "red", 2, parent=center_node, object_name=object_name)
        node_b = Node([(-grid_width / 2), (grid_width / 2), 0],
                      "red", 2, parent=center_node, object_name=object_name)
        node_c = Node([-(grid_width / 2), -(grid_width / 2), 0],
                      "red", 2, parent=center_node, object_name=object_name)
        node_d = Node([(grid_width / 2), -(grid_width / 2), 0],
                      "red", 2, parent=center_node, object_name=object_name)

        node_list = [node_a, node_b, node_c, node_d]

        # create reference plane lines
        line_list = []
        line_nodes_map = [node_a, node_b, node_c, node_d, node_a]
        for index_v in range(len(line_nodes_map) - 1):
            line_obj = Line(line_nodes_map[index_v], line_nodes_map[index_v + 1])
            line_list.append(line_obj)

        # create polygon surface
        surf_obj = Polygon([node_a, node_b, node_c, node_d])
        # surf_list = [surf_obj]

        plane_param = ["terrain_base_reference", center_node, node_list, line_list, [], []]
        reference_plane_obj = Object(plane_param)
        reference_plane_obj.child_objects = city_obj_list

        city_obj_list = [reference_plane_obj] + city_obj_list

        return city_obj_list

    @staticmethod
    def create_grid(grid_dimension=20, center=(50, 50, 50)):
        object_name = "grid"
        center_node = Node(center, "white", 2, object_name=object_name)

        # create nodes
        node_list = []
        nested_node_list = []
        for i in range(grid_dimension):
            row_list = []
            for ii in range(grid_dimension):
                c_x, c_y, c_z = center[0], center[1], center[2]
                increment = 40

                x, y, z = 0, 0, 0
                chance_to_introduce_grid_offset = random.randint(1, 100)
                if chance_to_introduce_grid_offset > 95:  # 20% chance
                    x, y, z = (random.randrange(60, 80, 5), random.randrange(60, 80, 5), random.randrange(150, 200, 5))
                position = [(i * increment), (ii * increment), z]
                node_obj = Node(rel_position=position, color="red", object_name="grid", parent=center_node, radius=0.5)
                row_list.append(node_obj)
                node_list.append(node_obj)
            nested_node_list.append(row_list)

        # create grid boundary nodes [do not add these nodes to node list]
        Z_SIZE = 400
        a, b, c, d = nested_node_list[0][0], nested_node_list[0][len(nested_node_list[0])-1]\
            , nested_node_list[len(nested_node_list[0])-1][0]\
            , nested_node_list[len(nested_node_list[0])-1][len(nested_node_list[0])-1]
        a1, b1, c1, d1 = [a.relative_position[0], a.relative_position[1], Z_SIZE]\
            , [b.relative_position[0], b.relative_position[1], Z_SIZE]\
            , [c.relative_position[0], c.relative_position[1], Z_SIZE]\
            , [d.relative_position[0], d.relative_position[1], Z_SIZE]
        a1, b1, c1, d1 = Node(rel_position=a1, color="red", object_name="grid", parent=center_node, radius=0.5)\
            , Node(rel_position=b1, color="red", object_name="grid", parent=center_node, radius=0.5)\
            , Node(rel_position=c1, color="red", object_name="grid", parent=center_node, radius=0.5)\
            , Node(rel_position=d1, color="red", object_name="grid", parent=center_node, radius=0.5)


        # create lines
        line_list = []
        for row_index in range(len(nested_node_list)):
            row = nested_node_list[row_index]
            for index in range(len(row) - 1):
                # horizontal lines of the grid
                node_a, node_b = row[index], row[index + 1]
                line_obj = Line(node_a, node_b)
                line_list.append(line_obj)

                # vertical lines of the grid
                node_a, node_b = nested_node_list[index][row_index], nested_node_list[index + 1][row_index]
                line_obj = Line(node_a, node_b)
                line_list.append(line_obj)
        # create boundary lines
        line_map = [[a1, a], [b1, b], [c1, c], [d1, d], [a1, b1], [b1, d1], [d1, c1], [c1, a1]]
        for l_val in line_map:
            line_obj = Line(l_val[0], l_val[1])
            line_list.append(line_obj)


        # create surfaces
        surface_list = []
        # for row_index in range(len(nested_node_list) - 1):
        #     row = nested_node_list[row_index]
        #     for index in range(len(row) - 1):
        #         node_a, node_b, node_c, node_d = nested_node_list[row_index][index], nested_node_list[row_index][index + 1], \
        #             nested_node_list[row_index + 1][index + 1], nested_node_list[row_index + 1][index]
        #         surf_obj = Polygon([node_a, node_b, node_c, node_d])
        #         surface_list.append(surf_obj)

        object_params = [object_name, center_node, node_list, line_list, surface_list, []]

        grid_object = Object(object_params)
        return grid_object

    def update(self, key_pressed_dict, cam_surface, mouse_obj, pygame_event):
        self.respond_to_events(key_pressed_dict, mouse_obj, pygame_event)

        if self.current_active_object_index is None and len(self.object_list) > 0:
            self.current_active_object_index = 0

        if len(self.object_list) > 0:
            # active_object = self.object_list[self.current_active_object_index]
            active_object = self.tank
            active_object = self.cam
            active_object.update(key_pressed_dict, mouse_obj)

            tank_position = active_object.center_node.relative_position
            random_bp_position = self.get_a_random_coordinate_on_base_plane()
            tank_bp_position = [tank_position[0], tank_position[1], random_bp_position[2]]
            plane_nodes = self.get_plane_nodes_based_on_base_plane_coordinate(tank_bp_position)
            # tank_projected_position = self.get_projected_position_on_plane_with_plane_nodes(plane_nodes, tank_bp_position)
            tank_projected_position = tank_bp_position

            active_object.center_node.relative_position = tank_projected_position

            for obj in self.object_list:
                if obj != active_object:
                    obj.update(None, None)

            self.cam.draw_yourself(cam_surface=cam_surface, active_object=active_object)


class TankGameWorld(GameWorld):
    def __init__(self, world_obj=None, load_from_disk=False):
        super().__init__(world_obj=world_obj, load_from_disk=load_from_disk)


class Human:
    pass


def game_world_generator():
    world_modes = ["test environment", "Code Engine test"]
    world_type = world_modes[0]
    if world_type == "test environment":
        test_run = True
        if test_run:
            tank_world = TankWorld()
            game_world = TankGameWorld(world_obj=tank_world)


    elif world_type == "Code Engine test":
        param_list = CodeEngine.generate_code_engine()
        game_world = GameWorld(object_list=param_list[0], camera=param_list[1])
    return game_world


game(new_game=True, game_world=game_world_generator())
# game(new_game=False)