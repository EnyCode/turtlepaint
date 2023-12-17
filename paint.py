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


def clear_canvas():
    global brush
    t.clear()
    loading.clear()
    if len(brush.draw_data) >= 1:
        brush.draw_data = [[(0, 0), 0, 0]]


def save_canvas():
    global brush
    # TODO: tell the user it has saved

    print("saving...")

    with open("drawings/drawing.txt", "wb") as file:
        for i in range(0, len(brush.draw_data) - 1):
            try:
                if brush.draw_data[i][0] == brush.draw_data[i + 1][0]:
                    brush.draw_data.pop(i)
            except IndexError:
                break
        pickle.dump(brush.draw_data, file)
    time.sleep(1)
    print("saved")


def load_canvas():
    print("loading...")
    clear_canvas()
    if os.path.isfile("drawings/drawing.txt"):
        global loading, brush, screen
        with open("drawings/drawing.txt", "rb") as file:
            file_data = pickle.load(file)
            loading.penup()
            loading.goto(file_data[0][0])
            loading.pencolor(colors[file_data[0][1]])
            loading.width(file_data[0][2])
            file_data.pop(0)

            loading.speed('fastest')

            for data in file_data:
                if data[2] == 0:
                    loading.penup()
                loading.goto(data[0])
                if data[2] != 0:
                    loading.pendown()
                loading.pencolor(colors[data[1]])
                loading.width(data[2])

            screen.update()

            brush.draw_data = file_data
    else:
        print("File not found")
    print("loaded")
    loading.hideturtle()

    ui.draw_ui(brush)


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

turtle.listen()
turtle.onkey(save_canvas, "s")
turtle.onkey(load_canvas, "l")
turtle.onkey(clear_canvas, "c")

t.speed(-1)

ui.draw_ui(brush)

screen.mainloop()
