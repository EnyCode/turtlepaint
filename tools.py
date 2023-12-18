from typing import Any
import brush
from colors import colors
import turtle
import math
from abc import abstractmethod, abstractstaticmethod
from enum import Enum

# we cant type brush as Brush because of circular imports
class Tool():
    @abstractmethod
    def cursor_down(self, x: float, y: float, brush: "brush.Brush"):
        """Runs when the left mouse button is clicked. """
        raise NotImplementedError

    @abstractmethod
    def cursor_up(self, x: float, y: float, brush: "brush.Brush"):
        """Runs when the left mouse button is released."""
        raise NotImplementedError

    @abstractmethod
    def follow_mouse(self, x: float, y: float, brush: "brush.Brush"):
        """Called when the mouse moves. """
        raise NotImplementedError

    @abstractstaticmethod
    def get_index() -> int:
        """Return the index of the tool in the list. Used for drawing the ui."""
        raise NotImplementedError
    
    @abstractstaticmethod
    def show_turtle() -> bool:
        """Return whether the turtle should be shown or not"""
        return False

    @abstractmethod
    def get_buffer(self) -> int:
        """Return the undo buffer for the tool"""
        raise NotImplementedError

    def reset_buffer(self):
        """Reset the move buffer"""
        # use pass because it's not necessary for every tool
        pass

class PencilTool(Tool):
    # is the turtle pen down
    pen_down: bool = False
    # is the left mouse button down
    mouse_down: bool = False

    # used to check if the cursor hasnt moved for dots
    click_pos: tuple[float, float] = (0., 0.)

    # used for undo
    buffer: int = 0
    move_buffer: int = 0

    def cursor_down(self, x, y, brush: "brush.Brush"):
        if not brush.oob(x, y):
            print(brush.t.undobufferentries() - self.move_buffer)
            self.pen_down = True
            self.mouse_down = True
            brush.t.pendown()
            self.click_pos = brush.t.pos()
            self.buffer = 1 + self.move_buffer
    
    def cursor_up(self, x, y, brush: "brush.Brush"):
        self.pen_down = False
        self.mouse_down = False
        brush.t.penup()
        self.buffer += 1
        self.move_buffer = 0

        # draw a dot if the mouse hasnt moved
        if (x, y) == self.click_pos:
            brush.t.dot()
            self.buffer += 1
        
        #brush.buffer.append(self.buffer)
        push_undo(self.buffer, brush)

        print(brush.t.undobufferentries())
        print(brush.buffer)
    
    def follow_mouse(self, x, y, brush: "brush.Brush"):
        if not self.pen_down and brush.draw_data[-1][2] == 0:
            pass
        else:
            brush.draw_data.append([brush.t.pos(), brush.color, brush.width if self.pen_down else 0])

        if brush.oob(x, y):
            brush.t.penup()
            self.buffer += 1
            self.pen_down = False
        elif self.pen_down == False and self.mouse_down:
            self.pen_down = True
            brush.t.pendown()
            self.buffer += 1
        self.move_buffer += 1
        
        # teleport the turtle
        brush.t.setpos(x, y)

        self.buffer += 1

        brush.screen.update()
    
    def get_buffer(self):
        return self.move_buffer

    def reset_buffer(self):
        self.move_buffer = 0
            
    
    # used for buttons
    @staticmethod
    def get_index():
        return 0
    
    @staticmethod
    def show_turtle():
        return True

