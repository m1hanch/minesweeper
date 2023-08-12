from tkinter import *
from tkinter import messagebox

import settings
import utils
from cell import Cell
def game():
    root = Tk()
    root.configure(bg='black')
    root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
    root.title("Minesweeper")
    root.resizable(False, False)

    top_frame = Frame(
        root,
        bg='black',
        width=settings.WIDTH,
        height=utils.height_prct(25),
    )
    top_frame.place(x=0, y=0)

    game_title = Label(top_frame, bg='black', fg='white', text='Minesweeper', font=('', 48))
    game_title.place(x=utils.width_prct(31), y=0)
    left_frame = Frame(
        root,
        bg='black',
        width=utils.width_prct(25),
        height=utils.height_prct(75)
    )
    left_frame.place(x=0, y=utils.height_prct(25))

    center_frame = Frame(
        root,
        bg='black',
        width=utils.width_prct(75),
        height=utils.width_prct(75)
    )
    center_frame.place(y=utils.height_prct(25), x=utils.width_prct(25))

    # photo = PhotoImage(file='mine.png').subsample(3,3)
    for x in range(settings.GRID_SIZE):
        for y in range(settings.GRID_SIZE):
            c = Cell(x, y)
            c.create_btn_object(center_frame)
            # c.cell_btn_object.configure(image = photo)
            c.cell_btn_object.grid(column=x, row=y)

    Cell.create_cell_count_label(left_frame)
    Cell.cell_count_label.place(x=0, y=0)
    Cell.randomize_mines()
    root.mainloop()


if __name__ == '__main__':
    game()

