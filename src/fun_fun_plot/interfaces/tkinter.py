from Tkinter import *



def __tkinter_canvas(width, height):
	"""This function creates a new Tkinter canvas."""
	w = Canvas(Tk(), width = width, height = height)
	w.pack()
	return w

def __tkinter_line(plot, x, y, fx, fy):
	"""This function draws a line with the Tkinter library."""
	plot.canvas.create_line(x, plot.height - y, fx, plot.height - fy)

def __tkinter_circle(plot, x, y, radius, background, border, width):
	"""This function draws a circle with the Tkinter library."""
	plot.canvas.create_oval(
		x - radius,
		plot.height - (y - radius),
		x + radius,
		plot.height - (y + radius),
		fill = background
	)

def __tkinter_rectangle(plot, x, y, dx, dy, background, border, width):
	"""This function draws a rectangle with the Tkinter library."""
	plot.canvas.create_rectangle(
		x,
		plot.height - y,
		x + dx,
		plot.height - (y + dy),
		fill = background
	)



# This dictionary stores all the primitives of the Tkinter library.
ffp_tkinter = {
	"canvas": __tkinter_canvas,
	"line": __tkinter_line,
	"circle": __tkinter_circle,
	"rectangle": __tkinter_rectangle
}
