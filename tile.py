import urwid

class Tile(urwid.GridFlow):
    def __init__(self, queen=False, color='black'):
        self.queen = queen
        self.color = color
        cells = []
        if self.color == 'black':
            for i in range(18):
                if i == 8 and self.queen:
                    cells.append(urwid.Text(('queen_on_black', u'\u265B'), 'center'))
                else:
                    cells.append(urwid.Text(('empty_black', u'\u0020')))
        elif self.color == 'white':
            for i in range(18):
                if i == 8 and self.queen:
                    cells.append(urwid.Text(('queen_on_white', u'\u265B'), 'center'))
                else:
                    cells.append(urwid.Text(('empty_white', u'\u0020')))
        super(Tile, self).__init__(cells, cell_width=1, h_sep=0, v_sep=0, align='left')

    def flip_to_queen_tile(self):
        self.queen = True
        if self.color == 'black':
            self.cells[8] = urwid.Text(('queen_on_black', u'\u265B'), 'center')
        elif self.color == 'white':
            self.cells[8] = urwid.Text(('queen_on_white', u'\u265B'), 'center')

    def flip_to_empty_tile(self):
        self.queen = False
        if self.color == 'black':
            self.cells[8] = urwid.Text(('empty_black', u'\u0020'), 'center')
        elif self.color == 'white':
            self.cells[8] = urwid.Text(('empty_white', u'\u0020'), 'center')
