from math import pi



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
	
	def __div__(self, operator):
		"""This method divides two operations."""
		return Operator(
			lambda plot, data, elem:
				self.eval(plot, data, elem) /
				operator.eval(plot, data, elem))



def Cons(value):
	"""This function returns a constant operator."""
	return Operator(lambda plot, data, elem: value)




# ACCESSING PLOT INFORMATION

# These operators return width and height of the plot
Width = Operator(lambda plot, data, elem: plot.get_width())
Height = Operator(lambda plot, data, elem: plot.get_height())

# These operators return dimensions of the plot
Left = Operator(lambda plot, data, elem: plot.get_left())
Right = Operator(lambda plot, data, elem: plot.get_right())
Top = Operator(lambda plot, data, elem: plot.get_top())
Bot = Operator(lambda plot, data, elem: plot.get_bottom())



# ACCESSING DATA

# This operator returns the current index of the data
Index = Operator(lambda plot, data, elem: elem)

# This operator returns the current value of the data
Value = Operator(lambda plot, data, elem: data[elem])

# This operator returns the n-th value of the attribute
Attr = lambda n: Operator(lambda plot, data, elem: data[elem][n.eval(plot, data, elem)])



# NORMALIZE DATA

# These operators returns the value normalized in the x or y axis
Xnormal = lambda op: Width * (op-Left) / (Right-Left)
Ynormal = lambda op: Height * (op-Bot) / (Top-Bot)



# CONSTANTS

# These operators return constants from zero to nine
Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine = list(map(Cons, range(10)))

# This operator returns the constant PI
Pi = Cons(pi)
