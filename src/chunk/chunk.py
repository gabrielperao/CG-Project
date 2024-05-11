import numpy as np

from src.object.object_id import ObjectId
from src.object.block import *


class Chunk:
    def __init__(self, index_x, index_z, max_gpu_data_array_index):
        self.SIZE = (16, 64, 16)
        self.OBJ_SIZE = 1  # depende do arquivo ".obj"
        self.index_x = index_x
        self.index_z = index_z
        self.max_gpu_data_array_index = max_gpu_data_array_index

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
            raise ValueError("Posição já ocupada")

        self.map[position] = object_code

    def remove_object(self, position: tuple):
        if not self.__is_valid_position(position):
            raise ValueError("Posição inválida")
        if self.map[position] == ObjectId.EMPTY:
            raise ValueError("Posição já vazia")

        self.map[position] = ObjectId.EMPTY

    def __calculate_object_coordinate(self, position):
        if not self.__is_valid_position(position):
            raise ValueError("Posição inválida")

        coordinate = np.array([
            self.index_x * self.SIZE[0] + position[0],
            position[1],
            self.index_z * self.SIZE[2] + position[2]
        ])
        return coordinate * self.OBJ_SIZE

    def __build_object(self, program, object_code, coord):
        obj = None
        if object_code == ObjectId.GRASS:
            obj = GrassBlock(program, coord, self.max_gpu_data_array_index)
        elif object_code == ObjectId.DIRT:
            obj = DirtBlock(program, coord, self.max_gpu_data_array_index)
        elif object_code == ObjectId.STONE:
            obj = StoneBlock(program, coord, self.max_gpu_data_array_index)
        elif object_code == ObjectId.COBBLESTONE:
            obj = CobblestoneBlock(program, coord, self.max_gpu_data_array_index)
        elif object_code == ObjectId.WOOD:
            obj = WoodBlock(program, coord)
        elif object_code == ObjectId.LEAF:
            obj = LeafBlock(program, coord, self.max_gpu_data_array_index)
        elif object_code == ObjectId.GLASS:
            obj = GlassBlock(program, coord, self.max_gpu_data_array_index)
        else:
            raise ValueError("Código de objeto não encontrado")

        return obj

    def build(self, program):
        for index, object_code in np.ndenumerate(self.map):
            if object_code != ObjectId.EMPTY:
                coord = self.__calculate_object_coordinate(index)
                obj = self.__build_object(program, object_code, coord)
                self.objects.append(obj)

    def render(self, window_height, window_width, camera):
        for obj in self.objects:
            obj.render(window_height, window_width, camera)
