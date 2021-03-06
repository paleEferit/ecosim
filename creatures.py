from __future__ import annotations
from ecosim_entities import *


class Grass(Plant):
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
        Plant.__init__(self,
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
        return Grass(start_life,
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

    def get_name(self) -> str:
        return 'grass'

    def _dist_sqr(self, obj: EcoObject) -> int:
        return (self.get_x() - obj.get_x())**2 + (self.get_y() - self.get_y())**2

    def act_on(self, object_list: List[EcoObject], engine: Engine) -> NoReturn:
        # breed sequence
        if self.can_breed():
            # candidate list
            acceptable: List[EcoObject] = []
            for eo in object_list:
                target_name = eo.get_name()
                my_name = self.get_name()
                target_can_breed = eo.can_breed()
                i_can_breed = self.can_breed()
                if eo.__ne__(self) and target_name.__eq__(my_name) and target_can_breed and engine.can_breed_on_turn(eo) and engine.can_breed_on_turn(self):
                    acceptable.append(eo)
            breed_range = engine.get_breed_range()
            real_candidates: List[EcoObject] = []
            for a in acceptable:
                if (self._dist_sqr(a) <= breed_range ** 2) and (engine.can_breed(self, a)):
                    real_candidates.append(a)
            if isinstance(self, Plant):
                if len(real_candidates) > 0:
                    max_energy = real_candidates[0].get_energy_value()
                    candidate = real_candidates[0]
                    for c in real_candidates:
                        if c.get_energy_value() > max_energy:
                            max_energy = c.get_energy_value()
                            candidate = c
                    engine.breed(self, candidate)
                else:
                    engine.breed(self, self)


class Rabbit(Animal):
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
        Animal.__init__(self,
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
                        sight,
                        strength,
                        gender)

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
        return Rabbit(start_life,
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
                      sight,
                      strength,
                      gender)

    def get_name(self) -> str:
        return 'rabbit'

    def can_eat(self, obj: EcoObject) -> bool:
        res = isinstance(obj, Plant)
        return res

    def act_on(self, object_list: List[EcoObject], engine: Engine):
        # resetting target
        if (self.is_target_set()) and (self.get_x() == self.get_target_x()) and (
                self.get_y() == self.get_target_y()):
            self.reset_target()

        action_is_possible_flag: bool = True
        # more for testing mb
        if self.is_target_set():
            action_is_possible_flag = False

        # making lists
        acceptable: List[EcoObject] = []
        eaters: List[Animal] = []
        food: List[EcoObject] = []
        # filling lists
        for eo in object_list:
            if eo.__ne__(self):
                if eo.get_name().__eq__(self.get_name()) and eo.can_breed() and engine.can_breed_on_turn(
                        eo) and engine.can_breed_on_turn(self):
                    if isinstance(eo, Animal) and isinstance(self, Animal):
                        if eo.get_gender() != self.get_gender():
                            acceptable.append(eo)
                    else:
                        acceptable.append(eo)
                if isinstance(eo, Animal):
                    tmp = eo
                    if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                        eaters.append(tmp)
                if self.can_eat(eo):
                    if isinstance(eo, Animal):
                        tmp = eo
                        if tmp.get_strength() < self.get_strength():
                            food.append(eo)
                    else:
                        food.append(eo)

        # run sequence
        if len(eaters) > 0 and not isinstance(self, Plant):
            action_is_possible_flag = False
            x_start = self.get_x()
            y_start = self.get_y()
            y_vec_sum = 0
            x_vec_sum = 0
            count = 0
            min_x = engine.get_min_x()
            max_x = engine.get_max_x()
            min_y = engine.get_min_y()
            max_y = engine.get_max_y()
            for ea in eaters:
                tmp_x_v = ea.get_x() - x_start
                tmp_y_v = ea.get_y() - y_start
                count += 1
                x_vec_sum += tmp_x_v
                y_vec_sum += tmp_y_v
            target_x: int = max(min(x_start - self.get_speed_max() * round(x_vec_sum / count), max_x), min_x)
            target_y: int = max(min(y_start - self.get_speed_max() * round(y_vec_sum / count), max_y), min_y)
            # updating target to not be cornered
            hostile_vector_x = round(x_vec_sum / count)
            hostile_vector_y = round(y_vec_sum / count)
            if (x_start == min_x or x_start == max_x) or (y_start == min_y or y_start == max_y) and (
                    target_x == x_start) and (target_y == y_start):
                if abs(hostile_vector_x) > abs(hostile_vector_y):
                    if hostile_vector_y > 0:
                        target_y = max_y
                    else:
                        target_y = min_y
                else:
                    if hostile_vector_x > 0:
                        target_x = max_x
                    else:
                        target_x = min_x
            self.set_target(target_x, target_y)

        #  feed sequence
        if (not self.can_breed() or len(acceptable) == 0) and not self.is_target_set() and len(
                food) > 0 and not engine.is_well_fed(self):
            action_is_possible_flag = False
            max_food_energy = food[0].get_energy_value()
            max_energy_candidate = food[0]
            min_food_distance = self._dist_sqr(food[0])
            min_distance_candidate = food[0]
            for f in food:
                energy = f.get_energy_value()
                distance = self._dist_sqr(f)
                if energy > max_food_energy:
                    max_food_energy = energy
                    max_energy_candidate = f
                if distance < min_food_distance:
                    min_food_distance = distance
                    min_distance_candidate = f
            candidate: EcoObject = max_energy_candidate

            ratio = self._dist_sqr(max_energy_candidate) / min_food_distance
            if ratio >= 4 or min_food_distance <= 2:
                candidate = min_distance_candidate
            # action selection
            food_distance = self._dist_sqr(candidate)
            if food_distance <= 2:
                engine.eat(self, candidate)
                self.reset_target()
            else:
                target_x = candidate.get_x()
                target_y = candidate.get_y()
                self.set_target(target_x, target_y)

        # breed sequence
        if self.can_breed() and len(acceptable) > 0 and not self.is_target_set():
            action_is_possible_flag = False
            # candidate list
            breed_range = engine.get_breed_range()
            real_candidates: List[EcoObject] = []
            for a in acceptable:
                if (self._dist_sqr(a) <= breed_range ** 2) and (engine.can_breed(self, a)):
                    real_candidates.append(a)
            if len(real_candidates) > 0:
                max_energy = real_candidates[0].get_energy_value()
                candidate = real_candidates[0]
                if isinstance(self, Plant):
                    if len(real_candidates) > 0:
                        for c in real_candidates:
                            if c.get_energy_value() > max_energy:
                                max_energy = c.get_energy_value()
                                candidate = c
                        engine.breed(self, candidate)
                    else:
                        engine.breed(self, self)
                elif isinstance(self, Animal):
                    for c in acceptable:
                        if c.get_energy_value() > max_energy:
                            max_energy = c.get_energy_value()
                            candidate = c
                    if (self._dist_sqr(candidate) <= breed_range ** 2) and (engine.can_breed(self, candidate)):
                        engine.breed(self, candidate)
                    else:
                        self.set_target(candidate.get_x(), candidate.get_y())
            else:
                action_is_possible_flag = True

        # pick random direction just in case there is nothing to do
        if (len(object_list) == 0) or (action_is_possible_flag and not self.is_target_set()):
            x_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
            y_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
            if x_v == 0 and y_v == 0:
                x_v = self.get_dist()
                y_v = - self.get_dist()
            min_x = engine.get_min_x()
            max_x = engine.get_max_x()
            min_y = engine.get_min_y()
            max_y = engine.get_max_y()
            target_x = max(min(self.get_x() + x_v, max_x), min_x)
            target_y = max(min(self.get_y() + y_v, max_y), min_y)
            self.set_target(target_x, target_y)

        # move sequence
        if self.is_target_set():
            # a crutch to fix out of range
            max_x = engine.get_max_x()
            min_x = engine.get_min_x()
            max_y = engine.get_max_y()
            min_y = engine.get_min_y()
            target_x = max(min(self.get_target_x(), max_x), min_x)
            target_y = max(min(self.get_target_y(), max_y), min_y)
            self.set_target(target_x, target_y)
            vector_x = target_x - self.get_x()
            vector_y = target_y - self.get_y()
            if engine.can_jump(self, vector_x, vector_y):
                engine.jump(self, vector_x, vector_y)
                self.reset_target()
            elif engine.can_breed_at_pos(self, target_x, target_y):
                engine.breed_by_pos(self, target_x, target_y)
            elif engine.can_eat_at_pos(self, target_x, target_y):
                engine.eat_by_pos(self, target_x, target_y)
            elif engine.can_step(self, vector_x, vector_y):
                engine.step(self, vector_x, vector_y)
            elif (vector_x != 0) or (vector_y != 0):
                dist_counter = self.get_dist()
                jump_flag = False
                while dist_counter > 1:
                    ratio = dist_counter / math.sqrt(vector_x ** 2 + vector_y ** 2)
                    vector_x = math.floor(vector_x * ratio)
                    vector_y = math.floor(vector_y * ratio)
                    if engine.can_jump(self, vector_x, vector_y):
                        jump_flag = True
                        break
                    dist_counter -= 1
                if jump_flag:
                    engine.jump(self, vector_x, vector_y)
                else:
                    self.reset_target()


class Wolf(Animal):
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
        Animal.__init__(self,
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
                        sight,
                        strength,
                        gender)

    def create_descendant(self, start_life: int,
                          start_energy: int,
                          max_life: int,
                          max_energy: int,
                          display: str,
                          x: int, y: int,
                          dist: int,
                          descendant_count_min: int,
                          descendant_count_max: int,
                          speed: int,
                          speed_max: int,
                          can_breed_on_self: bool,
                          sight: int,
                          strength: int,
                          gender: Gender) -> Animal:
        return Wolf(start_life,
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
                    sight,
                    strength,
                    gender)

    def get_name(self) -> str:
        return 'wolf'

    def can_eat(self, obj: EcoObject) -> bool:
        res = isinstance(obj, Animal) and not obj.get_name().__eq__(self.get_name()) and not obj.__eq__(self)
        return res

    def act_on(self, object_list: List[EcoObject], engine: Engine):
        # resetting target
        if (self.is_target_set()) and (self.get_x() == self.get_target_x()) and (
                self.get_y() == self.get_target_y()):
            self.reset_target()

        action_is_possible_flag: bool = True
        # more for testing mb
        if self.is_target_set():
            action_is_possible_flag = False

        # making lists
        acceptable: List[EcoObject] = []
        eaters: List[Animal] = []
        food: List[EcoObject] = []
        # filling lists
        for eo in object_list:
            if eo.__ne__(self):
                if eo.get_name().__eq__(self.get_name()) and eo.can_breed() and engine.can_breed_on_turn(eo) and engine.can_breed_on_turn(self):
                    if isinstance(eo, Animal) and isinstance(self, Animal):
                        if eo.get_gender() != self.get_gender():
                            acceptable.append(eo)
                    else:
                        acceptable.append(eo)
                if isinstance(eo, Animal):
                    tmp = eo
                    if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                        eaters.append(tmp)
                if self.can_eat(eo):
                    if isinstance(eo, Animal):
                        tmp = eo
                        if tmp.get_strength() < self.get_strength():
                            food.append(eo)
                    else:
                        food.append(eo)

        # run sequence
        if len(eaters) > 0 and not isinstance(self, Plant):
            action_is_possible_flag = False
            x_start = self.get_x()
            y_start = self.get_y()
            y_vec_sum = 0
            x_vec_sum = 0
            count = 0
            min_x = engine.get_min_x()
            max_x = engine.get_max_x()
            min_y = engine.get_min_y()
            max_y = engine.get_max_y()
            for ea in eaters:
                tmp_x_v = ea.get_x() - x_start
                tmp_y_v = ea.get_y() - y_start
                count += 1
                x_vec_sum += tmp_x_v
                y_vec_sum += tmp_y_v
            target_x: int = max(min(x_start - self.get_speed_max() * round(x_vec_sum / count), max_x), min_x)
            target_y: int = max(min(y_start - self.get_speed_max() * round(y_vec_sum / count), max_y), min_y)
            # updating target to not be cornered
            hostile_vector_x = round(x_vec_sum / count)
            hostile_vector_y = round(y_vec_sum / count)
            if (x_start == min_x or x_start == max_x) or (y_start == min_y or y_start == max_y) and (target_x == x_start) and (target_y == y_start):
                if abs(hostile_vector_x) > abs(hostile_vector_y):
                    if hostile_vector_y > 0:
                        target_y = max_y
                    else:
                        target_y = min_y
                else:
                    if hostile_vector_x > 0:
                        target_x = max_x
                    else:
                        target_x = min_x
            self.set_target(target_x, target_y)

        #  feed sequence
        if (not self.can_breed() or len(acceptable) == 0) and not self.is_target_set() and len(food) > 0 and not engine.is_well_fed(self):
            action_is_possible_flag = False
            max_food_energy = food[0].get_energy_value()
            max_energy_candidate = food[0]
            min_food_distance = self._dist_sqr(food[0])
            min_distance_candidate = food[0]
            for f in food:
                energy = f.get_energy_value()
                distance = self._dist_sqr(f)
                if energy > max_food_energy:
                    max_food_energy = energy
                    max_energy_candidate = f
                if distance < min_food_distance:
                    min_food_distance = distance
                    min_distance_candidate = f
            candidate: EcoObject = max_energy_candidate

            ratio = self._dist_sqr(max_energy_candidate) / min_food_distance
            if ratio >= 4 or min_food_distance <= 2:
                candidate = min_distance_candidate
            # action selection
            food_distance = self._dist_sqr(candidate)
            if food_distance <= 2:
                engine.eat(self, candidate)
                self.reset_target()
            else:
                target_x = candidate.get_x()
                target_y = candidate.get_y()
                self.set_target(target_x, target_y)

        # breed sequence
        if self.can_breed() and len(acceptable) > 0 and not self.is_target_set():
            action_is_possible_flag = False
            # candidate list
            breed_range = engine.get_breed_range()
            real_candidates: List[EcoObject] = []
            for a in acceptable:
                if (self._dist_sqr(a) <= breed_range ** 2) and (engine.can_breed(self, a)):
                    real_candidates.append(a)
            if len(real_candidates) > 0:
                max_energy = real_candidates[0].get_energy_value()
                candidate = real_candidates[0]
                if isinstance(self, Plant):
                    if len(real_candidates) > 0:
                        for c in real_candidates:
                            if c.get_energy_value() > max_energy:
                                max_energy = c.get_energy_value()
                                candidate = c
                        engine.breed(self, candidate)
                    else:
                        engine.breed(self, self)
                elif isinstance(self, Animal):
                    for c in acceptable:
                        if c.get_energy_value() > max_energy:
                            max_energy = c.get_energy_value()
                            candidate = c
                    if (self._dist_sqr(candidate) <= breed_range ** 2) and (engine.can_breed(self, candidate)):
                        engine.breed(self, candidate)
                    else:
                        self.set_target(candidate.get_x(), candidate.get_y())
            else:
                action_is_possible_flag = True

        # pick random direction just in case there is nothing to do
        if (len(object_list) == 0) or (action_is_possible_flag and not self.is_target_set()):
            x_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
            y_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
            if x_v == 0 and y_v == 0:
                x_v = self.get_dist()
                y_v = - self.get_dist()
            min_x = engine.get_min_x()
            max_x = engine.get_max_x()
            min_y = engine.get_min_y()
            max_y = engine.get_max_y()
            target_x = max(min(self.get_x() + x_v, max_x), min_x)
            target_y = max(min(self.get_y() + y_v, max_y), min_y)
            self.set_target(target_x, target_y)

        # move sequence
        if self.is_target_set():
            # a crutch to fix out of range
            max_x = engine.get_max_x()
            min_x = engine.get_min_x()
            max_y = engine.get_max_y()
            min_y = engine.get_min_y()
            target_x = max(min(self.get_target_x(), max_x), min_x)
            target_y = max(min(self.get_target_y(), max_y), min_y)
            self.set_target(target_x, target_y)
            vector_x = target_x - self.get_x()
            vector_y = target_y - self.get_y()
            if engine.can_jump(self, vector_x, vector_y):
                engine.jump(self, vector_x, vector_y)
                self.reset_target()
            elif engine.can_breed_at_pos(self, target_x, target_y):
                engine.breed_by_pos(self, target_x, target_y)
            elif engine.can_eat_at_pos(self, target_x, target_y):
                engine.eat_by_pos(self, target_x, target_y)
            elif engine.can_step(self, vector_x, vector_y):
                engine.step(self, vector_x, vector_y)
            elif (vector_x != 0) or (vector_y != 0):
                dist_counter = self.get_dist()
                jump_flag = False
                while dist_counter > 1:
                    ratio = dist_counter / math.sqrt(vector_x ** 2 + vector_y ** 2)
                    vector_x = math.floor(vector_x * ratio)
                    vector_y = math.floor(vector_y * ratio)
                    if engine.can_jump(self, vector_x, vector_y):
                        jump_flag = True
                        break
                    dist_counter -= 1
                if jump_flag:
                    engine.jump(self, vector_x, vector_y)
                else:
                    self.reset_target()


class Bear(Animal):
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
        Animal.__init__(self,
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
                        sight,
                        strength,
                        gender)

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
        return Bear(start_life,
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
                    sight,
                    strength,
                    gender)

    def get_name(self) -> str:
        return 'bear'

    def can_eat(self, obj: EcoObject) -> bool:
        res = (not isinstance(obj, Bear)) or (self.get_starving_plank() >= self.get_energy_value() and obj.get_gender() == self.get_gender())
        return res

    def act_on(self, object_list: List[EcoObject], engine: Engine):
        # resetting target
        if (self.is_target_set()) and (self.get_x() == self.get_target_x()) and (
                self.get_y() == self.get_target_y()):
            self.reset_target()

        action_is_possible_flag: bool = True
        # more for testing mb
        if self.is_target_set():
            action_is_possible_flag = False

        # making lists
        acceptable: List[EcoObject] = []
        eaters: List[Animal] = []
        food: List[EcoObject] = []
        # filling lists
        for eo in object_list:
            if eo.__ne__(self):
                if eo.get_name().__eq__(self.get_name()) and eo.can_breed() and engine.can_breed_on_turn(
                        eo) and engine.can_breed_on_turn(self):
                    if isinstance(eo, Animal) and isinstance(self, Animal):
                        if eo.get_gender() != self.get_gender():
                            acceptable.append(eo)
                    else:
                        acceptable.append(eo)
                if isinstance(eo, Animal):
                    tmp = eo
                    if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                        eaters.append(tmp)
                if self.can_eat(eo):
                    if isinstance(eo, Animal):
                        tmp = eo
                        if tmp.get_strength() < self.get_strength():
                            food.append(eo)
                    else:
                        food.append(eo)

        # run sequence
        if len(eaters) > 0 and not isinstance(self, Plant):
            action_is_possible_flag = False
            x_start = self.get_x()
            y_start = self.get_y()
            y_vec_sum = 0
            x_vec_sum = 0
            count = 0
            min_x = engine.get_min_x()
            max_x = engine.get_max_x()
            min_y = engine.get_min_y()
            max_y = engine.get_max_y()
            for ea in eaters:
                tmp_x_v = ea.get_x() - x_start
                tmp_y_v = ea.get_y() - y_start
                count += 1
                x_vec_sum += tmp_x_v
                y_vec_sum += tmp_y_v
            target_x: int = max(min(x_start - self.get_speed_max() * round(x_vec_sum / count), max_x), min_x)
            target_y: int = max(min(y_start - self.get_speed_max() * round(y_vec_sum / count), max_y), min_y)
            # updating target to not be cornered
            hostile_vector_x = round(x_vec_sum / count)
            hostile_vector_y = round(y_vec_sum / count)
            if (x_start == min_x or x_start == max_x) or (y_start == min_y or y_start == max_y) and (
                    target_x == x_start) and (target_y == y_start):
                if abs(hostile_vector_x) > abs(hostile_vector_y):
                    if hostile_vector_y > 0:
                        target_y = max_y
                    else:
                        target_y = min_y
                else:
                    if hostile_vector_x > 0:
                        target_x = max_x
                    else:
                        target_x = min_x
            self.set_target(target_x, target_y)

        #  feed sequence
        if (not self.can_breed() or len(acceptable) == 0) and not self.is_target_set() and len(
                food) > 0 and not engine.is_well_fed(self):
            action_is_possible_flag = False
            max_food_energy = food[0].get_energy_value()
            max_energy_candidate = food[0]
            min_food_distance = self._dist_sqr(food[0])
            min_distance_candidate = food[0]
            for f in food:
                energy = f.get_energy_value()
                distance = self._dist_sqr(f)
                if energy > max_food_energy:
                    max_food_energy = energy
                    max_energy_candidate = f
                if distance < min_food_distance:
                    min_food_distance = distance
                    min_distance_candidate = f
            candidate: EcoObject = max_energy_candidate

            ratio = self._dist_sqr(max_energy_candidate) / min_food_distance
            if ratio >= 4 or min_food_distance <= 2:
                candidate = min_distance_candidate
            # action selection
            food_distance = self._dist_sqr(candidate)
            if food_distance <= 2:
                engine.eat(self, candidate)
                self.reset_target()
            else:
                target_x = candidate.get_x()
                target_y = candidate.get_y()
                self.set_target(target_x, target_y)

        # breed sequence
        if self.can_breed() and len(acceptable) > 0 and not self.is_target_set():
            action_is_possible_flag = False
            # candidate list
            breed_range = engine.get_breed_range()
            real_candidates: List[EcoObject] = []
            for a in acceptable:
                if (self._dist_sqr(a) <= breed_range ** 2) and (engine.can_breed(self, a)):
                    real_candidates.append(a)
            if len(real_candidates) > 0:
                max_energy = real_candidates[0].get_energy_value()
                candidate = real_candidates[0]
                if isinstance(self, Plant):
                    if len(real_candidates) > 0:
                        for c in real_candidates:
                            if c.get_energy_value() > max_energy:
                                max_energy = c.get_energy_value()
                                candidate = c
                        engine.breed(self, candidate)
                    else:
                        engine.breed(self, self)
                elif isinstance(self, Animal):
                    for c in acceptable:
                        if c.get_energy_value() > max_energy:
                            max_energy = c.get_energy_value()
                            candidate = c
                    if (self._dist_sqr(candidate) <= breed_range ** 2) and (engine.can_breed(self, candidate)):
                        engine.breed(self, candidate)
                    else:
                        self.set_target(candidate.get_x(), candidate.get_y())
            else:
                action_is_possible_flag = True

        # pick random direction just in case there is nothing to do
        if (len(object_list) == 0) or (action_is_possible_flag and not self.is_target_set()):
            x_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
            y_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
            if x_v == 0 and y_v == 0:
                x_v = self.get_dist()
                y_v = - self.get_dist()
            min_x = engine.get_min_x()
            max_x = engine.get_max_x()
            min_y = engine.get_min_y()
            max_y = engine.get_max_y()
            target_x = max(min(self.get_x() + x_v, max_x), min_x)
            target_y = max(min(self.get_y() + y_v, max_y), min_y)
            self.set_target(target_x, target_y)

        # move sequence
        if self.is_target_set():
            # a crutch to fix out of range
            max_x = engine.get_max_x()
            min_x = engine.get_min_x()
            max_y = engine.get_max_y()
            min_y = engine.get_min_y()
            target_x = max(min(self.get_target_x(), max_x), min_x)
            target_y = max(min(self.get_target_y(), max_y), min_y)
            self.set_target(target_x, target_y)
            vector_x = target_x - self.get_x()
            vector_y = target_y - self.get_y()
            if engine.can_jump(self, vector_x, vector_y):
                engine.jump(self, vector_x, vector_y)
                self.reset_target()
            elif engine.can_breed_at_pos(self, target_x, target_y):
                engine.breed_by_pos(self, target_x, target_y)
            elif engine.can_eat_at_pos(self, target_x, target_y):
                engine.eat_by_pos(self, target_x, target_y)
            elif engine.can_step(self, vector_x, vector_y):
                engine.step(self, vector_x, vector_y)
            elif (vector_x != 0) or (vector_y != 0):
                dist_counter = self.get_dist()
                jump_flag = False
                while dist_counter > 1:
                    ratio = dist_counter / math.sqrt(vector_x ** 2 + vector_y ** 2)
                    vector_x = math.floor(vector_x * ratio)
                    vector_y = math.floor(vector_y * ratio)
                    if engine.can_jump(self, vector_x, vector_y):
                        jump_flag = True
                        break
                    dist_counter -= 1
                if jump_flag:
                    engine.jump(self, vector_x, vector_y)
                else:
                    self.reset_target()
