from pandas import read_csv
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from pandas import Series
#ver linha 41, 61, 91, 199
#Funções de teste do gráfico

def plotConstructor(MplWidget, file, times = 1, subplot = 'SUBPLOT_OFF'): ##Debug
    """Plota um gráfico a partir de MplWidget.axes,
    sendo times o número de sensores plotados
    e file um arquivo csv
    Se espera no csv as colunas:
    tempo; sensor_1; sensor_2; sensor_3
    problema: no momento apenas funciona com "data.csv"
    """
    MplWidget.plotOption = subplot #decide se vai ligar ou nao os subplots
    MplWidget.turnSubplot() #metodo de MplWidget para atualizar a decisão
    if file == 'data.csv': #para que a construção do gráfico seja feita apenas
    #usando 'data.csv'
    #usando serial, vc pode salvar os dados lidos pela serial num .csv
    #ou pode pensar numa forma de implementar diretamente passando para lista
        if subplot == 'SUBPLOT_OFF':
            createPlot(MplWidget, file, times)
        if subplot == 'SUBPLOT_ON':
            createSubplot(MplWidget, file, times)
    MplWidget.canvas.draw() #faz o desenho do grafico após sua criação

def createPlot(MplWidget, file, times):
    times = 3
    sensor_SG, sensor_T, sensor_A, tempo = dataCSVReader(file, times)
    #tempo = Series(tempo) / 60
    MplWidget.axes.clear() #importante
    MplWidget.axes.cla() #importante
    #MplWidget.axes.plot() faz a plotagem com os parametros abaixo
    timeConverter = False
    if timeConverter == False: #aqui fiz uma lógica para passar de s para min
        MplWidget.axes.set_xlabel('Tempo [s]')
        if max(tempo) <= 25:
            MplWidget.axes.plot(tempo, sensor_SG, label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
            MplWidget.axes.plot(tempo, sensor_T, label = 'T', color = colorDict["Temperatura"])
            MplWidget.axes.plot(tempo, sensor_A, label = 'Acelerômetro', color = colorDict["Acelerometro"])
        if max(tempo) > 25 and max(tempo) < 90:
            MplWidget.axes.plot(tempo[-25:], sensor_SG[-25:], label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
            MplWidget.axes.plot(tempo[-25:], sensor_T[-25:], label = 'T', color = colorDict["Temperatura"])
            MplWidget.axes.plot(tempo[-25:], sensor_A[-25:], label = 'Acelerômetro', color = colorDict["Acelerometro"])
    if max(tempo) > 90:
        timeConverter = True
    if timeConverter == True:
        tempo = Series(tempo) / 60
        MplWidget.axes.set_xlabel('Tempo [min]')
        MplWidget.axes.plot(tempo[-30:], sensor_SG[-30:], label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
        MplWidget.axes.plot(tempo[-30:], sensor_T[-30:], label = 'T', color = colorDict["Temperatura"])
        MplWidget.axes.plot(tempo[-30:], sensor_A[-30:], label = 'Acelerômetro', color = colorDict["Acelerometro"])
    MplWidget.axes.legend(bbox_to_anchor=(0, 0.99, 0, 0), loc = 3, ncol=3, borderaxespad=0)
    MplWidget.axes.grid(True) #importante
    MplWidget.axes.relim() #importante

#ou seja, para plotar o grafico, vc precisa que o metodo updateCanvas  ( ver linha 227, testesQt.py)
#chame uma função, por exemplo, f(), que faça:
#def f(MplWidget, *parametros que vc precisa):
    #MplWidget.axes.clear() #importante
    #MplWidget.axes.cla() #importante
    #MplWidget.axes.plot(*parametros dos dados lidos pela serial)
    #MplWidget.axes.set_xlabel("legenda dos dados lidos pela serial")
    #MplWidget.axes.legend(*parametros)
    #MplWidget.axes.grid(True) #importante
    #MplWidget.axes.relim() #importante
    #MplWidget.canvas.draw() #faz o desenho do grafico após sua criação
#tudo isso para plotar em apenas um unico grafico
#se quiser mais de um grafico, veja as funções createSubplot, subplot2 e subplot3
#que são repetições desse codigo
#para mais de um grafico, é preciso de mais de um .axes
#no caso, chamei de ax1, ax2 e ax3

def createSubplot(MplWidget, file, subplotIndex):
    MplWidget.subplotIndex = subplotIndex
    MplWidget.turnSubplot()
    # plotDict = MplWidget.plotDictionary
    counter_1 = 0
    counter_2 = 0
    if subplotIndex == 1:
        times = 1
        MplWidget.turnSubplot()
        s1, tempo = dataCSVReader(file, times)
    if subplotIndex == 2:
        times = 2

        s1, s2, tempo = dataCSVReader(file, times)
        subplot2(MplWidget, tempo, s1, s2)
    if subplotIndex == 3:
        times = 3

        # for i in MplWidget.plotDictionary:
        #     if MplWidget.plotDictionary[i]["Grafico_1"] == True:
        #         pass
        #     if MplWidget.plotDictionary[i]["Grafico_2"] == True:
        #         pass
        #     if MplWidget.plotDictionary[i]["Grafico_3"] == True:
        #         pass

        MplWidget.turnSubplot()
        s1, s2, s3, tempo = dataCSVReader(file, times)
        subplot3(MplWidget, tempo, s1, s2, s3)

def subplot2(MplWidget, tempo, s1, s2):
    MplWidget.ax1.clear()
    MplWidget.ax2.clear()
    timeConverter = False
    if timeConverter == False:
        MplWidget.ax2.set_xlabel('Tempo [s]')
        if max(tempo) <= 25:
            MplWidget.ax1.plot(tempo, s1, label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
            MplWidget.ax2.plot(tempo, s2, label = 'T', color = colorDict["Temperatura"])
        if max(tempo) > 25 and max(tempo) < 90:
            MplWidget.ax1.plot(tempo[-25:], s1[-25:], label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
            MplWidget.ax2.plot(tempo[-25:], s2[-25:], label = 'T', color = colorDict["Temperatura"])
    if max(tempo) > 90:
        timeConverter = True
    if timeConverter == True:
        tempo = Series(tempo) / 60
        MplWidget.ax2.set_xlabel('Tempo [min]')
        MplWidget.ax1.plot(tempo[-30:], s1[-30:], label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
        MplWidget.ax2.plot(tempo[-30:], s2[-30:], label = 'T', color = colorDict["Temperatura"])

    MplWidget.ax1.relim()
    MplWidget.ax1.legend(bbox_to_anchor=(0, -0.225, 1, 0), loc = 3, ncol=1, borderaxespad=0)
    MplWidget.ax1.grid(True)
    MplWidget.ax2.legend(bbox_to_anchor=(0, -0.225, 1, 0), loc = 3, ncol=1, borderaxespad=0)
    MplWidget.ax2.relim()
    MplWidget.ax2.grid(True)

def subplot3(MplWidget, tempo, s1, s2, s3):
    MplWidget.ax1.clear()
    MplWidget.ax2.clear()
    MplWidget.ax3.clear()
    timeConverter = False
    if timeConverter == False:
        MplWidget.ax3.set_xlabel('Tempo [s]')
        if max(tempo) <= 25:
            MplWidget.ax1.plot(tempo, s1, label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
            MplWidget.ax2.plot(tempo, s2, label = 'T', color = colorDict["Temperatura"])
            MplWidget.ax3.plot(tempo, s3, label = 'Acelerômetro', color = colorDict["Acelerometro"])
        if max(tempo) > 25 and max(tempo) < 90:
            MplWidget.ax1.plot(tempo[-25:], s1[-25:], label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
            MplWidget.ax2.plot(tempo[-25:], s2[-25:], label = 'T', color = colorDict["Temperatura"])
            MplWidget.ax3.plot(tempo[-25:], s3[-25:], label = 'Acelerômetro', color = colorDict["Acelerometro"])
    if max(tempo) > 90:
        timeConverter = True
    if timeConverter == True:
        tempo = Series(tempo) / 60
        MplWidget.ax3.set_xlabel('Tempo [min]')
        MplWidget.ax1.plot(tempo[-30:], s1[-30:], label = 'Strain Gauge', color = colorDict["Strain_Gauge"])
        MplWidget.ax2.plot(tempo[-30:], s2[-30:], label = 'T', color = colorDict["Temperatura"])
        MplWidget.ax3.plot(tempo[-30:], s3[-30:], label = 'Acelerômetro', color = colorDict["Acelerometro"])

    MplWidget.ax1.relim()
    MplWidget.ax1.legend(bbox_to_anchor=(0, -0.225, 1, 0), loc = 3, ncol=1, borderaxespad=0)
    MplWidget.ax1.grid(True)
    MplWidget.ax2.legend(bbox_to_anchor=(0, -0.225, 1, 0), loc = 3, ncol=1, borderaxespad=0)
    MplWidget.ax2.relim()
    MplWidget.ax2.grid(True)
    MplWidget.ax3.legend(bbox_to_anchor=(0, -0.425, 1, 0), loc = 3, ncol=1, borderaxespad=0)
    MplWidget.ax3.relim()
    MplWidget.ax3.grid(True)

def dataCSVReader(file, times = 1): #função que faz a leitura do .csv
#para testes, se usar outros dados, é só mudar os parametros tempo,
#sensor_1,sensor_2 e sensor_3 de acordo com as colunas do seu .csv
        data = read_csv(file)
        t = data['tempo']
        s1 = data['sensor_1']
        s2 = data['sensor_2']
        s3 = data['sensor_3']
        if times == 1:
            return (s1, t)
        if times == 2:
            return (s1, s2, t)
        if times == 3:
            return (s1, s2, s3, t)
