import sys 
import os
sys.path.append(os.path.abspath("../src"))

from fun_fun_plot.primitives import *
from fun_fun_plot.operators import *
from fun_fun_plot.interfaces.tkinter import *



BarPlot = Plot(
    Axis(
        Data(
            Rectangle(
                Index * (Width / DataLen),
                0,
                Width / DataLen,
                Ynormal(Attr(0)),
                background_color = ClassColor(Attr(2))
            ) +
            Text(
                (0.5 + Index) * (Width / DataLen),
                Ynormal(Attr(0)) - 10,
                Attr(0),
                font_size = 10
            )
        ),
        xticks = Range(DataLen, Width/DataLen/2, Width/DataLen),
        xlabels = Column(1)
    ),
    ffp_tkinter, width = 400, height = 400
)



BarPlot.draw([
    [20.0, "a", "class"],
    [40.0, "b", "class"],
    [15.0, "c", "class"],
    [75.0, "d", "class"],
    [50.0, "e", "class"],
    [23.0, "f", "class"],
    [56.0, "g", "class"]
])
