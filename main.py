from ecosim_entities import *
from ui_implementations import *
from creatures import *

# start creating objects
delay = 1

width = 50
height = 50
grass_count = 10
rabbit_count = 10
wolf_count = 10
bear_count = 10

grass_x = width//2
grass_y = height//2
rabbit_x = width - width//10
rabbit_y = height - height//8
wolf_x = width//8
wolf_y = height - height//10
bear_x = width//10
bear_y = height//10
print('Initializing...')
grass: List[EcoObject] = []
rabbits: List[EcoObject] = []
wolfs: List[EcoObject] = []
bears: List[EcoObject] = []
for i in range(grass_count):
    grass.append(Grass(40, 40, 40, 40, 'g', 0, 0, 1, 1, 3, 1, 1, True, 10))
for i in range(rabbit_count):
    gender = Gender.FEMALE
    if i % 2 == 0:
        gender = Gender.MALE
    rabbits.append(Rabbit(70, 70, 70, 70, 'r', 1, 1, 5, 1, 4, 4, 4, False, 10, 2, gender))
for i in range(wolf_count):
    gender = Gender.FEMALE
    if i % 2 == 0:
        gender = Gender.MALE
    wolfs.append(Wolf(90, 90, 90, 90, 'w', 1, 1, 7, 1, 2, 5, 5, False, 12, 5, gender))
for i in range(bear_count):
    gender = Gender.FEMALE
    if i % 2 == 0:
        gender = Gender.MALE
    bears.append(Bear(100, 100, 100, 100, 'b', 2, 2, 3, 1, 3, 5, 5, False, 8, 10, gender))
print('Eco entities ready...')

the_map: EcoMap = EcoMap(width, height, [], -1, '.', None)
the_map.add_multiple_objects_around(grass_x, grass_y, grass)
the_map.add_multiple_objects_around(rabbit_x, rabbit_y, rabbits)
the_map.add_multiple_objects_around(wolf_x, wolf_y, wolfs)
the_map.add_multiple_objects_around(bear_x, bear_y, bears)
print('Map is ready...')
ui_module: UIDisplay = GraphicPrintUI(the_map, 800, 600, 'Ecology simulator', '.')
print('UI is ready...')
print('Starting UI...')
ui_module.display()
print('Creating engine...')
engine: Engine = Engine(the_map)
print('Engine is ready...')
print('Starting engine...')
while True:
    engine.full_turn()
    ui_module.update_display()
    time.sleep(delay)
