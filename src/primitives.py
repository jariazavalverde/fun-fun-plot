class Element:
	"""This class defines the interface for any graphical component."""
		
	def get_attributes(self):
		"""This method returns all the parameters of the constructor."""
		return []
	
	def compute(self, canvas):
		"""This method computes some properties of the graphical component."""
		pass
	
	def draw(self, canvas):
		"""This method draws the graphical component in the canvas."""
		pass
	
	def eval(self, canvas, data, elem):
		"""This method returns an evaluated instance of the graphical component."""
		return self.__class__(
			*list(map(lambda x: x.eval(canvas, data, elem),
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
	
	def compute(self, canvas):
		self.left.compute(canvas)
		self.right.compute(canvas)
	
	def draw(self, canvas):
		self.left.draw(canvas)
		self.right.draw(canvas)
