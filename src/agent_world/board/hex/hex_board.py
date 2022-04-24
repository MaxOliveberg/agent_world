from src.agent_world.board.exceptions import InvalidCoordinateException
from src.agent_world.board.game_square import IBoardSquare
import numpy as np


def hex_to_cartesian(x, y, z):
    """
    Todo: Swap to tuple argument?
    Converts hex coordinates to cartesian coordinates
    :param x: int
    :param y: int
    :param z: int
    :return: float
    """
    return x + z * np.cos(np.pi * (1 / 3)), z * np.sin(np.pi * (1 / 3))


class IHexBoard:
    """
    Interface defining a game board with hexagonal squares
    Methods:
        get_coordinate(self, x:int, y:int, z:int) - IBoardSquare
            Returns the board square of the given coordinates
    """

    def get_coordinate(self, x, y, z):
        """
        :param x: int
        :param y: int
        :param z: int
        :return: IBoardSquare
        """
        raise NotImplementedError


class SquareAlreadyHasContentException(Exception):
    pass


class HexSquare(IBoardSquare):
    """
    Implementation of IBoardSquare with no actual hex specific functionality

    Extends:
        IBoardSquare
    """

    def __init__(self):
        self.__content = None

    def get_content(self):
        """
        Inherited from IBoardSquare
        """
        return self.__content

    def add(self, thing):
        """
        Inherited from IBoardSquare
        """
        if self.__content is None:
            self.__content = thing
        else:
            raise SquareAlreadyHasContentException

    def remove(self, thing):
        """
        Inherited from IBoardSquare
        """
        #  I have to think a bit harder about this interface
        self.__content = None


class CircleHexBoard(IHexBoard):
    """
    A hexagonal game board which is always "circular"

    Extends:
        IHexBoard

    """

    def __iter__(self):
        """
        Allows for iteration over the squares
        """
        # Todo: 2d iter over both coords and squares
        return self.__squares.values().__iter__()

    def __init__(self, radius, lazy_loading=True):
        self.__radius = radius
        self.__squares = {}
        if lazy_loading is False:
            self.__preload()

    def get_coordinate(self, x, y, z):
        """
        Inherited from IHexBoard
        """
        self.__validate_coordinates(x, y, z)
        try:
            return self.__squares[(x, y, z)]
        except KeyError:
            new_square = HexSquare()
            self.__squares[(x, y, z)] = new_square
            return new_square

    def __validate_coordinates(self, x, y, z):
        """
        Function to make sure that the given coordinates are valid for this game board, otherwise an
        InvalidCoordinateException is thrown.
        Todo: Rewrite to a bool function?
        :param x: int
        :param y: int
        :param z: int
        :return: None
        """
        if x + y + z != 0 or max([x, y, z]) > self.__radius:
            raise InvalidCoordinateException

    def __preload(self):
        """
        Initialises all board squares to avoid having to do so in a 'lazy' manner
        :return: None
        """
        # This is really dumb
        # Todo: Make this less dumb :)
        for i in range(-self.__radius, self.__radius + 1):
            for j in range(-self.__radius, self.__radius + 1):
                for k in range(-self.__radius, self.__radius + 1):
                    if i + j + k == 0:
                        self.get_coordinate(i, j, k)
