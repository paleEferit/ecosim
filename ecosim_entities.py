from __future__ import annotations
from typing import List
from typing import Dict
from typing import NoReturn
from enum import Enum
import random
import math


class EcoObject:

    @staticmethod
    def get_max_possible_life() -> int:
        return 100

    @staticmethod
    def get_max_possible_jump_distance() -> int:
        return 10

    @staticmethod
    def get_max_possible_energy() -> int:
        return 100

    @staticmethod
    def get_max_possible_sight() -> int:
        return 15

    @staticmethod
    def get_max_possible_descendants() -> int:
        return 10

    @staticmethod
    def get_max_possible_speed() -> int:
        return 10

    @staticmethod
    def get_mutation_range() -> int:
        return 2

    @staticmethod
    def calc_mutation(base_value: int, mutation_range: int, min_value: int, max_value: int) -> int:
        min_plank = max(min_value, base_value - mutation_range)
        max_plank = min(max_value, base_value + mutation_range)
        return random.randint(min_plank, max_plank)

    def __init__(self,
                 start_life: int,
                 start_energy: int,
                 max_life: int,
                 max_energy: int,
                 display: str,
                 x: int,
                 y: int,
                 dist: int,
                 descendant_count_min: int,
                 descendant_count_max: int,
                 speed: int,
                 speed_max: int,
                 can_breed_on_self: bool,
                 sight: int):
        if speed < 0 or speed_max < 1:
            raise ValueError('speed should be 0 or higher, max speed should be 1 or higher')
        if speed > speed_max:
            raise ValueError('speed can not be above speed_max')
        if start_life < 0:
            raise ValueError('too low life')
        if start_energy < 0:
            raise ValueError('too low energy')
        if x < 0 or y < 0:
            raise ValueError('insufficient position')
        if len(display) != 1:
            raise ValueError('display should be 1 symbol')
        if dist < 1:
            raise ValueError('dist should be 1+')
        if descendant_count_min < 1 or descendant_count_max <1:
            raise ValueError('insufficient descendant count')
        if descendant_count_min > descendant_count_max or descendant_count_max > EcoObject.get_max_possible_descendants():
            raise ValueError('descendant count min max mismatch')
        if sight <= 0 or sight > EcoObject.get_max_possible_sight():
            raise ValueError('insufficient sight')
        self._sight = sight
        self._start_life = start_life
        self._cur_life = start_life
        self._start_energy = start_energy
        self._cur_energy = start_energy
        self._display = display
        self._max_energy = max_energy
        self._max_life = max_life
        self._x = x
        self._y = y
        self._dist = dist
        self._speed = speed
        self._speed_max = speed_max
        self._descendant_count_max = descendant_count_max
        self._descendant_count_min = descendant_count_min
        self._can_breed_on_self = can_breed_on_self

    def get_sight(self) -> int:
        return self._sight

    def get_can_breed_on_self(self) -> bool:
        return self._can_breed_on_self

    def get_self_breed(self) -> bool:
        return self._can_breed_on_self

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def set_x(self, value: int) -> NoReturn:
        self._x = value

    def set_y(self, value: int) -> NoReturn:
        self._y = value

    def get_speed(self) -> int:
        return self._speed

    def has_speed(self) -> bool:
        return self.get_speed() > 0

    def alter_speed(self, delta: int) -> NoReturn:
        self._speed = min(max(0, self.get_speed() + delta), self.get_speed_max())

    def get_speed_max(self) -> int:
        return self._speed_max

    def get_descendant_count_max(self) -> int:
        return self._descendant_count_max

    def get_descendant_count_min(self) -> int:
        return self._descendant_count_min

    def get_descendant_count(self) -> int:
        return random.randint(self.get_descendant_count_min(), self.get_descendant_count_max())

    def get_dist(self) -> int:
        return self._dist

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

    def get_breed_energy_cost(self) -> int:
        pass

    def can_breed(self) -> bool:
        pass

    def get_name(self) -> str:
        pass

    def update(self):
        pass

    def get_breed(self, obj: EcoObject) -> List[EcoObject]:
        pass

    def act_on(self, object_list: List[EcoObject], engine: Engine) -> NoReturn:
        pass

    def __eq__(self, other) -> bool:
        if other is EcoObject:
            return self.get_name().__eq__(other.get_name()) and self.get_x() == other.get_x() and self.get_y() == other.get_y()
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


