import random
import sys
from tkinter import Button, Frame, Label, messagebox, PhotoImage
import settings
class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label = None
    answer = False

    def __init__(self,x,y, is_mine = False):
        self.is_mine = is_mine
        self.is_open = False
        self.cell_btn_object = None
        self.is_mine_candidate = False
        self.x = x
        self.y = y
        #Append the object to the 'all' list
        Cell.all.append(self)

    def create_btn_object(self, location: Frame):
        btn = Button(location, width=960//(settings.GRID_SIZE*8), height=540//(settings.GRID_SIZE*16))
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location: Frame):
        lbl = Label(location, text=f'Cells left: {Cell.cell_count}', bg='black', fg='white', font = ("",29))
        Cell.cell_count_label = lbl


    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
            sys.exit()
        else:
            if self.surrounded_cells_mines_length == 0 and not self.is_mine_candidate:
                self.is_mine_candidate = True
                for cell in self.surrounded_cells:
                    cell.show_cell()
                    cell.left_click_actions(event)
        self.show_cell()
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')



    def get_cell_by_axis(self,x,y):
        #Return a cell obj based on the value of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self) -> list:
        cells = list(filter(lambda c: (c.x != self.x or c.y != self.y),
                                       [self.get_cell_by_axis(x,y) for x in range(self.x - 1, self.x + 2)
                                        for y in range(self.y - 1, self.y + 2)
                                        if(settings.GRID_SIZE>x >= 0 and settings.GRID_SIZE>y >= 0)]))
        return cells

    @property
    def surrounded_cells_mines_length(self) -> int:
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_open:
            Cell.cell_count -= 1
            if self.surrounded_cells_mines_length == 0:
                self.cell_btn_object.configure(bg = '#bababa')
            else:
                self.cell_btn_object.configure(bg = '#bababa',text = self.surrounded_cells_mines_length)
            if Cell.cell_count_label:
                Cell.cell_count_label.configure(text = f'Cells left: {Cell.cell_count}')
            if Cell.cell_count == settings.MINES_COUNT:
                messagebox.showinfo('Victory!', "Congratulations! You've won")
                sys.exit()
        self.is_open = True

    def show_mine(self):
        bomb_photo = PhotoImage(file='mine.png')
        #можливий варіант із subsample
        #bomb_photo = PhotoImage(file='mine.png').subsample(20,20)

        #Cell.all повертає список усіх клітинок (об'єктів Cell), які були створені
        for cell in Cell.all:
            #якщо клітинка є міною то потрібно показати усі міни із зображенням і зупинити гру
            if cell.is_mine:
                cell.cell_btn_object.configure(image = bomb_photo)
        messagebox.showinfo('The end', "You've clicked on a mine")

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg='orange')
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(bg='SystemButtonFace')
            self.is_mine_candidate = False


    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True
            picked_cell.cell_btn_object.configure(text = 'bomb')

    def __repr__(self):
        return f'Cell({self.x}, {self.y})'