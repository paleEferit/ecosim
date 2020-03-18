from typing import List

class EcoObject:
    def __init__(self,
                 start_life: int,
                 start_energy: int,
                 max_life: int,
                 max_energy: int,
                 display: str,
                 x: int,
                 y: int):
        if start_life < 0:
            raise ValueError('too low life')
        if start_energy < 0:
            raise ValueError('too low energy')
        if x < 0 or y < 0:
            raise ValueError('insufficient position')
        if len(display) != 1:
            raise ValueError('display should be 1 symbol')
        self._start_life = start_life
        self._cur_life = start_life
        self._start_energy = start_energy
        self._cur_energy = start_energy
        self._display = display
        self._max_energy = max_energy
        self._max_life = max_life
        self._x = x
        self._y = y

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_display(self) -> str:
        return self._display

    def get_energy_value(self) -> int:
        return self._cur_energy

    def get_start_energy(self) -> int:
        return self._start_energy

    def get_max_energy(self) -> int:
        return self._max_energy

    def get_life_value(self) -> int:
        return self._cur_life

    def get_start_life(self) -> int:
        return self._start_life

    def get_max_life(self) -> int:
        return self._max_life

    def alter_energy(self, delta: int):
        energy = self.get_energy_value()
        self._cur_energy = min(max(0, energy + delta), self.get_max_energy())

    def alter_life(self, delta: int):
        life = self.get_life_value()
        self._cur_life = min(max(0, life + delta), self.get_max_life())

    def get_name(self) -> str:
        pass

    def update(self):
        pass


class Map:
    def __init__(self, width: int, height: int, objects: List[EcoObject], empty_id: int, empty_display: str):
        if width < 2 or height < 2:
            raise ValueError('insufficient map size, should be at least 2 x 2')
        if len(empty_display) != 1:
            raise ValueError('display should be 1 symbol')
        self._width = width
        self._height = height
        self._empty_id = empty_id
        self._empty_display = empty_display

    def get_empty_id(self) -> int:
        return self._empty_id

    def get_empty_display(self) -> str:
        return self._empty_display

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height




class Plant(EcoObject):
    def __init__(self,
                 start_life: int,
                 start_energy: int,
                 max_life: int,
                 max_energy: int,
                 display: str,
                 sight: int,
                 dist: int,
                 speed: int,
                 x: int,
                 y: int):
        EcoObject.__init__(self, start_life, start_energy, max_life, max_energy, display, x, y)
        self._sight = sight
        self._dist = dist
        self._speed = speed

    def get_name(self) -> str:
        return 'plant'

    def update(self):
        self.alter_life(-1)
        self.alter_energy(1)


class Animal(EcoObject):
    def __init__(self,
                 start_life: int,
                 start_energy: int,
                 max_life: int,
                 max_energy: int,
                 display: str,
                 x: int,
                 y: int):
        EcoObject.__init__(self, start_life, start_energy, max_life, max_energy, display, x, y)

    def get_name(self) -> str:
        return 'animal'

    def can_eat(self, obj: EcoObject) -> bool:
        pass

    def eat(self, obj: EcoObject) -> bool:
        if self.can_eat(obj):
            self.alter_energy(obj.get_energy_value()//2)
            return True
        else:
            return False

