if True:
    import tkinter as tk
    from random import shuffle
    from tkinter.messagebox import showinfo, showerror

    colors = {
        0: '#ffffff',
        1: '#0000ff',
        2: '#ff0000',
        3: '#5e0073',
        4: '#9300ff',
        5: '#9300ff',
        6: '#9300ff',
        7: '#9300ff',
        8: '#9300ff',
    }


    class MyButton(tk.Button):

        def __init__(self, master, x, y, *args, number=0, **kwargs):
            super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
            self.x = x
            self.y = y
            self.number = number
            self.is_mine = False
            self.count_bomb = 0
            self.is_open = False

        def __repr__(self):
            return f'MyButton #{self.number} x{self.x} y{self.y} {self.is_mine}'


    class MineSweeper:
        window = tk.Tk()
        # icon = tk.PhotoImage(file='bomb.png')
        # window.iconphoto(False, icon)
        window.title('Mine Sweeper')
        COLUMNS = 10
        ROW = 10
        MINES = 10
        flag_count = 0
        flag_list = []
        IS_GAME_OVER = False
        IS_FIRST_CLICK = True

        def __init__(self):
            self.buttons = []
            for i in range(MineSweeper.ROW + 2):
                temp = []
                for j in range(MineSweeper.COLUMNS + 2):
                    btn = MyButton(MineSweeper.window, x=j, y=i)
                    btn.config(command=lambda button_=btn: self.click(button_))
                    btn.bind("<Button-3>", self.right_click)
                    temp.append(btn)
                self.buttons.append(temp)

        def click(self, clicked_button: MyButton):

            if self.IS_GAME_OVER:
                return None

            if self.IS_FIRST_CLICK:
                self.insert_mines(clicked_button.number)
                self.count_mines_in_buttons()
                self.print_buttons()
                self.IS_FIRST_CLICK = False

            if clicked_button.is_mine:
                clicked_button.config(background='red')
                clicked_button.is_open = True
                self.IS_GAME_OVER = True
                for i in range(1, MineSweeper.ROW + 1):
                    for j in range(1, MineSweeper.COLUMNS + 1):
                        btn = self.buttons[i][j]
                        if btn.is_mine:
                            btn['text'] = '*'
                showinfo('Game over', 'ты БАБАХНУЛ!!!')
            else:
                color = colors.get(clicked_button.count_bomb, 'black')
                if clicked_button.count_bomb:
                    clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                    clicked_button.is_open = True
                else:
                    clicked_button.config(text='', disabledforeground=color)

            clicked_button.config(state='disabled')
            clicked_button.config(relief=tk.SUNKEN)

        def reload(self):
            [child.destroy() for child in self.window.winfo_children()]
            self.__init__()
            self.create_widgets()
            self.flag_count = 0
            self.flag_list = []
            self.IS_FIRST_CLICK = True
            self.IS_GAME_OVER = False
            self.flags()

        def create_settings_window(self):
            win_settings = tk.Toplevel(self.window)
            win_settings.wm_title('Настройки')
            tk.Label(win_settings, text='Количество колонок').grid(row=0, column=0)
            row_entry = tk.Entry(win_settings)
            row_entry.insert(0, MineSweeper.COLUMNS)
            row_entry.grid(row=0, column=1, padx=20, pady=20)
            tk.Label(win_settings, text='Количество строк').grid(row=1, column=0)
            column_entry = tk.Entry(win_settings)
            column_entry.insert(0, MineSweeper.ROW)
            column_entry.grid(row=1, column=1, padx=20, pady=20)
            tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
            mines_entry = tk.Entry(win_settings)
            mines_entry.insert(0, MineSweeper.MINES)
            mines_entry.grid(row=2, column=1, padx=20, pady=20)
            save_btn = tk.Button(win_settings, text='Применить',
                                 command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
            save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
            try:
                int(row.get()), int(column.get()), int(mines.get())
            except ValueError:
                showerror('Ошибка', 'Вы ввели неправильное значение.')
                return None
            MineSweeper.ROW = int(column.get())
            MineSweeper.COLUMNS = int(row.get())
            MineSweeper.MINES = int(mines.get())
            self.reload()

        def create_widgets(self):

            menu_bar = tk.Menu(self.window)
            self.window.config(menu=menu_bar)

            settings_menu = tk.Menu(menu_bar, tearoff=0)
            settings_menu.add_command(label='Играть', command=self.reload)
            settings_menu.add_command(label='Настройки', command=self.create_settings_window)
            settings_menu.add_command(label='Выход', command=self.window.destroy)
            menu_bar.add_cascade(label='Меню', menu=settings_menu)

            count = 1
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    btn.number = count
                    btn.grid(row=i, column=j, stick='NWES')
                    count += 1

            for i in range(1, MineSweeper.ROW + 1):
                tk.Grid.rowconfigure(self.window, i, weight=1)

            for i in range(1, MineSweeper.COLUMNS + 1):
                tk.Grid.columnconfigure(self.window, i, weight=1)

        def open_all_buttons(self):
            for i in range(MineSweeper.ROW + 2):
                for j in range(MineSweeper.COLUMNS + 2):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn.config(background='red')
                    elif btn.count_bomb in colors:
                        color = colors.get(btn.count_bomb, 'black')
                        btn.config(text=btn.count_bomb, fg=color)

        def print_buttons(self):
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        print('B', end='')
                    else:
                        print(btn.count_bomb, end='')
                print()

        def insert_mines(self, number: int):
            index_mines = self.get_mines_places(number)
            # print(index_mines)
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.number in index_mines:
                        btn.is_mine = True

        def count_mines_in_buttons(self):
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    count_bomb = 0
                    if not btn.is_mine:
                        for row_dx in [-1, 0, 1]:
                            for col_dx in [-1, 0, 1]:
                                neighbour = self.buttons[i + row_dx][j + col_dx]
                                if neighbour.is_mine:
                                    count_bomb += 1
                    btn.count_bomb = count_bomb

        def right_click(self, event):
            if MineSweeper.IS_GAME_OVER:
                return None
            cur_btn = event.widget
            if cur_btn['state'] == 'normal':
                if not (self.IS_GAME_OVER):
                    if not (self.flag_count == self.MINES):
                        cur_btn['state'] = 'disabled'
                        cur_btn['text'] = '🚩'
                        cur_btn['disabledforeground'] = 'red'
                        self.flag_count += 1
                        self.flag_list.append(cur_btn)
            elif cur_btn['text'] == '🚩':
                if not (self.IS_GAME_OVER):
                    cur_btn['text'] = ''
                    cur_btn['state'] = 'normal'
                    self.flag_count -= 1
                    self.flag_list.remove(cur_btn)
            self.flags()

        def flags(self):
            if self.IS_GAME_OVER:
                return None
            # print(self.flag_count, end='[')
            # for z in self.flag_list:
            #     print(z.number, z.is_mine, end=',')
            # print(']')
            tk.Label(self.window, text=f'Поставлено флагов: {self.flag_count}').grid(row=self.COLUMNS + 2 + 1, column=0,
                                                                                     columnspan=int(self.ROW / 2),
                                                                                     padx=20, pady=20)
            tk.Label(self.window, text=f'Осталось флагов: {self.MINES - self.flag_count}').grid(
                row=self.COLUMNS + 2 + 1,
                column=int(self.ROW / 2),
                columnspan=self.ROW)
            if self.flag_count == self.MINES:
                i = True
                for f in self.flag_list:
                    if not f.is_mine:
                        i = False
                if i:
                    showinfo('Win!', 'Ты выйграл!')
                    self.IS_GAME_OVER = True

        def start(self):
            self.flags()
            self.create_widgets()
            # self.open_all_buttons()
            MineSweeper.window.mainloop()

        @staticmethod
        def get_mines_places(exclude_number: int):
            indexes = list(range(1, MineSweeper.ROW * MineSweeper.COLUMNS + 1))
            indexes.remove(exclude_number)
            shuffle(indexes)
            return indexes[:MineSweeper.MINES]


    Mine_Sweeper = MineSweeper()
Mine_Sweeper.start()
