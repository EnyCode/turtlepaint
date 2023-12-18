from turtle import Turtle
from colors import *

class UiButton:
    size: int = 43

    def paint_button(self, t: Turtle):
        width: int = t.width()

        # glossy (top and left)
        t.pencolor(glossy)
        t.right(90)
        t.forward(self.size)
        t.left(180)
        t.pendown()

        # draw the glossy
        t.fillcolor(btn_fill)
        t.begin_fill()

        for x in range(2):
            t.forward(self.size)
            t.right(90)

        # draw the outline
        t.pencolor(outline)
        for x in range(2):
            t.forward(self.size)
            t.right(90)
        t.end_fill()

        # go to shadow
        t.penup()
        t.forward(width)
        t.right(90)
        t.forward(width)

        # draw shadow
        t.pencolor(shadow)
        t.pendown()
        t.forward(self.size - width * 2)
        t.left(90)
        t.forward(self.size - width * 2)

        # go to edge
        t.penup()
        t.forward(width)
        t.right(90)
        t.forward(width * 2)

    def paint_selected_button(self, t: Turtle):
        t.penup()
        t.right(90)
        t.forward(1)
        t.left(90)
        t.pendown()

        width = t.width()

        offset = 0

        for y in range(14):
            for x in range(14):
                t.pencolor(alpha_fill[(x + offset) % 2])
                t.forward(width)
            t.penup()
            t.backward(width * 14)
            t.right(90)
            t.forward(width)
            t.left(90)
            t.pendown()
            offset += 1

        t.pencolor(glossy)
        t.forward(self.size)
        t.left(90)
        t.forward(self.size)
        
        t.left(90)
        t.forward(3)
        t.pencolor(outline)
        t.forward(self.size - width)
        t.left(90)
        t.forward(self.size - width)
        t.left(90)
        t.forward(width)
        
        t.pencolor(btn_fill)
        t.forward(self.size - width * 2)
        t.left(90)
        t.forward(self.size - width * 2)
        t.left(90)
        t.forward(width)

        t.pencolor(shadow)
        t.forward(self.size - width * 3)
        t.left(90)
        t.forward(self.size - width * 3)

        # go to corner
        t.penup()
        t.left(90)
        t.forward(self.size)
        t.left(90)
        t.forward(self.size - width * 2)
        t.right(90)

    def paint_icon(self, t: Turtle):
        """
        paint_icon(self, t)
            paints the icon for a button

        the turtle will start in the top right and must end in the top right
        """

        name: str = type(self).__name__

        if name != "UiButton":
            print(name, "must override the paint_icon(self, t) function")

    def on_click(self):
        name: str = type(self).__name__

        if name != "UiButton":
            print(name, "must override the paint_icon(self, t) function")

class PressButton(UiButton):
    width: int = 80
    height: int = 30

    def paint_button(self, t: Turtle):
        width = t.width()

        # glossy (top and left)
        t.pencolor(glossy)
        t.right(90)
        t.forward(self.height)
        t.left(180)
        t.pendown()

        # draw the glossy
        t.fillcolor(btn_fill)
        t.begin_fill()

        t.forward(self.height)
        t.right(90)
        t.forward(self.width)
        t.right(90)

        # draw the outline
        t.pencolor(outline)
        t.forward(self.height)
        t.right(90)
        t.forward(self.width)
        t.right(90)
        t.end_fill()

        # go to shadow
        t.penup()
        t.forward(width)
        t.right(90)
        t.forward(width)

        # draw shadow
        t.pencolor(shadow)
        t.pendown()
        t.forward(self.width - width * 2)
        t.left(90)
        t.forward(self.height - width * 2)

        # go to edge
        t.penup()
        t.forward(width)
        t.right(90)
        t.forward(width * 2)
    
    def paint_selected_button(self, t: Turtle):
        t.penup()
        t.right(90)
        t.forward(1)
        t.left(90)
        t.pendown()

        width = t.width()

        offset = 0

        for y in range(9):
            for x in range(26):
                t.pencolor(alpha_fill[(x + offset) % 2])
                t.forward(width)
            t.penup()
            t.backward(width * 26)
            t.right(90)
            t.forward(width)
            t.left(90)
            t.pendown()
            offset += 1
        
        t.pencolor(glossy)
        t.forward(self.width)
        t.left(90)
        t.forward(self.height)

        t.left(90)
        t.forward(3)
        t.pencolor(outline)
        t.forward(self.width - width)
        t.left(90)
        t.forward(self.height - width)
        t.left(90)
        t.forward(width)

        t.pencolor(btn_fill)
        t.forward(self.width - width * 2)
        t.left(90)
        t.forward(self.height - width * 2)
        t.left(90)
        t.forward(width)

        t.pencolor(shadow)
        t.forward(self.width - width * 3)
        t.left(90)
        t.forward(self.height - width * 3)

        # go to corner
        t.penup()
        t.left(90)
        t.forward(self.width)
        t.left(90)
        t.forward(self.height - width * 2)
        t.right(90)

# button list
buttons: list[UiButton] = [UiButton(), UiButton(), UiButton(), UiButton(), UiButton(), UiButton()]

class SaveButton(PressButton):
    def paint_icon(self, t: Turtle):
        pass

class LoadButton(PressButton):
    def paint_icon(self, t: Turtle):
        pass