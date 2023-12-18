from turtle import Screen, Turtle
from buttons import *
from enum import Enum
from tools import *

colors: [str] = ["#000000", "#7a7a7a", "#7a0000", "#7a7a00", "#007a00", "#007a7a", "#00007a", "#7a007a", "#797a38", "#003937", "#007aff", "#013879", "#3800ff", "#793802", "#fefefe", "#bcbcbc", "#fe0000", "#fefe00", "#00fe00", "#00fefe", "#0000fe", "#fe00fe", "#fefe7a", "#00fe7a", "#7afffe", "#7a7afe", "#fe007a", "#fe7a39"]

alpha_fill: (str, str) = ("#b0b0b0", "#e9e9e9")

# colors
outline: (float, float, float) = (18 / 255, 18 / 255, 18 / 255)
glossy: str = "#f8f8f8"
shadow: (float, float, float) = (127 / 255, 127 / 255, 127 / 255)
btn_fill: str = "#bcbcbc"

# button list
buttons: [UiButton] = [UiButton(), UiButton(), UiButton(), UiButton(), UiButton(), UiButton()]

class ToolList(Enum):
    PENCIL = 0
    ERASER = 1
    LINE = 2
    RECTANGLE = 3
    CIRCLE = 4
    TEST = 5

    def get_tool(self):
        match self:
            case ToolList.PENCIL:
                return PencilTool()
            case ToolList.ERASER:
                return EraserTool()
            case ToolList.LINE:
                return LineTool()
            case ToolList.RECTANGLE:
                return RectangleTool()
            case ToolList.CIRCLE:
                return CircleTool()

class Brush():
    width: int = 3
    color: int = 0
    tool: Tool = PencilTool()

    screen: Screen = None
    t: Turtle = None
    loading: Turtle = None

    draw_data: [[(int, int), int, int]] = [[(0, 0), 0, 0]]

    # used for undo
    buffer: [int] = []

    # out of bounds check
    def oob(self, x: float, y: float) -> bool:
        if -self.screen.window_width() // 2 + 110 < x < self.screen.window_width() // 2 - 20 and -self.screen.window_height() // 2 + 20 < y < self.screen.window_height() // 2 - 50:
            return False
        return True