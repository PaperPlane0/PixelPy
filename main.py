import pygame
import UI
from funcs import canvas_flood_fill
import sys

pygame.init()

screen_size = (1200, 850)
canvas_size = (int(screen_size[0] / 1.2), int(screen_size[1] / 1.2))
flag = True


def debug():
    print('OK')

screen = pygame.display.set_mode(screen_size, 0, 16, pygame.HWACCEL)
clock = pygame.time.Clock()

canv_c, canv_r = 128, 128
canvas_keep_ratio = True
canvas_keep_rc = True
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

main_p_r, main_p_c = 12, 8
p_square = 20
p_title_h = 30
basic_color_tooltip = UI.UITooltip(5, 2, p_square * main_p_c, p_square * main_p_r, main_p_r, main_p_c, title_h=p_title_h, text=('Main palette', UI.black), font=('arial', 15))

for i in range(0, len(UI.colors), main_p_c):
    for col, color in enumerate(UI.colors[i:(i + main_p_c)]):
        b_c = (*color, 255)
        basic_color_tooltip.set_item((i // main_p_c), col, UI.UIButton(0, 0, 20, 20, color=b_c))

custom_color_tooltip = UI.UITooltip(5, basic_color_tooltip.height + 22, 156, 26, 1, 6, title_h=20, text=('Custom palette', UI.black), font=('arial', 15))

current_color_indicator = UI.UITooltip(15, custom_color_tooltip.y + 40, 46, 36, 1, 1, title_h=20, text=('color', UI.black), font=('arial', 15))
current_color_indicator.set_item(0, 0, UI.Rectangle(7, current_color_indicator.y + 2, 42, 32, color=UI.black))

cw_icon = pygame.image.load('icons/pick_color.png')
pick_color_button = UI.UIButton(custom_color_tooltip.width - 10 - current_color_indicator.height, custom_color_tooltip.y + 40, current_color_indicator.height, current_color_indicator.height, image=cw_icon)


canv_x = p_square * main_p_c + 40
canv_args = (canv_x, 2, *canvas_size, canv_r, canv_c)


def new_canvas(in_canv_args):
    return UI.Canvas(*in_canv_args)


canvas = new_canvas(canv_args)
size_slider = UI.UISlider(5, 450, 30, 170, min(canv_c // 8, 50), 0, slider_color=UI.red)

tool_square = 40
tool_r, tool_c = 4, 3
paint_tools_tooltip = UI.UITooltip(size_slider.x + size_slider.width + 10, 450, tool_square * tool_c, tool_square * tool_r, tool_r, tool_c, title_h=p_title_h, text=('Tools', UI.black), font=('arial', 15))

for i, item in enumerate(UI.icons):
    paint_tools_tooltip.set_item(i // paint_tools_tooltip.cols, i % paint_tools_tooltip.cols, UI.UIButton(0, 0, 24, 24, image=item))

layers = [[canvas, True]]
curr_layer = 0
layer_square = 80
layers_tooltip = UI.UITooltip(canvas_size[0] + canv_x + 20, 2, int(layer_square * 1.2), layer_square, 2, 1, title_h=p_title_h, text=('Layers', UI.black), font=('arial', 15))

layers_tooltip.set_item(0, 0, UI.UIButton(0, 0, layer_square, layer_square, image=pygame.image.load('icons/default_image.png')))
layers_tooltip.set_item(1, 0, UI.UITooltip(0, 0, int(1.2 * layer_square) - 4, layer_square // 2 - 4, 1, 2, show_grid=False))
layer_buttons_tooltip = layers_tooltip.get_item(-1, 0)
layer_buttons_tooltip.set_item(0, 0, UI.UIButton(0, 0, 16, 16, image=pygame.image.load('icons/visible.png')))
layer_buttons_tooltip.set_item(0, 1, UI.UIButton(0, 0, 16, 16, image=pygame.image.load('icons/delete.png')))

add_layer_button = UI.UIButton(layers_tooltip.x, layers_tooltip.y + layers_tooltip.height, layer_square + 15, 20, text=('+    add layer', UI.black), font=('arial', 15), image=pygame.image.load('icons/button_1.png'))

old_mouse_x, old_mouse_y, mouse_x, mouse_y = 0, 0, 0, 0
draw_color = UI.black

selected_brush = pygame.image.load('brushes/circle16.png')
brush = selected_brush
selected_layer_button = layers_tooltip.get_item(0, 0)
fr = 0

def setup():
    screen.fill(UI.white)
    canvas.draw(screen)
    pygame.display.flip()


def loop():
    global mouse_x
    global mouse_y
    global old_mouse_y
    global old_mouse_x
    global draw_color
    global selected_brush
    global brush
    global curr_layer
    global selected_layer_button
    global fr

    pygame.draw.rect(screen, UI.background, (layers_tooltip.x - 5, 0, layers_tooltip.width + 10, add_layer_button.x + 10))
    pygame.draw.rect(screen, UI.background, (paint_tools_tooltip.x - 5, paint_tools_tooltip.y - 5, paint_tools_tooltip.width + 10, paint_tools_tooltip.height + 10))

    draw_canvas = bool(layers)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            pass
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
                                if draw_canvas:
                                    draw_color = layers[curr_layer][0].bg_col
                                brush = None
                            elif ps == 3:
                                brush = canvas_flood_fill
                            paint_tools_tooltip.clicked = button
                            button.tint(True, amt=20)
                            break

            if layers_tooltip.mouse_hover():
                for i, obj in enumerate([x[0] for x in layers_tooltip.table]):
                    if obj.mouse_down():
                        layers_tooltip.clicked = obj
                        if isinstance(obj, UI.UIButton):
                            selected_layer_button = obj
                            curr_layer = i // 2
                            if layers[curr_layer][1]:
                                layers[curr_layer][0].draw(screen)
                            obj.color = UI.gray
                        elif isinstance(obj, UI.UITooltip):
                            visibility_toggle_button = obj.table[0][0]
                            delete_button = obj.table[0][1]
                            if visibility_toggle_button.mouse_down():
                                layers[i // 2][1] = not layers[i // 2][1]
                                if not layers[i // 2][1]:
                                    layers[i // 2][0].hide(screen, True)
                                    for canv_obj in layers:
                                        cv, do_draw = canv_obj
                                        if do_draw:
                                            cv.draw(screen)
                                else:
                                    layers[i // 2][0].draw(screen)
                                    layers[curr_layer][0].draw(screen)
                                pygame.display.update(layers[i // 2][0].get_rectangle())
                                if layers[i // 2][1]:
                                    visibility_toggle_button.image = pygame.image.load('icons/visible.png')
                                else:
                                    visibility_toggle_button.image = pygame.image.load('icons/invisible.png')
                                visibility_toggle_button.color = UI.gray
                                obj.clicked = visibility_toggle_button
                            elif delete_button.mouse_down():
                                delete_button.color = UI.gray
                                if layers:
                                    if len(layers_tooltip.table) > 2:
                                        layers_tooltip.pop_item(i - 1, 0)
                                        layers_tooltip.pop_item(i - 1, 0)

                                        layers.pop((i - 1) // 2)
                                        curr_layer = min(curr_layer, len(layers) - 1)

                                        selected_layer_button = layers_tooltip.get_item(curr_layer * 2, 0)

                                        old_add_layer_button_pos = add_layer_button.get_rectangle()
                                        add_layer_button.x, add_layer_button.y = layers_tooltip.x, layers_tooltip.y + layers_tooltip.height
                                        pygame.display.update(old_add_layer_button_pos)

                                        pygame.draw.rect(screen, UI.background, canvas.get_rectangle())

                                        for canv_obj in layers:
                                            cv, do_draw = canv_obj
                                            if do_draw:
                                                cv.draw(screen)

                                        pygame.display.update(canvas.get_rectangle())
                                obj.clicked = delete_button
                                break
                        else:
                            print(obj)
            if add_layer_button.mouse_hover():
                layers_tooltip.append_item(UI.UIButton(0, 0, layer_square, layer_square, image=pygame.image.load('icons/default_image.png')))
                layers_tooltip.append_item(UI.UITooltip(0, 0, int(1.2 * layer_square) - 4, layer_square // 2 - 4, 1, 2, show_grid=False))
                new_tooltip_element = layers_tooltip.get_item(-1, 0)
                new_tooltip_element.set_item(0, 0, UI.UIButton(0, 0, 16, 16, image=pygame.image.load('icons/visible.png')))
                new_tooltip_element.set_item(0, 1, UI.UIButton(0, 0, 16, 16, image=pygame.image.load('icons/delete.png')))
                layers.append([new_canvas(canv_args), True])
                curr_layer += 1
                layers_tooltip.update_item_sizes()
                old_add_layer_button_pos = add_layer_button.get_rectangle()
                add_layer_button.x, add_layer_button.y = layers_tooltip.x, layers_tooltip.y + layers_tooltip.height
                pygame.display.update(old_add_layer_button_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if basic_color_tooltip.clicked:
                basic_color_tooltip.clicked.tint(False)
                basic_color_tooltip.clicked = None
            if paint_tools_tooltip.clicked:
                paint_tools_tooltip.clicked.tint(False)
                paint_tools_tooltip.clicked = None
            if layers_tooltip.clicked:
                if isinstance(layers_tooltip.clicked, UI.UITooltip):
                    if layers_tooltip.clicked.clicked:
                        layers_tooltip.clicked.clicked.tint(False)
                        layers_tooltip.clicked.clicked = None
                else:
                    layers_tooltip.clicked.tint(False)

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
        now_canvas, do_draw = layers[curr_layer]
        overlay_layers = [x[0] for x in layers if x[0] != now_canvas and x[1]]
        if do_draw:
            brush_size = size_slider.value
            if now_canvas.mouse_down():
                if old_mouse_x != mouse_x or old_mouse_y != mouse_y:
                    now_canvas.line_paint((old_mouse_x, old_mouse_y), (mouse_x, mouse_y), color=draw_color,
                                      size=(brush_size, brush_size), brush=brush, surface=screen, overlays=overlay_layers)
                    pygame.display.update(now_canvas.get_rectangle())

    current_color_indicator.get_item(0, 0).color = draw_color

    basic_color_tooltip.draw(screen)
    size_slider.draw(screen)
    paint_tools_tooltip.draw(screen)
    layers_tooltip.draw(screen)
    selected_layer_button.draw_frame(screen, UI.red, width=5)
    add_layer_button.draw(screen)
    custom_color_tooltip.draw(screen)
    current_color_indicator.draw(screen)
    pick_color_button.draw(screen)


    pygame.display.update(basic_color_tooltip.get_rectangle())
    pygame.display.update(size_slider.get_rectangle())
    pygame.display.update(paint_tools_tooltip.get_rectangle())
    pygame.display.update(layers_tooltip.get_rectangle())
    pygame.display.update(custom_color_tooltip.get_rectangle())
    pygame.display.update(current_color_indicator.get_rectangle())
    pygame.display.update(pick_color_button.get_rectangle())
    pygame.display.update((layers_tooltip.x - 5, layers_tooltip.y + layers_tooltip.height, layers_tooltip.width + 10, layers_tooltip.row_size + 20))
    clock.tick(128)
    print(clock)


setup()
while flag:
    loop()
