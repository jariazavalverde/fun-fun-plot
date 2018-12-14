class Plot:
	"""This class stores a canvas for drawing."""
	
	def __init__(self, component, primitives, width, height):
		self.component = component
		self.primitives = primitives
		self.canvas = None
		self.width = width
		self.height = height
		# (left, right, top, bottom)
		self.dimensions = (float('inf'), float('-inf'), float('-inf'), float('inf'))
	
	def draw(self, data):
		"""This method plots a dataset."""
		length = len(data)
		instance = self.component.eval(self, data, length)
		self.canvas = self.primitives["canvas"](self.width, self.height)
		instance.draw(self)
	
	def set_max_dimensions(self, min_x, min_y, max_x, max_y):
		if min_x > max_x:
			min_x, max_x = max_x, min_x
		if min_y > max_y:
			min_y, max_y = max_y, min_y
		self.dimensions = (
			min(self.dimensions[0], min_x),
			max(self.dimensions[1], max_x),
			max(self.dimensions[2], max_y),
			min(self.dimensions[3], min_y))



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
			*list(map(lambda x: x.eval(plot, data, elem),
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
		plot.primitives["line"](plot.canvas, self.x, self.y, self.fx, self.fy)



class Operator:
	"""This class represents operations between data."""
	
	def __init__(self, operation):
		self.operation = operation
	
	def eval(self, plot, data, elem):
		"""This method evaluates the operation."""
		return self.operation(plot, data, elem)
		
	def __add__(self, operator):
		"""This method adds two operations."""
		return Operator(
			lambda plot, data, elem:
				self.eval(plot, data, elem) +
				operator.eval(plot, data, elem))
	
	def __sub__(self, operator):
		"""This method substracts two operations."""
		return Operator(
			lambda plot, data, elem:
				self.eval(plot, data, elem) -
				operator.eval(plot, data, elem))
		
	def __mul__(self, operator):
		"""This method multiplies two operations."""
		return Operator(
			lambda plot, data, elem:
				self.eval(plot, data, elem) *
				operator.eval(plot, data, elem))
	
	def __truediv__(self, operator):
		"""This method divides two operations."""
		return Operator(
			lambda plot, data, elem:
				self.eval(plot, data, elem) /
				operator.eval(plot, data, elem))



def Cons(value):
	"""This functions returns a constant operator."""
	return Operator(lambda plot, data, elem: value)



# This operator returns the index of the data
Index = Operator(lambda plot, data, elem: elem)
