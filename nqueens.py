import board
import itertools
import urwid

class NQueensModel(object):
    def __init__(self, N=4):
        self.N = N
        self.solution_list = []
        self.solution_index = None
        self.number_of_solutions = 0

    def solve(self):
        self.solution_list = []
        self.solution_index = None
        self.number_of_solutions = 0
        for perm in itertools.permutations(range(self.N)):
            diagonal1 = set()
            diagonal2 = set()
            for i in range(self.N):
                diagonal1.add(perm[i] + i)  # test \ diagonal
                diagonal2.add(perm[i] - i)  # test / diagonal
            if self.N == len(diagonal1) == len(diagonal2):
                self.solution_list.append(list(perm))
                self.number_of_solutions += 1
        if self.solution_list:
            self.solution_index = 0

    def set_n(self, N):
        self.N = N

    def get_current_solution(self):
        if self.number_of_solutions > 0:
            return self.solution_list[self.solution_index]
        else:
            return None

    def get_prev_solution(self):
        if self.solution_index > 0 and \
                self.solution_index is not None:
            self.solution_index -= 1
            return self.solution_list[self.solution_index]
        else:
            return None

    def get_next_solution(self):
        if self.solution_index < self.number_of_solutions - 1 and \
                self.solution_index is not None:
            self.solution_index += 1
            return self.solution_list[self.solution_index]
        else:
            return None

    def get_number_of_solutions(self):
        return self.number_of_solutions

    def get_solution_index(self):
        return self.solution_index

class NQueensView(urwid.WidgetWrap):
    palette = [
        ('empty_black', 'black', 'black'),
        ('empty_white', 'white', 'white'),
        ('queen_on_black', 'light blue', 'black', 'standout'),
        ('queen_on_white', 'light blue', 'white', 'standout'),
        ('body', 'black', 'light gray', 'standout'),
        ('screen_edge', 'light blue', 'dark blue'),
        ('main_shadow', 'dark gray', 'black'),
        ('line', 'black', 'light gray', 'standout'),
        ('button', 'white', 'dark blue', 'standout'),
    ]

    def __init__(self, controller, N=4):
        self.controller = controller
        self.N = N
        self.board = None
        self.controls = None
        super(NQueensView, self).__init__(self.main_window())

    def button(self, text, function):
        w = urwid.Button(text, function)
        w = urwid.AttrWrap(w, 'button')
        return w

    def control_panel(self):
        control_widgets = [
            urwid.Text('Number of queens: ' + str(self.N)),
            urwid.GridFlow([
                self.button('-', self.on_decrease_button),
                self.button('+', self.on_increase_button),
            ], cell_width=5, h_sep=2, v_sep=0, align='center'),
            urwid.Divider(),
            urwid.Text('Number of solutions: 0'),
            urwid.GridFlow([
                self.button('Solve', self.on_solve_button)
            ], cell_width=9, h_sep=0, v_sep=0, align='center'),
            urwid.Divider(),
            urwid.Text('Solution: 0', 'center'),
            urwid.GridFlow([
                self.button('Prev', self.on_prev_button),
                self.button('Next', self.on_next_button),
            ], cell_width=8, h_sep=2, v_sep=0, align='center'),
            urwid.Divider(),
            urwid.Divider(),
            urwid.Divider(),
            urwid.GridFlow([
                self.button('Quit', self.quit)
            ], cell_width=8, h_sep=0, v_sep=0, align='center'),
        ]
        w = urwid.ListBox(urwid.SimpleListWalker(control_widgets))
        return w

    def main_shadow(self, w):
        bg = urwid.AttrWrap(urwid.SolidFill(u'\u2592'), 'screen_edge')
        shadow = urwid.AttrWrap(urwid.SolidFill(u' '), 'main_shadow')
        bg = urwid.Overlay(shadow, bg,
            ('fixed left', 3), ('fixed right', 1),
            ('fixed top', 2), ('fixed bottom', 1))
        w = urwid.Overlay(w, bg,
            ('fixed left', 2), ('fixed right', 3),
            ('fixed top', 1), ('fixed bottom', 2))
        return w

    def main_window(self):
        self.board = board.Board(self.N)
        board_wrap = urwid.Filler(self.board, valign='top')
        vline = urwid.AttrWrap(urwid.SolidFill(u'\u2502'), 'line')
        self.controls = self.control_panel()
        w = urwid.Columns([
            board_wrap,
            ('fixed', 1, vline),
            ('fixed', 25, self.controls),
        ], dividechars=1, focus_column=2)
        w = urwid.Padding(w, ('fixed left', 1), ('fixed right', 0))
        w = urwid.AttrWrap(w, 'body')
        w = urwid.LineBox(w)
        w = urwid.AttrWrap(w, 'line')
        w = self.main_shadow(w)
        return w

    def on_decrease_button(self, w):
        if self.N > 1:
            self.N -= 1
            self.controller.set_n(self.N)
            self.controls.body[0].set_text('Number of queens: ' + str(self.N))
            self.controls.body[3].set_text('Number of solutions: 0')
            self.controls.body[6].set_text('Solution: 0')
            self.board.set_n(self.N)

    def on_increase_button(self, w):
        self.N += 1
        self.controller.set_n(self.N)
        self.controls.body[0].set_text('Number of queens: ' + str(self.N))
        self.controls.body[3].set_text('Number of solutions: 0')
        self.controls.body[6].set_text('Solution: 0')
        self.board.set_n(self.N)

    def on_solve_button(self, w):
        first_solution, number_of_solutions = self.controller.solve()
        if first_solution is not None and number_of_solutions != 0:
            self.board.draw_solution(first_solution)
            self.controls.body[3].set_text('Number of solutions: ' + str(number_of_solutions))
            self.controls.body[6].set_text('Solution: 1')
        else:
            self.controls.body[6].set_text('Solution: 0')

    def on_prev_button(self, w):
        prev_solution, solution_index = self.controller.get_prev_solution()
        if prev_solution is not None:
            self.board.draw_solution(prev_solution)
            self.controls.body[6].set_text('Solution: ' + str(solution_index + 1))

    def on_next_button(self, w):
        next_solution, solution_index = self.controller.get_next_solution()
        if next_solution is not None:
            self.board.draw_solution(next_solution)
            self.controls.body[6].set_text('Solution: ' + str(solution_index + 1))

    def quit(self, w):
        raise urwid.ExitMainLoop()

class NQueensController(object):
    def __init__(self, N=4):
        self.N = N
        self.model = NQueensModel(self.N)
        self.view = NQueensView(self, self.N)
        self.loop = None

    def set_n(self, N):
        self.N = N
        self.model.set_n(self.N)

    def solve(self):
        self.model.solve()
        return self.model.get_current_solution(), self.model.get_number_of_solutions()

    def get_prev_solution(self):
        return self.model.get_prev_solution(), self.model.get_solution_index()

    def get_next_solution(self):
        return self.model.get_next_solution(), self.model.get_solution_index()

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.run()

def main():
    NQueensController().main()

if __name__ == '__main__':
    main()