class EraserTool(Tool):
    # is the turtle pen down
    pen_down: bool = False
    # is the left mouse button down
    mouse_down: bool = False

    # used to check if the cursor hasnt moved for dots
    click_pos: tuple[float, float] = (0., 0.)

    # used for undo
    buffer: int = 0
    move_buffer: int = 0

    def cursor_down(self, x, y, brush: "brush.Brush"):
        print(x)
        brush.t.pencolor("white")
        brush.t.width(brush.width * 2)

        if not brush.oob(x, y):
            self.pen_down = True
            self.mouse_down = True
            brush.t.pendown()
            self.click_pos = brush.t.pos()
            self.buffer = 1 + self.move_buffer
    
    def cursor_up(self, x, y, brush: "brush.Brush"):
        self.pen_down = False
        self.mouse_down = False
        brush.t.penup()
        brush.t.width(brush.width)
        brush.t.pencolor(colors[brush.color])
        self.buffer += 1
        self.move_buffer = 0

        # draw a dot if the mouse hasnt moved
        if (x, y) == self.click_pos:
            brush.t.dot(size = brush.width * 2 - 1)
            self.buffer += 1
        
        push_undo(self.buffer, brush)
        
        brush.t.pencolor(colors[brush.color])
    
    def follow_mouse(self, x, y, brush: "brush.Brush"):
        if not self.pen_down and brush.draw_data[-1][2] == 0:
            pass
        else:
            brush.draw_data.append([brush.t.pos(), 14, brush.width if self.pen_down else 0])

        if brush.oob(x, y):
            brush.t.penup()
            self.pen_down = False
            self.buffer += 1
        elif self.pen_down == False and self.mouse_down:
            self.pen_down = True
            brush.t.pendown()
            self.buffer += 1
        self.move_buffer += 1
        
        # teleport the turtle
        brush.t.setpos(x, y)

        self.buffer += 1

        brush.screen.update()
    
    def get_buffer(self):
        return self.move_buffer

    # used for buttons
    @staticmethod
    def get_index():
        return 1
    
