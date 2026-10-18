from tkinter import Tk, BOTH, Canvas

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
        def __init__(self,win):
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
                self.__win.draw_line(line,fill_color=col)

        def get_pos(self):
                return Point((self.__x1+self.__x2)/2, (self.__y1+self.__y2)/2)



def main():
        win = Window(800,600)
        cell1 = Cell(win)
        cell1.has_right_wall=False
        cell2 = Cell(win)
        cell2.has_left_wall=False
        cell1.draw(100,100,200,200)
        cell2.draw(200,100,300,200)
        cell1.draw_move(cell2)

        win.wait_for_close()

main()
