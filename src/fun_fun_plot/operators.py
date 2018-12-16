#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides operators for plotting."""

from primitives import ffp_eval, Operator

__author__ = "José Antonio Riaza Valverde"
__copyright__ = "Copyright 2018, José Antonio Riaza Valverde"
__credits__ = ["José Antonio Riaza Valverde"]
__license__ = "BSD 3-Clause License"
__maintainer__ = "José Antonio Riaza Valverde"
__email__ = "riazavalverde@gmail.com"
__status__ = "Development"



# INVOKING FUNCTIONS

def Call(func):
	"""This function returns a function operator."""
	return lambda *args: Operator(lambda plot, data, elem, offset:
		func(*list(map(lambda x: ffp_eval(x, plot, data, elem, offset), args))))



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
Attr = lambda n: Operator(lambda plot, data, elem, offset: data[elem][ffp_eval(n, plot, data, elem, offset)])

# This operator returns the n-th column of the dataset
Column = lambda n: Operator(lambda plot, data, elem, offset:(lambda _n: list(map(lambda x: x[_n], data)))(ffp_eval(n, plot, data, elem, offset)))

# This operator returns the length of the data
DataLen = Operator(lambda plot, data, elem, offset: float(len(data)))

# This operator returns the value of the key data
Get = lambda key, default = None: Operator(lambda plot, data, elem, offset:
	plot.get_data(ffp_eval(key, plot, data, elem, offset),
	ffp_eval(default, plot, data, elem, offset)))



# NORMALIZE DATA

# These operators returns the value normalized in the x or y axis
Xnormal = lambda op: Width * (op-Left) / (Right-Left)
Ynormal = lambda op: Height * (op-Bot) / (Top-Bot)



# COLORS

# Assign color to a class
ClassColor = lambda classname: Operator(lambda plot, data, elem, offset: plot.class_color(ffp_eval(classname, plot, data, elem, offset)))



# LIST OPERATIONS

# This operator returns a range
def Range(n, start, incr):
	def _range(n, start, incr):
		return list(map(lambda i: start+incr*i, range(int(n))))
	return Operator(lambda plot, data, elem, offset: _range(
		ffp_eval(n, plot, data, elem, offset),
		ffp_eval(start, plot, data, elem, offset),
		ffp_eval(incr, plot, data, elem, offset)))
