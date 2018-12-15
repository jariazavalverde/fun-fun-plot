from operators import *



class Plot:
	"""This class stores a canvas for drawing."""
	
	def __init__(self, component, primitives, width = 200, height = 200, axis = True):
		self.component = component
		self.primitives = primitives
		self.computed = False
		self.colors = dict([])
		self.palette = ["red", "green", "blue", "yellow"]
		self.canvas = None
		self.width = width
		self.height = height
		self.axis = axis
		# (left, right, top, bottom)
		self.dimensions = (float('inf'), float('-inf'), float('-inf'), float('inf'))
	
	def copy(self):
		"""This method returns a new instance of the plot."""
		return Plot(self.component, self.primitives, self.width, self.height, self.axis)
	
	def draw(self, data):
		"""This method plots a dataset."""
		if self.computed:
			return self
		length = len(data)
		plot = self.copy()
		component = plot.component
		# Add axis
		if plot.axis:
			component = Rectangle(One, Zero, Width - One, Height - One, Cons("white")) + component
		# Compute data
		component.eval(plot, data, length).compute(plot)
		plot.computed = True
		# Create canvas
		plot.canvas = plot.primitives["canvas"](plot.width, plot.height)
		# Draw data
		component.eval(plot, data, length).draw(plot)
		return plot
	
	def set_max_dimensions(self, min_x, min_y, max_x, max_y):
		"""This method updates the maximum and minimum values."""
		if min_x > max_x:
			min_x, max_x = max_x, min_x
		if min_y > max_y:
			min_y, max_y = max_y, min_y
		self.dimensions = (
			min(self.dimensions[0], min_x),
			max(self.dimensions[1], max_x),
			max(self.dimensions[2], max_y),
			min(self.dimensions[3], min_y))
	
	def get_width(self):
		"""This method returns the width of the plot when it is computed."""
		if self.computed:
			return self.width
		return 1
	
	def get_height(self):
		"""This method returns the height of the plot when it is computed."""
		if self.computed:
			return self.height
		return 1
	
	def get_left(self):
		"""This method returns the most left value of the plot when it is computed."""
		if self.computed:
			return self.dimensions[0]
		return 0
	
	def get_right(self):
		"""This method returns the most right value of the plot when it is computed."""
		if self.computed:
			return self.dimensions[1]
		return 1
	
	def get_top(self):
		"""This method returns the most top value of the plot when it is computed."""
		if self.computed:
			return self.dimensions[2]
		return 1
	
	def get_bottom(self):
		"""This method returns the most bottom value of the plot when it is computed."""
		if self.computed:
			return self.dimensions[3]
		return 0
	
	def class_color(self, classname):
		"""This method assigns and returns colors for classes."""
		if self.colors.get(classname) is None:
			self.colors[classname] = self.palette[len(self.colors) % len(self.palette)]
		return self.colors[classname]



class Element:
	"""This class defines the interface for any graphical component."""
		
	def get_attributes(self):
		"""This method returns all the parameters of the constructor."""
		return []
	
	def compute(self, plot):
		"""This method computes some properties of the graphical component."""
		pass
	
	def draw(self, canvas):
		"""This method draws the graphical component in the canvas."""
		pass
	
	def eval(self, plot, data, elem):
		"""This method returns an evaluated instance of the graphical component."""
		return self.__class__(
			*list(map(lambda x: x.eval(plot, data, elem) if x is not None else None,
				self.get_attributes())))
	
	def __add__(self, elem):
		"""This method sequentially joins two graphical components."""
		return Compose(self, elem)



class Compose(Element):
	"""This class sequentially joins two graphical components."""
	
	def __init__(self, left, right):
		self.left = left
		self.right = right
	
	def get_attributes(self):
		return [self.left, self.right]
	
	def compute(self, plot):
		self.left.compute(plot)
		self.right.compute(plot)
	
	def draw(self, plot):
		self.left.draw(plot)
		self.right.draw(plot)



class Data(Element):
	"""This class maps the dataset with a graphical component."""
	
	def __init__(self, operator):
		self.operator = operator
	
	def get_attributes(self):
		return [self.operator]
	
	def eval(self, plot, data, length):
		operators = []
		for index in range(length):
			operators.append(self.operator.eval(plot, data, index))
		return Data(operators)
	
	def compute(self, plot):
		for op in self.operator:
			op.compute(plot)
	
	def draw(self, plot):
		for op in self.operator:
			op.draw(plot)



class Line(Element):
	"""This class represents a line from (x,y) to (fx,fy)."""
	
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
		plot.primitives["line"](plot, self.x, self.y, self.fx, self.fy)



class Circle(Element):
	"""This class represents a circle with center (x,y) and radius r."""
	
	def __init__(self, x, y, r, background_color = None, border_color = None, border_width = None):
		self.x = x
		self.y = y
		self.radius = r
		self.background_color = background_color
		self.border_color = border_color
		self.border_width = border_width
	
	def get_attributes(self):
		return [
			self.x, self.y, self.radius,
			self.background_color, self.border_color, self.border_width]
	
	def compute(self, plot):
		bw = self.border_width if self.border_width is not None else 1
		plot.set_max_dimensions(
			self.x - self.radius - bw, self.y - self.radius - bw,
			self.x + self.radius + bw, self.y + self.radius + bw)
	
	def draw(self, plot):
		plot.primitives["circle"](
			plot, self.x, self.y, self.radius,
			self.background_color, self.border_color, self.border_width)



class Rectangle(Element):
	"""This class represents a rectangle."""
	
	def __init__(self, x, y, dx, dy, background_color = None, border_color = None, border_width = None):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.background_color = background_color
		self.border_color = border_color
		self.border_width = border_width
	
	def get_attributes(self):
		return [
			self.x, self.y, self.dx, self.dy,
			self.background_color, self.border_color, self.border_width]
	
	def compute(self, plot):
		bw = self.border_width if self.border_width is not None else 1
		plot.set_max_dimensions(
			self.x - bw, self.y - bw,
			self.x + self.dx + bw, self.y + self.dy + bw)
	
	def draw(self, plot):
		plot.primitives["rectangle"](
			plot, self.x, self.y, self.dx, self.dy,
			self.background_color, self.border_color, self.border_width)
