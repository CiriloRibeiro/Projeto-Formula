from sys import argv, exit
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QAction, QFileDialog, QInputDialog, QListWidgetItem, QMessageBox
from PyQt5 import QtGui
from demoIniciamento import *
from demoGUI import *
#from functions import *
from serialPlotArduino import *
from mplwidget import MplWidget
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
##portName: Antena: 'COM6'
##          Cabo: 'COM3' ou a entrada normalmente usada pelo seu arduino
portName = 'COM6'
baudRate = 57600
maxPlotLength = 100
dataNumBytes = 4        # number of bytes of 1 data point
numPlots = 3

class Window(QMainWindow):
    """classe principal -> GUI"""
    def __init__(self, s):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('formula.ico'))
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.addToolBar(NavigationToolbar(self.gui.MplWidget.canvas, self))
        self.plotOption = self.gui.MplWidget.plotOption #inicia plotOption
        #como 'SUBPLOT_OFF', ver mplwidget.py
        self.subplotIndex = self.gui.MplWidget.subplotIndex #inicia o index
        #ver mplwidget.py

        self.gui.actionDesconectar.triggered.connect(self.quit)
        self.gui.actionAtivar.changed.connect(self.checkSubplot)
        self.gui.actionPlot_2.triggered.connect(self.turnPlot_2)
        self.gui.actionPlot_3.triggered.connect(self.turnPlot_3)



        self.timer = self.gui.MplWidget.canvas.new_timer(interval = 10, callbacks =[(self.updateCanvas, [], {})])
        self.timer.start()
        self.show()

    def quit(self):
        s.close()
        exit()

    def updateCanvas(self): #metodo que chama a função plotConstructor
    #com os parametros abaixo
    #ver functions.py
        """dados do gráfico e plotagem"""
        # plotConstructor(self.gui.MplWidget, 'data.csv', times, 'SUBPLOT_ON')
        # plotConstructor(self.gui.MplWidget, 'data.csv', self.subplotIndex, self.plotOption)

        ax = self.gui.MplWidget.axes
        ax.cla()
        ax.clear()
        ax.set_title('Acelerômetro')
        ax.set_xlabel("time")
        #ax.set_ylabel("AnalogRead Value")

        #lineLabel = 'Potentiometer Value'
        #timeText = ax.text(0.50, 0.95, '', transform=ax.transAxes)
        #lineValueText = ax.text(0.50, 0.90, '', transform=ax.transAxes)
        #lines = ax.plot([], [], label=lineLabel)[0]

        lineLabel = ['X', 'Y', 'Z']
        style = ['r-', 'c-', 'b-']  # linestyles for the different plots
        timeText = ax.text(0.70, 0.95, '', transform=ax.transAxes)
        lines = []
        lineValueText = []
        for i in range(numPlots):
            lines.append(ax.plot([], [], style[i], label=lineLabel[i])[0])
            lineValueText.append(ax.text(0.70, 0.90-i*0.05, '', transform=ax.transAxes))
        s.getSerialData(lines, lineValueText, lineLabel, timeText)
        ax.relim()
        ax.legend(loc="upper left")
        self.gui.MplWidget.canvas.draw()

    #MplWidget.axes.clear() #importante
    #MplWidget.axes.cla() #importante
    #MplWidget.axes.plot(*parametros dos dados lidos pela serial)
    #MplWidget.axes.set_xlabel("legenda dos dados lidos pela serial")
    #MplWidget.axes.legend(*parametros)
    #MplWidget.axes.grid(True) #importante
    #MplWidget.axes.relim() #importante

    def turnPlot_2(self):
        self.subplotIndex = 2
        print("PLOT_2 LIGADO")
        print("----------------------")

    def turnPlot_3(self):
        self.subplotIndex = 3
        print("PLOT_3 LIGADO")
        print("----------------------")


    def checkSubplot(self):
        if self.gui.actionAtivar.isChecked():
            self.gui.actionAtivar.setChecked(True)
            self.plotOption = "SUBPLOT_ON"
            print("teste: LIGADO")
        else:
            self.gui.actionAtivar.setChecked(False)
            print("teste: DESLIGADO")
            self.plotOption = "SUBPLOT_OFF"
        print(self.plotOption)
        print("----------------------")



if __name__ == '__main__':
    try:
        s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes, numPlots)   # initializes all required variables
        s.readSerialStart()
    except Exception as e:
        # raise e
        s.close()
        exit()
    QApplication.setStyle("Fusion")
    app = QApplication(argv)
    w = Window(s)
    w.show()
    exit(app.exec_())