class EcoMap:
    def __init__(self, width: int,
                 height: int,
                 objects: List[EcoObject],
                 empty_id: int,
                 empty_display: str,
                 obj_placeholder: EcoObject):
        if width < 2 or height < 2:
            raise ValueError('insufficient map size, should be at least 2 x 2')
        if len(empty_display) != 1:
            raise ValueError('display should be 1 symbol')
        for obj in objects:
            if (obj.get_y() < 0) or (obj.get_y() > height - 1) or (obj.get_x() < 0) or (obj.get_x() > width -1):
                raise ValueError('one or more objects are out of bounds')
        self._width = width
        self._height = height
        self._empty_id = empty_id
        self._empty_display = empty_display
        self._obj_placeholder = obj_placeholder
        self._object_map: List[List[int]] = []
        for i in range(height):
            tmp_lst: List[int] = []
            for j in range(width):
                tmp_lst.append(empty_id)
            self._object_map.append(tmp_lst)
        self._object_dict: Dict[int, EcoObject] = {}
        self._free_ids: List[int] = []
        for obj in objects:
            print('')

    def has_point_inside(self, x_pos: int, y_pos: int) -> bool:
        return (x_pos >= 0) and (x_pos < self.get_width()) and (y_pos >= 0) and (y_pos < self.get_height())

    def get_empty_display(self) -> str:
        return self._empty_display

    def get_empty_id(self) -> int:
        return self._empty_id

    def get_next_free_id(self) -> int:
        res_id = self.get_empty_id()
        if len(self._free_ids) > 0:
            res_id = self._free_ids[0]
            del self._free_ids[0]
        else:
            key_list = list(self._object_dict.keys())
            if len(key_list) == 0:
                res_id = self.get_empty_id() + 1
            else:
                max_id = key_list[0]
                for k in key_list:
                    if k > max_id:
                        max_id = k
                res_id = max_id + 1
        return res_id

    def get_obj_id_by_pos(self, x: int, y: int) -> int:
        return self._object_map[y][x]

    def add_obj_no_placing(self, obj: EcoObject) -> bool:
        x_pos = obj.get_x()
        y_pos = obj.get_y()
        tmp_id = self.get_obj_id_by_pos(x_pos, y_pos)
        if tmp_id != self.get_empty_id() or obj in self._object_dict.values():
            return False
        else:
            new_id = self.get_next_free_id()
            self._object_dict[new_id] = obj
            self._object_map[y_pos][x_pos] = new_id
            return True

    def add_obj_to_pos(self, obj: EcoObject, x_pos: int, y_pos: int) -> bool:
        tmp_id = self.get_obj_id_by_pos(x_pos, y_pos)
        if tmp_id != self.get_empty_id() or obj in self._object_dict.values():
            return False
        else:
            obj.set_x(x_pos)
            obj.set_y(y_pos)
            new_id = self.get_next_free_id()
            self._object_dict[new_id] = obj
            self._object_map[y_pos][x_pos] = new_id
            return True

    def has_object_id(self, obj_id: int) -> bool:
        return obj_id in self._object_dict.keys()

    def has_object(self, obj: EcoObject) -> bool:
        return obj in self._object_dict.values()

    def count_free_space(self, start_x, start_y, end_x, end_y) -> int:
        if self.has_point_inside(start_x, start_y) and self.has_point_inside(end_x, end_y):
            min_x = min(start_x, end_x)
            min_y = min(start_y, end_y)
            max_x = max(start_x, end_x)
            max_y = max(start_y, end_y)
            count: int = 0
            for i in range(min_y, max_y + 1, 1):
                for j in range(min_x, max_x + 1, 1):
                    if not self.has_object_at(j, i):
                        count += 1
            return count

    def has_free_space(self, start_x, start_y, end_x, end_y) -> int:
        if self.has_point_inside(start_x, start_y) and self.has_point_inside(end_x, end_y):
            min_x = min(start_x, end_x)
            min_y = min(start_y, end_y)
            max_x = max(start_x, end_x)
            max_y = max(start_y, end_y)
            res: bool = False
            for i in range(min_y, max_y + 1, 1):
                for j in range(min_x, max_x + 1, 1):
                    if not self.has_object_at(j, i):
                        res = True
                        break
                if res:
                    break
            return res

    def get_object_id(self, obj: EcoObject) -> int:
        if not self.has_object(obj):
            raise ValueError('obj not found')
        else:
            for k in self._object_dict:
                if self._object_dict[k].__eq__(obj):
                    return k
        return self.get_empty_id()

    def has_object_at(self, x_pos: int, y_pos: int) -> bool:
        return self.get_empty_id() != self._object_map[y_pos][x_pos]

    def _replace_id_on_map(self, target_id: int, new_id: int) -> int:
        count = 0
        for i in range(self.get_height()):
            for j in range(self.get_width()):
                if self._object_map[i][j] == target_id:
                    count += 1
                    self._object_map[i][j] = new_id

    def _remove_id_from_table(self, target_id: int) -> bool:
        if target_id in self._object_dict.keys():
            self._free_ids.append(target_id)
            del self._object_dict[target_id]
            return True
        else:
            return False

    def remove_obj(self, obj: EcoObject) -> bool:
        if self.has_object(obj):
            tmp_id = self.get_object_id(obj)
            return self.remove_obj_by_id(tmp_id)
        else:
            return False

    def remove_obj_by_id(self, obj_id: int) -> bool:
        if self.has_object_id(obj_id) and obj_id != self.get_empty_id():
            tmp_id = obj_id
            self._replace_id_on_map(tmp_id, self.get_empty_id())
            self._remove_id_from_table(tmp_id)
            return True
        else:
            return False

    def remove_obj_by_pos(self, x_pos: int, y_pos: int) -> bool:
        tmp_id = self.get_obj_id_by_pos(x_pos, y_pos)
        return self.remove_obj_by_id(tmp_id)

    def get_placeholder_obj(self) -> EcoObject:
        return self._obj_placeholder

    def get_eco_obj_by_id(self, obj_id: int) -> EcoObject:
        if self.has_object_id(obj_id):
            return self._object_dict[obj_id]
        else:
            return self.get_placeholder_obj()

    def get_eco_obj_by_pos(self, x_pos: int, y_pos: int) -> EcoObject:
        obj_id = self.get_obj_id_by_pos(x_pos, y_pos)
        if obj_id != self.get_empty_id():
            return self.get_eco_obj_by_id(obj_id)
        else:
            return self.get_placeholder_obj()

    def get_obj_by_id(self, obj_id: int) -> EcoObject:
        if obj_id != self.get_empty_id():
            return self._object_dict[obj_id]
        else:
            return self.get_placeholder_obj()

    def get_obj_by_pos(self, x_pos: int, y_pos: int) -> EcoObject:
        pos_id = self.get_obj_id_by_pos(x_pos, y_pos)
        return self.get_obj_by_id(pos_id)

    def get_display_by_pos(self, x_pos: int, y_pos: int) -> str:
        pos_id = self.get_obj_id_by_pos(x_pos, y_pos)
        if pos_id == self.get_empty_id():
            return self.get_empty_display()
        else:
            return self.get_obj_by_id(pos_id).get_display()

    def update_partial(self, start_x: int, start_y: int, end_x: int, end_y: int) -> NoReturn:
        if self.has_point_inside(start_x, start_y) and self.has_point_inside(end_x, end_y):
            min_x = min(start_x, end_x)
            max_x = max(start_x, end_x)
            min_y = min(start_y, end_y)
            max_y = max(start_y, end_y)
            for i in range(min_y, max_y + 1, 1):
                for j in range(min_x, max_x + 1, 1):
                    self._object_map[i][j] = self.get_empty_id()
            for k in self._object_dict:
                tmp_obj = self._object_dict[k]
                if (tmp_obj.get_x( )>= min_x) and (tmp_obj.get_x() <= max_x) and (tmp_obj.get_y() >= min_y) and (tmp_obj.get_y() <= max_y):
                    self._object_map[tmp_obj.get_y()][tmp_obj.get_x()] = k
        else:
            raise ValueError('insufficient position values')

    def get_objects_in_zone(self, start_x: int, start_y: int, end_x: int, end_y: int) -> List[EcoObject]:
        res: List[EcoObject] = []
        if self.has_point_inside(start_x, start_y) and self.has_point_inside(end_x, end_y):
            min_x = max(min(start_x, end_x), 0)
            max_x = min(max(start_x, end_x), self.get_width()-1)
            min_y = min(max(min(start_y, end_y), 0), self.get_height()-1)
            max_y = max(start_y, end_y)
            for i in range(min_y, max_y + 1, 1):
                for j in range(min_x, max_x + 1, 1):
                    key_val = self._object_map[i][j]
                    if key_val != self.get_empty_id():
                        res.append(self.get_obj_by_id(key_val))
        return res

    def update_positions(self) -> NoReturn:
        for i in range(self.get_height()):
            for j in range(self.get_width()):
                self._object_map[i][j] = self.get_empty_id()
        for k in self._object_dict:
            tmp_obj = self._object_dict[k]
            self._object_map[tmp_obj.get_y()][tmp_obj.get_x()] = k

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def move_multiple_objects_to(self, pos_x: int, pos_y: int, spread: int, keys: List[int]) -> bool:
        min_x = max(0, pos_x - spread)
        max_x = min(pos_x + spread, self.get_width() - 1)
        min_y = max(0, pos_y - spread)
        max_y = min(pos_y + spread, self.get_height() - 1)
        y_len = max_y - min_y + 1
        x_len = max_x - min_x + 1
        total = self.count_free_space(min_x, min_y, max_x, max_y)
        obj_count = len(keys)
        lst_select: List[int] = list(range(x_len * y_len))
        for i in range(y_len):
            for j in range(x_len):
                if self.has_object_at(j, i):
                    lst_select.remove(x_len * i + j)
        if total < obj_count:
            return False
        else:
            index = 0
            samples = random.sample(lst_select, obj_count)
            for s in samples:
                s_x = s // x_len
                s_y = s % x_len
                tmp_obj = self.get_obj_by_id(keys[index])
                tmp_x = tmp_obj.get_x()
                tmp_y = tmp_obj.get_y()
                self.move_object(tmp_x, tmp_y, s_x, s_y)
                index += 1
            return True

    def add_multiple_objects_around(self, pos_x: int, pos_y: int, spread: int, objects: List[EcoObject]) -> bool:
        min_x = max(0, pos_x - spread)
        max_x = min(pos_x + spread, self.get_width() - 1)
        min_y = max(0, pos_y - spread)
        max_y = min(pos_y + spread, self.get_height() - 1)
        y_len = max_y - min_y + 1
        x_len = max_x - min_x + 1
        total = self.count_free_space(min_x, min_y, max_x, max_y)
        obj_count = len(objects)
        lst_select: List[int] = list(range(x_len*y_len))
        for i in range(y_len):
            for j in range(x_len):
                if self.has_object_at(j, i):
                    lst_select.remove(x_len*i + j)
        if total < obj_count:
            return False
        else:
            index = 0
            samples = random.sample(lst_select, obj_count)
            for s in samples:
                s_x = s // x_len
                s_y = s % x_len
                self.add_obj_to_pos(objects[index], s_x, s_y)
                index += 1
            return True

    def move_object(self, obj_x: int, obj_y: int, new_x: int, new_y: int) -> bool:
        if self.has_point_inside(obj_x, obj_y) and self.has_point_inside(new_x, new_y):
            if self.has_object_at(obj_x, obj_y) and not self.has_object_at(new_x, new_y):
                eco_obj = self.get_eco_obj_by_pos(obj_x, obj_y)
                obj_id = self.get_obj_id_by_pos(obj_x, obj_y)
                self._object_map[obj_y][obj_x] = self.get_empty_id()
                self._object_map[new_y][new_x] = obj_id
                eco_obj.set_x(new_x)
                eco_obj.set_y(new_y)
                return True
            else:
                return False
        else:
            return False

    def get_all_animals(self) -> List[Animal]:
        res: List[Animal] = []
        for k in self._object_dict:
            obj = self._object_dict[k]
            if obj is Animal:
                res.append((Animal)(obj))
        return res

    def get_all_plants(self) -> List[Plant]:
        res: List[Plant] = []
        for k in self._object_dict:
            obj = self._object_dict[k]
            if obj is Animal:
                res.append((Plant)(obj))
        return res

    def get_all_obj_keys(self) -> List[int]:
        return list(self._object_dict.keys())

    def get_all_animal_keys(self) -> List[int]:
        res: List[int] = []
        for k in self._object_dict:
            obj = self._object_dict[k]
            if obj is Animal:
                res.append(k)
        return res

    def get_all_plant_keys(self) -> List[int]:
        res: List[int] = []
        for k in self._object_dict:
            obj = self._object_dict[k]
            if obj is Plant:
                res.append(k)
        return res


