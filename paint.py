import turtle
import os
from tkinter import Canvas, Event
from brush import Brush
import ui

__dirname = os.path.dirname(__file__)
drawings_dir_path = os.path.join(__dirname, 'drawings')

try:
    os.makedirs(drawings_dir_path, exist_ok=True)
except OSError as error:
    pass

# all the info about the program
brush: Brush = Brush()

# whether the turtle is currently loading
loading: bool = False

dragging: bool = False


def brush_down(x: float, y: float):
    global brush

    ui.on_click(x, y, brush)

    brush.tool.cursor_down(x, y, brush)

def brush_up(event: Event):
    global brush

    x, y = canvas.canvasx(event.x), -canvas.canvasy(event.y)

    ui.cursor_up(event)

    brush.tool.cursor_up(x, y, brush)

def follow_mouse(event: Event):
    global brush, dragging

    if not dragging:
        dragging = True
        (x, y) = canvas.canvasx(event.x), -canvas.canvasy(event.y)

        ui.drag_slider(x, y, brush)

        brush.tool.follow_mouse(x, y, brush)

        dragging = False
    
def undo(event: Event):
    global brush, t, screen

    if len(brush.buffer) > 0:
        print(brush.buffer, brush.tool.get_buffer())
        for x in range(brush.buffer[-1][0] + brush.tool.get_buffer()):
            t.undo()
        brush.draw_data = brush.draw_data[:-brush.buffer[-1][1]]
        brush.buffer.pop()
        brush.tool.reset_buffer()

        screen.update()

screen: turtle._Screen = turtle.Screen()
screen.setup(1300, 900)
screen.tracer(0)

brush.screen = screen

canvas: Canvas = screen.getcanvas()
t: turtle.Turtle = turtle.Turtle()
#loading: turtle.Turtle = turtle.Turtle()

brush.t = t

t.width(3)
t.setundobuffer(10000)

brush.loading = turtle.Turtle()
brush.loading.hideturtle()

t.shapesize(0.25, 0.25)
t.penup()
t.shape("circle")

# when mouse clicks
canvas.bind("<Motion>", follow_mouse)
# on mouse click
canvas.bind("<ButtonRelease-1>", brush_up)
# resize ui on window resize
canvas.bind("<Configure>", lambda event : ui.draw_ui(brush))
canvas.bind("<Control-KeyPress-z>", undo)

screen.listen()

# on click, put brush down
# opposite on release
turtle.onscreenclick(brush_down)

t.speed(-1)

ui.draw_ui(brush)

screen.mainloop()
