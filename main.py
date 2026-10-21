from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
        def __init__(self,width,height):
                self.root_widget = Tk()
                self.root_widget.title("Maze Solver")
                self.canvas = Canvas(self.root_widget, bg="white",width=width, height=height)
                self.canvas.pack(fill=BOTH, expand=1)
                self.is_running = False
                self.root_widget.protocol("WM_DELETE_WINDOW", self.close)

        def redraw(self):
                self.root_widget.update_idletasks()
                self.root_widget.update()

        def wait_for_close(self):
                self.is_running = True
                while self.is_running:
                        self.redraw()
                print("window closed...")

        def close(self):
                self.is_running = False

        def draw_line(self,line,fill_color="black"):
                line.draw(self.canvas,fill_color)

class Point:
        def __init__(self,x,y):
                self.x=x
                self.y=y

class Line:
        def __init__(self,p1, p2):
                self.p1=p1
                self.p2=p2

        def draw(self,tk_canvas, fill_color):
                tk_canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

class Cell:
        def __init__(self,win=None):
                self.has_left_wall=True
                self.has_right_wall=True
                self.has_top_wall=True
                self.has_bottom_wall=True
                self.__x1=-1.0
                self.__x2=-1.0
                self.__y1=-1.0
                self.__y2=-1.0
                self.__win=win
                self.visited=False

        def draw(self,x1,y1,x2,y2):
                self.__x1=x1
                self.__y1=y1
                self.__x2=x2
                self.__y2=y2
                if not self.__win:
                        return
                self.__win.draw_line(Line(Point(x1,y1),Point(x1,y2)),"black" if self.has_left_wall else "white")
                self.__win.draw_line(Line(Point(x2,y1),Point(x2,y2)), "black" if self.has_right_wall else "white")
                self.__win.draw_line(Line(Point(x1,y1),Point(x2,y1)), "black" if self.has_top_wall else "white")
                self.__win.draw_line(Line(Point(x1,y2),Point(x2,y2)), "black" if self.has_bottom_wall else "white")

        def draw_move(self,to_cell,undo=False):
                col = "gray" if undo else "red"
                self_pos = self.get_pos()
                target_pos = to_cell.get_pos()
                line = Line(self_pos,target_pos)
                if not self.__win:
                        return
                self.__win.draw_line(line,fill_color=col)

        def get_pos(self):
                return Point((self.__x1+self.__x2)/2, (self.__y1+self.__y2)/2)

