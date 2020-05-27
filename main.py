import pygame
import UI
from funcs import canvas_flood_fill
import sys

pygame.init()

screen_size = (1200, 850)
screen_w, screen_h = screen_size
canvas_size = (int(screen_size[0] / 1.2), int(screen_size[1] / 1.2))
flag = True


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
pick_color_button.state = False

canv_x = p_square * main_p_c + 40
canv_args = (canv_x, 2, *canvas_size, canv_r, canv_c)


def new_canvas(in_canv_args):
    return UI.Canvas(*in_canv_args)


canvas = new_canvas(canv_args)
size_slider = UI.UISlider(5, 450, 30, 170, min(canv_c // 8, 50), 1, slider_color=UI.red)

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

pick_color_popup_w, pick_color_popup_h = 700, 350
pick_color_popup = UI.Popup((screen_w - pick_color_popup_w) // 2, (screen_h - pick_color_popup_h) // 2, pick_color_popup_w, pick_color_popup_h,
                            text=('  Pick a color', UI.black), font=('courier new', 20), title_h=30)
new_tt_y = pick_color_popup.y + 20
new_tt_square = 20
for i, key in enumerate(UI.colors2.keys()):
    color_lst = UI.colors2[key]
    new_tt = UI.UITooltip(pick_color_popup.x + 20, new_tt_y, new_tt_square * len(color_lst),
                          new_tt_square, 1, len(color_lst), title_h=20, font=('arial', 16),
                          text=(key, UI.black), bg_color=UI.white, border_w=2)
    pick_color_popup.add_item(new_tt, 20, new_tt_y - pick_color_popup.y + 20, name=f'palette{i}')
    for j, clr in enumerate(color_lst):
        new_tt.set_item(0, j, UI.UIButton(0, 0, 20, 20, color=clr))
    new_tt_y += 60

color_wheel_rect = UI.Rectangle(0, 0, 256, 256, image=pygame.image.load('icons/color_picker.png'), color=None)
pick_color_popup.add_item(color_wheel_rect, new_tt.width + 80, pick_color_popup_h - color_wheel_rect.height + 12, name='color_wheel')
old_color_ind = UI.UITooltip(color_wheel_rect.x + 20, color_wheel_rect.y - 84, 54, 64, 1, 1, title_h=20, text=('old', UI.black), font=('arial', 16))
pick_color_popup.add_item(old_color_ind, 20, -84, name='old_color_ind', reference_element=color_wheel_rect)
old_color_ind.set_item(0, 0, UI.Rectangle(0, 0, 62, 62, UI.white))
arrow_rect = UI.Rectangle(0, 0, 64, 64, image=pygame.image.load('icons/arrow_right.png'), color=None)
pick_color_popup.add_item(arrow_rect, old_color_ind.width + 20, 0, name='arrow', reference_element=old_color_ind)
new_color_ind = UI.UITooltip(arrow_rect.x + arrow_rect.width + 15, arrow_rect.y, 54, 64, 1, 1, title_h=20, text=('new', UI.black), font=('arial', 16))
pick_color_popup.add_item(new_color_ind, arrow_rect.width + 15, 0, name='new_color_ind', reference_element=arrow_rect)
new_color_ind.set_item(0, 0, UI.Rectangle(0, 0, 62, 62, UI.red))

sl_x = 40
for i, sl_name in enumerate(('R: ', 'G: ', 'B: ')):
    new_col_slider = UI.UISlider(new_color_ind.x + new_color_ind.width + sl_x + 20,
                                 new_color_ind.y, 40, color_wheel_rect.height + 40,
                                 255, 0, slider_color=UI.red, bg_color=UI.white, color=(80, 80, 80),
                                 text=(sl_name, UI.black), scale_h=color_wheel_rect.height - 15, title_h=20)
    pick_color_popup.add_item(new_col_slider, new_color_ind.width + sl_x + 20, 0,
                              f'slider{i}', reference_element=new_color_ind)
    sl_x += 65

ok_button = UI.UIButton(0, 0, 86, 24, color=UI.gray, text=('Ok', UI.black), font=('arial', 18), frame_col=UI.green, frame_w=2)
pick_color_popup.add_item(ok_button, pick_color_popup_w - ok_button.width - 20, pick_color_popup_h - 15, name='ok_button')
cancel_button = UI.UIButton(0, 0, 86, 24, color=UI.gray, text=('Cancel', UI.black), font=('arial', 18), frame_col=UI.red, frame_w=2)
pick_color_popup.add_item(cancel_button, -(cancel_button.width + 20), 0, name='cancel_button', reference_element=ok_button)

current_popup = None

ui_elements = [basic_color_tooltip, size_slider, paint_tools_tooltip, layers_tooltip, add_layer_button,
               custom_color_tooltip, current_color_indicator, pick_color_button]


def draw_layers(layers1, final_layer=-1):
    if final_layer < 0 or final_layer >= len(layers):
        final_layer = len(layers1) - 1
    if layers1:
        pygame.draw.rect(screen, UI.background, layers1[0][0].get_rectangle())
        for canv_obj in layers1[:final_layer + 1]:
            cv, do_draw = canv_obj
            if do_draw:
                cv.draw(screen)


def setup():
    global brush
    screen.fill(UI.white)
    canvas.draw(screen)
    pygame.display.flip()
    brush = selected_brush


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
    global current_popup

    pygame.draw.rect(screen, UI.background, (layers_tooltip.x - 5, 0, layers_tooltip.width + 10, add_layer_button.x + 10))
    pygame.draw.rect(screen, UI.background, (paint_tools_tooltip.x - 5, paint_tools_tooltip.y - 5, paint_tools_tooltip.width + 10, paint_tools_tooltip.height + 10))

    draw_canvas = bool(layers)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and layers[curr_layer][1]:
                    layers[curr_layer][0].scale(-1, mouse_x, mouse_y)
                    layers[curr_layer][0].hide(screen, True)
                    draw_layers(layers, curr_layer)
                    pygame.display.update(layers[curr_layer][0].get_rectangle())
            if event.button == 5 and layers[curr_layer][1]:
                    layers[curr_layer][0].scale(1, mouse_x, mouse_y)
                    layers[curr_layer][0].hide(screen, True)
                    draw_layers(layers, curr_layer)
                    pygame.display.update(layers[curr_layer][0].get_rectangle())
            if current_popup is None:
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
                                paint_tools_tooltip.selected = button
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
                    for obj_i, obj in enumerate([x[0] for x in layers_tooltip.table]):
                        if obj.mouse_down():
                            layers_tooltip.clicked = obj
                            if isinstance(obj, UI.UIButton):
                                selected_layer_button = obj
                                curr_layer = obj_i // 2
                                draw_layers(layers, curr_layer)
                                obj.color = UI.gray
                                pygame.display.update(layers[curr_layer][0].get_rectangle())
                                break
                            elif isinstance(obj, UI.UITooltip):
                                visibility_toggle_button = obj.table[0][0]
                                delete_button = obj.table[0][1]
                                if visibility_toggle_button.mouse_down():
                                    layers[obj_i // 2][1] = not layers[obj_i // 2][1]
                                    draw_layers(layers, curr_layer)
                                    pygame.display.update(layers[obj_i // 2][0].get_rectangle())
                                    if layers[obj_i // 2][1]:
                                        visibility_toggle_button.image = pygame.image.load('icons/visible.png')
                                    else:
                                        visibility_toggle_button.image = pygame.image.load('icons/invisible.png')
                                    visibility_toggle_button.color = UI.gray
                                    obj.clicked = visibility_toggle_button
                                elif delete_button.mouse_down():
                                    delete_button.color = UI.gray
                                    if layers:
                                        if len(layers_tooltip.table) > 2:
                                            layers_tooltip.pop_item(obj_i - 1, 0)
                                            layers_tooltip.pop_item(obj_i - 1, 0)

                                            layers.pop((obj_i - 1) // 2)
                                            curr_layer = min(curr_layer, len(layers) - 1)

                                            selected_layer_button = layers_tooltip.get_item(curr_layer * 2, 0)

                                            old_add_layer_button_pos = add_layer_button.get_rectangle()
                                            add_layer_button.x, add_layer_button.y = layers_tooltip.x, layers_tooltip.y + layers_tooltip.height
                                            pygame.display.update(old_add_layer_button_pos)

                                            draw_layers(layers, curr_layer)

                                            pygame.display.update(canvas.get_rectangle())
                                    obj.clicked = delete_button
                                    break
                            else:
                                print(obj)

                if add_layer_button.mouse_hover():
                    layers_tooltip.append_item(
                        UI.UIButton(0, 0, layer_square, layer_square,
                                    image=pygame.image.load('icons/default_image.png')))
                    layers_tooltip.append_item(
                        UI.UITooltip(0, 0, int(1.2 * layer_square) - 4, layer_square // 2 - 4, 1, 2, show_grid=False))
                    new_tooltip_element = layers_tooltip.get_item(-1, 0)
                    new_tooltip_element.set_item(0, 0,
                                                 UI.UIButton(0, 0, 16, 16,
                                                             image=pygame.image.load('icons/visible.png')))
                    new_tooltip_element.set_item(0, 1,
                                                 UI.UIButton(0, 0, 16, 16, image=pygame.image.load('icons/delete.png')))
                    layers.append([new_canvas(canv_args), True])
                    curr_layer += 1
                    layers_tooltip.update_item_sizes()
                    old_add_layer_button_pos = add_layer_button.get_rectangle()
                    add_layer_button.x, add_layer_button.y = layers_tooltip.x, layers_tooltip.y + layers_tooltip.height
                    pygame.display.update(old_add_layer_button_pos)
                if pick_color_button.mouse_hover():
                    pick_color_button.onclick()
                    if pick_color_button.state:
                        current_popup = pick_color_popup
                        pick_color_popup.items['old_color_ind'].table[0][0].color = draw_color
                        pick_color_popup.draw(screen)
                    pygame.display.update(pick_color_popup.get_rectangle())
                if custom_color_tooltip.mouse_hover():
                    for item in custom_color_tooltip.table[0]:
                        if item.mouse_down():
                            draw_color = item.color
                            item.tint(True, amt=20)
                            custom_color_tooltip.clicked = item
                            custom_color_tooltip.selected = item

            elif current_popup == pick_color_popup:
                for key in pick_color_popup.items.keys():
                    item = pick_color_popup.items[key]
                    if item.mouse_hover():
                        if 'palette' in key:
                            for color_button in item.table[0]:
                                if color_button.mouse_hover():
                                    color_button.tint(False)
                                    pick_color_popup.items['new_color_ind'].table[0][0].color = color_button.color
                                    r, g, b = color_button.color
                                    pick_color_popup.items['slider0'].set_value(r)
                                    pick_color_popup.items['slider1'].set_value(g)
                                    pick_color_popup.items['slider2'].set_value(b)
                                    color_button.tint(True, amt=20)
                                    item.clicked = color_button
                        elif 'color_wheel' in key:
                            c_w = pick_color_popup.items[key]
                            new_clr = list(c_w.image.get_at((mouse_x - c_w.x, mouse_y - c_w.y)))[:3]
                            pick_color_popup.items['new_color_ind'].table[0][0].color = new_clr
                        elif 'ok_button' in key or 'cancel_button' in key:
                            if 'ok_button' in key:
                                draw_color = pick_color_popup.items['new_color_ind'].table[0][0].color
                                if custom_color_tooltip.selected:
                                    custom_color_tooltip.selected.color = draw_color
                                    custom_color_tooltip.selected.old_color = draw_color
                            screen.fill(UI.white)
                            draw_layers(layers, curr_layer)
                            pygame.display.flip()
                            current_popup = None

        if event.type == pygame.MOUSEBUTTONUP:
            if basic_color_tooltip.clicked:
                basic_color_tooltip.clicked.tint(False)
                basic_color_tooltip.clicked = None
            if paint_tools_tooltip.clicked:
                paint_tools_tooltip.clicked.tint(False)
                paint_tools_tooltip.clicked = None
            if custom_color_tooltip.clicked:
                custom_color_tooltip.clicked.tint(False)
                custom_color_tooltip.clicked = None
            if layers_tooltip.clicked:
                if isinstance(layers_tooltip.clicked, UI.UITooltip):
                    if layers_tooltip.clicked.clicked:
                        layers_tooltip.clicked.clicked.tint(False)
                        layers_tooltip.clicked.clicked = None
                else:
                    layers_tooltip.clicked.tint(False)
            if current_popup == pick_color_popup:
                for key in pick_color_popup.items.keys():
                    if 'palette' in key:
                        if pick_color_popup.items[key].clicked:
                            pick_color_popup.items[key].clicked.tint(False)
                            pick_color_popup.items[key].clicked = None

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
            if current_popup == pick_color_popup:
                for key in pick_color_popup.items.keys():
                    if 'palette' in key:
                        for obj in pick_color_popup.items[key].table[0]:
                            obj.tint(obj.mouse_hover())
                    elif 'slider' in key:
                        sl = pick_color_popup.items[key]
                        if sl.mouse_down():
                            sl.move_slider()
                            new_clr = [pick_color_popup.items[key].value for key in pick_color_popup.items.keys() if 'slider' in key]
                            pick_color_popup.items['new_color_ind'].table[0][0].color = new_clr
            if pygame.mouse.get_pressed()[1] and layers[curr_layer][1]:
                layers[curr_layer][0].pan(mouse_x - old_mouse_x, mouse_y - old_mouse_y)
                layers[curr_layer][0].hide(screen, True)
                draw_layers(layers, curr_layer)
                pygame.display.update(layers[curr_layer][0].get_rectangle())

    if not layers:
        draw_canvas = False

    if draw_canvas and current_popup is None:
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

    for el in ui_elements:
        el.draw(screen)

    selected_layer_button.draw_frame(screen, UI.red, width=5)

    for el in ui_elements:
        pygame.display.update(el.get_rectangle())

    if current_popup is not None:
        current_popup.draw(screen)
        pygame.display.update(current_popup.get_rectangle())

    pygame.display.update((layers_tooltip.x - 5, layers_tooltip.y + layers_tooltip.height,
                           layers_tooltip.width + 10, layers_tooltip.row_size + 20))
    clock.tick(128)
    #print(clock)


setup()
while flag:
    loop()