class Engine:

    @staticmethod
    def get_breed_range() -> int:
        return 5

    @staticmethod
    def get_failed_str_spread() -> int:
        return 2

    def __init__(self, eco_map: EcoMap):
        self._eco_map = eco_map

    def get_eco_map(self) -> EcoMap:
        return self._eco_map

    def can_breed(self, parent_1: EcoObject, parent_2: EcoObject) -> bool:
        equality: bool = (parent_1.get_x() == parent_2.get_x()) and (parent_1.get_y() == parent_2.get_y())
        species: bool = parent_1.get_name().__eq__(parent_2.get_name())
        p_breed: bool = parent_1.can_breed() and parent_2.can_breed()
        diff_pos = (parent_1.get_x() - parent_2.get_x())**2 + (parent_1.get_y() - parent_2.get_y())**2
        close_enough = diff_pos <= Engine.get_breed_range()**2
        gender = True
        if (parent_1 is Animal) and (parent_2 is Animal):
            an1 = (Animal)(parent_1)
            an2 = (Animal)(parent_2)
            gender = an1.get_gender() != an2.get_gender()
        return ((not equality) or (parent_1.get_can_breed_on_self() and parent_2.get_can_breed_on_self())) and species and p_breed and close_enough and gender

    def can_eat(self, obj: Animal, food: EcoObject) -> bool:
        x_diff = abs(obj.get_x() - food.get_x())
        y_diff = abs(obj.get_y() - food.get_y())
        res: bool = False
        if (x_diff <= 1) and (y_diff <= 1):
            point_x = food.get_x()
            point_y = food.get_y()
            the_map  = self.get_eco_map()
            if obj.can_eat(food):
                if food is Animal:
                    tmp_animal = (Animal)(food)
                    nx_1 = max(point_x - Engine.get_failed_str_spread(), 0)
                    nx_2 = min(point_x + Engine.get_failed_str_spread(), the_map.get_width() -1)
                    ny_1 = max(point_y - Engine.get_failed_str_spread(), 0)
                    ny_2 = min(point_y + Engine.get_failed_str_spread(), the_map.get_height() -1)
                    res = (obj.get_strength() > tmp_animal.get_strength()) or the_map.has_free_space(nx_1, ny_1, nx_2, ny_2)
                else:
                    res = True
        return res

    def can_step(self, obj: EcoObject, x_dir: int, y_dir: int) -> bool:
        if x_dir == 0 and y_dir == 0:
            raise ValueError('no step data')
        point_x = obj.get_x()
        point_y = obj.get_y()
        if x_dir > 0:
            point_x += 1
        elif x_dir < 0:
            point_x -= 1

        if y_dir > 0:
            point_y += 1
        elif y_dir < 0:
            point_y -= 1
        the_map = self.get_eco_map()
        free_flag = the_map.has_point_inside(point_x, point_y) and not the_map.has_object_at(point_x, point_y)
        return free_flag

    def can_jump(self, obj: Animal, x_dir: int, y_dir: int) -> bool:
        if x_dir == 0 and y_dir == 0:
            raise ValueError('no jump data')
        point_x = obj.get_x() + x_dir
        point_y = obj.get_y() + y_dir
        range_flag = obj.get_dist() >= round(math.sqrt((point_x - obj.get_x())**2 + (point_y - obj.get_y())**2))
        the_map = self.get_eco_map()
        pos_flag = the_map.has_point_inside(point_x, point_y)
        obj_flag = not the_map.has_object_at(point_x, point_y)
        if not obj_flag:
            tmp_obj = the_map.get_obj_by_pos(point_x, point_y)
            if obj.can_eat(tmp_obj):
                if tmp_obj is Animal:
                    tmp_animal = (Animal)(tmp_obj)
                    nx_1 = max(point_x - Engine.get_failed_str_spread(), 0)
                    nx_2 = min(point_x + Engine.get_failed_str_spread(), the_map.get_width() -1)
                    ny_1 = max(point_y - Engine.get_failed_str_spread(), 0)
                    ny_2 = min(point_y + Engine.get_failed_str_spread(), the_map.get_height() -1)
                    obj_flag = (obj.get_strength() > tmp_animal.get_strength()) or the_map.has_free_space(nx_1, ny_1, nx_2, ny_2)
                else:
                    obj_flag = True
        return pos_flag and range_flag and obj_flag

    def step(self, obj: EcoObject, x_dir: int, y_dir: int) -> bool:
        if self.can_step(obj, x_dir, y_dir) and obj.has_speed():
            pre_x = obj.get_x()
            point_x = pre_x
            pre_y = obj.get_y()
            point_y = pre_y
            if x_dir > 0:
                point_x += 1
            elif x_dir < 0:
                point_x -= 1
            if y_dir > 0:
                point_y += 1
            elif y_dir < 0:
                point_y -= 1
            the_map = self.get_eco_map()
            the_map.move_object(pre_x, pre_y, point_x, point_y)
            obj.alter_speed(-1)
            return True
        else:
            return False

    def jump(self, obj: Animal, x_dir: int, y_dir: int) -> bool:
        if self.can_jump(obj, x_dir, y_dir) and obj.has_speed():
            pre_x = obj.get_x()
            pre_y = obj.get_y()
            point_x = obj.get_x() + x_dir
            point_y = obj.get_y() + y_dir
            cur_map = self.get_eco_map()
            if cur_map.has_object_at(point_x, point_y):
                food = cur_map.get_obj_by_pos(point_x, point_y)
                # food type
                if food is Plant:
                    obj.eat(food)
                    obj.alter_energy(- obj.get_dist())
                    cur_map.remove_obj_by_pos(point_x, point_y)
                    cur_map.move_object(pre_x, pre_y, point_x, point_y)
                else:
                    animal_food = (Animal)(food)
                    food_strength = animal_food.get_strength()
                    obj_strength = obj.get_strength()
                    delta = abs(obj_strength - food_strength)
                    # fail to hunt
                    if food_strength >= obj_strength:
                        obj.alter_energy(-delta)
                        animal_food.alter_energy(-delta)
                        obj.alter_life(-delta)
                        animal_food.alter_life(-delta)
                        cur_map.remove_obj_by_pos(pre_x, pre_y)
                        obj.alter_energy(- obj.get_dist())
                        spread = Engine.get_failed_str_spread()
                        cur_map.move_multiple_objects_to(point_x, point_y, spread, [cur_map.get_obj_id_by_pos(pre_x, pre_y)])
                    else:
                        obj.alter_energy(- obj.get_dist())
                        obj.eat(animal_food)
                        cur_map.remove_obj_by_pos(point_x, point_y)
                        cur_map.move_object(pre_x, pre_y, point_x, point_y)
            obj.alter_speed(-1)
            return True
        else:
            return False

    def eat(self, eater_obj: Animal, prey_obj: EcoObject) -> bool:
        if self.can_eat(eater_obj, prey_obj):
            pre_x = eater_obj.get_x()
            pre_y = eater_obj.get_y()
            point_x = prey_obj.get_x()
            point_y = prey_obj.get_y()
            cur_map = self.get_eco_map()
            # food type
            if prey_obj is Plant:
                eater_obj.eat(prey_obj)
                eater_obj.alter_energy(- eater_obj.get_dist())
                cur_map.remove_obj_by_pos(point_x, point_y)
                cur_map.move_object(pre_x, pre_y, point_x, point_y)
            else:
                animal_food = (Animal)(prey_obj)
                food_strength = animal_food.get_strength()
                obj_strength = eater_obj.get_strength()
                delta = abs(obj_strength - food_strength)
                # fail to hunt
                if food_strength >= obj_strength:
                    eater_obj.alter_energy(-delta)
                    animal_food.alter_energy(-delta)
                    eater_obj.alter_life(-delta)
                    animal_food.alter_life(-delta)
                    cur_map.remove_obj_by_pos(pre_x, pre_y)
                    spread = 2
                    cur_map.move_multiple_objects_to(point_x, point_y, spread, [cur_map.get_obj_id_by_pos(pre_x, pre_y)])
                else:
                    eater_obj.eat(animal_food)
                    cur_map.remove_obj_by_pos(point_x, point_y)
                    cur_map.move_object(pre_x, pre_y, point_x, point_y)

            eater_obj.alter_speed(-1)
            return True
        else:
            return False

    def _add_offsprings(self, offsprings: List[EcoObject], x_pos: int, y_pos: int) -> bool:
        the_map = self.get_eco_map()
        free_space: int = the_map.get_height()*the_map.get_width() - len(the_map.get_all_obj_keys())
        target_count = len(offsprings)
        if free_space < target_count:
            return False
        else:
            start_spread = Engine.get_breed_range()
            x_min = x_pos - start_spread
            x_max = x_pos + start_spread
            y_min = y_pos - start_spread
            y_max = y_pos + start_spread
            while the_map.count_free_space(x_min, y_min, x_max, y_max) < target_count:
                start_spread += 1
                x_min = x_pos - start_spread
                x_max = x_pos + start_spread
                y_min = y_pos - start_spread
                y_max = y_pos + start_spread
            the_map.add_multiple_objects_around(x_pos, y_pos, start_spread, offsprings)

    def breed(self, parent_1: EcoObject, parent_2: EcoObject) -> bool:
        if self.can_breed(parent_1, parent_2):
            x_pos = parent_1.get_x()
            y_pos = parent_1.get_y()
            offsprings: List[EcoObject] = []
            if parent_1 is Plant:
                offsprings.extend(parent_1.get_breed(parent_2))

            elif(parent_1 is Animal) and (parent_2 is Animal):
                an1 = (Animal)(parent_1)
                an2 = (Animal)(parent_2)
                if an2.get_gender() == Gender.FEMALE:
                    offsprings.extend(an2.get_breed(an1))
                    x_pos = parent_2.get_x()
                    y_pos = parent_2.get_y()
                else:
                    offsprings.extend(an1.get_breed(an1))
            tmp: bool = self._add_offsprings(offsprings, x_pos, y_pos)
            if tmp:
                parent_1.alter_energy(-parent_1.get_breed_energy_cost())
                parent_2.alter_energy(-parent_2.get_breed_energy_cost())
                return True
            else:
                return False
        else:
            return False

    def sub_turn(self) -> int:
        the_map = self.get_eco_map()
        keys = the_map.get_all_obj_keys()
        count: int = 0
        for k in keys:
            obj = the_map.get_eco_obj_by_id(k)
            if obj.get_speed() > 0:
                count += 1
                x_pos = obj.get_x()
                y_pos = obj.get_y()
                spread = obj.get_sight()
                x_min = x_pos - spread
                x_max = x_pos + spread
                y_min = y_pos - spread
                y_max = y_pos + spread
                interactable = the_map.get_objects_in_zone(x_min, y_min, x_max, y_max)
                obj.act_on(interactable, self)
                obj.alter_speed(-1)
        return count

    def full_turn(self) -> int:
        count = 0
        while self.sub_turn() > 0:
            count += 1
        self.update()
        return count

    def update(self) -> NoReturn:
        the_map = self.get_eco_map()
        keys = the_map.get_all_obj_keys()
        for k in keys:
            obj = the_map.get_eco_obj_by_id(k)
            obj.update()


