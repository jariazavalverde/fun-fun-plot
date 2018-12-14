from Tkinter import *



def __tkinter_canvas(width, height):
	"""This function creates a new Tkinter canvas."""
	w = Canvas(Tk(), width=width, height=height)
	w.pack()
	return w

def __tkinter_line(canvas, x, y, fx, fy):
	"""This function draws a line with the Tkinter library."""
	canvas.create_line(x, y, fx, fy)

def __tkinter_circle(canvas, x, y, radius):
	"""This function draws a circle with the Tkinter library."""
	canvas.create_oval(x-radius, y-radius, x+radius, y+radius)



# This dictionary stores all the primitives of the Tkinter library.
ffp_tkinter = {
	"canvas": __tkinter_canvas,
	"line": __tkinter_line,
	"circle": __tkinter_circle
}
