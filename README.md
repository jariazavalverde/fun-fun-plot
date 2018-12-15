# Fun Fun Plot
## A Python 2D declarative plotting library

## Examples
#### Scatter plot

```python
ScatterPlot = Plot(Axis(
    Data(
        Circle(
            Xnormal(Attr(Zero)),
            Ynormal(Attr(One)),
            Four,
            background_color = ClassColor(Attr(Two))
        )
    )),
    ffp_tkinter, width = 400, height = 400
)
```

```python
ScatterPlot.draw(iris)
```

![Scatter plot](samples/scatter.png)

## License
Source code is released under the terms of the [BSD 3-Clause License](LICENSE).