class UIDisplay:
    def __init__(self, eco_map: EcoMap):
        self._eco_map = eco_map

    def get_eco_map(self) -> EcoMap:
        return self._eco_map

    def display(self) -> NoReturn:
        pass

    def update_display(self) -> NoReturn:
        pass

    def init(self):
        pass

    def clear_all(self) -> NoReturn:
        pass


class Gender(Enum):
    MALE = 1,
    FEMALE = 2


class Plant(EcoObject):
    def __init__(self,
                 start_life: int,
                 start_energy: int,
                 max_life: int,
                 max_energy: int,
                 display: str,
                 x: int,
                 y: int,
                 dist: int,
                 descendant_count_min: int,
                 descendant_count_max: int,
                 speed: int,
                 speed_max: int,
                 can_breed_on_self: bool,
                 sight: int):
        EcoObject.__init__(self,
                           start_life,
                           start_energy,
                           max_life,
                           max_energy,
                           display,
                           x,
                           y,
                           dist,
                           descendant_count_min,
                           descendant_count_max,
                           speed,
                           speed_max,
                           can_breed_on_self,
                           sight)

    def get_breed_energy_cost(self) -> int:
        return int(self.get_max_energy()/5)

    def can_breed(self) -> bool:
        return self.get_energy_value() > self.get_breed_energy_cost() + int(self.get_max_energy()/10) + 1

    def create_descendant(self,
                          start_life: int,
                          start_energy: int,
                          max_life: int,
                          max_energy: int,
                          display: str,
                          x: int,
                          y: int,
                          dist: int,
                          descendant_count_min: int,
                          descendant_count_max: int,
                          speed: int,
                          speed_max: int,
                          can_breed_on_self: bool,
                          sight: int) -> Plant:
        pass

    def get_breed(self, obj: Plant) -> List[Plant]:
        res = []
        if obj.get_name().__eq__(self.get_name()):
            sight_limit = EcoObject.get_max_possible_sight()
            descendants_limit = EcoObject.get_max_possible_descendants()
            energy_limit = EcoObject.get_max_possible_energy()
            speed_limit = EcoObject.get_max_possible_speed()
            life_limit = EcoObject.get_max_possible_life()
            dist_limit = EcoObject.get_max_possible_jump_distance()
            mutation_min = -EcoObject.get_mutation_range()
            mutation_max = EcoObject.get_mutation_range()
            breed_count = random.randint(self.get_descendant_count_min(), self.get_descendant_count_max())
            for i in range(breed_count):
                sight_val: int = min(
                    round((self.get_sight() + obj.get_sight()) / 2) + random.randint(mutation_min, mutation_max),
                    sight_limit)
                descendants_min_val: int = min(
                    round((self.get_descendant_count_min() + obj.get_descendant_count_min()) / 2) + random.randint(
                        mutation_min, mutation_max), descendants_limit)
                descendants_max_val: int = min(
                    round((self.get_descendant_count_max() + obj.get_descendant_count_max()) / 2) + random.randint(
                        mutation_min, mutation_max), descendants_limit)
                if descendants_min_val > descendants_max_val:
                    tmp_val = descendants_max_val
                    descendants_max_val = descendants_min_val
                    descendants_min_val = tmp_val
                energy_max_val: int = min(
                    round((self.get_max_energy() + obj.get_max_energy()) / 2) + random.randint(mutation_min,
                                                                                               mutation_max),
                    energy_limit)
                speed_val: int = min(
                    round((self.get_speed_max() + obj.get_speed_max()) / 2) + random.randint(mutation_min,
                                                                                             mutation_max), speed_limit)
                life_max_val: int = min(
                    round((self.get_max_life() + obj.get_max_life()) / 2) + random.randint(mutation_min, mutation_max),
                    life_limit)
                dist_val: int = min(
                    round((self.get_dist() + obj.get_dist()) / 2) + random.randint(mutation_min, mutation_max),
                    dist_limit)
                start_life_val = life_max_val
                can_breed_on_self_val = self.get_can_breed_on_self()
                start_energy_val = energy_max_val // 2 + 2
                display_val = self.get_display()
                x_val = self.get_x()
                y_val = self.get_y()
                offspring = self.create_descendant(life_max_val,
                                                   start_energy_val,
                                                   life_max_val,
                                                   energy_max_val,
                                                   display_val,
                                                   x_val,
                                                   y_val,
                                                   dist_val,
                                                   descendants_min_val,
                                                   descendants_max_val,
                                                   speed_val,
                                                   speed_val,
                                                   can_breed_on_self_val,
                                                   sight_val)
                res.append(offspring)
        return res

    def get_name(self) -> str:
        pass

    def act_on(self, object_list: List[EcoObject], engine: Engine) -> NoReturn:
        pass

    def update(self):
        self.alter_life(-1)
        self.alter_energy(1)


