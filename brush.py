from tools import Tool, PencilTool
from turtle import _Screen, Turtle
from typing import Any

class Brush():
    width: int = 3
    color: int = 0
    tool: Tool = PencilTool()

    screen: _Screen
    t: Turtle
    loading: Turtle

    draw_data: list[list[Any]] = [[(0, 0), 0, 0]]

    # used for undo
    # 0 -> turtle undo
    # 1 -> draw data undo
    buffer: list[tuple[int, int]] = [(0, 0)]

    # out of bounds check
    def oob(self, x: float, y: float) -> bool:
        if -self.screen.window_width() // 2 + 110 < x < self.screen.window_width() // 2 - 20 and -self.screen.window_height() // 2 + 20 < y < self.screen.window_height() // 2 - 50:
            return False
        return True