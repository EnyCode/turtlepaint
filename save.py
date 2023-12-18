import pickle
import time
from brush import Brush
from colors import colors
import ui
from tkinter import filedialog as fd

def save_canvas(brush: Brush):
    # TODO: tell the user it has saved

    print("saving...")

    file = fd.asksaveasfile(mode="wb", filetypes=[("Turtle Paint File", ".tpf")])
    if file is None:
        print("cancelled...")
    else:
        with file:
            for i in range(0, len(brush.draw_data) - 1):
                try:
                    if brush.draw_data[i][0] == brush.draw_data[i + 1][0]:
                        brush.draw_data.pop(i)
                except IndexError:
                    break
            pickle.dump(brush.draw_data, file)
    time.sleep(1)
    print("saved")


def load_canvas(brush: Brush):
    print("loading...")
    brush.t.clear()
    brush.loading.clear()
    file = fd.askopenfile(mode="rb", filetypes=[("Turtle Paint File", ".tpf")])
    if file is None:
        print("cancelled...")
    else:
        with file:
            file_data = pickle.load(file)
            brush.loading.penup()
            brush.loading.goto(file_data[0][0])
            brush.loading.pencolor(colors[file_data[0][1]])
            brush.loading.width(file_data[0][2])
            file_data.pop(0)

            brush.loading.speed('fastest')

            for data in file_data:
                if data[2] == 0:
                    brush.loading.penup()
                brush.loading.goto(data[0])
                if data[2] != 0:
                    brush.loading.pendown()
                brush.loading.pencolor(colors[data[1]])
                brush.loading.width(data[2])

            brush.screen.update()

        brush.draw_data = file_data
    print("loaded")
    brush.loading.hideturtle()

    ui.draw_ui(brush)