class Animal(EcoObject):
    @staticmethod
    def get_max_possible_strength() -> int:
        return 20

    def __init__(self,
                 start_life: int,
                 start_energy: int,
                 max_life: int,
                 max_energy: int,
                 display: str,
                 x: int,
                 y: int,
                 dist: int,
                 descendant_count_min: int,
                 descendant_count_max: int,
                 speed: int,
                 speed_max: int,
                 can_breed_on_self: bool,
                 sight: int,
                 strength: int,
                 gender: Gender):
        EcoObject.__init__(self,
                           start_life,
                           start_energy,
                           max_life,
                           max_energy,
                           display,
                           x,
                           y,
                           dist,
                           descendant_count_min,
                           descendant_count_max,
                           speed,
                           speed_max,
                           can_breed_on_self,
                           sight)
        self._strength = strength
        self._gender = gender

    def create_descendant(self,
                          start_life: int,
                          start_energy: int,
                          max_life: int,
                          max_energy: int,
                          display: str,
                          x: int,
                          y: int,
                          dist: int,
                          descendant_count_min: int,
                          descendant_count_max: int,
                          speed: int,
                          speed_max: int,
                          can_breed_on_self: bool,
                          sight: int,
                          strength: int,
                          gender: Gender) -> Animal:
        pass

    def get_strength(self) -> int:
        return self._strength

    def get_gender(self) -> Gender:
        return self._gender

    def get_starving_plank(self) -> int:
        return int(self.get_max_energy() / 2)

    def get_breed_energy_cost(self) -> int:
        return int(self.get_max_energy() / 4)

    def get_name(self) -> str:
        pass

    def can_breed(self) -> bool:
        return self.get_energy_value() > self.get_breed_energy_cost() + self.get_starving_plank() + 1

    def get_breed(self, obj: Animal) -> List[Animal]:
        res = []
        if obj.get_name().__eq__(self.get_name()):
            sight_limit = EcoObject.get_max_possible_sight()
            descendants_limit = EcoObject.get_max_possible_descendants()
            energy_limit = EcoObject.get_max_possible_energy()
            speed_limit = EcoObject.get_max_possible_speed()
            life_limit = EcoObject.get_max_possible_life()
            strength_limit = Animal.get_max_possible_strength()
            dist_limit = EcoObject.get_max_possible_jump_distance()
            mutation_min = -EcoObject.get_mutation_range()
            mutation_max = EcoObject.get_mutation_range()
            breed_count = random.randint(self.get_descendant_count_min(), self.get_descendant_count_max())
            for i in range(breed_count):
                sight_val: int = min(round((self.get_sight()+obj.get_sight())/2) + random.randint(mutation_min, mutation_max), sight_limit)
                descendants_min_val: int = min(round((self.get_descendant_count_min() + obj.get_descendant_count_min())/2) + random.randint(mutation_min, mutation_max), descendants_limit)
                descendants_max_val: int = min(round((self.get_descendant_count_max() + obj.get_descendant_count_max())/2) + random.randint(mutation_min, mutation_max), descendants_limit)
                if descendants_min_val > descendants_max_val:
                    tmp_val = descendants_max_val
                    descendants_max_val = descendants_min_val
                    descendants_min_val = tmp_val
                strength_val: int = min(round((self.get_strength()+obj.get_strength())/2) + random.randint(mutation_min, mutation_max), strength_limit)
                energy_max_val: int = min(round((self.get_max_energy()+obj.get_max_energy())/2) + random.randint(mutation_min, mutation_max), energy_limit)
                speed_val: int = min(round((self.get_speed_max()+obj.get_speed_max())/2) + random.randint(mutation_min, mutation_max), speed_limit)
                life_max_val: int = min(round((self.get_max_life()+obj.get_max_life())/2) + random.randint(mutation_min, mutation_max), life_limit)
                dist_val: int = min(round((self.get_dist()+obj.get_dist())/2) + random.randint(mutation_min, mutation_max), dist_limit)
                start_life_val = life_max_val
                can_breed_on_self_val = self.get_can_breed_on_self()
                start_energy_val = energy_max_val // 2 + 2
                display_val = self.get_display()
                x_val = self.get_x()
                y_val = self.get_y()
                gender_val = Gender.FEMALE
                tmp_selector = random.randint(1, 2)
                if tmp_selector == 1:
                    gender_val = Gender.MALE
                offspring = self.create_descendant(life_max_val,
                                                   start_energy_val,
                                                   life_max_val,
                                                   energy_max_val,
                                                   display_val,
                                                   x_val,
                                                   y_val,
                                                   dist_val,
                                                   descendants_min_val,
                                                   descendants_max_val,
                                                   speed_val,
                                                   speed_val,
                                                   can_breed_on_self_val,
                                                   sight_val,
                                                   strength_val,
                                                   gender_val)
                res.append(offspring)
        return res

    def can_eat(self, obj: EcoObject) -> bool:
        pass

    def update(self):
        if self.get_energy_value() > self.get_starving_plank():
            self.alter_life(-1)
        else:
            self.alter_life(-3)
        self.alter_energy(-(self.get_strength() + self.get_speed_max() - self.get_speed()))

    def eat(self, obj: EcoObject) -> bool:
        if self.can_eat(obj):
            self.alter_energy(obj.get_energy_value()//2)
            return True
        else:
            return False

    def act_on(self, object_list: List[EcoObject], engine: Engine) -> NoReturn:
        pass

