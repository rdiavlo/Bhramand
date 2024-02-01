
"""
V1.32 - [1st Jan 2024]
    -- Object hierarchy and rotation about arbitrary point
    -- Game state persistence: Pickling
V1.321 - [1st Jan][Partial]
    -- Primitive: Cylinder added [Partial]
V1.322 - [1st Jan][Partial]
    -- Cam surface added and cam plane view
    -- Needs mod on 1st Vs. 3rd quadrant identification [Partial]
V1.33 - [3rd Jan][Partial]
    -- Needs mod on 1st Vs. 3rd quadrant identification [Partial]
    -- Perspective based scaling added
V1.331 - [3rd Jan][Partial]
    -- Added city block [Cube enhanced parameterization - cuboid]
V1.34 - [5th Jan][Partial]
    Fixed:
        -- 1st Vs. 3rd quadrant identification & scaling
    Issues:
        -- Occlusion needs to be corrected [Partial]
V1.35 - [13th Jan]
    Feature (+)::
        -- Added objected selection through cursor
    Issues (!):
        -- Occlusion needs to be corrected [Partial]
V1.36 - [15th Jan]
    Fixed:
        -- Axis rotation merged from test arena[Anomaly: Exists and pops up in rare cases. WHY??]
    Feature (+):
        -- Added tank game script
    Issues (!):
        -- Occlusion needs to be corrected [Partial]
        -- Projection onto cam plane needs to be corrected

TODO:
    Add World Grid
    Add Tank
    Make tank traverse world grid
"""

import math
import time
import random

import pygame
import pickle

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = (1000, 600)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Node:
    node_list = []

    def __init__(self, rel_position, color="red", radius=2, parent=None, object_name=None):

        generated_name = Node.generate_unique_name_by_object_type(object_name)
        Node.pre_checks(generated_name)

        self.name = generated_name
        self.parent = parent
        self.relative_position = rel_position
        self.color = color
        self.radius = radius
        self.axis = None
        self.parent_object = None

        self.time_constraint = {"movement": [time.time(), 0.2], "c_1": [time.time(), 1]}
        Node.node_list.append(self)

    @classmethod
    def generate_unique_name_by_object_type(cls, object_name):
        # get all similar object names
        object_name_already_present = []
        for node in Node.node_list:
            if object_name in node.name:
                object_name_already_present.append(node.name)

        # if no similar objects create first name. otherwise add 1 to the highest name
        if len(object_name_already_present) == 0:
            return object_name + "_1"
        else:
            object_name_already_present = [int(o_name[o_name.find('_') + 1:]) for o_name in object_name_already_present]
            return object_name + "_" + str(max(object_name_already_present) + 1)

    @staticmethod
    def pre_checks(name):
        for node in Node.node_list:
            if node.name == name:
                raise ValueError

    def get_your_position(self):
        if self.parent is None:
            ref_position = [0, 0, 0]
        else:
            ref_position = self.parent.get_your_position()
        absolute_position = [ref_position[0] + self.relative_position[0], ref_position[1] + self.relative_position[1],
                             ref_position[2] + self.relative_position[2]]
        return absolute_position

    def rotate_yourself(self, angle_to_rotate_by_main, axis_override=False, axis=None):
        def get_angle_from_position(pos):
            angle_p = math.atan(pos[1] / (pos[0] + 0.00000000000000001))
            angle_p = math.degrees(angle_p)
            angle_p = round(angle_p, 4)
            if angle_p == 0 and pos[0] <= 0 and pos[1] <= 0:
                angle_p = 180
            if angle_p == -90 and pos[0] == 0 and pos[1] <= 0:
                angle_p = 270
            elif pos[0] < 0 < pos[1]:
                angle_p += 180
            elif pos[0] < 0 and pos[1] < 0:
                angle_p += 180
            elif pos[0] > 0 > pos[1]:
                angle_p += 360
            # print("the angle_p is: ", angle_p)
            return angle_p

        def increase_angle_and_return_new_position(pos, old_ang, ang):
            new_ang = old_ang + ang
            dist = math.sqrt(pos[0] ** 2 + pos[1] ** 2)
            x, y = dist * math.cos(math.radians(new_ang)), dist * math.sin(math.radians(new_ang))
            x, y = round(x, 6), round(y, 6)
            return [x, y], dist

        # get vector positions
        if axis_override:
            node_a_position, node_b_position, node_p_position = axis.nodes[0].get_your_position(), \
                axis.nodes[1].get_your_position(), self.get_your_position()
        else:
            node_a_position, node_b_position, node_p_position = self.axis.nodes[0].get_your_position(), \
                self.axis.nodes[1].get_your_position(), self.get_your_position()
        # vector_ab = [node_a_position, node_b_position]
        # vector_ap = [node_a_position, node_p_position]

        # STEP-1: translate vectors to origin
        x_offset, y_offset, z_offset = node_a_position[0], node_a_position[1], node_a_position[2]
        trans_b_pos = [node_b_position[0] - x_offset, node_b_position[1] - y_offset, node_b_position[2] - z_offset]
        trans_p_pos = [node_p_position[0] - x_offset, node_p_position[1] - y_offset, node_p_position[2] - z_offset]

        # STEP-2: align vector along 'XZ' plane [rotate about 'Z' axis: 'z' coordinate remains constant]
        x_angle_ab = get_angle_from_position(trans_b_pos)
        x_angle_ap = get_angle_from_position(trans_p_pos)

        angle_to_rotate_by = 360 - x_angle_ab
        start_position = [trans_b_pos[0], trans_b_pos[1]]
        rotated_pos, mag = increase_angle_and_return_new_position(start_position, x_angle_ab, angle_to_rotate_by)
        trans_b_pos = [rotated_pos[0], rotated_pos[1], trans_b_pos[2]]

        start_position = [trans_p_pos[0], trans_p_pos[1]]
        rotated_pos, mag = increase_angle_and_return_new_position(start_position, x_angle_ap, angle_to_rotate_by)
        trans_p_pos = [rotated_pos[0], rotated_pos[1], trans_p_pos[2]]

        # STEP-3: align vector_ab with 'X' axis [rotate about 'Y' axis: 'Y' coordinate remains constant]
        # get angle made by vector_ab w.r.t 'Z' axis
        z_angle_ab = get_angle_from_position([trans_b_pos[0], trans_b_pos[2]])
        z_angle_ap = get_angle_from_position([trans_p_pos[0], trans_p_pos[2]])
        angle_to_rotate_by_x = 360 - z_angle_ab
        start_position = [trans_b_pos[0], trans_b_pos[2]]
        rotated_pos, mag = increase_angle_and_return_new_position(start_position, z_angle_ab, angle_to_rotate_by_x)
        trans_b_pos = [rotated_pos[0], trans_b_pos[1], rotated_pos[1]]

        start_position = [trans_p_pos[0], trans_p_pos[2]]
        rotated_pos, mag = increase_angle_and_return_new_position(start_position, z_angle_ap, angle_to_rotate_by_x)
        trans_p_pos = [rotated_pos[0], trans_p_pos[1], rotated_pos[1]]

        # STEP-4: Rotate vector_ap about 'X' axis
        x_angle_ap = get_angle_from_position([trans_p_pos[1], trans_p_pos[2]])
        start_position = [trans_p_pos[1], trans_p_pos[2]]
        rotated_pos, mag = increase_angle_and_return_new_position(start_position, x_angle_ap, angle_to_rotate_by_main)
        trans_p_pos = [trans_p_pos[0], rotated_pos[0], rotated_pos[1]]

        # STEP-5: reverse align vector_ab about 'X' axis [rotate about 'Y' axis: 'Y' coordinate remains constant]
        z_angle_ap = get_angle_from_position([trans_p_pos[0], trans_p_pos[2]])
        angle_to_rotate_by_x = z_angle_ab
        start_position = [trans_p_pos[0], trans_p_pos[2]]
        rotated_pos, mag = increase_angle_and_return_new_position(start_position, z_angle_ap, angle_to_rotate_by_x)
        trans_p_pos = [rotated_pos[0], trans_p_pos[1], rotated_pos[1]]

        # STEP-6: reverse align vector along 'XZ' plane [rotate about 'Z' axis: 'z' coordinate remains constant]
        x_angle_ap_final = get_angle_from_position(trans_p_pos)
        angle_to_rotate_by = x_angle_ab
        start_position = [trans_p_pos[0], trans_p_pos[1]]
        rotated_pos, mag = increase_angle_and_return_new_position(start_position, x_angle_ap_final, angle_to_rotate_by)
        trans_p_pos = [rotated_pos[0], rotated_pos[1], trans_p_pos[2]]

        # STEP-7: reverse translate vectors to origin
        trans_p_pos = [trans_p_pos[0] + x_offset, trans_p_pos[1] + y_offset, trans_p_pos[2] + z_offset]
        trans_p_pos = [round(trans_p_pos[0], 2), round(trans_p_pos[1], 2), round(trans_p_pos[2], 2)]

        if self.parent is not None:
            parent_position = self.parent.get_your_position()
        else:
            parent_position = [0, 0, 0]
        rel_position = [trans_p_pos[0] - parent_position[0], trans_p_pos[1] - parent_position[1],
                        trans_p_pos[2] - parent_position[2]]

        self.relative_position = rel_position

    def check_time_constraint(self, param):
        if time.time() - self.time_constraint[param][0] >= self.time_constraint[param][1]:
            self.time_constraint[param][0] = time.time()
            return True
        return False

    def respond_to_events(self, key_pressed_dict):
        pass

    def update(self, key_pressed_dict):
        self.respond_to_events(key_pressed_dict)

    @classmethod
    def return_node_by_name(cls, name):
        for n in cls.node_list:
            if n.name == name:
                return n
        return None