class LineTool(Tool):
    # where the line is first clicked
    click_pos: tuple[float, float] = (0., 0.)

    dragging: bool = False

    preview: turtle.Turtle

    # used for undo
    buffer: int = 0

    def __init__(self):
        self.preview = turtle.Turtle()
        self.preview.hideturtle()

    def cursor_down(self, x, y, brush: "brush.Brush"):
        if not brush.oob(x, y):
            brush.draw_data.append([(x - 1, y - 1), brush.color, 0])
            brush.draw_data.append([(x, y), brush.color, brush.width])
            brush.t.penup()
            brush.t.setpos(x, y)
            self.click_pos = brush.t.pos()
            self.dragging = True
            self.buffer = 0
    
    def cursor_up(self, x, y, brush: "brush.Brush"):
        if self.dragging:
            brush.t.penup()
            brush.t.goto(self.click_pos)
            brush.t.pendown()
            brush.t.goto(min(max(x, -brush.screen.window_width() // 2 + 110), brush.screen.window_width() // 2 - 20), max(min(y, brush.screen.window_height() // 2 - 50), -brush.screen.window_height() // 2 + 20))
            brush.t.penup()
            self.buffer += 5
            self.dragging = False
            self.preview.clear()

            brush.screen.update()

            push_undo(self.buffer, brush)

            brush.draw_data.append([(x, y), brush.color, brush.width])

            print(brush.buffer)
    
    def follow_mouse(self, x, y, brush: "brush.Brush"):
        if self.dragging:
            self.preview.penup()
            self.preview.clear()
            self.preview.width(brush.width)
            self.preview.pencolor(colors[brush.color])

            coords = (min(max(x, -brush.screen.window_width() // 2 + 110), brush.screen.window_width() // 2 - 20), max(min(y, brush.screen.window_height() // 2 - 50), -brush.screen.window_height() // 2 + 20))

            self.preview.goto(self.click_pos)
            self.preview.setheading(self.preview.towards(coords))
            distance = self.preview.distance(coords)

            for x in range(5):
                self.preview.penup()
                self.preview.forward(distance / 10)
                self.preview.pendown()
                self.preview.forward(distance / 10)

            brush.screen.update()
        
    def get_buffer(self):
        return 0

    @staticmethod
    def get_index():
        return 2

class RectangleTool(Tool):
    click_pos: tuple[float, float] = (0., 0.)

    dragging: bool = False

    preview: turtle.Turtle

    def __init__(self):
        self.preview = turtle.Turtle()
        self.preview.hideturtle()

    def cursor_down(self, x, y, brush: "brush.Brush"):
        if not brush.oob(x, y):
            brush.t.penup()
            brush.t.setpos(x, y)
            self.click_pos = brush.t.pos()
            self.dragging = True

    def cursor_up(self, x, y, brush: "brush.Brush"):
        if self.dragging:
            brush.t.penup()
            brush.t.goto(self.click_pos)
            brush.t.pendown()

            # dont go on the ui
            coords = (min(max(x, -brush.screen.window_width() // 2 + 110), brush.screen.window_width() // 2 - 20), max(min(y, brush.screen.window_height() // 2 - 50), -brush.screen.window_height() // 2 + 20))

            distance_x = coords[0] - brush.t.pos()[0]
            distance_y = brush.t.pos()[1] - coords[1]

            brush.t.setheading(0)

            for i in range(2):
                brush.t.fd(distance_x)
                brush.t.rt(90)
                brush.t.fd(distance_y)
                brush.t.rt(90)

            brush.t.penup()
            self.dragging = False
            self.preview.clear()

            push_undo(12, brush)

            print(brush.buffer)

            brush.screen.update()

    def follow_mouse(self, x, y, brush: "brush.Brush"):
        if self.dragging:
            self.preview.penup()
            self.preview.clear()
            self.preview.width(brush.width)
            self.preview.pencolor(colors[brush.color])

            self.preview.goto(self.click_pos)
            self.preview.pendown()

            # dont go on the ui
            coords = (min(max(x, -brush.screen.window_width() // 2 + 110), brush.screen.window_width() // 2 - 20), max(min(y, brush.screen.window_height() // 2 - 50), -brush.screen.window_height() // 2 + 20))

            distance_x = coords[0] - self.preview.pos()[0]
            distance_y = self.preview.pos()[1] - coords[1]

            for i in range(2):
                for x in range(5):
                    self.preview.penup()
                    self.preview.fd(distance_x / 10)
                    self.preview.pendown()
                    self.preview.fd(distance_x / 10)
                self.preview.rt(90)
                for x in range(5):
                    self.preview.penup()
                    self.preview.fd(distance_y / 10)
                    self.preview.pendown()
                    self.preview.fd(distance_y / 10)
                self.preview.rt(90)

            brush.screen.update()
    
    def get_buffer(self):
        return 0

    @staticmethod
    def get_index():
        return 3



class CircleTool(Tool):
    click_pos: tuple[float, float] = (0., 0.)

    dragging: bool = False

    preview: turtle.Turtle

    def __init__(self):
        self.preview = turtle.Turtle()
        self.preview.hideturtle()

    def cursor_down(self, x, y, brush: "brush.Brush"):
        if not brush.oob(x, y):
            print(brush.t.undobufferentries())
            brush.t.penup()
            brush.t.setpos(x, y)
            self.click_pos = brush.t.pos()
            self.dragging = True

    def cursor_up(self, x, y, brush: "brush.Brush"):
        if self.dragging:
            brush.t.penup()
            brush.t.goto(self.click_pos)

            difference = min(abs(x - self.click_pos[0]), abs(y - self.click_pos[1]))
            c = math.pi * difference

            if y > self.click_pos[1]:
                brush.t.setheading(90)
                brush.t.forward(difference)

            brush.t.setheading(0) if x > self.click_pos[0] else brush.t.setheading(180)
            brush.t.forward(difference / 2)
            brush.t.pendown()
            
            for i in range(360):
                brush.t.forward(c / 360)
                brush.t.right(1) if x > self.click_pos[0] else brush.t.left(1)

            self.preview.clear()

            brush.screen.update()

            push_undo(725, brush)

            print(brush.buffer)
        self.dragging = False

    def follow_mouse(self, x, y, brush: "brush.Brush"):
        if self.dragging:
            self.preview.penup()
            self.preview.clear()
            self.preview.width(brush.width)
            self.preview.pencolor(colors[brush.color])

            self.preview.goto(self.click_pos)
            
            difference = min(abs(x - self.click_pos[0]), abs(y - self.click_pos[1]))
            c = math.pi * difference

            if y > self.click_pos[1]:
                self.preview.setheading(90)
                self.preview.forward(difference)

            self.preview.setheading(0) if x > self.click_pos[0] else self.preview.setheading(180)
            self.preview.forward(difference / 2)

            for i in range(360):
                if i % 5 == 0:
                    self.preview.penup() if self.preview.pen()["pendown"] else self.preview.pendown()

                self.preview.forward(c / 360)
                self.preview.right(1) if x > self.click_pos[0] else self.preview.left(1)

            brush.screen.update()
    
    def get_buffer(self):
        return 0

    @staticmethod
    def get_index():
        return 4

def push_undo(value: int, brush: "brush.Brush"):
    if sum(brush.buffer) + value > 10000:
        brush.buffer.pop(0)
    brush.buffer.append(value)

class ToolList(Enum):
    PENCIL = 0
    ERASER = 1
    LINE = 2
    RECTANGLE = 3
    CIRCLE = 4
    TEST = 5

    def get_tool(self) -> Tool:
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
            case _:
                return PencilTool()