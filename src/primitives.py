class Plot:
	"""This class stores a canvas for drawing."""
	
	def __init__(self, component, canvas, width, height):
		self.component = component
		self.canvas = canvas(width, height)
		self.width = width
		self.height = height
		# (left, right, top, bottom)
		self.dimensions = (float('inf'), float('-inf'), float('-inf'), float('inf'))
	
	def draw(self, data):
		"""This method plots a dataset."""
		length = len(data)
		self.component.eval(self, data, length).draw(self)



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



class Operator:
	"""This class represents operations beeween data."""
	
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
