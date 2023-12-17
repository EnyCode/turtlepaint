import config
import turtle
from abc import abstractmethod, abstractstaticmethod

class Tool():
    @abstractmethod
    def cursor_down(self, x, y, brush):
        """
        Runs when the left mouse button is clicked. 

        Keyword arguments:
        self -- the tool
        x -- the x position of the mouse click
        y -- the y position of the mouse click
        brush -- the brush object
        """
        return NotImplementedError

    @abstractmethod
    def cursor_up(self, x, y, brush):
        """
        Runs when the left mouse button is released.

        Keyword arguments:
        self -- the tool
        x -- the x position of the mouse click
        y -- the y position of the mouse click
        brush -- the brush object
        """
        return NotImplementedError

    @abstractmethod
    def follow_mouse(self, x, y, brush):
        """
        Called when the mouse moves. 

        Keyword arguments:
        self -- the tool
        x -- the x position of the mouse click
        y -- the y position of the mouse click
        brush -- the brush object
        """
        return NotImplementedError

    @abstractmethod
    def get_index():
        """
        Return the index of the tool in the list

        Keyword arguments:
        self -- the tool
        
        Returns:
        the index of the tool (int)
        """
        return NotImplementedError

    @abstractmethod
    def get_buffer(self):
        """
        Return the undo buffer for the tool
        
        Keyword arguments:
        self -- the tool
        
        Returns:
        the undo buffer (int)
        """

class PencilTool(Tool):
    # is the turtle pen down
    pen_down = False
    # is the left mouse button down
    mouse_down = False

    # used to check if the cursor hasnt moved for dots
    click_pos = (0, 0)

    # used for undo
    buffer = 0

    def cursor_down(self, x, y, brush):
        if not brush.oob(x, y):
            self.pen_down = True
            self.mouse_down = True
            brush.t.pendown()
            self.click_pos = brush.t.pos()
            self.buffer = 1
    
    def cursor_up(self, x, y, brush):
        self.pen_down = False
        self.mouse_down = False
        brush.t.penup()
        self.buffer += 1

        # draw a dot if the mouse hasnt moved
        if (x, y) == self.click_pos:
            brush.t.dot(size = int(brush.width * 1.5))
            self.buffer += 1
        
        brush.buffer.append(self.buffer)

        print(brush.buffer)
    
    def follow_mouse(self, x, y, brush):
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
        
        # teleport the turtle
        brush.t.setpos(x, y)

        self.buffer += 1

        brush.screen.update()
    
    def get_buffer(self):
        return self.buffer - 2
            
    
    # used for buttons
    @staticmethod
    def get_index():
        return 0

class EraserTool(Tool):
    # is the turtle pen down
    pen_down = False
    # is the left mouse button down
    mouse_down = False

    # used to check if the cursor hasnt moved for dots
    click_pos = (0, 0)

    def cursor_down(self, x, y, brush):
        brush.t.pencolor("white")
        brush.t.width(brush.width * 2)

        if not brush.oob(x, y):
            self.pen_down = True
            self.mouse_down = True
            brush.t.pendown()
            self.click_pos = brush.t.pos()
    
    def cursor_up(self, x, y, brush):
        self.pen_down = False
        self.mouse_down = False
        brush.t.penup()
        brush.t.width(brush.width)

        # draw a dot if the mouse hasnt moved
        if (x, y) == self.click_pos:
            brush.t.dot(size = brush.width * 2 - 1)
        
        brush.t.pencolor(config.colors[brush.color])
    
    def follow_mouse(self, x, y, brush):
        if not self.pen_down and brush.draw_data[-1][2] == 0:
            pass
        else:
            brush.draw_data.append([brush.t.pos(), 14, brush.width if self.pen_down else 0])

        if brush.oob(x, y):
            brush.t.penup()
            self.pen_down = False
        elif self.pen_down == False and self.mouse_down:
            self.pen_down = True
            brush.t.pendown()
        
        # teleport the turtle
        brush.t.setpos(x, y)

        brush.screen.update()
    
    # used for buttons
    @staticmethod
    def get_index():
        return 1
    
