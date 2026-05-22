from textual.app import ComposeResult
from textual.widget import Widget
from textual_plotext import PlotextPlot
from textual.reactive import reactive


class GraphView(Widget):

    data = reactive([("01/01/1999", 0)])

    def compose(self) -> ComposeResult:
        yield PlotextPlot()

    def watch_data(self, old, new):

        plot = self.query_one(PlotextPlot)
        plt = plot.plt
        plt.clear_figure()

        if len(self.data) > 0:
            x, y = zip(*self.data)
            plt.plot(x, y)
        plot.refresh()