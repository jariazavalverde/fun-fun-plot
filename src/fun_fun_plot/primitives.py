#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides primitive classes for plotting."""

__author__ = "José Antonio Riaza Valverde"
__copyright__ = "Copyright 2018, José Antonio Riaza Valverde"
__credits__ = ["José Antonio Riaza Valverde"]
__license__ = "BSD 3-Clause License"
__maintainer__ = "José Antonio Riaza Valverde"
__email__ = "riazavalverde@gmail.com"
__status__ = "Development"



class Plot:
	"""This class stores a canvas for drawing."""
	
	def __init__(self, component, primitives, width = 200, height = 200):
		self.component = component
		self.primitives = primitives
		self.computed = False
		self.colors = dict([])
		self.palette = ["red", "green", "blue", "yellow"]
		self.canvas = None
		self.width = width
		self.height = height
		# (left, right, top, bottom)
		self.dimensions = (float('inf'), float('-inf'), float('-inf'), float('inf'))
	
	def copy(self):
		"""This method returns a new instance of the plot."""
		return Plot(self.component, self.primitives, self.width, self.height)
	
	def draw(self, data):
		"""This method plots a dataset."""
		if self.computed:
			return self
		length = len(data)
		plot = self.copy()
		# Compute data
		plot.component.eval(plot, data, length, (0,0,0,0)).compute(plot)
		plot.computed = True
		# Create canvas
		plot.canvas = plot.primitives["canvas"](plot.width, plot.height)
		# Draw data
		plot.component.eval(plot, data, length, (0,0,0,0)).draw(plot)
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
	
	def get_width(self, offset):
		"""This method returns the width of the plot when it is computed."""
		if self.computed:
			return self.width - offset[0] - offset[1]
		return 1
	
	def get_height(self, offset):
		"""This method returns the height of the plot when it is computed."""
		if self.computed:
			return self.height - offset[2] - offset[3]
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
	
	# This attribute stores the initial offsets (left, right, top, bottom)
	offset = (0, 0, 0, 0)
	
	def get_offset_left(self):
		"""This method returns the left offset."""
		return self.offset[0]
	
	def get_offset_right(self):
		"""This method returns the right offset."""
		return self.offset[1]
	
	def get_offset_top(self):
		"""This method returns the top offset."""
		return self.offset[2]
	
	def get_offset_bottom(self):
		"""This method returns the bottom offset."""
		return self.offset[3]
		
	def get_attributes(self):
		"""This method returns all the parameters of the constructor."""
		return []
	
	def compute(self, plot):
		"""This method computes some properties of the graphical component."""
		pass
	
	def draw(self, plot):
		"""This method draws the graphical component in the canvas."""
		pass
	
	def eval(self, plot, data, elem, offset = (0,0,0,0)):
		"""This method returns an evaluated instance of the graphical component."""
		return self.__class__(
			*list(map(lambda x: x.eval(plot, data, elem, offset) if x is not None else None,
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
	
	def eval(self, plot, data, length, offset):
		left = self.left.eval(plot, data, length, offset)
		right = self.right.eval(plot, data, length, offset)
		left.offset = offset
		right.offset = offset
		return Compose(left, right)
	
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
	
	def eval(self, plot, data, length, offset):
		operators = []
		for index in range(length):
			operator = self.operator.eval(plot, data, index, offset)
			operator.offset = offset
			operators.append(operator)
		return Data(operators)
	
	def compute(self, plot):
		for op in self.operator:
			op.compute(plot)
	
	def draw(self, plot):
		for op in self.operator:
			op.draw(plot)



class Axis(Element):
	"""This class represents the axis."""
	
	# Default margins for axis
	margin_left = 60
	margin_right = 30
	margin_top = 30
	margin_bottom = 30
	
	# Default number of ticks
	nb_ticks = 5
	
	def __init__(self, component, xticks = None, yticks = None, xlabels = None, ylabels = None):
		self.component = component
		self.xticks = xticks
		self.yticks = yticks
		self.xlabels = xlabels
		self.ylabels = ylabels
		
	
	def get_attributes(self):
		return [self.component, self.xticks, self.yticks, self.xlabels, self.ylabels]
	
	def eval(self, plot, data, elem, offset):
		left, right, top, bottom = offset
		new_offset = (
			left+self.margin_left, right+self.margin_right,
			top+self.margin_top, bottom+self.margin_bottom)
		axis = Axis(*list(map(
			lambda x: x.eval(plot, data, elem, new_offset) if x is not None else None,
				self.get_attributes())))
		axis.component.offset = new_offset
		return axis
	
	def compute(self, plot):
		self.component.compute(plot)
	
	def draw(self, plot):
		width = plot.width - self.get_offset_left() - self.get_offset_right() - self.margin_left - self.margin_right
		height = plot.height - self.get_offset_bottom() - self.get_offset_top() - self.margin_top - self.margin_bottom
		xticks = [float(width)/float(self.nb_ticks-1)*i for i in range(self.nb_ticks)] if self.xticks is None else self.xticks
		yticks = [float(height)/float(self.nb_ticks-1)*i for i in range(self.nb_ticks)] if self.yticks is None else self.yticks
		xlabels = [plot.get_left() + float(plot.get_right()-plot.get_left())/float(len(xticks)-1)*i for i in range(len(xticks))] if self.xlabels is None else self.xlabels
		ylabels = [plot.get_bottom() + float(plot.get_top()-plot.get_bottom())/float(len(yticks)-1)*i for i in range(len(yticks))] if self.ylabels is None else self.ylabels
		# Draw background
		plot.primitives["rectangle"](plot,
			self.margin_left + self.get_offset_left(),
			self.margin_bottom + self.get_offset_bottom(),
			width,
			height,
			"white", "black", 1)
		# Draw component inside
		self.component.draw(plot)
		# Draw axis
		for i in range(len(xticks)):
			xi = self.margin_left + self.get_offset_left() + xticks[i]
			plot.primitives["line"](
				plot,
				xi,
				self.margin_bottom + self.get_offset_bottom() - 5,
				xi,
				self.margin_bottom + self.get_offset_bottom() + 5,
				"black", 1)
			plot.primitives["text"](
				plot,
				xi,
				self.margin_bottom + self.get_offset_bottom() - 15,
				str(xlabels[i]),
				"Arial", 10, "black", "center")
		for i in range(len(yticks)):
			yi = self.margin_bottom + self.get_offset_bottom() + yticks[i]
			plot.primitives["line"](
				plot,
				self.margin_left + self.get_offset_left() - 5,
				yi,
				self.margin_left + self.get_offset_left() + 5,
				yi,
				"black", 1)
			plot.primitives["text"](
				plot,
				self.margin_left + self.get_offset_left() - 10,
				yi,
				str(ylabels[i]),
				"Arial", 10, "black", "right")
			



class Line(Element):
	"""This class represents a line from (x,y) to (fx,fy)."""
	
	def __init__(self, x, y, fx, fy, border_color = None, border_width = None):
		self.x = x
		self.y = y
		self.fx = fx
		self.fy = fy
		self.border_color = border_color
		self.border_width = border_width
	
	def get_attributes(self):
		return [self.x, self.y, self.fx, self.fy, self.border_color, self.border_width]
	
	def compute(self, plot):
		plot.set_max_dimensions(self.x, self.y, self.fx, self.fy)
	
	def draw(self, plot):
		plot.primitives["line"](
			plot,
			self.x + self.get_offset_left(),
			self.y + self.get_offset_bottom(),
			self.fx + self.get_offset_left(),
			self.fy + self.get_offset_bottom(),
			self.border_color, self.border_width)



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
		plot.set_max_dimensions(self.x, self.y, self.x, self.y)
	
	def draw(self, plot):
		plot.primitives["circle"](
			plot,
			self.x + self.get_offset_left(),
			self.y + self.get_offset_bottom(),
			self.radius,
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
		plot.set_max_dimensions(self.x, self.y, self.x + self.dx, self.y + self.dy)
	
	def draw(self, plot):
		plot.primitives["rectangle"](
			plot,
			self.x + self.get_offset_left(),
			self.y + self.get_offset_bottom(),
			self.dx, self.dy,
			self.background_color, self.border_color, self.border_width)



class Text(Element):
	"""This class represents a text."""
	
	def __init__(self, x, y, text, font_family = None, font_size = None, font_color = None, text_align = None):
		self.x = x
		self.y = y
		self.text = text
		self.font_family = font_family
		self.font_size = font_size
		self.font_color = font_color
		self.text_align = text_align
	
	def get_attributes(self):
		return [
			self.x, self.y, self.text,
			self.font_family, self.font_size, self.font_color, self.text_align]
	
	def compute(self, plot):
		plot.set_max_dimensions(self.x, self.y, self.x, self.y)
	
	def draw(self, plot):
		fs = 16 if self.font_size is None else self.font_size
		ff = "Helvetica" if self.font_family is None else self.font_family
		fc = "black" if self.font_color is None else self.font_color
		ta = "center" if self.text_align is None else self.text_algin
		plot.primitives["text"](
			plot,
			self.x + self.get_offset_left(),
			self.y + self.get_offset_bottom(),
			str(self.text), ff, fs, fc, ta)
