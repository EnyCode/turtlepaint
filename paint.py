import turtle
import os
import pickle
import time

import ui
from config import *

__dirname = os.path.dirname(__file__)
drawings_dir_path = os.path.join(__dirname, 'drawings')

try:
    os.makedirs(drawings_dir_path, exist_ok=True)
except OSError as error:
    pass

# all the info about the program
brush = Brush()

# whether the turtle is currently loading
loading = False

dragging = False


def brush_down(x, y):
    global brush

    ui.on_click(x, y, screen, t, brush)

    brush.tool.cursor_down(x, y, brush)

def brush_up(event):
    global brush

    x, y = canvas.canvasx(event.x), -canvas.canvasy(event.y)

    ui.cursor_up(event)

    brush.tool.cursor_up(x, y, brush)

def follow_mouse(event):
    global brush, dragging

    if not dragging:
        dragging = True
        (x, y) = canvas.canvasx(event.x), -canvas.canvasy(event.y)

        ui.drag_slider(x, y, brush)

        brush.tool.follow_mouse(x, y, brush)

        dragging = False


screen = turtle.Screen()
screen.setup(1300, 900)
screen.tracer(0)

brush.screen = screen

canvas = screen.getcanvas()
t = turtle.Turtle()
loading = turtle.Turtle()

brush.t = t

loading.hideturtle()

loading.width(3)
t.width(3)

brush.loading = loading

t.shapesize(0.25, 0.25)
t.penup()
t.shape("circle")

canvas.bind("<Motion>", follow_mouse)
canvas.bind("<ButtonRelease-1>", brush_up)
canvas.bind("<Configure>", lambda event : ui.draw_ui(brush))

# on click, put brush down
# opposite on release
turtle.onscreenclick(brush_down)

t.speed(-1)

ui.draw_ui(brush)

screen.mainloop()
