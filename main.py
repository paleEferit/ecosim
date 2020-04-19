from ecosim_entities import *
from ui_implementations import *
from creatures import *
from forms import *
import time

# start creating objects
delay = 1

width = 40
height = 30
grass_count = 1
rabbit_count = 1
wolf_count = 1
bear_count = 1
grass_spread = 2
rabbit_spread = 2
wolf_spread = 2
bear_spread = 2
resolution_width = 800
resolution_height = 600

grass_x = width//2
grass_y = height//2
rabbit_x = width//2+1
rabbit_y = height//2+1
wolf_x = width//2-1
wolf_y = height//2-1
bear_x = width//2-1
bear_y = height//2+1
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
the_map.add_multiple_objects_around(grass_x, grass_y, grass_spread, grass)
the_map.add_multiple_objects_around(rabbit_x, rabbit_y, rabbit_spread, rabbits)
the_map.add_multiple_objects_around(wolf_x, wolf_y, wolf_spread, wolfs)
the_map.add_multiple_objects_around(bear_x, bear_y, bear_spread, bears)
print('Map is ready...')
print('Initing UI...')
root = tk.Tk()
app = VisualApp(engine=None, ui_dis=None, canvas_width=resolution_width, canvas_height=resolution_height, master=root)
ui_module: UIDisplay = GraphicPrintUI(the_map, resolution_width, resolution_height, app.get_sp_canvas(),
                                      (255, 255, 255),
                                      (0, 0, 0))
print('UI is ready...')
print('Starting UI...')
ui_module.display()
print('Creating engine...')
engine: Engine = Engine(the_map)
print('Engine is ready...')
print('Starting app...')
for i in range(10, 0, -1):
    print("Waiting %i" % i)
    time.sleep(1)

# main loop
app.set_ui(ui_module)
app.set_engine(engine)
app.mainloop()

