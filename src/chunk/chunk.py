import numpy as np

from src.object.object_id import ObjectId
from src.object.block import *
from src.object.misc import *


class Chunk:
    SIZE = (16, 64, 16)
    OBJ_SIZE = 1  # depende do arquivo ".obj"

    def __init__(self, index_x, index_z, illumination, objs_ilum_parameters):
        self.illumination = illumination
        self.obj_ilum_parameters = objs_ilum_parameters
        self.index_x = index_x
        self.index_z = index_z

        self.map = np.zeros(self.SIZE, dtype=int)
        self.objects = []

    def __is_valid_position(self, position):
        for i in range(3):
            if position[i] < 0 or position[i] >= self.SIZE[i]:
                return False

        return True

    def put_object(self, position: tuple, object_code):
        if not self.__is_valid_position(position):
            raise ValueError("Posição inválida")
        if self.map[position] != ObjectId.EMPTY:
            raise ValueError(f"Posição já ocupada: {position}, {self.map[position]}")

        self.map[position] = object_code

    def remove_object(self, position: tuple):
        if not self.__is_valid_position(position):
            raise ValueError("Posição inválida")
        if self.map[position] == ObjectId.EMPTY:
            raise ValueError("Posição já vazia")

        self.map[position] = ObjectId.EMPTY

    def __calculate_object_coordinate(self, position, object_code):
        if not self.__is_valid_position(position):
            raise ValueError("Posição inválida")

        coordinate = np.array([
            self.index_x * self.SIZE[0] + position[0],
            position[1],
            self.index_z * self.SIZE[2] + position[2]
        ], dtype=float)

        # centraliza a posição da tocha
        if object_code == ObjectId.TORCH:
            coordinate -= np.array([0.0625, 0.5, 0.0625])

        # centraliza a posição da flor
        if object_code == ObjectId.FLOWER:
            coordinate -= np.array([0.13255, 0.5, 0.13255])

        return coordinate * self.OBJ_SIZE

    @staticmethod
    def __build_object(program, object_code, index, coord, illumination, obj_ilum_parameters, ilum_sources):
        obj = None
        if object_code == ObjectId.GRASS:
            obj = GrassBlock(program, index, coord, obj_ilum_parameters, ilum_sources)
        elif object_code == ObjectId.DIRT:
            obj = DirtBlock(program, index, coord, obj_ilum_parameters, ilum_sources)
        elif object_code == ObjectId.STONE:
            obj = StoneBlock(program, index, coord, obj_ilum_parameters, ilum_sources)
        elif object_code == ObjectId.COBBLESTONE:
            obj = CobblestoneBlock(program, index, coord, obj_ilum_parameters, ilum_sources)
        elif object_code == ObjectId.WOOD:
            obj = WoodBlock(program, index, coord, obj_ilum_parameters, ilum_sources)
        elif object_code == ObjectId.LEAF:
            obj = LeafBlock(program, index, coord, obj_ilum_parameters, ilum_sources)
        elif object_code == ObjectId.GLASS:
            obj = GlassBlock(program, index, coord, obj_ilum_parameters, ilum_sources)
        elif object_code == ObjectId.TORCH:
            obj = Torch(program, index, coord, illumination)
        elif object_code == ObjectId.FLOWER:
            obj = Flower(program, index, coord, obj_ilum_parameters, ilum_sources)
        elif object_code == ObjectId.SLIME:
            obj = Slime(program, index, coord, illumination)
        else:
            raise ValueError("Código de objeto não encontrado")

        return obj

    def __get_illumination_source_indexes(self):
        ilum_indexes = []
        for index, object_code in np.ndenumerate(self.map):
            # busca pelos objetos que produzem luz
            if object_code == ObjectId.TORCH or object_code == ObjectId.SLIME:
                ilum_indexes.append(index)

        return ilum_indexes

    def __has_block(self, position):
        return (self.map[position] >= ObjectId.GRASS) and (self.map[position] <= ObjectId.WOOD)

    def __is_path_clear(self, target, font, recursive=False):
        x1, y1, z1 = target
        x2, y2, z2 = font

        # define as distâncias para cada eixo
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1

        # calcula o incremento por iteração para cada eixo
        steps = max(abs(dx), abs(dy), abs(dz))
        if steps == 0:
            return True

        x_inc = dx / steps
        y_inc = dy / steps
        z_inc = dz / steps

        # incrementa os eixos no sentido definido verificando obstáculos no caminho
        x, y, z = x1, y1, z1
        for _ in range(steps):
            x += x_inc
            y += y_inc
            z += z_inc
            current_index = tuple([round(x), round(y), round(z)])

            if not self.__is_valid_position(current_index) or self.__has_block(current_index):
                # caso encontrou um obstáculo, verifica a luz para alguma fronteira do bloco que não esteja coberta
                for direction in [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]:
                    new_target = tuple(np.array(target) + np.array(direction))
                    if recursive and self.__is_valid_position(new_target) and not self.__has_block(new_target):
                        return self.__is_path_clear(new_target, font, recursive=False)
                return False

        return True

    def __get_illumination_sources(self, index_map_object, ilum_source_indexes):
        ilum_source_obj = []
        for ilum_source in ilum_source_indexes:
            if self.__is_path_clear(index_map_object, ilum_source, recursive=True):
                ilum_source_obj.append(ilum_source)

        return ilum_source_obj

    def build(self, program):
        ilum_indexes = self.__get_illumination_source_indexes()
        for index, object_code in np.ndenumerate(self.map):
            if object_code != ObjectId.EMPTY:
                coord = self.__calculate_object_coordinate(index, object_code)
                ilum_sources = self.__get_illumination_sources(index, ilum_indexes)
                obj = self.__build_object(program, object_code, index, coord, self.illumination,
                                          self.obj_ilum_parameters, ilum_sources)
                self.objects.append(obj)

    def update_ilum_parameters(self, new_objs_ilum_parameters):
        for obj in self.objects:
            if isinstance(obj, Block) or isinstance(obj, Flower):
                obj.set_surface_illumination_proprieties(new_objs_ilum_parameters['ka'], new_objs_ilum_parameters['kd'],
                                                         new_objs_ilum_parameters['ks'], new_objs_ilum_parameters['ns'])

    def __has_block_neighbors(self, obj):
        neighbors = [False] * 6  # orientação: -y, y, x, z, -x, -z
        index = np.array(obj.index_in_chunk)

        for i, increment in enumerate([[0, -1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1], [-1, 0, 0], [0, 0, -1]]):
            current_position = tuple(index + increment)
            if self.__is_valid_position(current_position) and self.__has_block(current_position):
                neighbors[i] = True

        return neighbors

    def __render_obj_faces_optimizer(self, obj, window_height, window_width, camera):
        faces = [True] * 6
        if isinstance(obj, Block):
            faces = [not i for i in self.__has_block_neighbors(obj)]

        obj.render(window_height, window_width, camera, self.illumination, faces=faces)

    def render(self, window_height, window_width, camera):
        for obj in self.objects:
            if hasattr(obj, 'dynamic_render'):
                obj.dynamic_render(window_height, window_width, camera, self.illumination)
            else:
                self.__render_obj_faces_optimizer(obj, window_height, window_width, camera)

    def update_entities(self, time):
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(time)
