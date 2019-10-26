from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import style
style.use(['dark_background', 'seaborn', 'fast'])


class MplWidget(QWidget):
      def __init__(self, parent = None):
            super().__init__()
            self.createFigure()
            self.plotOption = 'SUBPLOT_OFF'
            self.subplotIndex = 3
            vertical_layout = QVBoxLayout()
            vertical_layout.setContentsMargins(0, 0, 0, 0)
            vertical_layout.addWidget(self.canvas)
            if self.plotOption == 'SUBPLOT_OFF':
                  self.canvas.figure.clf()
                  self.axes = self.canvas.figure.subplots()
                  self.axes.set_autoscale_on(True)
            self.setLayout(vertical_layout)

      def createFigure(self):
            fig = Figure(dpi=100)
            self.fig = fig
            self.canvas = FigureCanvas(fig)
            self.canvas.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.canvas.updateGeometry()

      def turnSubplot(self):
            if self.plotOption == 'SUBPLOT_OFF':
                  self.canvas.figure.clf()
                  self.axes = self.canvas.figure.subplots()
                  self.axes.set_autoscale_on(True)
            if self.plotOption == 'SUBPLOT_ON':
                  if self.subplotIndex == 1:
                        self.canvas.figure.clf()
                        self.ax1 = self.canvas.figure.subplots(1, 1, sharex=True)
                        self.ax1.set_autoscale_on(True)
                  if self.subplotIndex == 2:
                        self.canvas.figure.clf()
                        self.ax1, self.ax2 = self.canvas.figure.subplots(2, 1, sharex=True)
                        self.ax1.set_autoscale_on(True)
                        self.ax2.set_autoscale_on(True)
                  if self.subplotIndex == 3:
                        self.canvas.figure.clf()
                        self.ax1, self.ax2, self.ax3 = self.canvas.figure.subplots(3, 1, sharex=True)
                        self.ax1.set_autoscale_on(True)
                        self.ax2.set_autoscale_on(True)
                        self.ax3.set_autoscale_on(True)


