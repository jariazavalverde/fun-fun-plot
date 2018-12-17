import sys 
import os
from math import pi, sin, cos
sys.path.append(os.path.abspath("../src"))

from fun_fun_plot.primitives import *
from fun_fun_plot.operators import *
from fun_fun_plot.interfaces.tkinter import *



PiePlot = Plot(
    Data(
        Empty(
            Get("angle", 0) + Get("alpha", 0) >> "angle"
        ) +
        Pie(
            Width/2,
            Height/2,
            Width/3 >> "radius",
            Get("angle"),
            Attr(0) * 360 / Call(sum)(Column(0)) >> "alpha",
            background_color = ClassColor(Attr(1))
        ) +
        Text(
            Width/2 + Call(cos)((Get("angle") + Get("alpha")/2)*pi/180) * Get("radius")/2,
            Height/2 + Call(sin)((Get("angle") + Get("alpha")/2)*pi/180) * Get("radius")/2,
            Call(str)(Get("alpha") / 3.6) + " %",
            font_size = 12
        )
    ),
    ffp_tkinter, width = 400, height = 400
)



PiePlot.draw([
    [20.0, "a", "class"],
    [40.0, "b", "class"],
    [65.0, "c", "class"],
    [75.0, "d", "class"],
    [50.0, "e", "class"]
])
