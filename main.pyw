from sys import argv, exit
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QAction, QFileDialog, QInputDialog, QListWidgetItem, QMessageBox
from PyQt5 import QtGui
from demoIniciamento import *
from demoGUI import *
from functions import *
from mplwidget import MplWidget
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
#ver linha 120, 95, 98, 227
class MyForm(QDialog):
    """classe para caixa de iniciação"""
    def __init__(self):
        super().__init__()
        self.files = []
        self.index = 0
        self.foiConectado = 0
        self.ui = Ui_dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('formula.ico'))
        self.ui.listWidget.addItem("-------------------------------------------------")
        self.ui.listWidget.addItem("\t  Dialog pré-GUI")
        self.ui.listWidget.addItem("-------------------------------------------------")
        self.ui.pushButtonCarregar.clicked.connect(self.addlist)
        self.ui.pushButtonDeletar.clicked.connect(self.delitem)
        self.ui.pushButtonConectar.clicked.connect(self.connect)
        self.ui.pushButtonIniciar.clicked.connect(self.iniciar)
        self.show()

    def addlist(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '~/Projeto')
        try:
            if fname[0]:
                self.ui.listWidgetCSV.clear()
                self.ui.listWidgetCSV.addItem(fname[0])
                self.files.append(fname[0])
                self.index += 1

        except Exception as e:
            print(e)

    def delitem(self):
        if self.index != 0:
            row = self.ui.listWidgetCSV.currentRow()
            self.ui.listWidgetCSV.takeItem(row)
            try:
                print("{} foi deletado...".format(self.files[row]))
                self.ui.listWidgetCSV.clear()
                self.ui.listWidgetCSV.addItem("------------------------------------------------")
                self.ui.listWidgetCSV.addItem("{} foi deletado...".format(self.files[row]))
                self.ui.listWidgetCSV.addItem("------------------------------------------------")
                self.index -= 1
                self.files.pop(row)
            except Exception as e:
                print(e)

    def connect(self):
        #testes por enquanto
        #print de lista de arquivos
        i = int(self.index)
        print(i)
        try:
            for x in range(i):
                print(self.files[x])
            self.ui.listWidget.addItem("\t  conectado")
            self.ui.listWidget.addItem("-------------------------------------------------")
            self.foiConectado = 1
        except Exception as e:
            print(e)

    def iniciar(self):
        """inicializa a janela principal"""
        if self.index != 0 and self.foiConectado == False: #condição para abrir o gráfico
            graph_file = Window(self.index, self.files) #abre o grafico
            graph_file.show()      #aqui
        if self.index == 0 and self.foiConectado == True:
            graph_mavlink = Window(self.index) #abre o grafico
            graph_mavlink.show()      #aqui
        if  self.index != 0 and self.foiConectado == True:
            graph_file_with_mavlink = Window(self.index, self.files)
            graph_file_with_mavlink.show()
        if  self.index == 0 and self.foiConectado == False:
            self.ui.listWidgetCSV.addItem("ERRO: Conecte ou carregue um arquivo")
        self.close()