class Line:
    line_list = []

    def __init__(self, node_a, node_b, color="purple"):
        self.color = color
        self.nodes = [node_a, node_b]
        Line.line_list.append(self)


class Polygon:
    surfaces_list = []

    def __init__(self, node_list, color=(255, 165, 0)):
        self.color = color
        self.nodes = node_list
        Polygon.surfaces_list.append(self)


class Object:
    def __init__(self, object_params):
        self.type = "generic object"
        self.name = None
        self.center_node = None
        self.nodes = None
        self.lines = None
        self.surfaces = None
        self.child_objects = None
        self.axis_line_list = None
        self.initialize(object_params)

        self.show_polygon = True
        self.time_constraint = {"movement": [time.time(), 0.05]}
        self.rotation_rate = 5

    def initialize(self, object_params):
        name, center_node, n_list, l_list, s_list, child_objects = object_params
        self.name = name
        self.center_node = center_node
        self.nodes, self.lines, self.surfaces = n_list, l_list, s_list
        self.child_objects = child_objects

        # create axis system for each object
        def create_random_node_with_parent_as_center_node(position):
            random_node = Node(position, "blue", 2, parent=center_node, object_name="axisPoint")
            return random_node

        node_a, node_b, node_c = create_random_node_with_parent_as_center_node([0, 0, 100]), \
            create_random_node_with_parent_as_center_node([0, 100, 0]), \
            create_random_node_with_parent_as_center_node([100, 0, 0])
        axis_line_forward = Line(center_node, node_a, color="green")
        axis_line_x = Line(center_node, node_c, color="pink")
        axis_line_y = Line(center_node, node_b, color="yellow")
        self.lines += [axis_line_forward, axis_line_x, axis_line_y]
        self.axis_line_list = [axis_line_forward, axis_line_x, axis_line_y]

        for node in self.nodes:
            node.parent_object = self

    def move_about_your_axis(self, axis, direction, axis_override=False):

        def scale_displacement_vector(vector, scaling_factor):
            x, y, z = vector[0] * scaling_factor, vector[1] * scaling_factor, vector[2] * scaling_factor
            x, y, z = round(x, 2), round(y, 2), round(z, 2)
            return [x, y, z]

        if axis_override:
            axis = axis
        else:
            if axis == "longitudinal":
                axis = self.axis_line_list[0]
            elif axis == "x_axis":
                axis = self.axis_line_list[1]
            elif axis == "y_axis":
                axis = self.axis_line_list[2]

        a_vector, b_vector = axis.nodes[0].get_your_position(), axis.nodes[1].get_your_position()
        x, y, z = a_vector[0] - b_vector[0], a_vector[1] - b_vector[1], a_vector[2] - b_vector[2]
        if direction == "forward":
            displacement_vector = [x, y, z]
        else:
            displacement_vector = [-x, -y, -z]
        scaled_displacement_vector = scale_displacement_vector(displacement_vector, 0.1)

        # first move yourself
        center_position = self.center_node.relative_position
        self.center_node.relative_position = [center_position[0] + scaled_displacement_vector[0],
                                              center_position[1] + scaled_displacement_vector[1],
                                              center_position[2] + scaled_displacement_vector[2]]

        # then move all your child objects
        for c_obj in self.child_objects:
            c_obj.move_about_your_axis(axis, direction, axis_override=True)

    def rotate_about_cartesian_axis(self, axis_type, angle_to_rotate_by):
        longitudinal_axis = self.axis_line_list[0]
        base_point = longitudinal_axis.nodes[0]
        point_to_rotate = longitudinal_axis.nodes[1]
        base_point_position = base_point.relative_position
        top_point = None

        if axis_type in ["X", "Y", "Z"]:
            # first rotate yourself
            if axis_type == "X":
                top_point = Node(
                    [base_point_position[0] + 10, base_point_position[1] + 0, base_point_position[2] + 0],
                    "blue", 2, object_name="randomPoint")
            elif axis_type == "Y":
                top_point = Node(
                    [base_point_position[0] + 0, base_point_position[1] + 10, base_point_position[2] + 0],
                    "blue", 2, object_name="randomPoint")
            elif axis_type == "Z":
                top_point = Node(
                    [base_point_position[0] + 0, base_point_position[1] + 0, base_point_position[2] + 10],
                    "blue", 2, object_name="randomPoint")

            temp_axis_line = Line(base_point, top_point, color="yellow")
            point_to_rotate.rotate_yourself(angle_to_rotate_by, axis_override=True, axis=temp_axis_line)

            # rotate nodes of other 2 axis [X & Y] of camera plane
            x_axis, y_axis = self.axis_line_list[1], self.axis_line_list[2]
            point_to_rotate = x_axis.nodes[1]
            point_to_rotate.rotate_yourself(angle_to_rotate_by, axis_override=True, axis=temp_axis_line)
            point_to_rotate = y_axis.nodes[1]
            point_to_rotate.rotate_yourself(angle_to_rotate_by, axis_override=True, axis=temp_axis_line)

            for node_o in self.nodes:
                node_o.rotate_yourself(angle_to_rotate_by, axis_override=True, axis=temp_axis_line)

            # then rotate all your child objects
            for c_obj in self.child_objects:
                c_obj.rotate_about_cartesian_axis(axis_type, angle_to_rotate_by)

    def rotate_about_axis(self, axis_to_rotate_around, angle_to_rotate_by="default", highest_parent_object=True):
        if angle_to_rotate_by == "default":
            angle_to_rotate_by = self.rotation_rate
        else:
            angle_to_rotate_by = angle_to_rotate_by

        # first rotate yourself
        if axis_to_rotate_around == "X":
            rotation_axis = self.axis_line_list[1]
        elif axis_to_rotate_around == "Y":
            rotation_axis = self.axis_line_list[2]
        elif axis_to_rotate_around == "Z":
            rotation_axis = self.axis_line_list[0]
        elif axis_to_rotate_around == "-X":
            rotation_axis = self.axis_line_list[1]
            rotation_axis = Line(rotation_axis.nodes[1], rotation_axis.nodes[0])
        elif axis_to_rotate_around == "-Y":
            rotation_axis = self.axis_line_list[2]
            rotation_axis = Line(rotation_axis.nodes[1], rotation_axis.nodes[0])
        elif axis_to_rotate_around == "-Z":
            rotation_axis = self.axis_line_list[0]
            rotation_axis = Line(rotation_axis.nodes[1], rotation_axis.nodes[0])
        else:
            rotation_axis = axis_to_rotate_around
        global_axis = rotation_axis

        # rotate center node
        self.center_node.rotate_yourself(angle_to_rotate_by, axis_override=True, axis=rotation_axis)
        center_node_position = self.center_node.get_your_position()

        if not highest_parent_object:
            # move rotation axis to local center
            node_a, node_b = rotation_axis.nodes[0], rotation_axis.nodes[1]
            node_a_position, node_b_position = node_a.get_your_position(), node_b.get_your_position()
            x, y, z = node_b_position[0] - node_a_position[0], node_b_position[1] - node_a_position[1],\
                node_b_position[2] - node_a_position[2]
            base_node = Node(center_node_position, color="red", object_name="tempnode")
            top_node_position = [center_node_position[0] + x, center_node_position[1] + y, center_node_position[2] + z]
            top_node = Node(top_node_position, color="red", object_name="tempnode")
            rotation_axis = Line(base_node, top_node)

        # rotate axis nodes about rotation axis
        axis_nodes_list = [self.axis_line_list[0].nodes[1], self.axis_line_list[1].nodes[1], self.axis_line_list[2].nodes[1]]
        for axis_node in axis_nodes_list:
            axis_node.rotate_yourself(angle_to_rotate_by, axis_override=True, axis=rotation_axis)

        # rotate nodes about rotation axis
        for node_o in self.nodes:
            node_o.rotate_yourself(angle_to_rotate_by, axis_override=True, axis=rotation_axis)

        # then rotate all your child objects
        for c_obj in self.child_objects:
            c_obj.rotate_about_axis(axis_to_rotate_around=global_axis, angle_to_rotate_by=angle_to_rotate_by, highest_parent_object=False)

    def check_time_constraint(self, param):
        if time.time() - self.time_constraint[param][0] >= self.time_constraint[param][1]:
            self.time_constraint[param][0] = time.time()
            return True
        return False

    def respond_to_events(self, key_pressed_dict, mouse_object):
        # let object respond to event
        if self.check_time_constraint("movement"):
            if key_pressed_dict[pygame.K_x] and key_pressed_dict[pygame.K_UP]:
                # rotate_about_cartesian_axis(axis_type="X")
                pass
            #     self.rotate_about_axis(axis_to_rotate_around="X")
            # elif key_pressed_dict[pygame.K_y] and key_pressed_dict[pygame.K_UP]:
            #     self.rotate_about_axis(axis_to_rotate_around="Y")
            elif key_pressed_dict[pygame.K_z] and key_pressed_dict[pygame.K_UP]:
                self.rotate_about_axis(axis_to_rotate_around="Z")
            # elif key_pressed_dict[pygame.K_x] and key_pressed_dict[pygame.K_DOWN]:
            #     self.rotate_about_axis(axis_to_rotate_around="-X")
            # elif key_pressed_dict[pygame.K_y] and key_pressed_dict[pygame.K_DOWN]:
            #     self.rotate_about_axis(axis_to_rotate_around="-Y")
            elif key_pressed_dict[pygame.K_z] and key_pressed_dict[pygame.K_DOWN]:
                self.rotate_about_axis(axis_to_rotate_around="-Z")

            # elif key_pressed_dict[pygame.K_PAGEUP]:
            #     self.move_about_your_axis(axis="longitudinal", direction="reverse")
            # elif key_pressed_dict[pygame.K_PAGEDOWN]:
            #     self.move_about_your_axis(axis="longitudinal", direction="forward")
            elif key_pressed_dict[pygame.K_UP]:
                self.move_about_your_axis(axis="y_axis", direction="reverse")
            elif key_pressed_dict[pygame.K_DOWN]:
                self.move_about_your_axis(axis="y_axis", direction="forward")
            elif key_pressed_dict[pygame.K_LEFT]:
                self.move_about_your_axis(axis="x_axis", direction="forward")
            elif key_pressed_dict[pygame.K_RIGHT]:
                self.move_about_your_axis(axis="x_axis", direction="reverse")

        # let each node respond to event [Ex: rotate yourself]
        for node in self.nodes:
            node.update(key_pressed_dict)

    def update(self, key_pressed_dict, mouse_obj):
        if key_pressed_dict is not None:
            self.respond_to_events(key_pressed_dict, mouse_obj)


