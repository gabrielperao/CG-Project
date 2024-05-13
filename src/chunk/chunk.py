import numpy as np

from src.object.object_id import ObjectId
from src.object.block import *
from src.object.misc import *


class Chunk:
    def __init__(self, index_x, index_z, gpu_manager):
        self.SIZE = (16, 64, 16)
        self.OBJ_SIZE = 1  # depende do arquivo ".obj"
        self.index_x = index_x
        self.index_z = index_z
        self.gpu_manager = gpu_manager

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

    def __build_object(self, program, object_code, coord):
        obj = None
        if object_code == ObjectId.GRASS:
            obj = GrassBlock(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.GRASS))
        elif object_code == ObjectId.DIRT:
            obj = DirtBlock(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.DIRT))
        elif object_code == ObjectId.STONE:
            obj = StoneBlock(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.STONE))
        elif object_code == ObjectId.COBBLESTONE:
            obj = CobblestoneBlock(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.COBBLESTONE))
        elif object_code == ObjectId.WOOD:
            obj = WoodBlock(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.WOOD))
        elif object_code == ObjectId.LEAF:
            obj = LeafBlock(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.LEAF))
        elif object_code == ObjectId.GLASS:
            obj = GlassBlock(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.GLASS))
        elif object_code == ObjectId.TORCH:
            obj = Torch(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.TORCH))
        elif object_code == ObjectId.FLOWER:
            obj = Flower(program, coord, self.gpu_manager.get_size_index_for_object_id(ObjectId.FLOWER))
        else:
            raise ValueError("Código de objeto não encontrado")

        return obj

    def build(self, program):
        for index, object_code in np.ndenumerate(self.map):
            if object_code != ObjectId.EMPTY:
                coord = self.__calculate_object_coordinate(index, object_code)
                obj = self.__build_object(program, object_code, coord)
                self.objects.append(obj)

    def render(self, window_height, window_width, camera):
        for obj in self.objects:
            obj.render(window_height, window_width, camera, faces=[True]*6)
