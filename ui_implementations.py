from __future__ import annotations
from ecosim_entities import *
import tkinter as tk
from typing import Tuple


class GraphicPrintUI(UIDisplay):
    def __init__(self, eco_map: EcoMap, width: int, height: int, canvas: tk.Canvas,
                 bg_color: Tuple[int, int, int], fg_color: Tuple[int, int, int]):
        UIDisplay.__init__(self, eco_map)
        if not GraphicPrintUI._check_color(bg_color):
            raise ValueError('bg color out of bounds')
        if not GraphicPrintUI._check_color(fg_color):
            raise ValueError('fg color out of bounds')
        if (width < 1) or (height < 1):
            raise ValueError('size mishap')
        if ((width // eco_map.get_width()) == 0) or ((height // eco_map.get_height()) == 0):
            raise ValueError('element mishap')
        self._sub_width = width // eco_map.get_width()
        self._sub_height = height // eco_map.get_height()
        self._width = width
        self._height = height
        self._canvas = canvas
        self._bg_color = bg_color
        self._fg_color = fg_color
        self.clear_all()

    @staticmethod
    def _check_color(color: Tuple[int, int, int]) -> bool:
        return (color[0] >= 0) and (color[0] <= 255) and (color[1] >= 0) and (color[1] <= 255) and (color[2] >= 0) and (color[2] <= 255)

    def _get_canvas(self) -> tk.Canvas:
        return self._canvas

    def _get_bg(self) -> Tuple[int, int, int]:
        return self._bg_color

    def _get_fg(self) -> Tuple[int, int, int]:
        return self._fg_color

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def _get_sub_height(self) -> int:
        return self._sub_height

    def _get_sub_width(self) -> int:
        return self._sub_width

    def _create_symbol(self, data: str, x_cell: int, y_cell: int, r: int, g: int, b: int) -> NoReturn:
        if not GraphicPrintUI._check_color((r, g, b)):
            raise ValueError('inconsistent color')
        tmp_cnv = self._get_canvas()
        fill_color = '#%02x%02x%02x' % (r, g, b)
        x_pos = round((x_cell + 0.3)*self._get_sub_width())
        y_pos = round((y_cell + 0.5)*self._get_sub_width())
        tmp_cnv.create_text(x_pos, y_pos, anchor=tk.W, font=("Purisa", self._get_sub_height()), text=data, fill=fill_color)

    def clear_all(self) -> NoReturn:
        tmp_cnv = self._get_canvas()
        bgc = '#%02x%02x%02x' % self._bg_color
        fgc = '#%02x%02x%02x' % self._fg_color
        tmp_cnv.create_rectangle(0, 0, self.get_width(), self.get_height(), outline=bgc, fill=bgc, width=2)
        w = self.get_width() // self._get_sub_width()
        h = self.get_height() // self._get_sub_height()
        max_x = self.get_width()
        max_y = self.get_height()
        x_step = self._get_sub_width()
        y_step = self._get_sub_height()
        for i in range(h):
            tmp_cnv.create_line(0, i*y_step, max_x, i*y_step)
        for j in range(w):
            tmp_cnv.create_line(j*x_step, 0, j*x_step, max_y)

    def display(self) -> NoReturn:
        the_map = self.get_eco_map()
        w = the_map.get_width()
        h = the_map.get_height()
        for i in range(h):
            for j in range(w):
                x_pos = j * self._get_sub_width()
                y_pos = i * self._get_sub_height()
                r = 0
                g = 0
                b = 0
                if the_map.has_object_at(j, i):
                    tmp_obj = the_map.get_obj_by_pos(j, i)
                    if isinstance(tmp_obj, Animal):
                        r = 255
                    if isinstance(tmp_obj, Plant):
                        g = 255
                    self._create_symbol(tmp_obj.get_display(), j, i, r, g, b)
                else:
                    self._create_symbol(the_map.get_empty_display(), j, i, r, g, b)

    def update_display(self) -> NoReturn:
        self.clear_all()
        self.display()

    def init(self) -> NoReturn:
        print('init is not implemented yet')


