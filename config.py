from buttons import *
from enum import Enum
from tools import *

colors = ["#000000", "#7a7a7a", "#7a0000", "#7a7a00", "#007a00", "#007a7a", "#00007a", "#7a007a", "#797a38", "#003937", "#007aff", "#013879", "#3800ff", "#793802", "#fefefe", "#bcbcbc", "#fe0000", "#fefe00", "#00fe00", "#00fefe", "#0000fe", "#fe00fe", "#fefe7a", "#00fe7a", "#7afffe", "#7a7afe", "#fe007a", "#fe7a39"]

alpha_fill = ("#b0b0b0", "#e9e9e9")

# colors
outline = (18 / 255, 18 / 255, 18 / 255)
glossy = "#f8f8f8"
shadow = (127 / 255, 127 / 255, 127 / 255)
btn_fill = "#bcbcbc"

# button list
buttons = [UiButton(), UiButton(), UiButton(), UiButton(), UiButton(), UiButton()]

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

class Brush():
    width = 3
    color = 0
    tool = PencilTool()

    screen = None
    t = None

    draw_data = [[(0, 0), 0, 0]]

    # out of bounds check
    def oob(self, x, y):
        if -self.screen.window_width() // 2 + 110 < x < self.screen.window_width() // 2 - 20 and -self.screen.window_height() // 2 + 20 < y < self.screen.window_height() // 2 - 50:
            return False
        return True