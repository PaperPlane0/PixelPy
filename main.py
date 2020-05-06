import pygame
import UI
from funcs import canvas_flood_fill

pygame.init()

screen_size = (1200, 1000)
canvas_size = (int(screen_size[0] / 1.5), int(screen_size[1] / 1.5))
flag = True


def debug():
    print('OK')


screen = pygame.display.set_mode(screen_size, 0, 16, pygame.HWACCEL)
clock = pygame.time.Clock()

canv_c, canv_r = 128, 128
canvas_keep_ratio = True
canvas_keep_rc = False
canv_px_w = canvas_size[0] // canv_c
canv_px_h = canvas_size[1] // canv_r
if canvas_keep_ratio:
    mn = min(canv_px_h, canv_px_w)
    canv_px_h, canv_px_w = mn, mn
    if not canvas_keep_rc:
        cw, ch = canvas_size
        cw, ch = cw - cw % mn, ch - ch % mn
        canvas_size = cw, ch
        canv_c, canv_r = cw // mn, ch // mn
        canv_c, canv_r = canv_c - canv_c % mn, canv_r - canv_r % mn
    canvas_size = mn * canv_c, mn * canv_r

main_p_r, main_p_c = 13, 8
p_square = 20
p_title_h = 30
basic_color_tooltip = UI.UITooltip(5, 2, p_square * main_p_c, p_square * main_p_r, main_p_r, main_p_c, title_h=p_title_h, text=('main palette', UI.black), font=('arial', 15))

canv_x = p_square * main_p_c + 40

canv_args = (canv_x, 2, *canvas_size, canv_r, canv_c)


def new_canvas(in_canv_args):
    return UI.Canvas(*in_canv_args)


canvas = new_canvas(canv_args)

