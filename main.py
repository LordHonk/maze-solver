from tkinter import Tk, BOTH, Canvas
import time

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

        def draw(self,x1,y1,x2,y2):
                self.__x1=x1
                self.__y1=y1
                self.__x2=x2
                self.__y2=y2
                if not self.__win:
                        return
                if self.has_left_wall:
                        self.__win.draw_line(Line(Point(x1,y1),Point(x1,y2)))
                if self.has_right_wall:
                        self.__win.draw_line(Line(Point(x2,y1),Point(x2,y2)))
                if self.has_top_wall:
                        self.__win.draw_line(Line(Point(x1,y1),Point(x2,y1)))
                if self.has_bottom_wall:
                        self.__win.draw_line(Line(Point(x1,y2),Point(x2,y2)))

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
                ) -> None:
                self.x1=x1
                self.y1=y1
                self.num_rows=num_rows
                self.num_cols=num_cols
                self.cell_size_x=cell_size_x
                self.cell_size_y=cell_size_y
                self.win=win
                self.__cells = []
                self.__create_cells()

        def __create_cells(self):
                self.__cells = [[Cell(self.win) for _ in range(self.num_cols)] for _ in range(self.num_rows)]
                for col in range(self.num_cols):
                        for row in range(self.num_rows):
                                self.__cells[row][col] = Cell(self.win)
                                self.__draw_cell(row,col)

        def __draw_cell(self,i,j):
                pos_x = i * self.cell_size_x
                pos_y = j * self.cell_size_y
                self.__cells[i][j].draw(pos_x,pos_y,pos_x+self.cell_size_x,pos_y+self.cell_size_y)
                self.__animate()

        def __animate(self):
                if not self.win:
                        return
                self.win.redraw()
                time.sleep(0.05)


def main():
        #win = Window(800,600)
        #maze = Maze(0,0,30,20,800/30,600/20,win)
        #win.wait_for_close()
        pass

main()
