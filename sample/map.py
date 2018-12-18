import sys 
import os
from math import pi, log, tan, radians
sys.path.append(os.path.abspath("../src"))

from fun_fun_plot.primitives import *
from fun_fun_plot.operators import *
from fun_fun_plot.interfaces.tkinter import *



MapPlot = Plot(
	Image(0, 0, "../res/web-mercator.png") +
	Data(
		Circle(
			Width/(2*pi) * (Call(radians)(Attr(1)) + pi) >> "x",
			Height/(2*pi) * (pi + Call(log)(Call(tan)(pi/4 + Call(radians)(Attr(0))/2))) >> "y",
			3,
			background_color = "red"
		) +
		Text(
			Get("x"),
			Get("y") - 10,
			Attr(2),
			font_size = 10
		)
	),
    ffp_tkinter, width = 830, height = 830
)



MapPlot.draw([
	[48.86,  2.33,   "Paris"],
	[41.9,   12.48,  "Roma"],
	[45.41,  -75.7,  "Ottawa"],
	[54.03,  10.45,  "Berlin"],
	[-34.61, -58.50, "Buenos Aires"],
	[40.43,  -3.82,  "Madrid"],
	[-15.77, -48.07, "Brasilia"],
	[30.06,  31.22,  "El Cairo"],
	[38.89,  -82.0,  "Washington D. C"],
	[60.19,  24.94,  "Helsinki"],
	[4.64,   -74.24, "Bogota"],
	[28.52,  77.13,  "Nueva Delhi"],
	[35.67,  139.56, "Tokio"],
	[39.93,  116.11, "Pekin"],
	[48.22,  16.30,  "Viena"]
])
