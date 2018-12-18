#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides an interface for the Tkinter library."""

from math import sin, cos
from Tkinter import Canvas, Tk, CENTER, E, W, PIESLICE, ARC, PhotoImage, NW

__author__ = "José Antonio Riaza Valverde"
__copyright__ = "Copyright 2018, José Antonio Riaza Valverde"
__credits__ = ["José Antonio Riaza Valverde"]
__license__ = "BSD 3-Clause License"
__maintainer__ = "José Antonio Riaza Valverde"
__email__ = "riazavalverde@gmail.com"
__status__ = "Development"



def __tkinter_canvas(width, height):
	"""This function creates a new Tkinter canvas."""
	w = Canvas(Tk(), width = width, height = height)
	w.pack()
	return w

def __tkinter_after(plot):
	plot.canvas.mainloop()

def __tkinter_line(plot, x, y, fx, fy, border, width):
	"""This function draws a line with the Tkinter library."""
	plot.canvas.create_line(
		x,
		plot.height - y,
		fx,
		plot.height - fy,
		fill = border,
		width = width
	)

def __tkinter_pie(plot, x, y, radius, alpha, beta, background, border, width):
	"""This function draws a sector with the Tkinter library."""
	plot.canvas.create_arc(
		x - radius,
		plot.height - (y - radius),
		x + radius,
		plot.height - (y + radius),
		start = alpha,
		extent = beta,
		fill = background,
		outline = border,
		width = width,
		style = PIESLICE
	)

def __tkinter_arc(plot, x, y, radius, alpha, beta, background, border, width):
	"""This function draws a sector with the Tkinter library."""
	plot.canvas.create_arc(
		x - radius,
		plot.height - (y - radius),
		x + radius,
		plot.height - (y + radius),
		start = alpha,
		extent = beta,
		fill = background,
		outline = border,
		width = width,
		style = ARC
	)

def __tkinter_circle(plot, x, y, radius, background, border, width):
	"""This function draws a circle with the Tkinter library."""
	plot.canvas.create_oval(
		x - radius,
		plot.height - (y - radius),
		x + radius,
		plot.height - (y + radius),
		fill = background,
		outline = border,
		width = width
	)

def __tkinter_rectangle(plot, x, y, dx, dy, background, border, width):
	"""This function draws a rectangle with the Tkinter library."""
	plot.canvas.create_rectangle(
		x,
		plot.height - y,
		x + dx,
		plot.height - (y + dy),
		fill = background,
		outline = border,
		width = width
	)

def __tkinter_text(plot, x, y, text, family, size, color, align):
	"""This function draws a text with the Tkinter library."""
	if align == "left":
		anchor = W
	elif align == "right":
		anchor = E
	else:
		anchor = CENTER
	plot.canvas.create_text(
		x,
		plot.height - y,
		text = text,
		font = (family, size),
		fill = color,
		anchor = anchor
	)

def __tkinter_image(plot, path, x, y):
	"""This function draws an image with the Tkinter library."""
	img = PhotoImage(file = path)
	plot.canvas.create_image(x, y, image=img, anchor=NW)



# This dictionary stores all the primitives of the Tkinter library.
ffp_tkinter = {
	"canvas": __tkinter_canvas,
	"after": __tkinter_after,
	"line": __tkinter_line,
	"pie": __tkinter_pie,
	"arc": __tkinter_arc,
	"circle": __tkinter_circle,
	"rectangle": __tkinter_rectangle,
	"text": __tkinter_text,
	"image": __tkinter_image
}
