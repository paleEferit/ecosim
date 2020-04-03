from __future__ import annotations
from ecosim_entities import *
from graphics import *


class GraphicPrintUI(UIDisplay):
    def __init__(self, eco_map: EcoMap, width: int, height: int, name: str, empty_sign: str):
        UIDisplay.__init__(self, eco_map)
        if (width < 1) or (height < 1):
            raise ValueError('size mishap')
        if (width // eco_map.get_width() == 0) or (height // eco_map.get_height()):
            raise ValueError('element mishap')
        if len(empty_sign)==0:
            raise ValueError('empty value mismatch')
        self._sub_width = width // eco_map.get_width()
        self._sub_height = height // eco_map.get_height()
        self._width = width
        self._height = height
        self._name = name
        self._empty_symbol = empty_sign
        self._win = GraphWin(self.get_name(), self.get_width(), self.get_height())
        self._obj_list: List[GraphicsObject] = []

    def _get_empty_symbol(self) -> str:
        return self._empty_symbol

    def _get_window(self) -> GraphWin:
        return self._win

    def get_name(self) -> str:
        return self._name

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def _get_sub_height(self) -> int:
        return self._sub_height

    def _get_sub_width(self) -> int:
        return self._sub_width

    def _add_element(self, elem: GraphicsObject) -> NoReturn:
        self._obj_list.append(elem)
        the_win = self._get_window()
        elem.draw(the_win)

    def _remove_element(self, elem: GraphicsObject) -> NoReturn:
        the_win = self._get_window()
        the_win.delItem(elem)
        self._obj_list.remove(elem)

    def _create_symbol(self, data: str, x: int, y: int) -> NoReturn:
        label = Text(Point(x, y), data)
        self._add_element(label)

    def _clear_all(self) -> NoReturn:
        the_win = self._get_window()
        for lbl in self._obj_list:
            the_win.delItem(lbl)
        self._obj_list.clear()

    def display(self) -> NoReturn:
        the_map = self.get_eco_map()
        w = the_map.get_width()
        h = the_map.get_height()
        for i in range(h):
            for j in range(w):
                x_pos = j * self._get_sub_width()
                y_pos = i * self._get_sub_height()
                if the_map.has_object_at(j, i):
                    self._create_symbol(self._get_empty_symbol(), x_pos, y_pos)
                else:
                    tmp_obj = the_map.get_obj_by_pos(x_pos, y_pos)
                    self._create_symbol(tmp_obj.get_display(), x_pos, y_pos)

    def update_display(self) -> NoReturn:
        self._clear_all()
        self.display()

    def init(self) -> NoReturn:
        print('init is not implemented yet')
