import turtle
import math
from config import *

ui = turtle.Turtle()

ui.width(3)
ui.speed(-1)

#screen = ui.getscreen()
#screen.title("Turtle Paint")
#screen.setup(1300, 900)

cl_size = 30

# we need this to fix a recursion bug
dragging = False

# coordinates
# these are stored for each updated component so we can quickly
# teleport back and update it
color_coords = (0, 0)
button_coords = (0, 0)
width_coords = (0, 0)

# slider information 
slider_dragged = False
slider_pos = (0, 0)

#cv = screen.getcanvas()
#cv.bind("<Configure>", lambda event : draw_ui())
#cv.bind("<Motion>", lambda event : drag_slider(cv.canvasx(event.x), cv.canvasy(event.y)))

def draw_ui(brush):
    global color_coords, button_coords, width_coords, buttons, slider_pos
    ui.clear()

    ui.penup()

    # go to the top left of the window
    ui.goto(-brush.screen.window_width() // 2, brush.screen.window_height() // 2)

    # draw titlebar
    ui.width(5)
    ui.pencolor(btn_fill)
    ui.fillcolor("#00007a")

    ui.begin_fill()

    for x in range(4):
        ui.forward(brush.screen.window_width() if x % 2 == 0 else 38)
        ui.right(90)

    ui.end_fill()

    # draw icon
    ui.penup()
    ui.forward(10)
    ui.right(90)
    ui.forward(5)

    ui.width(2)
    ui.pencolor("#7876a5")
    ui.pendown()
    ui.fillcolor("#fefefe")
    ui.begin_fill()

    # draw rectangle
    for x in range(4):
        ui.forward(25 if x % 2 == 0 else 20)
        ui.left(90)

    ui.end_fill()

    # draw paintbrush
    ui.width(4)
    ui.penup()
    ui.forward(20)
    ui.left(90)
    ui.forward(7)
    ui.left(23)
    ui.pencolor("#8b0d0e")
    ui.pendown()
    ui.forward(10)
    ui.left(20)
    ui.pencolor("#0908ab")
    ui.forward(15)

    # draw paint
    ui.penup()
    ui.backward(15)
    ui.right(20)
    ui.backward(10)
    ui.right(23)
    ui.forward(3)
    ui.left(90)
    ui.forward(6)

    ui.width(1)

    ui.pencolor("#257919")
    ui.fillcolor("#43d022")

    ui.pendown()
    ui.begin_fill()
    ui.circle(4)
    ui.end_fill()

    ui.penup()
    ui.right(90)

    ui.pencolor("#741513")
    ui.fillcolor("#c01a1a")

    ui.begin_fill()
    ui.pendown()

    for x in range(4):
        ui.forward(8)
        ui.left(90)

    ui.end_fill()

    ui.penup()

    # go to top left
    # to write the title
    ui.goto(-brush.screen.window_width() // 2, brush.screen.window_height() // 2)

    # write "Paint"
    ui.forward(50)
    ui.right(90)
    ui.forward(7.5)
    ui.width(3)
    ui.pendown()
    ui.pencolor("#e0dfff")
    # "P"
    ui.forward(20)
    ui.right(90)
    ui.forward(3)
    ui.left(90)
    ui.backward(20)
    ui.left(90)
    ui.forward(12)

    ui.right(90)
    ui.forward(9)
    ui.left(180)
    ui.forward(3)
    ui.right(90)
    ui.forward(3)
    ui.left(90)
    ui.forward(3)
    ui.penup()
    ui.left(180)
    ui.forward(6)
    ui.right(90)
    ui.forward(3)
    ui.pendown()
    ui.forward(9)

    # "a"
    ui.penup()
    ui.left(180)
    ui.forward(21)
    ui.left(90)
    ui.forward(3)
    ui.right(90)

    ui.pendown()
    ui.forward(9)
    ui.right(90)
    ui.forward(12)
    ui.left(90)
    ui.forward(3)
    ui.left(90)
    ui.forward(9)
    ui.back(3)
    ui.left(90)
    ui.forward(12)
    ui.left(90)
    ui.forward(9)

    ui.left(180)
    ui.forward(3)
    ui.left(90)
    ui.forward(3)
    ui.right(90)
    ui.forward(3)

    ui.left(180)
    ui.penup()
    ui.forward(6)
    ui.left(90)
    ui.forward(3)
    ui.pendown()
    ui.forward(9)

    # "i"
    ui.penup()
    ui.forward(9)
    ui.pendown()
    ui.left(90)
    ui.forward(12)
    ui.right(90)
    ui.forward(3)
    ui.right(90)
    ui.forward(12)

    ui.left(180)
    ui.forward(12)
    ui.penup()
    ui.forward(9)
    ui.left(90)
    ui.pendown()
    ui.forward(3)

    # "n"
    ui.penup()
    ui.right(180)
    ui.forward(9)
    ui.right(90)
    ui.forward(9)
    ui.pendown()
    ui.forward(12)
    ui.left(90)
    ui.forward(3)
    ui.left(90)
    ui.forward(12)

    ui.right(90)
    ui.forward(3)
    ui.right(90)
    ui.forward(3)
    ui.back(3)
    ui.left(90)
    ui.forward(6)
    ui.right(90)
    ui.forward(12)
    ui.left(90)
    ui.forward(3)
    ui.left(90)
    ui.forward(9)

    # "t"
    ui.penup()
    ui.right(90)
    ui.forward(6)
    ui.left(90)
    ui.forward(9)
    ui.right(180)

    ui.pendown()
    ui.forward(15)
    ui.backward(15)
    ui.left(90)
    ui.forward(3)
    ui.right(90)
    ui.forward(6)
    ui.left(90)
    ui.forward(3)
    ui.right(180)
    ui.forward(3)
    ui.left(90)
    ui.forward(12)

    ui.left(90)
    ui.forward(3)

    # go to top right
    # to draw the close button
    ui.penup()
    ui.goto(brush.screen.window_width() // 2, brush.screen.window_height() // 2)
    ui.right(180)
    ui.forward(18)
    ui.left(90)
    ui.forward(6)

    ui.pencolor(outline)
    ui.pendown()

    for x in range(2):
        ui.forward(26)
        ui.right(90)

    ui.forward(3)
    ui.pencolor("#eeedff")
    ui.forward(23)
    ui.right(90)
    ui.forward(23)

    ui.right(90)
    ui.forward(3)

    ui.pencolor(shadow)
    ui.fillcolor(btn_fill)
    ui.begin_fill()

    ui.forward(20)
    ui.right(90)
    ui.forward(20)
    ui.right(90)
    ui.forward(3)
    ui.pencolor("#dddddf")
    ui.forward(17)
    ui.right(90)
    ui.forward(17)

    ui.end_fill()

    ui.penup()

    ui.backward(11)
    ui.right(90)
    ui.forward(6)
    ui.left(45)

    ui.pendown()

    ui.pencolor("#121212")
    ui.forward(11)
    ui.backward(5.5)
    ui.left(90)
    ui.forward(5.5)
    ui.backward(11)

    ui.right(135)

    ui.penup()
    ui.goto(-brush.screen.window_width() // 2, brush.screen.window_height() // 2 - 39)

    ui.pencolor(btn_fill)
    ui.fillcolor(btn_fill)

    # draw side bar
    ui.pendown()
    ui.begin_fill()
    for x in range(4):
        ui.forward(brush.screen.window_height() - 39 if x % 2 == 0 else 100)
        ui.left(90)
    ui.end_fill()

    ui.left(90)

    ui.begin_fill()

    # draw border
    for x in range(4):
        ui.forward(brush.screen.window_width() if x % 2 == 0 else 3)
        ui.right(90)

    ui.forward(brush.screen.window_width())
    ui.right(90)

    for x in range(4):
        ui.forward(brush.screen.window_height() - 39 if x % 2 == 0 else 10)
        ui.right(90)


    ui.end_fill()

    ui.forward(brush.screen.window_height() - 39)

    ui.right(90)

    ui.begin_fill()

    for x in range(4):
        ui.forward(brush.screen.window_width() if x % 2 == 0 else 10)
        ui.right(90)

    ui.end_fill()

    # draw indents
    ui.penup()
    ui.forward(13)
    ui.right(90)
    ui.forward(13)

    ui.pencolor("#eeeeee")
    ui.pendown()

    ui.forward(brush.screen.window_height() - 58)
    ui.left(90)
    ui.pencolor(shadow)
    ui.forward(brush.screen.window_width() - 116)

    ui.left(90)
    ui.forward(brush.screen.window_height() - 58)
    ui.left(90)
    ui.forward(3)
    ui.pencolor("#eeeeee")
    ui.forward(brush.screen.window_width() - 122)

    ui.pencolor(outline)
    ui.left(90)
    ui.penup()
    ui.forward(3)
    ui.pendown()
    ui.forward(brush.screen.window_height() - 64)
    ui.left(90)
    ui.forward(brush.screen.window_width() - 122)
    ui.left(90)
    ui.forward(brush.screen.window_height() - 64)
    ui.left(90)
    ui.forward(brush.screen.window_width() - 122)

    ui.penup()

    # now we need to get to a position to draw the buttons
    ui.goto(-brush.screen.window_width() // 2 + 7, brush.screen.window_height() // 2 - 56)
    button_coords = ui.pos()

    # buttons
    rows = math.ceil(len(buttons) / 2)

    for row in range(rows):
        for button in buttons[(row * 2):(row * 2 + 2)]:
            if buttons.index(button) == brush.tool.get_index():
                button.paint_selected_button(ui)
            else: 
                button.paint_button(ui)
            button.paint_icon(ui)
        ui.backward(46 * 2)
        ui.right(90)
        ui.forward(46)
        ui.left(90)

    # colors
    ui.right(90)
    ui.forward(20)
    ui.left(90)

    ui.forward(9)

    ui.pencolor(outline)

    ui.pendown()

    # slider
    width_coords = ui.pos()

    ui.forward(70)

    ui.backward(45)

    # draw the slider
    ui.penup()
    ui.left(90)
    ui.forward(9)
    ui.right(180)

    ui.pendown()

    slider_pos = ui.pos()

    ui.pencolor(glossy)
    ui.fillcolor(btn_fill)
    ui.begin_fill()

    ui.forward(21)
    ui.left(90)
    ui.pencolor(outline)
    ui.forward(12)
    ui.left(90)
    ui.forward(21)
    ui.left(90)
    ui.forward(3)
    ui.pencolor(glossy)
    ui.forward(9)
    ui.end_fill()

    ui.backward(9)
    ui.left(90)
    ui.forward(3)
    ui.pencolor(shadow)
    ui.forward(15)
    ui.right(90)
    ui.forward(6)

    # go to colors
    ui.penup()
    ui.forward(24)
    ui.left(90)
    ui.forward(22)
    ui.left(90)

    # colors
    size = cl_size * 2 + 3

    # draw currently selected color
    # outline
    ui.pendown()
    ui.pencolor(shadow)
    ui.forward(size)
    ui.right(90)
    ui.pencolor(glossy)
    ui.forward(size)
    ui.right(90)
    ui.forward(size)
    ui.right(90)
    # we do this so we dont go over the color thats already there
    # its also done a lot more
    ui.forward(3)
    ui.pencolor(shadow)
    ui.forward(size - 6)
    ui.right(90)
    # inline
    ui.forward(3)
    ui.pencolor("black")
    ui.forward(size - 6)
    ui.right(90)
    ui.pencolor("#bcbcbc")
    ui.forward(size - 6)
    ui.right(90)
    ui.forward(size - 6)
    ui.right(90)
    ui.forward(3)
    ui.pencolor("black")
    ui.forward(size - 12)
    ui.right(90)
    ui.forward(3)

    offset = 0

    # this leaves behind a trail
    for y in range(18):
        for x in range(18):
            ui.pencolor(alpha_fill[(x + offset) % 2])
            ui.forward(3)
        ui.penup()
        ui.backward(3 * 18)
        ui.right(90)
        ui.forward(3)
        ui.left(90)
        ui.pendown()
        offset += 1

    # so we have to fix it
    ui.penup()
    ui.forward(size - 9)
    ui.left(90)
    ui.pencolor("#bcbcbc")
    ui.pendown()
    ui.forward(size - 9)

    # now we need to draw the selected color
    # go there
    ui.penup()
    ui.left(90)
    ui.forward(13)
    ui.left(90)
    ui.forward(10)
    # draw outline
    ui.pencolor(shadow)
    ui.pendown()
    ui.forward(30)
    ui.right(90)
    ui.forward(30)
    ui.pencolor(glossy)
    ui.right(90)
    ui.forward(30)
    ui.right(90)
    ui.forward(30)
    # inline
    ui.backward(3)
    ui.right(90)
    ui.forward(3)
    ui.pencolor(btn_fill)
    ui.fillcolor(colors[Brush.color])
    ui.begin_fill()
    color_coords = ui.pos()
    ui.forward(24)
    ui.right(90)
    ui.forward(24)
    ui.right(90)
    ui.forward(24)
    ui.right(90)
    ui.forward(24)
    ui.end_fill()

    # go to colors
    ui.penup()
    ui.backward(44)
    ui.right(90)
    ui.forward(47)
    ui.left(90)

    # draw each color
    rows = math.ceil(len(colors) / 2)

    for row in range(2):
        for color in colors[row * 14:(row + 1) * 14]:
            # configure pen
            ui.pendown()
            ui.fillcolor(color)
            ui.begin_fill()

            # draw the outline of color
            ui.pencolor(shadow)
            ui.forward(cl_size)
            ui.right(90)
            ui.pencolor(glossy)
            ui.forward(cl_size)
            ui.right(90)
            ui.forward(cl_size)
            ui.right(90)
            ui.forward(3)
            ui.pencolor(shadow)
            ui.forward(cl_size - 6)

            # draw the inline (the second outline)
            ui.right(90)
            ui.forward(3)
            ui.fillcolor(color)
            ui.pencolor("black")
            ui.begin_fill()
            ui.forward(cl_size - 6)
            ui.pencolor(btn_fill)
            ui.right(90)
            ui.forward(cl_size - 6)
            ui.right(90)
            ui.forward(cl_size - 6)
            ui.right(90)
            ui.forward(3)
            ui.pencolor("black")
            ui.forward(cl_size - 12)
            ui.end_fill()

            # go to next color
            ui.penup()
            ui.backward(cl_size - 3)
            ui.right(90)
            ui.backward(3)
        ui.forward(cl_size + 3)
        ui.left(90)
        ui.forward((cl_size + 3) * rows)
        ui.right(90)
    
    # draw save and load buttons
    ui.penup()
    ui.backward((cl_size + 3) * 2 + 7)
    ui.right(90)
    ui.forward((cl_size + 3) * 14 + 10)
    ui.left(90)

    save = SaveButton()
    load = LoadButton()
    save.paint_button(ui)

    ui.penup()
    ui.backward(83)
    ui.right(90)
    ui.forward(36)
    ui.left(90)

    load.paint_button(ui)

    brush.screen.update()

def on_click(x, y, screen, t, brush):
    global color_coords

    # slider
    cursor_down(x, y)

    # handle colors
    if (-screen.window_width() // 2 + 20) < x < (-screen.window_width() // 2 + 86) and (screen.window_height() // 2 - 766) < y < (screen.window_height() // 2 - 304):
        row = 13 - math.floor((y - (screen.window_height() // 2 - 766)) / 33)
        column = math.floor((x - (-screen.window_width() // 2 + 20)) / 33)
        brush.color = column * 14 + row

        ui.penup()
        ui.goto(color_coords[0] - 1, color_coords[1] - 2)

        ui.fillcolor(colors[brush.color])
        ui.begin_fill()

        for x in range(4):
            ui.right(90)
            ui.forward(21)
        
        ui.end_fill()

        screen.update()

        t.pencolor(colors[brush.color])
    
    # handle tools
    elif (-screen.window_width() // 2 + 7) < x < (-screen.window_width() // 2 + 99) and (screen.window_height() // 2 - 194) < y < (screen.window_height() // 2 - 56):
        column = 2 - math.floor((y - (screen.window_height() // 2 - 194)) / 46)
        row = math.floor((x - (-screen.window_width() // 2 + 7)) / 46)
        brush.tool = ToolList(column * 2 + row).get_tool()

        ui.penup()
        ui.goto(button_coords)

        # draw the buttons again
        rows = math.ceil(len(buttons) / 2)

        for row in range(rows):
            for button in buttons[(row * 2):(row * 2 + 2)]:
                if buttons.index(button) == brush.tool.get_index():
                    button.paint_selected_button(ui)
                else: 
                    button.paint_button(ui)
                button.paint_icon(ui)
            ui.backward(46 * 2)
            ui.right(90)
            ui.forward(46)
            ui.left(90)

        screen.update()
    
    # handle close button
    elif (screen.window_width() // 2 - 44) < x < (screen.window_width() // 2 - 15) and (screen.window_height() // 2 - 35) < y < (screen.window_height() - 6):
        print("Closing Turtle Paint...")
        screen.bye()

# handles sliders
def cursor_down(x, y):
    global slider_pos, slider_dragged
    if slider_pos[0] < x < slider_pos[0] + 15 and slider_pos[1] - 18 < y < slider_pos[1] + 9:
        slider_dragged = True

def cursor_up(event):
    global slider_dragged
    slider_dragged = False

def drag_slider(x, y, brush):
    global width_coords, slider_pos, slider_dragged
    if slider_dragged:
        adjust = min(61, max(0, x - width_coords[0] - 6))

        brush.width = adjust // 10

        brush.t.width(brush.width)

        # go over the slider
        ui.penup()
        ui.goto(width_coords[0] - 1, width_coords[1] + 10)

        ui.pencolor(btn_fill)
        ui.fillcolor(btn_fill)
        ui.begin_fill()

        for x in range(4):
            ui.forward(76 if x % 2 == 0 else 24)
            ui.right(90)
        
        ui.end_fill()

        # draw a new slider
        ui.penup()
        ui.goto(width_coords)
        ui.pencolor(outline)
        ui.pendown()
        ui.forward(70)

        ui.backward(70 - adjust)

        slider_pos = ui.pos()

        ui.pencolor(glossy)
        ui.fillcolor(btn_fill)

        ui.left(90)
        ui.forward(9)
        ui.right(180)

        ui.begin_fill()

        ui.forward(21)
        ui.left(90)
        ui.pencolor(outline)
        ui.forward(12)
        ui.left(90)
        ui.forward(21)
        ui.left(90)
        ui.forward(3)
        ui.pencolor(glossy)
        ui.forward(9)
        ui.end_fill()

        ui.backward(9)
        ui.left(90)
        ui.forward(3)
        ui.pencolor(shadow)
        ui.forward(15)
        ui.right(90)
        ui.forward(6)

        ui.left(180)

        brush.screen.update()

#draw_ui()
#screen.onclick(on_click)

#cv.bind("<ButtonRelease-1>", cursor_up)

#screen.mainloop()
