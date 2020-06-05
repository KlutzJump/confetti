import cairo, random

'''
A GridCanvas consists of a grid of smaller "subcanvases" onto which each
iteration is drawn.

Explanation of initializer args:
    title: filename of final image
    w: subcanvas width
    h: subcanvas height
    rows: number of grid rows
    cols: number of grid columns
    gap: empty space "padding" between subcanvases (as well as between
            subcanvases and edges)
    bgcolor: background color (r,g,b) of the entire canvas
'''

class GridCanvas:
    def __init__(self, title, w, h, rows, cols, gap, bgcolor):
        self.title = str(title) + ".svg"
        self.w = w
        self.h = h
        self.rows = rows
        self.cols = cols
        self.n = self.rows * self.cols
        self.gap = gap

        # create the surface, context, and fill with bgcolor
        surface_w = (self.rows * w) + ((self.rows + 1) * self.gap)
        surface_h = (self.cols * h) + ((self.cols + 1) * self.gap)
        self.surface = cairo.SVGSurface(self.title, surface_w, surface_h)
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgb(bgcolor[0], bgcolor[1], bgcolor[2])
        self.context.rectangle(0, 0, surface_w, surface_h)
        self.context.fill()

    # self.run() iterates self.draw() over each subcanvas
    def run(self):
        current_row = 1
        current_col = 1

        for _ in range(self.n):
            '''
            Boundaries of rectangular "subcanvas" given by set of four points
            at each corner:
                a: top left
                b: top right
                c: bottom left
                d: bottom right

            Each point is referenced by x coordinate 0 and y coordinate 1.
            Half are redundant, so only a0, a1, b0, b1 are used
            '''
            a0 = (self.gap * current_col) + (self.w * (current_col - 1))
            a1 = (self.gap * current_row) + (self.h * (current_row - 1))
            b0 = (self.gap * current_col) + (self.w * current_col)
            c1 = (self.gap * current_row) + (self.h * current_row)

            self.draw(a0, b0, a1, c1)

            # move to next cell, shift down a row when current row fills up
            current_col = (current_col + 1) % (self.cols + 1)

            if current_col == 0:
                current_col = 1
                current_row += 1

    # the drawing that occures on a subcanvas
    def draw(self, a0, b0, a1, c1):
        # randomly get a color and n number of triangles
        r = random.random()
        g = random.random()
        b = random.random()
        n = random.randint(10, 50)
        
        for _ in range(n):
            # slightly nudge the color of each triangle
            new_r = r + random.randrange(-5, 5, 1) / 50
            new_g = g + random.randrange(-5, 5, 1) / 50
            new_b = b + random.randrange(-5, 5, 1) / 50

            self.context.set_source_rgb(new_r, new_g, new_b)
            self.context.set_line_width(1)

            # randomly get 2 vertices
            x1 = random.randrange(a0, b0)
            y1 = random.randrange(a1, c1)
            x2 = random.randrange(a0, b0)
            y2 = random.randrange(a1, c1)

            # create with 2 random vertices and one vertex at the subcanvas
            # center
            self.context.move_to(a0 + ((b0 - a0) / 2), a1 + ((c1 - a1) / 2))
            self.context.line_to(x1, y1)
            self.context.line_to(x2, y2)
            self.context.fill()

def main():
    canvas = GridCanvas("glyph3", 1000, 1000, 7, 7, 50, (0.8, 0.8, 0.8))
    canvas.run()

if __name__ == "__main__":
    main()