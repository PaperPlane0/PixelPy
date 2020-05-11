import pygame
import funcs

aqua = (0, 255, 255, 0)   # морская волна
black = (0, 0, 0, 0)   # черный
blue = (0, 0, 255, 0)   # синий
fuchsia = (255, 0, 255, 0)   # фуксия
gray = (128, 128, 128, 0)   # серый
green = (0, 128, 0, 0)   # зеленый
lime = (0, 255, 0, 0)   # цвет лайма
orange = (255, 128, 0)  # оранжевый
maroon = (128, 0, 0, 0)   # темно-бордовый
navy_blue = (0, 0, 128, 0)   # темно-синий
olive = (128, 128, 0, 0)   # оливковый
purple = (128, 0, 128, 0)   # фиолетовый
red = (255, 0, 0, 0)   # красный
silver = (192, 192, 192, 0)   # серебряный
teal = (0, 128, 128, 0)   # зелено-голубой
white = (255, 255, 255, 0)   # белый
yellow = (255, 255, 0, 0)   # желтый
light_gray = (204, 204, 204)

# warm = [(238, 0, 0), (238, 238, 0), (238, 0, 238), (238, 18, 137), (238, 44, 44), (238, 48, 167), (238, 58, 140), (238, 59, 59), (238, 64, 0), (238, 92, 66), (238, 99, 99), (238, 106, 80), (238, 118, 0), (238, 118, 33), (238, 121, 66), (238, 130, 98), (238, 154, 0), (238, 154, 73), (238, 173, 14), (238, 180, 34), (238, 201, 0)]
# cold = [(0, 0, 238), (67, 110, 238), (92, 172, 238), (0, 178, 238), (0, 229, 238), (0, 238, 238), (0, 238, 0), (0, 238, 118), (78, 238, 148), (92, 172, 238), (118, 238, 0), (122, 103, 238), (145, 44, 238), (159, 121, 238), (178, 58, 238), (209, 95, 238)]

colors = [[0, 0, 0], [24,24,24], [48,48,48], [64,64,64], [128,128,128],[155,155,155],[200,200,200],[255,255,255],
           [27,38,49],[40,55,71],[46,64,83],[52,73,94],[93,109,126],[133,146,158],[174,182,191],[214,219,223],
           [77,86,86],[95,106,106],[113,125,126],[149,165,166],[170,183,184],[191,201,202],[213,219,219],[229,232,232],
           [98,101,103],[121,125,127],[144,148,151],[189,195,199],[202,207,210],[229,231,233],[248,249,249],[255,255,255],
           [100,30,22],[123,36,28],[146,43,33],[192,57,43],[205,97,85],[217,136,128],[230,176,170],[242,215,213],
           [120,40,31],[148,49,38],[176,58,46],[220,76,60],[236,112,99],[241,148,138],[245,183,177],[250,219,216],
           [74,35,90],[91,44,111],[108,52,131],[142,68,173],[165,105,189],[187,143,206],[210,180,222],[232,218,239],
           [21,67,96],[26,82,118],[31,97,141],[41,128,185],[84,153,199],[127,179,213],[169,204,227],[212,230,241],
           [20,90,50],[25,111,61],[34,141,84],[34,174,96],[82,190,128],[125,206,160],[169,223,191],[212,239,223],
           [125,102,8],[154,125,10],[183,149,11],[230,196,15],[244,208,63],[247,220,111],[249,231,159],[252,243,207],
           [126,81,9],[156,100,12],[185,119,14],[242,156,18],[245,176,65],[248,196,113],[250,215,160],[253,235,208],
           [110,44,0],[135,54,0],[160,64,0],[211,84,0],[220,118,51],[229,152,102],[237,187,153],[246,221,204]
           ]

colors2 = {'Skins': ([241,157,154],[241,179,164],[246,209,190],[252,225,213],[242,193,173],[241,175,153]),
           'Soft Hues': ([128,232,221],[124,194,246],[175,129,228],[231,132,186],[249,193,160],[183,246,175]),
           'Forest': ([100,93,62],[130,123,92],[156,151,115],[86,113,80],[46,71,43],[16,42,10]),
           'Sunset': ([252,120,150],[193,107,188],[152,89,197],[108,66,196],[85,56,193],[30,171,215]),
           'Coffee': ([92,58,42],[121,84,63],[172,138,104],[200,173,139],[223,213,191],[206,159,85])}

background = white

draw = pygame.draw

