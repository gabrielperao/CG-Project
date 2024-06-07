import numpy as np

from src.object.object_id import ObjectId
from src.object.block import *
from src.object.misc import *


class Chunk:
    SIZE = (16, 64, 16)
    OBJ_SIZE = 1  # depende do arquivo ".obj"

    def __init__(self, index_x, index_z, illumination):
        self.illumination = illumination
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
    def __build_object(program, object_code, index, coord, illumination):
        obj = None
        if object_code == ObjectId.GRASS:
            obj = GrassBlock(program, index, coord)
        elif object_code == ObjectId.DIRT:
            obj = DirtBlock(program, index, coord)
        elif object_code == ObjectId.STONE:
            obj = StoneBlock(program, index, coord)
        elif object_code == ObjectId.COBBLESTONE:
            obj = CobblestoneBlock(program, index, coord)
        elif object_code == ObjectId.WOOD:
            obj = WoodBlock(program, index, coord)
        elif object_code == ObjectId.LEAF:
            obj = LeafBlock(program, index, coord)
        elif object_code == ObjectId.GLASS:
            obj = GlassBlock(program, index, coord)
        elif object_code == ObjectId.TORCH:
            obj = Torch(program, index, coord, illumination)
        elif object_code == ObjectId.FLOWER:
            obj = Flower(program, index, coord)
        elif object_code == ObjectId.SLIME:
            obj = Slime(program, coord, illumination)
        else:
            raise ValueError("Código de objeto não encontrado")

        return obj

    def build(self, program):
        for index, object_code in np.ndenumerate(self.map):
            if object_code != ObjectId.EMPTY:
                coord = self.__calculate_object_coordinate(index, object_code)
                obj = self.__build_object(program, object_code, index, coord, self.illumination)
                self.objects.append(obj)

    def __has_block(self, position):
        return (self.map[position] >= ObjectId.GRASS) and (self.map[position] <= ObjectId.WOOD)

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

        obj.render(window_height, window_width, camera, faces=faces)

    def render(self, window_height, window_width, camera):
        for obj in self.objects:
            if hasattr(obj, 'dynamic_render'):
                obj.dynamic_render(window_height, window_width, camera)
            else:
                self.__render_obj_faces_optimizer(obj, window_height, window_width, camera)

    def update_entities(self, time):
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(time)
