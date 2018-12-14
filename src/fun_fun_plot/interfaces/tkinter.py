from Tkinter import *



def __tkinter_canvas(width, height):
	"""This function creates a new Tkinter canvas."""
	w = Canvas(Tk(), width=width, height=height)
	w.pack()
	return w

def __tkinter_line(canvas, x, y, fx, fy):
	"""This function draws a line with te Tkinter library."""
	canvas.create_line(x, y, fx, fy)



# This dictionary stores all the primitives of the Tkinter library.
ffp_tkinter = {
	"canvas": __tkinter_canvas,
	"line": __tkinter_line
}