class Plane(Object):
    count = 1

    def __init__(self, cam_orientation, plane_dimensions=(SCREEN_WIDTH, SCREEN_HEIGHT), object_name=None,
                 center_position=None):
        self.type = "plane"
        self.plane_dimensions = plane_dimensions
        self.initialize_yourself(cam_orientation, object_name, center_position)

        self.normal, self.axis_line_x, self.axis_line_y = (self.axis_line_list[2].nodes[1], self.axis_line_list[1],
                                                           self.axis_line_list[0])

    def initialize_yourself(self, cam_orientation, object_name, center_position):
        if object_name is None:
            object_name = self.type + str(Plane.count)

        object_params = self.generate_plane(object_name=object_name, orientation=cam_orientation,
                                            center_position=center_position)
        super().__init__(object_params)

    def generate_plane(self, object_name, orientation, center_position=None):
        if center_position is None:
            center = [0, 0, 0]
        else:
            center = center_position
        length = 60
        point_list = {}
        if orientation == "XZ":
            point_list = {"a": [length // 2, 0, length // 2],
                          "b": [length // 2, 0, -length // 2],
                          "c": [-length // 2, 0, length // 2],
                          "d": [-length // 2, 0, -length // 2]}
        elif orientation == "XY":
            point_list = {"a": [length // 2, length // 2, 0],
                          "b": [length // 2, -length // 2, 0],
                          "c": [-length // 2, length // 2, 0],
                          "d": [-length // 2, -length // 2, 0]}
        elif orientation == "YZ":
            point_list = {"a": [0, length // 2, length // 2],
                          "b": [0, length // 2, -length // 2],
                          "c": [0, -length // 2, length // 2],
                          "d": [0, -length // 2, -length // 2]}

        center_node = Node(center, "white", 2, object_name=object_name)
        assumed_name_to_actual_name_mapping_dict = {"O": center_node.name}

        node_list = []
        for point_name in point_list:
            n_obj = Node(point_list[point_name], "red", 2, parent=center_node, object_name="axisPoint")
            actual_name = n_obj.name
            assumed_name_to_actual_name_mapping_dict[point_name] = actual_name
            node_list.append(n_obj)

        line_mapping = {"a": ["b", "c"], "d": ["b", "c"]}

        line_list = []
        for node_name in line_mapping:
            node = Node.return_node_by_name(assumed_name_to_actual_name_mapping_dict[node_name])
            for neighbor_node_name in line_mapping[node_name]:
                n_obj = Node.return_node_by_name(assumed_name_to_actual_name_mapping_dict[neighbor_node_name])
                line_obj = Line(node, n_obj)
                line_list.append(line_obj)

        # add parent objects to nodes
        for node_obj in node_list:
            node_obj.parent_object = self

        return [object_name, center_node, node_list, line_list, [], []]

    def find_distance_to_plane_from_a_point(self, node_to_project):
        normal_node = self.normal
        center_node = self.center_node

        normal_position = normal_node.relative_position
        magnitude_of_normal_vector = math.sqrt((normal_position[0]) ** 2 + (normal_position[1]) ** 2
                                               + (normal_position[2]) ** 2)
        unit_normal_vector = [normal_position[0] / magnitude_of_normal_vector, normal_position[1] /
                              magnitude_of_normal_vector, normal_position[2] / magnitude_of_normal_vector]

        origin_position = center_node.get_your_position()
        point_position = node_to_project.get_your_position()

        # Make a vector from your orig point to the point of interest:
        v_x, v_y, v_z = point_position[0] - origin_position[0], point_position[1] - origin_position[1],\
            point_position[2] - origin_position[2]

        # Take the dot product of that vector with the unit normal vector n
        dist = (v_x * unit_normal_vector[0]) + (v_y * unit_normal_vector[1]) + (v_z * unit_normal_vector[2])

        return dist

    def project_point_on_plane(self, node_to_project):
        normal_node = self.normal
        center_node = self.center_node

        normal_position = normal_node.relative_position
        magnitude_of_normal_vector = math.sqrt((normal_position[0]) ** 2 + (normal_position[1]) ** 2
                                               + (normal_position[2]) ** 2)
        unit_normal_vector = [normal_position[0] / magnitude_of_normal_vector, normal_position[1] /
                              magnitude_of_normal_vector, normal_position[2] / magnitude_of_normal_vector]

        origin_position = center_node.get_your_position()
        point_position = node_to_project.get_your_position()

        # Make a vector from your orig point to the point of interest:
        v_x, v_y, v_z = point_position[0] - origin_position[0], point_position[1] - origin_position[1], \
                        point_position[2] - origin_position[2]

        # Take the dot product of that vector with the unit normal vector n
        dist = (v_x * unit_normal_vector[0]) + (v_y * unit_normal_vector[1]) + (v_z * unit_normal_vector[2])

        # Multiply the unit normal vector by the distance, and subtract that vector from your point.
        projected_dist = [dist * unit_normal_vector[0], dist * unit_normal_vector[1], dist * unit_normal_vector[2]]
        projected_point = [point_position[0] - projected_dist[0], point_position[1] - projected_dist[1],
                           point_position[2] - projected_dist[2]]

        return projected_point


class Camera(Plane):
    count = 0

    def __init__(self, objects_to_project, cam_orientation):
        self.type = "camera"
        self.invert_y_axis = True

        super().__init__(cam_orientation=cam_orientation, object_name=self.type + str(Camera.count))
        Camera.count += 1

        self.objects_to_project = objects_to_project
        self.history_projected_nodal_positions = []

    def get_cam_plane_coordinate_from_point(self, point_position, perpendicular_distance_from_node_to_plane):

        # Make a vector from 'c' point to the 'b' point: Reference vector
        d_point, a_point = self.axis_line_x.nodes[0].get_your_position(), self.axis_line_y.nodes[1].get_your_position()
        r_x, r_y, r_z = a_point[0] - d_point[0], a_point[1] - d_point[1], a_point[2] - d_point[2]

        # Make a vector from 'c' point to the point of interest:
        v_x, v_y, v_z = point_position[0] - d_point[0], point_position[1] - d_point[1], point_position[2] - d_point[2]

        # get angle between interest vector and reference vector
        dot_product_check = (r_x * v_x) + (r_y * v_y) + (r_z * v_z)

        # 1. Project the point
        # Make a vector from 'c' point to the 'd' point: Reference vector
        c_point, d_point = self.axis_line_x.nodes[0].get_your_position(), self.axis_line_x.nodes[1].get_your_position()

        r_x, r_y, r_z = d_point[0] - c_point[0], d_point[1] - c_point[1], d_point[2] - c_point[2]

        # Make a vector from 'c' point to the point of interest:
        v_x, v_y, v_z = point_position[0] - c_point[0], point_position[1] - c_point[1], point_position[2] - c_point[2]

        # get angle between interest vector and reference vector
        dot_product = (r_x*v_x) + (r_y*v_y) + (r_z*v_z)
        magnitude_reference_vector = math.sqrt((r_x ** 2) + (r_y ** 2) + (r_z ** 2))
        magnitude_interest_vector = math.sqrt((v_x ** 2) + (v_y ** 2) + (v_z ** 2))
        res = dot_product / ((magnitude_interest_vector * magnitude_reference_vector) + 0.0000001)
        theta = math.degrees(math.acos(res))

        # get plane coordinate from angle and magnitude (polar coordinate)
        magnitude = magnitude_interest_vector
        x, y = magnitude * math.cos(math.radians(theta)), magnitude * math.sin(math.radians(theta))
        x, y = round(x), round(y)

        if dot_product_check > 0:
            projected_cam_plane_position = [x, y]
        else:
            projected_cam_plane_position = [x, -y]

        projected_cam_plane_position = self.scale_point_to_perspective(projected_cam_plane_position,
                                                                       perpendicular_distance_from_node_to_plane)
        return projected_cam_plane_position

    def scale_point_to_perspective(self, node_projected_position, node_perpendicular_dist_to_plane):
        x_angle, y_angle = 30, 30
        screen_x, screen_y = self.plane_dimensions[0], self.plane_dimensions[1]

        def get_scaling_factor(angle, base_length, perpendicular_dist):
            face_length = (perpendicular_dist * math.tan(math.radians(angle))) + base_length
            face_length = round(face_length, 2)

            scaling_factor = base_length/face_length
            scaling_factor = round(scaling_factor, 8)
            return scaling_factor

        # x-coordinate is:
        x_scale_factor = get_scaling_factor(x_angle, screen_x, node_perpendicular_dist_to_plane)
        node_x = node_projected_position[0]
        width = node_x - (screen_x/2)
        width = x_scale_factor * width
        node_x = (screen_x/2) + width

        # y-coordinate is:
        y_scale_factor = get_scaling_factor(y_angle, screen_y, node_perpendicular_dist_to_plane)
        node_y = node_projected_position[1]
        height = node_y - (screen_y/2)
        height = y_scale_factor * height
        node_y = (screen_y/2) + height

        return [node_x, node_y]

    def get_object_selection_from_mouse_position(self, mouse_position):
        object_history_nodal_positions = self.history_projected_nodal_positions

        if len(object_history_nodal_positions) > 0:
            def get_distance_between_points(point_a, point_b):
                d_x, d_y = point_a[0] - point_b[0], point_a[1] - point_b[1]
                dist = math.sqrt((d_x**2) + (d_y**2))
                dist = round(dist, 3)
                return dist

            # get nodes distance from cursor
            dist_to_node_map = {}
            dist_list = []
            for object_v in object_history_nodal_positions:
                object_obj = object_v[0]
                nodal_positions_list = object_v[1:]
                for node_position in nodal_positions_list:
                    if (node_position[0] > 0) and (node_position[1] > 0):
                        dist_res = get_distance_between_points(mouse_position, node_position)
                        dist_to_node_map[dist_res] = object_obj
                        dist_list.append(dist_res)

            if len(dist_to_node_map) > 0:
                # get the closest object to cursor within THRESHOLD
                dist_list.sort()
                distance_threshold = 15
                closest_distance = dist_list[0]
                if closest_distance <= distance_threshold:
                    closest_object = dist_to_node_map[dist_list[0]]
                    return closest_object
        return None

    def draw_point_on_cam_surface(self, node_p, surface_param, color, perpendicular_dist):
        projected_position = self.project_point_on_plane(node_p)
        cam_axis_position = self.get_cam_plane_coordinate_from_point(projected_position, perpendicular_dist)
        if cam_axis_position is not None:
            if self.invert_y_axis:
                cam_axis_position[1] = self.plane_dimensions[1] - cam_axis_position[1]
            pygame.draw.circle(surface_param, color, cam_axis_position, node_p.radius)
        return cam_axis_position

    def draw_line_on_cam_surface(self, line_obj, surface_param, color, perpendicular_dist):
        node_a, node_b = line_obj.nodes[0], line_obj.nodes[1]
        projected_position = self.project_point_on_plane(node_a)
        cam_axis_position_a = self.get_cam_plane_coordinate_from_point(projected_position, perpendicular_dist)
        projected_position = self.project_point_on_plane(node_b)
        cam_axis_position_b = self.get_cam_plane_coordinate_from_point(projected_position, perpendicular_dist)

        if None not in [cam_axis_position_a, cam_axis_position_b]:
            if self.invert_y_axis:
                cam_axis_position_a[1] = self.plane_dimensions[1] - cam_axis_position_a[1]
                cam_axis_position_b[1] = self.plane_dimensions[1] - cam_axis_position_b[1]
            pygame.draw.line(surface_param, color, cam_axis_position_a, cam_axis_position_b)

    def draw_surface_on_cam_surface(self, surface_obj, surface_param, color, perpendicular_dist):
        node_position_list = []
        for node_obj in surface_obj.nodes:
            projected_position = self.project_point_on_plane(node_obj)
            cam_axis_position = self.get_cam_plane_coordinate_from_point(projected_position, perpendicular_dist)
            node_position_list.append(cam_axis_position)
        node_position_list += [node_position_list[0]]
        if None not in node_position_list:
            if self.invert_y_axis:
                node_position_list = [[i[0], self.plane_dimensions[1] - i[1]] for i in node_position_list]
            pygame.draw.polygon(surface_param, color, node_position_list)

    def draw_yourself(self, cam_surface, active_object):
        if self.objects_to_project is not None:

            # 1. Fist create a list from closest to furthest object. Draw furthest to closest. Occlusion.
            object_distance_list = []
            closest_to_furthest_dist = set()
            for obj in self.objects_to_project:
                dist = self.find_distance_to_plane_from_a_point(obj.center_node)
                if dist > 0:
                    # get only points 'IN-FRONT' of cam plane
                    object_distance_list.append([obj, dist])
                    closest_to_furthest_dist.add(dist)

            closest_to_furthest_dist = sorted(closest_to_furthest_dist, reverse=True)

            # draw projected nodes
            # 2. draw objects in order of furthest to closest
            history_projected_nodal_positions = []
            for dist in closest_to_furthest_dist:
                object_list = []
                # get objects with that distance
                for obj in object_distance_list:
                    if obj[1] == dist:
                        object_list.append(obj[0])

                for obj in object_list:
                    object_nodal_positions = [obj]
                    for surf in obj.surfaces:
                        self.draw_surface_on_cam_surface(surf, cam_surface, surf.color, dist)
                    for node in obj.nodes:
                        projected_node_position = self.draw_point_on_cam_surface(node, cam_surface, "red", dist)
                        object_nodal_positions.append(projected_node_position)

                    # draw other cam projections
                    # if obj.type == "camera":
                    #     for obj_p in obj.objects_to_project:
                    #         for node in obj_p.nodes:
                    #             projected_position = obj.project_point_on_plane(node)
                    #             # print(projected_position)
                    #             temp_node = Node(projected_position, color="blue", object_name="hoohah")
                    #             self.draw_point_on_cam_surface(temp_node, cam_surface, "green", 100)

                    history_projected_nodal_positions.append(object_nodal_positions)
                    for line in obj.lines:
                        if obj == active_object:
                            color = "white"
                        else:
                            color = line.color
                        self.draw_line_on_cam_surface(line, cam_surface, color, dist)

                # Archive the projected node positions on camera plane
                self.history_projected_nodal_positions = history_projected_nodal_positions


class World:
    def __init__(self, camera=None, object_list=None):
        self.current_active_object_index = None
        self.object_list = object_list
        self.cam = camera

        self.time_constraint = {"user_key_inp": [time.time(), 0.1]}

    def add_objects(self, object_list):
        self.object_list += object_list

    def check_time_constraint(self, param):
        if time.time() - self.time_constraint[param][0] >= self.time_constraint[param][1]:
            self.time_constraint[param][0] = time.time()
            return True
        return False

    def respond_to_events(self, key_pressed_dict, mouse_obj, pygame_event_list):
        if self.check_time_constraint("user_key_inp"):
            # switch between objects
            if key_pressed_dict[pygame.K_TAB]:
                if len(self.object_list) > 0:
                    if self.current_active_object_index is None:
                        self.current_active_object_index = 0
                    else:
                        new_index = self.current_active_object_index + 1
                        self.current_active_object_index = new_index % len(self.object_list)

        # Activate objects based on user clicks
        for event in pygame_event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = mouse_obj.get_pos()
                object_to_activate = self.cam.get_object_selection_from_mouse_position(mouse_position)
                if object_to_activate is not None:
                    self.current_active_object_index = self.object_list.index(object_to_activate)
                    # print(f"Object selected is: {self.object_list[self.current_active_object_index ].name}")

    def update(self, key_pressed_dict, cam_surface, mouse_obj, pygame_event):
        self.respond_to_events(key_pressed_dict, mouse_obj, pygame_event)

        if self.current_active_object_index is None and len(self.object_list) > 0:
            self.current_active_object_index = 0
        if len(self.object_list) > 0:
            # active_object = self.object_list[self.current_active_object_index]
            active_object = self.cam
            active_object.update(key_pressed_dict, mouse_obj)

            for obj in self.object_list:
                if obj != active_object:
                    obj.update(None, None)

            self.cam.draw_yourself(cam_surface=cam_surface, active_object=active_object)

    @classmethod
    def object_generator(cls, type_of_object, center_pos, object_name, dimensional_vals=(60, 60, 60),
                         mode="return_object", parent_node=None):
        def generate_cylinder(center_pos, object_name):
            number_of_nodes_on_each_ceiling = 25
            length = 60

            center = center_pos
            center_node = Node(center, "white", 2, object_name=object_name, parent=parent_node)

            angle_step = 360 / number_of_nodes_on_each_ceiling
            node_list = []
            top_nodes, bottom_nodes = [], []
            # get top circle nodes
            for index in range(0, number_of_nodes_on_each_ceiling):
                angle = angle_step * index
                x, y = length * math.cos(math.radians(angle)), length * math.sin(math.radians(angle))
                x, y = round(x, 2), round(y, 2)

                top_node_position = [center[0] + x, center[1] + y, center[2] + length // 2]
                n_obj_top = Node(top_node_position, "red", 2, parent=center_node, object_name=object_name)
                top_nodes.append(n_obj_top)

                bottom_node_position = [center[0] + x, center[1] + y, center[2] - length // 2]
                n_obj_bottom = Node(bottom_node_position, "red", 2, parent=center_node, object_name=object_name)
                bottom_nodes.append(n_obj_bottom)

                node_list += [n_obj_top, n_obj_bottom]

            line_list = []
            top_line_map = top_nodes + [top_nodes[0]]
            for index_v in range(len(top_line_map) - 1):
                node_a = top_line_map[index_v]
                node_b = top_line_map[index_v + 1]
                line_obj = Line(node_a, node_b)
                line_list.append(line_obj)

            bottom_line_map = bottom_nodes + [bottom_nodes[0]]
            for index_v in range(len(top_line_map) - 1):
                node_a = bottom_line_map[index_v]
                node_b = bottom_line_map[index_v + 1]
                line_obj = Line(node_a, node_b)
                line_list.append(line_obj)

            # circle connecting bars
            for index in range(len(top_nodes)):
                node_a = top_nodes[index]
                node_b = bottom_nodes[index]
                line_obj = Line(node_a, node_b)
                line_list.append(line_obj)

            # create surfaces
            surface_map_1 = top_nodes + [top_nodes[0]]
            surface_map_2 = bottom_nodes + [bottom_nodes[0]]
            surface_list = []
            # 1. cylinder side surfaces
            for index_v in range(len(surface_map_1) - 1):
                n_a, n_b = surface_map_1[index_v], surface_map_1[index_v + 1]
                n_c, n_d = surface_map_2[index_v], surface_map_2[index_v + 1]
                node_obj_list = [n_a, n_b, n_d, n_c]
                surf_obj = Polygon(node_obj_list)
                surface_list.append(surf_obj)
            # 2. cylinder ceiling/bottom surfaces
            surf_obj = Polygon(surface_map_1)
            surface_list.append(surf_obj)
            surf_obj = Polygon(surface_map_2)
            surface_list.append(surf_obj)

            return [object_name, center_node, node_list, line_list, surface_list, []]

        def generate_cube(center_pos, object_name, dimensional_vals=dimensional_vals):
            center = center_pos
            x_length, y_length, z_length = dimensional_vals
            point_list = {"a": [-x_length // 2, -y_length // 2, 0],
                          "b": [x_length // 2, -y_length // 2, 0],
                          "c": [-x_length // 2, y_length // 2, 0],
                          "d": [x_length // 2, y_length // 2, 0],
                          "e": [-x_length // 2, -y_length // 2, z_length],
                          "f": [x_length // 2, -y_length // 2, z_length],
                          "g": [-x_length // 2, y_length // 2, z_length],
                          "h": [x_length // 2, y_length // 2, z_length]}

            center_node = Node(center, "white", 2, object_name=object_name, parent=parent_node)

            assumed_name_to_actual_name_mapping_dict = {}
            node_list = []
            for point_name in point_list:
                n_obj = Node(point_list[point_name], "red", 2, parent=center_node, object_name=object_name)
                actual_name = n_obj.name
                assumed_name_to_actual_name_mapping_dict[point_name] = actual_name
                node_list.append(n_obj)

            line_mapping = {"a": ["c", "e", "b"], "b": ["a", "f", "d"], "c": ["a", "d", "g"], "d": ["c", "h", "b"],
                            "e": ["a", "g", "f"], "f": ["e", "h", "b"], "g": ["c", "h", "e"], "h": ["d", "g", "f"]}

            line_list = []
            for node_name in line_mapping:
                node = Node.return_node_by_name(assumed_name_to_actual_name_mapping_dict[node_name])
                for neighbor_node_name in line_mapping[node_name]:
                    n_obj = Node.return_node_by_name(assumed_name_to_actual_name_mapping_dict[neighbor_node_name])
                    line_obj = Line(node, n_obj)
                    line_list.append(line_obj)

            surface_mapping = {"1": ["a", "b", "c", "d"], "2": ["a", "e", "f", "b"], "3": ["b", "f", "h", "d"],
                               "4": ["c", "d", "h", "g"], "5": ["c", "a", "e", "g"], "6": ["g", "e", "f", "h"]}

            surface_list = []
            for s_name in surface_mapping:
                node_obj_list = []
                for node_name in surface_mapping[s_name]:
                    n_obj = Node.return_node_by_name(assumed_name_to_actual_name_mapping_dict[node_name])
                    node_obj_list.append(n_obj)
                surf_obj = Polygon(node_obj_list)
                surface_list.append(surf_obj)

            return [object_name, center_node, node_list, line_list, surface_list, []]

        if mode == "return_object":
            if type_of_object == "cylinder":
                cylinder_param = generate_cylinder(center_pos, object_name)
                return Object(cylinder_param)
            elif type_of_object == "cube":
                cube_param = generate_cube(center_pos, object_name, dimensional_vals)
                return Object(cube_param)
        elif mode == "return_params":
            if type_of_object == "cylinder":
                cylinder_param = generate_cylinder(center_pos, object_name)
                return cylinder_param
            elif type_of_object == "cube":
                cube_param = generate_cube(center_pos, object_name, dimensional_vals)
                return cube_param
        return None


class GameWorld:
    def __init__(self, world_obj=None, load_from_disk=False):
        self.directory = "./assets/game_objects/"
        self.file_name = "temp_save_bhramand_world.obj"
        self.world_object = world_obj
        if load_from_disk:
            self.load()

        self.cam_surface = pygame.surface.Surface(self.world_object.cam.plane_dimensions)
        self.cam_surface.fill("black")

        self.time_constraint = {"user_key_inp": [time.time(), 0.1]}

    def check_time_constraint(self, param):
        if time.time() - self.time_constraint[param][0] >= self.time_constraint[param][1]:
            self.time_constraint[param][0] = time.time()
            return True
        return False

    def blit_surfaces(self):
        screen.blit(self.cam_surface, (0, 0))
        font = pygame.font.Font('freesansbold.ttf', 32)
        world = self.world_object
        text = font.render(world.object_list[world.current_active_object_index].name, True, "green", "blue")
        screen.blit(text, [40, 40])

        active_object_center_node = world.object_list[world.current_active_object_index].center_node
        text = font.render(str(active_object_center_node.get_your_position()), True, "green", "blue")
        screen.blit(text, [40, 80])

    def load(self):
        world_obj = self.world_object
        # load objects from file into world
        file_path = self.directory + self.file_name
        with open(file_path, 'rb') as file_obj:
            obj = pickle.load(file_obj)
            world_obj.object_list = obj.object_list
            world_obj.cam = obj.cam
        print("The world has been loaded Signore!!!")

    def save(self):
        file_path = self.directory + self.file_name
        with open(file_path, 'wb') as file_obj:
            pickle.dump(self.world_object, file_obj)
        print("The world has been saved Signore!!!")

    def respond_to_events(self, key_pressed_dict):
        # save the game state
        if self.check_time_constraint("user_key_inp"):
            if key_pressed_dict[pygame.K_s]:
                self.save()

    def update(self, key_pressed_dict, mouse_obj, pygame_event):
        self.respond_to_events(key_pressed_dict)
        self.world_object.update(key_pressed_dict, self.cam_surface, mouse_obj, pygame_event)


def game(new_game=True, game_world=None):

    # Step-1: Initialize the Game objects
    if new_game:
        game_world = game_world
    else:
        game_world = GameWorld(load_from_disk=True)

    # Step-2: Trigger the game run
    clock = pygame.time.Clock()
    game_run_state = True
    while game_run_state:

        pygame_events = pygame.event.get()
        for even in pygame_events:
            if even.type == pygame.QUIT:
                game_run_state = False
                break

        key_pressed_dict = pygame.key.get_pressed()

        game_world.update(key_pressed_dict, pygame.mouse, pygame_events)

        game_world.blit_surfaces()

        pygame.display.flip()
        game_world.cam_surface.fill("black")
        screen.fill("black")
        clock.tick(60)


if __name__ == "__main__":
    def test_game_world_generator():
        cube_1 = World.object_generator(type_of_object="cube", center_pos=[60, 60, 10], object_name="cube1")
        cube_2 = World.object_generator(type_of_object="cube", center_pos=[120, 120, 10], object_name="cube2")
        cube_1.child_objects = [cube_2]
        cube_3 = World.object_generator(type_of_object="cube", center_pos=[180, 180, 10], object_name="cube3")
        cube_2.child_objects = [cube_3]

        # cylinder_1_params = generate_cylinder(center_pos=[60, 60, 60], object_name="cylinder1")
        # cylinder_1 = Object(cylinder_1_params)
        # cube_1.child_objects = [cylinder_1]

        # random_node = Node([120, 120, 40], "orange", 2, object_name="planePoint")
        # cube_1.node_to_rotate_about = random_node
        # test_object = Object(["test_obj_1", random_node, [random_node], [], [], []])


        # plane_1 = Camera([cube_1, cube_2], cam_orientation="XZ")
        # w_object_list = [cube_1, cube_2, plane_1]
        # plane_2 = Camera(w_object_list, cam_orientation="XZ")


        #
        plane_1 = Camera([cube_1], cam_orientation="XZ")
        plane_3 = Camera([cube_1], cam_orientation="XZ")
        w_object_list = [cube_1, cube_2, plane_1, cube_3, plane_3]
        plane_2 = Camera(w_object_list, cam_orientation="XZ")
        plane_2.move_about_your_axis("longitudinal", direction="forward")


        # plane_1 = Camera([cube_1, cylinder_1, plane_2, test_object])
        # plane_1 = Camera([test_object])

        # w_object_list = [cube_1, cube_2, plane_1, cylinder_1]
        # w_object_list = [cube_1, cylinder_1, plane_1, test_object, plane_2]

        game_world = GameWorld(object_list=w_object_list, camera=plane_2)
        return game_world

    game(new_game=True, game_world=test_game_world_generator())
    # game(new_game=False)