size_slider = UI.UISlider(5, 350, 30, 190, (canv_c + canv_c) // 16, 0, slider_color=UI.red)

tool_square = 40
tool_r, tool_c = 4, 3
paint_tools_tooltip = UI.UITooltip(size_slider.x + size_slider.width + 10, 350, tool_square * tool_c, tool_square * tool_r, tool_r, tool_c, title_h=p_title_h, text=('tools', UI.black), font=('arial', 15))
for i, item in enumerate(UI.icons):
    paint_tools_tooltip.set_item(i // paint_tools_tooltip.cols, i % paint_tools_tooltip.cols, UI.UIButton(0, 0, 24, 24, image=item))

layers = [canvas]
curr_layer = 0
layer_square = 80
layers_tooltip = UI.UITooltip(canvas_size[0] + canv_x + 20, 2, int(layer_square * 1.2), layer_square, 2, 1, title_h=p_title_h, text=('layers', UI.black), font=('arial', 15))

layers_tooltip.set_item(0, 0, UI.UIButton(0, 0, layer_square, layer_square, image=pygame.image.load('icons/default_image.png')))
layers_tooltip.set_item(1, 0, UI.UITooltip(0, 0, int(1.2 * layer_square) - 4, layer_square // 2 - 4, 1, 2))
layer_buttons_tooltip = layers_tooltip.get_item(-1, 0)
layer_buttons_tooltip.set_item(0, 0, UI.UIButton(0, 0, 16, 16, image=pygame.image.load('icons/visible.png')))
layer_buttons_tooltip.set_item(0, 1, UI.UIButton(0, 0, 16, 16, image=pygame.image.load('icons/delete.png')))


old_mouse_x, old_mouse_y, mouse_x, mouse_y = 0, 0, 0, 0
draw_color = UI.black

for i in range(0, len(UI.colors), 8):
    for col, color in enumerate(UI.colors[i:(i + 8)]):
        b_c = (*color, 255)
        basic_color_tooltip.set_item((i // 8), col, UI.UIButton(0, 0, 20, 20, color=b_c))

selected_brush = pygame.image.load('brushes/circle16.png')
brush = selected_brush

def setup():
    screen.fill(UI.background)


def loop():
    global mouse_x
    global mouse_y
    global old_mouse_y
    global old_mouse_x
    global draw_color
    global selected_brush
    global brush
    global curr_layer

    screen.fill(UI.background)

    draw_canvas = bool(layers)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if basic_color_tooltip.mouse_hover():
                for row in basic_color_tooltip.table:
                    for button in row:
                        if button.mouse_down() and isinstance(button, UI.UIButton):
                            button.tint(False)
                            draw_color = button.color
                            basic_color_tooltip.clicked = button
                            button.tint(True, amt=20)
                            break
            if paint_tools_tooltip.mouse_hover():
                for i, row in enumerate(paint_tools_tooltip.table):
                    for j, button in enumerate(row):
                        if button.mouse_down() and isinstance(button, UI.UIButton):
                            ps = i * paint_tools_tooltip.cols + j
                            if ps == 0:
                                brush = selected_brush
                            elif ps == 1:
                                brush = None
                            elif ps == 2:
                                draw_color = canvas.bg_col
                            elif ps == 3:
                                brush = canvas_flood_fill
                            paint_tools_tooltip.clicked = button
                            button.tint(True, amt=20)
                            break
            if layers_tooltip.mouse_hover():
                for i, obj in enumerate([o for o in [x[0] for x in layers_tooltip.table] if o.mouse_down()]):
                    layers_tooltip.clicked = obj
                    if isinstance(obj, UI.UIButton):
                        curr_layer = i // 2
                        obj.color = UI.gray
                    elif isinstance(obj, UI.UITooltip):
                        visibility_toggle_button = obj.table[0][0]
                        delete_button = obj.table[0][1]
                        if visibility_toggle_button.mouse_down():
                            pass  # TODO: figure out how to make layers visible
                        elif delete_button.mouse_down():
                            delete_button.color = UI.gray
                            if layers:
                                if len(layers_tooltip.table) > 2:
                                    layers_tooltip.pop_item(i, 0)
                                    layers.pop((i - 1) // 2)
                                    layers_tooltip.pop_item(-1, 0)
                            obj.clicked = delete_button
                            break
                    else:
                        print(obj)
        if event.type == pygame.MOUSEBUTTONUP:
            if basic_color_tooltip.clicked:
                basic_color_tooltip.clicked.tint(False)
                basic_color_tooltip.clicked = None
            if paint_tools_tooltip.clicked:
                paint_tools_tooltip.clicked.tint(False)
                paint_tools_tooltip.clicked = None
            if layers_tooltip.clicked:
                if isinstance(layers_tooltip.clicked, UI.UITooltip):
                    layers_tooltip.clicked.clicked.tint(False)
                    layers_tooltip.clicked.clicked = None
                layers_tooltip.clicked.tint(False)
                layers_tooltip.clicked = None
        if event.type == pygame.MOUSEMOTION:
            old_mouse_x, old_mouse_y = mouse_x, mouse_y
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if basic_color_tooltip.mouse_hover():
                for row in basic_color_tooltip.table:
                    for button in row:
                        button.tint(button.mouse_hover())
                        if button.mouse_hover():
                            basic_color_tooltip.tinted = button
                            break
            elif basic_color_tooltip.tinted:
                basic_color_tooltip.tinted.tint(False)
                basic_color_tooltip.tinted = None
            if size_slider.mouse_down():
                size_slider.move_slider()

    if not layers:
        draw_canvas = False

    if draw_canvas:
        now_canvas = layers[curr_layer]
        now_canvas.draw(screen)

    brush_size = size_slider.value

    if draw_canvas:
        if now_canvas.mouse_down():
            now_canvas.line_paint((old_mouse_x, old_mouse_y), (mouse_x, mouse_y), color=draw_color, size=(brush_size, brush_size), brush=brush)

    basic_color_tooltip.draw(screen)
    size_slider.draw(screen)
    paint_tools_tooltip.draw(screen)
    layers_tooltip.draw(screen)
    pygame.display.update()
    clock.tick(240)


setup()
while flag:
    loop()
