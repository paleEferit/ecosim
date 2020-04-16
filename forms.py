import tkinter as tk
from typing import *
from ecosim_entities import UIDisplay
from ecosim_entities import Engine


class VisualApp(tk.Frame):
    def __init__(self, engine: Engine, ui_dis: UIDisplay, canvas_width: int, canvas_height: int, master=None):
        # basic stuff
        super().__init__(master)
        self.master = master
        self.pack()
        # setting fields
        self._ui_display = ui_dis
        self._engine = engine
        self._canvas_width = canvas_width
        self._canvas_height = canvas_height
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

        # quit button
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

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
        self._ui_display.update_display()

    def clear_graphics(self):
        self._ui_display.clear_all()

    def turn_engine(self):
        self._engine.full_turn()

    def sub_turn_engine(self):
        self._engine.sub_turn()

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
