#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides operators for plotting."""

from math import pi, sin, cos

__author__ = "José Antonio Riaza Valverde"
__copyright__ = "Copyright 2018, José Antonio Riaza Valverde"
__credits__ = ["José Antonio Riaza Valverde"]
__license__ = "BSD 3-Clause License"
__maintainer__ = "José Antonio Riaza Valverde"
__email__ = "riazavalverde@gmail.com"
__status__ = "Development"



class Operator:
	"""This class represents operations between data."""
	
	def __init__(self, operation):
		self.operation = operation
	
	def eval(self, plot, data, elem, offset):
		"""This method evaluates the operation."""
		return self.operation(plot, data, elem, offset)
		
	def __add__(self, operator):
		"""This method adds two operations."""
		return Operator(
			lambda plot, data, elem, offset:
				self.eval(plot, data, elem, offset) +
				operator.eval(plot, data, elem, offset))
	
	def __sub__(self, operator):
		"""This method substracts two operations."""
		return Operator(
			lambda plot, data, elem, offset:
				self.eval(plot, data, elem, offset) -
				operator.eval(plot, data, elem, offset))
		
	def __mul__(self, operator):
		"""This method multiplies two operations."""
		return Operator(
			lambda plot, data, elem, offset:
				self.eval(plot, data, elem, offset) *
				operator.eval(plot, data, elem, offset))
	
	def __truediv__(self, operator):
		"""This method divides two operations."""
		return Operator(
			lambda plot, data, elem, offset:
				self.eval(plot, data, elem, offset) /
				operator.eval(plot, data, elem, offset))
	
	def __div__(self, operator):
		"""This method divides two operations."""
		return Operator(
			lambda plot, data, elem, offset:
				self.eval(plot, data, elem, offset) /
				operator.eval(plot, data, elem, offset))
				
	def __rshift__(self, key):
		"""This method stores the value in the plot."""
		def _set(plot, key, value):
			plot.store_data(key, value)
			return value
		return Operator(lambda plot, data, elem, offset: _set(
			plot,
			key.eval(plot, data, elem, offset),
			self.eval(plot, data, elem, offset)))



def Cons(value):
	"""This function returns a constant operator."""
	return Operator(lambda plot, data, elem, offset: value)

def Call(func):
	"""This function returns a function operator."""
	return lambda *args: Operator(lambda plot, data, elem, offset:
		func(*list(map(lambda x: x.eval(plot, data, elem, offset), args))))



# ACCESSING PLOT INFORMATION

# These operators return width and height of the plot
Width = Operator(lambda plot, data, elem, offset: plot.get_width(offset))
Height = Operator(lambda plot, data, elem, offset: plot.get_height(offset))

# These operators return dimensions of the plot
Left = Operator(lambda plot, data, elem, offset: plot.get_left())
Right = Operator(lambda plot, data, elem, offset: plot.get_right())
Top = Operator(lambda plot, data, elem, offset: plot.get_top())
Bot = Operator(lambda plot, data, elem, offset: plot.get_bottom())



# ACCESSING DATA

# This operator returns the current index of the data
Index = Operator(lambda plot, data, elem, offset: float(elem))

# This operator returns the current value of the data
Value = Operator(lambda plot, data, elem, offset: data[elem])

# This operator returns the n-th value of the attribute
Attr = lambda n: Operator(lambda plot, data, elem, offset: data[elem][n.eval(plot, data, elem, offset)])

# This operator returns the n-th column of the dataset
Column = lambda n: Operator(lambda plot, data, elem, offset:(lambda _n: list(map(lambda x: x[_n], data)))(n.eval(plot, data, elem, offset)))

# This operator returns the length of the data
DataLen = Operator(lambda plot, data, elem, offset: float(len(data)))

# This operator returns the value of the key data
Get = lambda key, default = Cons(None): Operator(lambda plot, data, elem, offset:
	plot.get_data(key if isinstance(key, basestring) else key.eval(plot, data, elem, offset),
	default.eval(plot, data, elem, offset)))



# NORMALIZE DATA

# These operators returns the value normalized in the x or y axis
Xnormal = lambda op: Width * (op-Left) / (Right-Left)
Ynormal = lambda op: Height * (op-Bot) / (Top-Bot)



# CONSTANTS

# These operators return constants from zero to nine
Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine = list(map(Cons, range(10)))

# This operator returns the constant PI
Pi = Cons(pi)



# COLORS

# Assign color to a class
ClassColor = lambda classname: Operator(lambda plot, data, elem, offset: plot.class_color(classname.eval(plot, data, elem, offset)))



# LIST OPERATIONS

# This operator returns a range
def Range(n, start, incr):
	def _range(n, start, incr):
		return list(map(lambda i: start+incr*i, range(int(n))))
	return Operator(lambda plot, data, elem, offset: _range(
		n.eval(plot, data, elem, offset),
		start.eval(plot, data, elem, offset),
		incr.eval(plot, data, elem, offset)))



# ARITHMETIC OPERATIONS
Sum = lambda lst: Operator(lambda plot, data, elem, offset: sum(lst.eval(plot, data, elem, offset)))
Sin = Call(sin)
Cos = Call(cos)
Radians = lambda angle: angle * Pi / Cons(180)
Str = Call(str)
