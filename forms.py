import tkinter as tk
from typing import *
from ecosim_entities import UIDisplay
from ecosim_entities import Engine
# threading stuff
from threading import RLock
from threading import Lock
from threading import Thread
from threading import Event


class VisualApp(tk.Frame):
    def __init__(self, engine: Engine, ui_dis: UIDisplay, canvas_width: int, canvas_height: int, fps: int, aps: int, master=None):
        # basic stuff
        super().__init__(master)
        self.master = master
        self.pack()
        # setting fields
        self._ui_display = ui_dis
        self._engine = engine
        self._canvas_width = canvas_width
        self._canvas_height = canvas_height
        self._loop_map_lock = RLock()
        self._loop_stop_event = Event()
        self._loop_flag = False
        self._manual_flag = False
        self._draw_period = 1.0/fps
        self._action_period = 1.0/aps
        self._loop_thread: Thread = None
        # canvas

        self._blank = VisualApp.get_blank_image(width=self._canvas_width, height=self._canvas_height, r=255, g=255, b=0)
        self._my_canvas = tk.Canvas(self.master, width=self._canvas_width, height=self._canvas_height)
        self._my_canvas.pack(side="top")
        self._my_canvas.create_image(0, 0, image=self._blank, anchor=tk.NW)

        # button update graphics
        self.btn_graphics_update = tk.Button(self)
        self.btn_graphics_update["text"] = "Update graphics"
        self.btn_graphics_update["command"] = self.update_graphics
        self.btn_graphics_update.pack(side="top")

        # button clear graphics
        self.btn_graphics_clear = tk.Button(self)
        self.btn_graphics_clear["text"] = "Clear canvas"
        self.btn_graphics_clear["command"] = self.clear_graphics
        self.btn_graphics_clear.pack(side="top")

        # button full turn
        self.btn_turn_full = tk.Button(self)
        self.btn_turn_full["text"] = "Full turn"
        self.btn_turn_full["command"] = self.turn_engine
        self.btn_turn_full.pack(side="top")

        # button subturn
        self.btn_subturn_full = tk.Button(self)
        self.btn_subturn_full["text"] = "Sub turn"
        self.btn_subturn_full["command"] = self.sub_turn_engine
        self.btn_subturn_full.pack(side="top")

        # --- auto loops

        # button start loops
        self.btn_start_loops = tk.Button(self)
        self.btn_start_loops["text"] = "Start loops"
        self.btn_start_loops["command"] = self.start_auto_loops
        self.btn_start_loops.pack(side="top")

        # button stop loops
        self.btn_stop_loops = tk.Button(self)
        self.btn_stop_loops["text"] = "Stop loops"
        self.btn_stop_loops["command"] = self.stop_auto_loops
        self.btn_stop_loops.pack(side="top")

        # ==quit button
        self.btn_quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.btn_quit.pack(side="bottom")

        # setting buttons
        self.set_stop_loops_button_state(self.get_loop_flag())

    def get_draw_period(self) -> float:
        return self._draw_period

    def get_action_period(self) -> float:
        return self._action_period

    def get_loop_flag(self) -> bool:
        return self._loop_flag

    def set_loop_flag(self, value: bool) -> NoReturn:
        self.set_manual_buttons_state(not value)
        self.set_start_loops_button_state(not value)
        self.set_stop_loops_button_state(value)
        self._loop_flag = value

    def get_manual_flag(self) -> bool:
        return self._manual_flag

    def set_manual_flag(self, value: bool) -> NoReturn:
        self.set_start_loops_button_state(not value)
        self._manual_flag = value

    def set_manual_buttons_state(self, flag: bool) -> NoReturn:
        if flag:
            self.btn_graphics_clear.configure(state=tk.NORMAL)
            self.btn_graphics_update.configure(state=tk.NORMAL)
            self.btn_subturn_full.configure(state=tk.NORMAL)
            self.btn_turn_full.configure(state=tk.NORMAL)
        else:
            self.btn_graphics_clear.configure(state=tk.DISABLED)
            self.btn_graphics_update.configure(state=tk.DISABLED)
            self.btn_subturn_full.configure(state=tk.DISABLED)
            self.btn_turn_full.configure(state=tk.DISABLED)

    def set_start_loops_button_state(self, flag: bool) -> NoReturn:
        if flag:
            self.btn_start_loops.configure(state=tk.NORMAL)
        else:
            self.btn_start_loops.configure(state=tk.DISABLED)

    def set_stop_loops_button_state(self, flag: bool) -> NoReturn:
        if flag:
            self.btn_stop_loops.configure(state=tk.NORMAL)
        else:
            self.btn_stop_loops.configure(state=tk.DISABLED)

    def start_auto_loops(self) -> NoReturn:
        my_thread = Thread(target=self.start_loops_function)
        my_thread.start()

    def stop_auto_loops(self) -> NoReturn:
        self.raise_stop_loop_event()

    def draw_loop(self, r_lock: RLock, stop_event: Event, draw_period: float) -> NoReturn:
        while not stop_event.wait(draw_period):
            r_lock.acquire()
            self._ui_display.update_display()
            # debug
            # print('-graphics')
            r_lock.release()

    def engine_loop(self, r_lock: RLock, stop_event: Event, act_period: float) -> NoReturn:
        the_engine = self.get_engine()
        while not stop_event.wait(act_period):
            r_lock.acquire()
            tmp_val = the_engine.sub_turn()
            the_engine.clear_acted_list()
            if tmp_val <= 0:
                the_engine.update()
            # debug
            # print('-engine')
            r_lock.release()

    def start_loops_function(self):
        self.set_loop_flag(True)
        threads: List[Thread] = []
        threads.append(
            Thread(target=self.draw_loop, args=[self._loop_map_lock, self._loop_stop_event, self.get_draw_period()]))
        threads.append(
            Thread(target=self.engine_loop, args=[self._loop_map_lock, self._loop_stop_event, self.get_action_period()]))
        threads[0].start()
        threads[1].start()
        for t in threads:
            t.join()
        self.set_loop_flag(False)
        self._loop_stop_event.clear()

    def raise_stop_loop_event(self):
        self._loop_stop_event.set()

    def get_sp_canvas(self) -> tk.Canvas:
        return self._my_canvas

    def get_engine(self) -> Engine:
        return self._engine

    def set_engine(self, val: Engine) -> NoReturn:
        self._engine = val

    def get_ui(self) -> UIDisplay:
        return self._ui_display

    def set_ui(self, val: UIDisplay) -> NoReturn:
        self._ui_display = val

    def update_graphics(self):
        self.set_manual_flag(True)
        self._ui_display.update_display()
        self.set_manual_flag(False)

    def clear_graphics(self):
        self.set_manual_flag(True)
        self._ui_display.clear_all()
        self.set_manual_flag(False)

    def turn_engine(self):
        self.set_manual_flag(True)
        self._engine.full_turn()
        self.set_manual_flag(False)

    def sub_turn_engine(self):
        self.set_manual_flag(True)
        self._engine.sub_turn()
        self._engine.clear_acted_list()
        self.set_manual_flag(False)

    @staticmethod
    def get_blank_image(width: int, height: int, r: int, g: int, b: int) -> tk.PhotoImage:
        if (width <= 0) or (height <= 0):
            raise ValueError('inconsistent size')
        if (r < 0) or (r > 255):
            raise ValueError('inconsistent red')
        if (g < 0) or (g > 255):
            raise ValueError('inconsistent green')
        if (b < 0) or (b > 255):
            raise ValueError('inconsistent blue')

        tmp_img = tk.PhotoImage(width=width, height=height)
        for row in range(height):
            for column in range(width):
                tmp_img.put('#%02x%02x%02x' % (r, g, b), (row, column))
        return tmp_img