class Maze:
        def __init__(
                self,
                x1:int,
                y1:int,
                num_rows:int,
                num_cols:int,
                cell_size_x:float,
                cell_size_y:float,
                win:Window|None=None,
                seed=None
                ) -> None:
                self.x1=x1
                self.y1=y1
                self.num_rows=num_rows
                self.num_cols=num_cols
                self.cell_size_x=cell_size_x
                self.cell_size_y=cell_size_y
                self.win=win
                self.__cells = []
                if seed != None:
                        random.seed(seed)
                self.__create_cells()

        def __create_cells(self):
                self.__cells = [[Cell(self.win) for _ in range(self.num_cols)] for _ in range(self.num_rows)]
                for col in range(self.num_cols):
                        for row in range(self.num_rows):
                                self.__cells[row][col] = Cell(self.win)
                                self.__draw_cell(row,col)
                self.__break_entrance_and_exit()

        def __draw_cell(self,i,j):
                pos_x = i * self.cell_size_x+self.x1
                pos_y = j * self.cell_size_y+self.y1
                self.__cells[i][j].draw(pos_x,pos_y,pos_x+self.cell_size_x,pos_y+self.cell_size_y)
                self.__animate()

        def __animate(self):
                if not self.win:
                        return
                self.win.redraw()
                time.sleep(0.05)

        def __break_entrance_and_exit(self):
                self.__cells[0][0].has_top_wall = False
                self.__cells[self.num_rows-1][self.num_cols-1].has_bottom_wall = False
                self.__draw_cell(0,0)
                self.__draw_cell(self.num_rows-1,self.num_cols-1)
                self.__break_walls_r(0,0)

        def __break_walls_r(self, i: int, j: int) -> None:
                self.__cells[i][j].visited = True
                while True:
                        next_index_list = []

                        # determine which cell(s) to visit next
                        # left
                        if i > 0 and not self.__cells[i - 1][j].visited:
                                next_index_list.append((i - 1, j))
                        # right
                        if i < self.num_rows - 1 and not self.__cells[i + 1][j].visited:
                                next_index_list.append((i + 1, j))
                        # up
                        if j > 0 and not self.__cells[i][j - 1].visited:
                                next_index_list.append((i, j - 1))
                        # down
                        if j < self.num_cols - 1 and not self.__cells[i][j + 1].visited:
                                next_index_list.append((i, j + 1))

                        # if there is nowhere to go from here
                        # just break out
                        if len(next_index_list) == 0:
                                self.__draw_cell(i, j)
                                return

                        # randomly choose the next direction to go
                        direction_index = random.randrange(len(next_index_list))
                        next_index = next_index_list[direction_index]

                        # knock out walls between this cell and the next cell(s)
                        # right
                        if next_index[0] == i + 1:
                                self.__cells[i][j].has_right_wall = False
                                self.__cells[i + 1][j].has_left_wall = False
                        # left
                        if next_index[0] == i - 1:
                                self.__cells[i][j].has_left_wall = False
                                self.__cells[i - 1][j].has_right_wall = False
                        # down
                        if next_index[1] == j + 1:
                                self.__cells[i][j].has_bottom_wall = False
                                self.__cells[i][j + 1].has_top_wall = False
                        # up
                        if next_index[1] == j - 1:
                                self.__cells[i][j].has_top_wall = False
                                self.__cells[i][j - 1].has_bottom_wall = False

                        # recursively visit the next cell
                        self.__break_walls_r(next_index[0], next_index[1])
                self.__reset_cells_visited()

        def __reset_cells_visited(self):
                for col in range(len(cells)):
                      for row in range(len(cells[0])):
                              self.cells[row][col].visited = False

        def solve(self):
                return self.__solve_r(0,0)

        def __solve_r(self,i,j):
                self.__animate()
                self.__cells[i][j].visited=True
                if i == self.num_rows-1 and j == self.num_cols-1:
                        return True
                #left
                if (i > 0 and not self.__cells[i][j].has_left_wall and not self.__cells[i-1][j].visited):
                        self.__cells[i][j].draw_move(self.__cells[i-1][j])
                        if self.__solve_r(i-1,j):
                                return True
                        else:
                                self.__cells[i][j].draw_move(self.__cells[i-1][j],True)
                #right
                if (i < self.num_rows-1 and not self.__cells[i][j].has_right_wall and not self.__cells[i+1][j].visited):
                        self.__cells[i][j].draw_move(self.__cells[i+1][j])
                        if self.__solve_r(i+1,j):
                                return True
                        else:
                                self.__cells[i][j].draw_move(self.__cells[i+1][j],True)

                #up
                if (j > 0 and not self.__cells[i][j].has_top_wall and not self.__cells[i][j-1].visited):
                        self.__cells[i][j].draw_move(self.__cells[i][j-1])
                        if self.__solve_r(i,j-1):
                                return True
                        else:
                                self.__cells[i][j].draw_move(self.__cells[i][j-1],True)

                #down
                if (j < self.num_cols-1 and not self.__cells[i][j].has_bottom_wall and not self.__cells[i][j+1].visited):
                        self.__cells[i][j].draw_move(self.__cells[i][j+1])
                        if self.__solve_r(i,j+1):
                                return True
                        else:
                                self.__cells[i][j].draw_move(self.__cells[i][j+1],True)

                return False


def main():
        win = Window(800,600)
        #win = None
        maze = Maze(50,50,15,10,700/15,500/10,win)
        print("maze created")
        is_solvable = maze.solve()
        if not is_solvable:
                print("maze cannot be solved!")
        else:
                print("maze solved!")
        win.wait_for_close()
        pass

if __name__ == "__main__":
        main()