brush_icon = pygame.image.load('icons/brush.png')
circle_icon = pygame.image.load('icons/circle.png')
eraser_icon = pygame.image.load('icons/eraser.png')
fill_icon = pygame.image.load('icons/fill.png')
pencil_icon = pygame.image.load('icons/pencil.png')
color_pick_icon = pygame.image.load('icons/color_pick.png')
rect_icon = pygame.image.load('icons/rect.png')
swap_col_icon = pygame.image.load('icons/swap_col.png')
rotate_icon = pygame.image.load('icons/rotate.png')
move_icon = pygame.image.load('icons/move.png')
line_icon = pygame.image.load('icons/line.png')
mirror_icon = pygame.image.load('icons/mirror.png')
icons = [brush_icon, pencil_icon, eraser_icon, fill_icon, color_pick_icon, swap_col_icon, circle_icon, rect_icon, line_icon, rotate_icon, move_icon, mirror_icon]
draw_tools = {}

class UIItem:
    def __init__(self, x, y, width, height, image=None, color=None, text=('', white), font=('arial', 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.color = color
        self.text = text[0]
        self.text_col = text[1]
        self.font_name = font[0]
        self.font_size = font[1]
        self.old_color = color

    def mouse_hover(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x in range(self.x, self.x + self.width) and mouse_y in range(self.y, self.y + self.height):
            return True
        return False

    def get_rectangle(self):
        x = max(0, self.x - 5)
        y = max(0, self.y - 5)
        return (x, y, self.width + 10, self.height + 10)

    def mouse_down(self):
        if self.mouse_hover() and pygame.mouse.get_pressed()[0] == 1:
            return True
        return False

    def tint(self, enabled, amt=2):
        if enabled:
            if self.color:
                self.color = funcs.decrease_brightness(self.old_color, amt=amt)
            else:
                self.color = gray
        else:
            if self.color:
                self.color = self.old_color

    def draw_frame(self, surface, color1, width=2):
        padding = width // 2
        pygame.draw.rect(surface, color1, (self.x + padding, self.y + padding, self.width - 2 * padding, self.height - 2 * padding), width)

    def draw(self, surface, color_override=None):
        col = black
        if self.color:
            col = self.color
        if color_override:
            col = color_override
        if self.image:
            img = pygame.transform.scale(self.image, (self.width, self.height))
            if self.color:
                funcs.colorize(img, self.color)
            surface.blit(img, (self.x, self.y))
        else:
            rgb_col = funcs.rgba_to_rgb(col, white)
            draw.rect(surface, rgb_col, ((self.x, self.y), (self.width, self.height)))
        if self.text:
            fsize = self.font_size
            if not fsize:
                fsize = min((self.height - 2), (self.width // len(self.text)))
            font = pygame.font.SysFont(self.font_name, fsize, bold=True)
            title = font.render(self.text, 0, self.text_col)
            text_rect = title.get_rect()
            text_len = text_rect.width
            text_height = text_rect.height
            tx = (self.width - text_len) // 2
            ty = (self.height - text_height) // 2
            surface.blit(title, (self.x + tx, self.y + ty))

    def hide(self, on, surface):
        if on:
            self.draw(surface, background)


class UIButton(UIItem):
    def __init__(self, x, y, width, height, action=None, image=None, color=None, text=('', white), font=('arial', 0)):
        super().__init__(x, y, width, height, image=image, color=color, text=text, font=font)
        self.action = action

    def onclick(self):
        if self.mouse_down() and self.action:
            if isinstance(self.action, funcs.tool):
                self.action.use()
            else:
                return self.action(self)


class Rectangle(UIItem):
    def __init__(self, x, y, width, height, color=white, image=None, text=('', white), font=('arial', 0)):
        super().__init__(x, y, width, height, color=color, image=image, text=text, font=font)
        self.neighbors = []


class Canvas(UIItem):
    def __init__(self, x, y, width, height, rows, cols, bg_col=white):
        super().__init__(x, y, width, height)
        self.rows = rows
        self.cols = cols
        self.row_size = height // rows
        self.col_size = width // cols
        self.paint_history = []
        self.bg_col = bg_col
        cs, rs = self.col_size, self.row_size
        self.table = [[Rectangle((i * cs + x), (j * rs + y), cs, rs, color=bg_col) for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if i:
                    self.table[i][j].neighbors.append(self.table[i - 1][j])
                if i < rows - 1:
                    self.table[i][j].neighbors.append(self.table[i + 1][j])
                if j:
                    self.table[i][j].neighbors.append(self.table[i][j - 1])
                if j < cols - 1:
                    self.table[i][j].neighbors.append(self.table[i][j + 1])

    def merge_img(self, col, row, img, color=None, surface=None):
        image = img
        history_obj = []
        x, y = image.get_size()
        if min(x, y) == 0:
            return
        if color:
            if color != image.get_at((x // 2, y // 2)):
                funcs.colorize(image, color)
        lm_y, lm_x = min(y, self.rows - 1), min(x, self.cols - 1)
        for i in range(lm_y):
            for j in range(lm_x):
                pix = image.get_at((i, j))
                p_row = min((row + i - y // 2), self.rows - 1)
                p_col = min((col + j - x // 2), self.cols - 1)
                if self.table[p_row][p_col].color != pix and pix[3] != 0:
                    cl = self.table[p_row][p_col].color
                    history_obj.append({self.table[p_row][p_col]: self.table[p_row][p_col].color})
                    self.table[p_row][p_col].color = funcs.rgba_to_rgb(cl, pix)
                    if surface:
                        self.table[p_row][p_col].draw(surface)
        self.paint_history.append(history_obj)

    def pixel_paint(self, col, row, color=black, brush=None, size=(1, 1), alpha=None, surface=None):
        row = min(abs(row), self.rows - 1)
        col = min(abs(col), self.cols - 1)
        startrow = max((row - size[1] // 2), 0)
        endrow = min((row + size[1] // 2), self.rows - 1)
        startcol = max((col - size[0] // 2), 0)
        endcol = min((col + size[0] // 2), self.cols - 1)
        if brush:
            if isinstance(brush, pygame.Surface):
                if brush.get_size() != size:
                    br = pygame.transform.scale(brush, size)
                else:
                    br = brush
                self.merge_img(col, row, br, color, surface=surface)
            elif callable(brush):
                brush(self, row, col, color, surface=surface)
        else:
            history_obj = []
            # print(f'srow:{startrow}, endrow:{endrow}, startcol:{startcol}, endcol:{endcol}')
            if alpha:
                color = (*color[:3], alpha)
            for i in range(startrow, endrow + 1):
                for j in range(startcol, endcol + 1):
                    if self.table[i][j].color != color:
                        history_obj.append([{self.table[i][j]: self.table[i][j].color}])
                        self.table[i][j].color = color
                        if surface:
                            self.table[i][j].draw(surface)
            self.paint_history.append(history_obj)
        if len(self.paint_history) > 100:
            self.paint_history.pop(0)
        return max(0, startrow - 5), max(0, startcol - 5), min(self.rows, endrow + 5), min(self.cols, endcol + 5)

    def undo(self):
        if self.paint_history:
            history_obj = self.paint_history.pop()
            for obj in history_obj:
                pixel = obj.key
                color = obj.value
                pixel.color = color

    def line(self, p0, p1):
        points = []
        n = funcs.diagonal_distance(p0, p1)
        for step in range(n + 1):
            t = step / n if n else 0
            lerp_x, lerp_y = funcs.lerp_point(p0, p1, t)
            row, col = funcs.grid_snap(lerp_x, lerp_y, self.x, self.y, self.row_size, self.col_size)
            points.append((int(row), int(col)))
        return points

    def line_paint(self, old_mpos, new_mpos, color=black, brush=None, size=(1, 1), alpha=255, surface=None):
        line = self.line(old_mpos, new_mpos)
        if min(size) == 0:
            return
        if brush and isinstance(brush, pygame.Surface):
            step = max(min(size) // 3, 1)
        else:
            step = 1
        for i in range(1, len(line), step):
            row, col = line[i]
            changed = self.pixel_paint(col, row, color=color, size=size, brush=brush, alpha=alpha, surface=surface)
        return changed

    def draw(self, surface, col_override=None, area=None):
        if area:
            startrow, startcol, endrow, endcol = area
            for i in range(startrow, endrow + 1):
                for j in range(startcol, endcol + 1):
                    self.table[i][j].draw(surface)
            return
        draw.rect(surface, black, ((self.x - 1, self.y - 1), (self.width + 2, self.height + 2)), 2)
        for row in self.table:
            for px in row:
                if px.color != background:
                    px.draw(surface, color_override=col_override)

    def clear(self):
        for row in self.table:
            for px in row:
                px.color = background
        self.paint_history = []

    def hide(self, surface, on):
        if on:
            self.draw(surface, col_override=background)


class UISlider(UIItem):
    def __init__(self, x, y, width, height, max_v, min_v, slider_color=None, color=black, bg_color=light_gray, image=None, scale_w=6, scale_h=None, title_h=20, text=('', black), font=('arial', 15)):
        super().__init__(x, y + title_h, width, height, color=color, text=text, font=font)
        self.title_x = x
        self.title_y = y
        self.title_h = title_h
        self.slider_color = color
        if slider_color:
            self.slider_color = slider_color
        if scale_h:
            self.scale_h = scale_h
        else:
            self.scale_h = self.height - scale_w * 2
        scale_indent = max(2, (self.height - self.scale_h) // 2)
        self.scale_y = self.y + scale_indent
        self.scale_x = x + (width - scale_w) // 2
        self.scale_w = scale_w
        self.min_v = min_v
        self.max_v = max_v
        self.bg_color = bg_color
        self.slider_r = scale_w
        self.slider_y = self.scale_y + self.scale_h - self.slider_r
        self.value = min_v
        self.title = Rectangle(x, y, width + 1, title_h, color=bg_color, image=image, text=text, font=font)

    def move_slider(self):
        mouse_y = pygame.mouse.get_pos()[1]
        self.slider_y = funcs.constrain(mouse_y, self.scale_y, (self.scale_y + self.scale_h))
        self.value = self.max_v - funcs.map_value(self.slider_y, self.scale_y, (self.scale_y + self.scale_h), self.min_v, self.max_v)
        text = self.title.text
        self.title.text = text[:text.find(' ') + 1] + str(self.value)

    def draw(self, surface):
        draw.rect(surface, self.bg_color, ((self.x, self.y), (self.width, self.height)))
        self.title.draw(surface)
        draw.line(surface, self.color, (self.x, self.y), (self.x + self.width, self.y))
        draw.line(surface, self.color, (self.title_x, self.title_y), (self.title_x + self.width, self.title_y))
        draw.line(surface, self.color, (self.title_x, self.title_y), (self.title_x, self.y))
        draw.line(surface, self.color, (self.title_x + self.width, self.title_y), (self.title_x + self.width, self.y))
        draw.line(surface, self.color, (self.x, self.y), (self.x, self.y + self.height))
        draw.line(surface, self.color, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height))
        draw.line(surface, self.color, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height))
        r = self.scale_w // 2
        s_y, s_h = self.scale_y + r, self.scale_h - self.scale_w
        draw.rect(surface, self.color, ((self.scale_x, s_y), (self.scale_w, s_h)))
        draw.circle(surface, self.color, (self.scale_x + r, s_y), r)
        draw.circle(surface, self.color, (self.scale_x + r, s_y + s_h), r)
        draw.circle(surface, self.slider_color, (self.scale_x + r, self.slider_y), self.slider_r)

    def get_rectangle(self):
        x = max(0, self.x - 5)
        y = max(0, self.y - 5 - self.title_h)
        return (x, y, self.width + 10, self.height + 10 + self.title_h)


class UITooltip(UIItem):
    def __init__(self, x, y, width, height, rows, cols, color=black, bg_color=light_gray, image=None, title_h=0, text=('', black), font=('arial', 0), show_grid=True):
        super().__init__(x, y + title_h, width, height + title_h, color=color)
        self.title_x = x
        self.title_y = y
        self.tinted = None
        self.clicked = None
        self.show_grid = show_grid
        self.rows = rows
        self.cols = cols
        self.title_h = title_h
        self.row_size = height // rows
        self.col_size = width // cols
        rs, cs = self.row_size, self.col_size
        self.title = Rectangle(x, y, width + 1, title_h, color=bg_color, image=image, text=text, font=font)
        self.table = [[Rectangle((x + 1 + j * cs), (y + title_h + 1 + i * rs), cs - 1, rs - 1, color=background) for j in range(cols)] for i in range(rows)]

    def draw_grid(self, surface):
        draw.line(surface, self.color, (self.title_x, self.title_y), (self.title_x + self.width, self.title_y))
        draw.line(surface, self.color, (self.title_x, self.title_y), (self.title_x, self.y))
        draw.line(surface, self.color, (self.title_x + self.width, self.title_y), (self.title_x + self.width, self.y))
        hor_space, vert_space = self.col_size, self.row_size
        x, y = self.x, self.y
        for i in range(self.rows + 1):
            draw.line(surface, self.color, (x, y), (x + self.width, y))
            y += vert_space
        for i in range(self.cols + 1):
            draw.line(surface, self.color, (x, self.y), (x, y - self.row_size))
            x += hor_space

    def get_rectangle(self):
        x = max(0, self.x - 5)
        y = max(0, self.y - 5 - self.title_h)
        return (x, y, self.width + 10, self.height + 10 + self.title_h)

    def update_item_sizes(self):
        self.row_size = (self.height - self.title_h) // self.rows
        self.col_size = self.width // self.cols
        for row, line in enumerate(self.table):
            for col, item in enumerate(line):
                item.height = self.row_size - 3
                item.width = self.col_size - 3
                item.x = self.x + 2 + col * self.col_size
                item.y = self.y + 2 + row * self.row_size
                if isinstance(item, UITooltip):
                    item.update_item_sizes()

    def set_table_size(self, rows1=0, cols1=0):
        if rows1 == 0:
            rows1 = self.rows
        if cols1 == 0:
            cols1 = self.cols
        self.rows = rows1
        self.cols = cols1
        while len(self.table) < rows1:
            self.table.append([None for i in range(self.cols)])
            for i in range(self.cols):
                self.set_item(-1, i, Rectangle(1, 1, 1, 1, white))

        while len(self.table[0]) < cols1:
            for i, line in enumerate(self.table):
                line.append(None)
                self.set_item(i, -1, Rectangle(1, 1, 1, 1, white))

        while len(self.table) > rows1:
            self.table.pop()

        while len(self.table[0]) > cols1:
            for line in self.table:
                line.pop()
        self.update_item_sizes()

    def get_item(self, row1, col1):
        return self.table[row1][col1]

    def append_item(self, item):
        if not self.table or len([x for x in self.table[-1] if isinstance(x, Rectangle) or x is None]) == 0:
            self.height += self.row_size
            self.rows += 1
            self.table.append([None for i in range(self.cols)])
            self.set_item(-1, 0, item)
            for i in range(1, self.cols):
                self.set_item(-1, i, Rectangle(1, 1, 1, 1, white))
        else:
            occupied = len([x for x in self.table[-1] if isinstance(x, UIButton)])
            self.set_item(-1, occupied, item)

    def pop_item(self, index=-1, col=-1):
        if self.table:
            if len(self.table[-1]) == 1:
                self.table.pop(index)
                self.height -= self.row_size
                self.rows -= 1
                self.update_item_sizes()
            else:
                self.table[-1].pop(col)

    def set_item(self, row, col, item):
        item.height = self.row_size - 3
        item.width = self.col_size - 3
        xcol, xrow = col, row
        if col < 0:
            xcol = xcol * -1 + 1
        if row < 0:
            xrow = xrow * -1 + 1
        item.x = self.x + 2 + xcol * self.col_size
        item.y = self.y + 2 + xrow * self.row_size
        self.table[row][col] = item

    def draw(self, surface):
        self.title.draw(surface)
        if self.show_grid:
            self.draw_grid(surface)
        for row in self.table:
            for item in row:
                item.draw(surface)


class Popup(UIItem):
    def __init__(self, x, y, width, height, color=black, starting_items = [], bg_color=light_gray, image=None, title_h=0, text=('', black), font=('arial', 0)):
        super().__init__(x, y + title_h, width, height + title_h, color=color)
        self.title_x = x
        self.title_y = y
        self.items = starting_items
        self.tinted = None
        self.clicked = None
        self.bg_color = bg_color
        self.image = image
        self.title_h = title_h
        self.title = Rectangle(x, y, width, title_h, color=bg_color, image=image, text=text, font=font)

    def add_item(self, item, x, y, size = None, reference_element=None):
        if reference_element:
            if reference_element in self.items:
                item.x = reference_element.x + x
                item.y = reference_element.y + y
        else:
            item.x = self.x + x
            item.y = self.y + y
        if size:
            item.width, item.height = size
        else:
            item.width, item.height = min(self.width, item.width), min(self.height, item.height)
        self.items.append(item)

    def draw(self, surface, color_override=None):
        draw.rect(surface, self.bg_color, (self.x, self.title_y, self.width, self.height + self.title_h))
        if self.image:
            img = pygame.transform.scale(self.image, (self.width, self.height))
            surface.blit(img)
        for item in self.items:
            item.draw(surface)
        draw.rect(surface, self.color, (self.x, self.title_y, self.width, self.height + self.title_h), 2)
        draw.line(surface, self.color, (self.x, self.y), (self.x + self.width, self.y), 2)