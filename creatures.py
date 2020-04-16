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
        return Grass(self,
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
                if eo.__ne__(self) and eo.get_name().__eq__(self.get_name()) and eo.can_breed():
                    acceptable.append(eo)
            breed_range = engine.get_breed_range()
            real_candidates: List[EcoObject] = []
            for a in acceptable:
                if (self._dist_sqr(a) <= breed_range ** 2) and (engine.can_breed(self, a)):
                    real_candidates.append(a)
            if self is Plant:
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
        else:
            self.alter_speed(-1)


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
        self._target_x = -1
        self._target_y = -1

    def is_target_set(self) -> bool:
        return self._target_x >= 0 and self._target_y >= 0

    def reset_target(self):
        self.set_target_x(-1)
        self.set_target_y(-1)

    def get_target_x(self) -> int:
        return self._target_x

    def get_target_y(self) -> int:
        return self._target_y

    def set_target_x(self, val: int) -> NoReturn:
        self._target_x = val

    def set_target_y(self, val: int) -> NoReturn:
        self._target_y = val

    def set_target(self, x: int, y: int) -> NoReturn:
        self.set_target_x(x)
        self.set_target_y(y)

    def _dist_sqr(self, obj: EcoObject) -> int:
        return (self.get_x() - obj.get_x())**2 + (self.get_y() - self.get_y())**2

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
        return obj is Plant

    def act_on(self, object_list: List[EcoObject], engine: Engine):
        # reseting target
        if (self.is_target_set()) and (self.get_x() == self.get_target_x()) and (self.get_y() == self.get_target_y()):
            self.reset_target()
        if len(object_list) == 0:
            x_v = self.get_speed_max()*random.randint(-self.get_dist(), self.get_dist())
            y_v = self.get_speed_max()*random.randint(-self.get_dist(), self.get_dist())
            if x_v == 0 and y_v ==0:
                x_v = self.get_dist()
                y_v = - self.get_dist()
            self.set_target(x_v, y_v)

        # making lists
        acceptable: List[EcoObject] = []
        eaters: List[Animal] = []
        food: List[EcoObject] = []
        # filling lists
        for eo in object_list:
            if eo.__ne__(self) and eo.get_name().__eq__(self.get_name()) and eo.can_breed():
                acceptable.append(eo)
            if eo is Animal:
                tmp = (Animal)(eo)
                if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                    eaters.append(tmp)
            if self.can_eat(eo):
                if eo is Animal:
                    tmp = (Animal)(eo)
                    if tmp.get_strength() < self.get_strength():
                        food.append(eo)
                else:
                    food.append(eo)
        for eater in object_list:
            if eater is Animal:
                tmp = (Animal)(eater)
                if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                    eaters.append(tmp)

        # run sequence
        if len(eaters) > 0 and self is not Plant:
            x_start = self.get_x()
            y_start = self.get_y()
            y_vec_sum = 0
            x_vec_sum = 0
            count = 0
            for ea in eaters:
                tmp_x_v = ea.get_x() - x_start
                tmp_y_v = ea.get_y() - y_start
                count += 1
                x_vec_sum += tmp_x_v
                y_vec_sum += tmp_y_v
            target_x: int = round(x_vec_sum/count)
            target_y: int = round(y_vec_sum/count)
            self.set_target(target_x, target_y)
        #  feed sequence
        if not self.can_breed() and not self.is_target_set() and len(food) > 0:
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
            ratio = self._dist_sqr(max_energy_candidate)/min_food_distance
            if ratio >= 4:
                candidate = min_distance_candidate
            # action selection
            target_x = candidate.get_x()
            target_y = candidate.get_y()
            self.set_target(target_x, target_y)

        # breed sequence
        if self.can_breed() and not self.is_target_set():
            # candidate list
            breed_range = engine.get_breed_range()
            real_candidates: List[EcoObject] = []
            for a in acceptable:
                if (self._dist_sqr(a) <= breed_range ** 2) and (engine.can_breed(self, a)):
                    real_candidates.append(a)
            if self is Plant:
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
            elif self is Animal:
                max_energy = acceptable[0].get_energy_value()
                candidate = acceptable[0]
                for c in acceptable:
                    if c.get_energy_value() > max_energy:
                        max_energy = c.get_energy_value()
                        candidate = c
                if (self._dist_sqr(candidate) <= breed_range ** 2) and (engine.can_breed(self, candidate)):
                    engine.breed(self, candidate)
                else:
                    self.set_target(candidate.get_x(), candidate.get_y())

        # move sequence
        if self.is_target_set():
            target_x = self.get_target_x()
            target_y = self.get_target_y()
            vector_x = target_x - self.get_x()
            vector_y = target_y - self.get_y()
            if engine.can_jump(self, target_x, target_y):
                engine.jump(self, target_x, target_y)
                self.reset_target()
            elif engine.can_step(self, vector_x, vector_y):
                engine.step(self, vector_x, vector_y)
            else:
                ratio = self.get_dist()/math.sqrt(vector_x**2 + vector_y**2)
                vector_x = math.floor(vector_x*ratio)
                vector_y = math.floor(vector_y*ratio)
                engine.jump(self, vector_x, vector_y)


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

        def get_name(self) -> str:
            return 'wolf'

        def can_eat(self, obj: EcoObject) -> bool:
            return obj is Animal and not obj.get_name().__eq__(self.get_name)

        def act_on(self, object_list: List[EcoObject], engine: Engine):
            # reseting target
            if (self.is_target_set()) and (self.get_x() == self.get_target_x()) and (
                    self.get_y() == self.get_target_y()):
                self.reset_target()
            if len(object_list) == 0:
                x_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
                y_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
                self.set_target(x_v, y_v)
            # making lists
            acceptable: List[EcoObject] = []
            eaters: List[Animal] = []
            food: List[EcoObject] = []
            # filling lists
            for eo in object_list:
                if eo.__ne__(self) and eo.get_name().__eq__(self.get_name()) and eo.can_breed():
                    acceptable.append(eo)
                if eo is Animal:
                    tmp = (Animal)(eo)
                    if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                        eaters.append(tmp)
                if self.can_eat(eo):
                    if eo is Animal:
                        tmp = (Animal)(eo)
                        if tmp.get_strength() < self.get_strength():
                            food.append(eo)
                    else:
                        food.append(eo)
            for eater in object_list:
                if eater is Animal:
                    tmp = (Animal)(eater)
                    if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                        eaters.append(tmp)

            # run sequence
            if len(eaters) > 0 and self is not Plant:
                x_start = self.get_x()
                y_start = self.get_y()
                y_vec_sum = 0
                x_vec_sum = 0
                count = 0
                for ea in eaters:
                    tmp_x_v = ea.get_x() - x_start
                    tmp_y_v = ea.get_y() - y_start
                    count += 1
                    x_vec_sum += tmp_x_v
                    y_vec_sum += tmp_y_v
                target_x: int = round(x_vec_sum / count)
                target_y: int = round(y_vec_sum / count)
                self.set_target(target_x, target_y)
            #  feed sequence
            if not self.can_breed() and not self.is_target_set() and len(food) > 0:
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
                if ratio >= 4:
                    candidate = min_distance_candidate
                # action selection
                target_x = candidate.get_x()
                target_y = candidate.get_y()
                self.set_target(target_x, target_y)

            # breed sequence
            if self.can_breed() and not self.is_target_set():
                # candidate list
                breed_range = engine.get_breed_range()
                real_candidates: List[EcoObject] = []
                for a in acceptable:
                    if (self._dist_sqr(a) <= breed_range ** 2) and (engine.can_breed(self, a)):
                        real_candidates.append(a)
                if self is Plant:
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
                elif self is Animal:
                    max_energy = acceptable[0].get_energy_value()
                    candidate = acceptable[0]
                    for c in acceptable:
                        if c.get_energy_value() > max_energy:
                            max_energy = c.get_energy_value()
                            candidate = c
                    if (self._dist_sqr(candidate) <= breed_range ** 2) and (engine.can_breed(self, candidate)):
                        engine.breed(self, candidate)
                    else:
                        self.set_target(candidate.get_x(), candidate.get_y())

            # move sequence
            if self.is_target_set():
                target_x = self.get_target_x()
                target_y = self.get_target_y()
                vector_x = target_x - self.get_x()
                vector_y = target_y - self.get_y()
                if engine.can_jump(self, target_x, target_y):
                    engine.jump(self, target_x, target_y)
                    self.reset_target()
                elif engine.can_step(self, vector_x, vector_y):
                    engine.step(self, vector_x, vector_y)
                else:
                    ratio = self.get_dist() / math.sqrt(vector_x ** 2 + vector_y ** 2)
                    vector_x = math.floor(vector_x * ratio)
                    vector_y = math.floor(vector_y * ratio)
                    engine.jump(self, vector_x, vector_y)


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
            pass

        def get_name(self) -> str:
            return 'bear'

        def can_eat(self, obj: EcoObject) -> bool:
            return not obj.get_name().__eq__(self.get_name)

        def act_on(self, object_list: List[EcoObject], engine: Engine):
            # reseting target
            if (self.is_target_set()) and (self.get_x() == self.get_target_x()) and (
                    self.get_y() == self.get_target_y()):
                self.reset_target()
            if len(object_list) == 0:
                x_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
                y_v = self.get_speed_max() * random.randint(-self.get_dist(), self.get_dist())
                self.set_target(x_v, y_v)
            # making lists
            acceptable: List[EcoObject] = []
            eaters: List[Animal] = []
            food: List[EcoObject] = []
            # filling lists
            for eo in object_list:
                if eo.__ne__(self) and eo.get_name().__eq__(self.get_name()) and eo.can_breed():
                    acceptable.append(eo)
                if eo is Animal:
                    tmp = (Animal)(eo)
                    if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                        eaters.append(tmp)
                if self.can_eat(eo):
                    if eo is Animal:
                        tmp = (Animal)(eo)
                        if tmp.get_strength() < self.get_strength():
                            food.append(eo)
                    else:
                        food.append(eo)
            for eater in object_list:
                if eater is Animal:
                    tmp = (Animal)(eater)
                    if (tmp.can_eat(self)) and (self.get_strength() < tmp.get_strength()):
                        eaters.append(tmp)

            # run sequence
            if len(eaters) > 0 and self is not Plant:
                x_start = self.get_x()
                y_start = self.get_y()
                y_vec_sum = 0
                x_vec_sum = 0
                count = 0
                for ea in eaters:
                    tmp_x_v = ea.get_x() - x_start
                    tmp_y_v = ea.get_y() - y_start
                    count += 1
                    x_vec_sum += tmp_x_v
                    y_vec_sum += tmp_y_v
                target_x: int = round(x_vec_sum / count)
                target_y: int = round(y_vec_sum / count)
                self.set_target(target_x, target_y)
            #  feed sequence
            if not self.can_breed() and not self.is_target_set() and len(food) > 0:
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
                if ratio >= 4:
                    candidate = min_distance_candidate
                # action selection
                target_x = candidate.get_x()
                target_y = candidate.get_y()
                self.set_target(target_x, target_y)

            # breed sequence
            if self.can_breed() and not self.is_target_set():
                # candidate list
                breed_range = engine.get_breed_range()
                real_candidates: List[EcoObject] = []
                for a in acceptable:
                    if (self._dist_sqr(a) <= breed_range ** 2) and (engine.can_breed(self, a)):
                        real_candidates.append(a)
                if self is Plant:
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
                elif self is Animal:
                    max_energy = acceptable[0].get_energy_value()
                    candidate = acceptable[0]
                    for c in acceptable:
                        if c.get_energy_value() > max_energy:
                            max_energy = c.get_energy_value()
                            candidate = c
                    if (self._dist_sqr(candidate) <= breed_range ** 2) and (engine.can_breed(self, candidate)):
                        engine.breed(self, candidate)
                    else:
                        self.set_target(candidate.get_x(), candidate.get_y())

            # move sequence
            if self.is_target_set():
                target_x = self.get_target_x()
                target_y = self.get_target_y()
                vector_x = target_x - self.get_x()
                vector_y = target_y - self.get_y()
                if engine.can_jump(self, target_x, target_y):
                    engine.jump(self, target_x, target_y)
                    self.reset_target()
                elif engine.can_step(self, vector_x, vector_y):
                    engine.step(self, vector_x, vector_y)
                else:
                    ratio = self.get_dist() / math.sqrt(vector_x ** 2 + vector_y ** 2)
                    vector_x = math.floor(vector_x * ratio)
                    vector_y = math.floor(vector_y * ratio)
                    engine.jump(self, vector_x, vector_y)
