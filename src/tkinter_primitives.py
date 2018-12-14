from primitives import *
from Tkinter import *



def tkinter_canvas(width, height):
	"""This function creates a new Tkinter canvas."""
	w = Canvas(Tk(), width=width, height=height)
	w.pack()
	return w



class Line(Element):
	"""This class represents a line for Tkinter library."""
	
	def __init__(self, x, y, fx, fy):
		self.x = x
		self.y = y
		self.fx = fx
		self.fy = fy
	
	def get_attributes(self):
		return [self.x, self.y, self.fx, self.fy]
	
	def compute(self, plot):
		plot.set_max_dimensions(self.x, self.y, self.fx, self.fy)
	
	def draw(self, plot):
		plot.canvas.create_line(self.x, self.y, self.fx, self.fy)