class LineTool(Tool):
    # where the line is first clicked
    click_pos = (0, 0)

    dragging = False

    preview = None

    def __init__(self):
        self.preview = turtle.Turtle()
        self.preview.hideturtle()

    def cursor_down(self, x, y, brush):
        if not brush.oob(x, y):
            brush.t.penup()
            brush.t.setpos(x, y)
            self.click_pos = brush.t.pos()
            self.dragging = True
    
    def cursor_up(self, x, y, brush):
        if self.dragging:
            brush.t.penup()
            brush.t.goto(self.click_pos)
            brush.t.pendown()
            brush.t.goto(min(max(x, -brush.screen.window_width() // 2 + 110), brush.screen.window_width() // 2 - 20), max(min(y, brush.screen.window_height() // 2 - 50), -brush.screen.window_height() // 2 + 20))
            brush.t.penup()
            self.dragging = False
    
    def follow_mouse(self, x, y, brush):
        if self.dragging:
            self.preview.penup()
            self.preview.clear()
            self.preview.width(brush.width)

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
        
    
    @staticmethod
    def get_index():
        return 2

class RectangleTool(Tool):
    click_pos = (0, 0)

    dragging = False

    preview = None

    def __init__(self):
        self.preview = turtle.Turtle()

    def cursor_down(self, x, y, brush):
        if not brush.oob(x, y):
            brush.t.penup()
            brush.t.setpos(x, y)
            self.click_pos = brush.t.pos()
            self.dragging = True

    def cursor_up(self, x, y, brush):
        brush.t.penup()
        brush.t.goto(self.click_pos)
        brush.t.pendown()

        distance_x = x - brush.t.pos()[0]
        distance_y = brush.t.pos()[1] - y

        for i in range(0, 2):
            brush.t.fd(distance_x)
            brush.t.rt(90)
            brush.t.fd(distance_y)
            brush.t.rt(90)

        brush.t.penup()
        self.dragging = False

    def follow_mouse(self, x, y, brush):
        if self.dragging:
            self.preview.penup()
            self.preview.clear()
            self.preview.width(brush.width)

            self.preview.goto(self.click_pos)
            self.preview.pendown()
            distance_x = x - self.preview.pos()[0]
            distance_y = self.preview.pos()[1] - y

            for i in range(0, 2):
                self.preview.fd(distance_x)
                self.preview.rt(90)
                self.preview.fd(distance_y)
                self.preview.rt(90)

            brush.screen.update()

    @staticmethod
    def get_index():
        return 3



class CircleTool(Tool):
    click_pos = (0, 0)

    dragging = False

    preview = None

    def __init__(self):
        self.preview = turtle.Turtle()

    def cursor_down(self, x, y, brush):
        if not brush.oob(x, y):
            brush.t.penup()
            brush.t.setpos(x, y)
            self.click_pos = brush.t.pos()
            self.dragging = True

    def cursor_up(self, x, y, brush):
        brush.t.penup()
        brush.t.goto(self.click_pos)
        brush.t.pendown()
        brush.t.setheading(brush.t.towards(x, y) - 90)
        brush.t.circle(round(brush.t.distance(x, y) / 2, 0))
        brush.t.penup()
        self.dragging = False

    def follow_mouse(self, x, y, brush):
        if self.dragging:
            self.preview.penup()
            self.preview.clear()
            self.preview.width(brush.width)

            self.preview.goto(self.click_pos)
            self.preview.setheading(self.preview.towards(x, y) - 90)
            self.preview.pendown()
            self.preview.circle(round(self.preview.distance(x, y) / 2, 0), 360)

            brush.screen.update()

    @staticmethod
    def get_index():
        return 4