class Window(QMainWindow):
    """classe principal -> GUI"""
    def __init__(self, index, files = None):
        super().__init__()
        self.files = files
        self.setWindowIcon(QtGui.QIcon('formula.ico'))
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.addToolBar(NavigationToolbar(self.gui.MplWidget.canvas, self))
        self.plotOption = self.gui.MplWidget.plotOption #inicia plotOption
        #como 'SUBPLOT_OFF', ver mplwidget.py
        self.subplotIndex = self.gui.MplWidget.subplotIndex #inicia o index
        #ver mplwidget.py
        self.plotDictionary = plotDictionary
        self.printDict()

        self.gui.actionAtivar.changed.connect(self.checkSubplot)
        self.gui.actionPlot_2.triggered.connect(self.turnPlot_2)
        self.gui.actionPlot_3.triggered.connect(self.turnPlot_3)

        self.gui.actionGrafico1_SG.changed.connect(self.updatePlotDict)
        self.gui.actionGrafico2_SG.changed.connect(self.updatePlotDict)
        self.gui.actionGrafico3_SG.changed.connect(self.updatePlotDict)

        self.gui.actionGrafico1_T.changed.connect(self.updatePlotDict)
        self.gui.actionGrafico2_T.changed.connect(self.updatePlotDict)
        self.gui.actionGrafico3_T.changed.connect(self.updatePlotDict)

        self.gui.actionGrafico1_A.changed.connect(self.updatePlotDict)
        self.gui.actionGrafico2_A.changed.connect(self.updatePlotDict)
        self.gui.actionGrafico3_A.changed.connect(self.updatePlotDict)

        if index != 0:
            self.filesTest()
        else: #timer que atualiza o grafico usando o método updateCanvas(importante)
            self.timer = self.gui.MplWidget.canvas.new_timer(100, [(self.updateCanvas, (), {})])
            self.timer.start()
        self.show()

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

    def printDict(self):
        #arrumar a estrutura disso!
        print("----------------------")
        for i in self.plotDictionary:
            print(self.plotDictionary[i]["Grafico_1"], end = "\t")
            print(self.plotDictionary[i]["Grafico_2"], end = "\t")
            print(self.plotDictionary[i]["Grafico_3"], end = "\n")
        print("----------------------")

    def clearChecked(self, i):
        if i == 0:
            self.gui.actionGrafico1_SG.setChecked(False)
            self.gui.actionGrafico2_SG.setChecked(False)
            self.gui.actionGrafico3_SG.setChecked(False)
        if i == 1:
            self.gui.actionGrafico1_T.setChecked(False)
            self.gui.actionGrafico2_T.setChecked(False)
            self.gui.actionGrafico3_T.setChecked(False)
        if i == 2:
            self.gui.actionGrafico1_A.setChecked(False)
            self.gui.actionGrafico2_A.setChecked(False)
            self.gui.actionGrafico3_A.setChecked(False)

    def updatePlotDict(self):
        #boolMatrix(bool_1, bool_2, bool_3, index) --> return boolDict[index]
        if self.gui.actionDescartar_SG.isChecked():
            self.gui.actionDescartar_SG.setChecked(True)
            self.plotDictionary[0] = boolMatrix(False, False, False, 0)
            self.clearChecked(0)
        if self.gui.actionDescartar_T.isChecked():
            self.gui.actionDescartar_T.setChecked(True)
            self.plotDictionary[1] = boolMatrix(False, False, False, 1)
            self.clearChecked(1)
        if self.gui.actionDescartar_A.isChecked():
            self.gui.actionDescartar_A.setChecked(True)
            self.plotDictionary[2] = boolMatrix(False, False, False, 2)
            self.clearChecked(2)

        if self.gui.actionGrafico1_SG.isChecked():
            self.plotDictionary[0] = boolMatrix(True, False, False, 0)
            self.gui.actionGrafico1_SG.setChecked(self.plotDictionary[0]["Grafico_1"])
        if self.gui.actionGrafico2_SG.isChecked():
            self.plotDictionary[0] = boolMatrix(False, True, False, 0)
            self.gui.actionGrafico2_SG.setChecked(self.plotDictionary[0]["Grafico_2"])
        if self.gui.actionGrafico3_SG.isChecked():
            self.plotDictionary[0] = boolMatrix(False, False, True, 0)
            self.gui.actionGrafico3_SG.setChecked(self.plotDictionary[0]["Grafico_3"])

        if self.gui.actionGrafico1_T.isChecked():
            self.plotDictionary[1] = boolMatrix(True, False, False, 1)
            self.gui.actionGrafico1_T.setChecked(self.plotDictionary[1]["Grafico_1"])
        if self.gui.actionGrafico2_T.isChecked():
            self.plotDictionary[1] = boolMatrix(False, True, False, 1)
            self.gui.actionGrafico2_T.setChecked(self.plotDictionary[1]["Grafico_2"])
        if self.gui.actionGrafico3_T.isChecked():
            self.plotDictionary[1] = boolMatrix(False, False, True, 1)
            self.gui.actionGrafico3_T.setChecked(self.plotDictionary[1]["Grafico_3"])

        if self.gui.actionGrafico1_A.isChecked():
            self.plotDictionary[2] = boolMatrix(True, False, False, 2)
            self.gui.actionGrafico1_A.setChecked(self.plotDictionary[2]["Grafico_1"])
        if self.gui.actionGrafico2_A.isChecked():
            self.plotDictionary[2] = boolMatrix(False, True, False, 2)
            self.gui.actionGrafico2_A.setChecked(self.plotDictionary[2]["Grafico_2"])
        if self.gui.actionGrafico3_A.isChecked():
            self.plotDictionary[2] = boolMatrix(False, False, True, 2)
            self.gui.actionGrafico3_A.setChecked(self.plotDictionary[2]["Grafico_3"])

        self.printDict()
        self.plotDictionary = self.gui.MplWidget.plotDictionary

    def filesTest(self):
        times = 3
        arq = self.files[0] #corta o caminho
        arq = arq.split('/')[-1]
        print(arq)
        # plotConstructor(self.gui.MplWidget, arq, times, 'SUBPLOT_ON')
        plotConstructor(self.gui.MplWidget, arq, times, self.plotOption)

    def updateCanvas(self): #metodo que chama a função plotConstructor
    #com os parametros abaixo
    #ver functions.py
        """dados do gráfico e plotagem"""
        # plotConstructor(self.gui.MplWidget, 'data.csv', times, 'SUBPLOT_ON')
        plotConstructor(self.gui.MplWidget, 'data.csv', self.subplotIndex, self.plotOption)

if __name__ == '__main__':
    QApplication.setStyle("Fusion")
    app = QApplication(argv)
    w = MyForm()
    w.show()
    exit(app.exec_())
