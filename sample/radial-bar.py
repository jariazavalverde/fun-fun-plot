import sys 
import os
sys.path.append(os.path.abspath("../src"))

from fun_fun_plot.primitives import *
from fun_fun_plot.operators import *
from fun_fun_plot.interfaces.tkinter import *



RadialBarPlot = Plot(
    Rectangle(0, 0, Width, Height, background_color = "white", border_width = 0) +
    Data(
        Pie(
            Width / 2,
            Height / 2,
            Width / 2 / (DataLen + 2) * (DataLen - Index + 1) >> "height",
            90,
            -270,
            background_color = "white"
        ) +
        Pie(
            Width / 2,
            Height / 2,
            Get("height"),
            90,
            Normal(Attr(0), Column(0)) * (-180) - 90,
            background_color = ClassColor(Attr(2))
        ) +
        Text(
            Width / 2,
            Height / 2 + Get("height") - 10,
            Attr(1) + " ",
            text_align = "right",
            font_size = 12
        )
    ) +
    Circle(
        Width / 2,
        Height / 2,
        Width / 2 / (DataLen + 2),
        background_color = "white",
        border_width = 0
    ) +
    Arc(
        Width / 2,
        Height / 2,
        Width / 2 / (DataLen + 2),
        90,
        -270
    ),
    ffp_tkinter, width = 400, height = 400
)



RadialBarPlot.draw([
	[27.0, "Dark",     "class"],
	[26.0, "Light",    "class"],
	[15.0, "Water",    "class"],
	[13.0, "Electric", "class"],
	[13.0, "Neutral",  "class"],
	[12.0, "Wind",     "class"],
	[10.0, "Plant",    "class"],
	[9.0,  "Fire",     "class"],
	[6.0,  "Earth",    "class"]
])
