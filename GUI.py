# Author: Juan Diego Cardenas
# Date: 7/2/2016
# Copyright: (C) Juan Diego Cardenas
# Licence:  GNU GENERAL PUBLIC LICENSE
#---------------------------------------

from Tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.lines as lines
import matplotlib.patches as patches
import Busqueda
import math

import numpy as np
import copy

style.use("ggplot")

class Ambiente:
    def __init__(self):
        self.mapa = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
                     [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                     [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1],
                     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                     [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                     [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                     [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 1]]

        self.obst = copy.copy(self.mapa)
        self.ubicaRob = [-1, -1]
        self.BuscarDatos()


    def BuscarDatos(self):
        ubica = [-1, -1]
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                if self.mapa[i][j] == 2: #Localiza el robot
                    self.ubicaRob = [i, j]
                    self.obst[i][j] = 0
                """
                if self.mapa[i][j] == 3: #Localiza la meta
                    UbicaMeta = [i, j]
                    self.obst[i, j] = 0
                """


    def GenerarRuta(self):
        self.solucion = gensol(self.mapa)
        self.nodesol = busquedaancho(self.mapa, self.solucion)
        self.ruta = printresult(self.nodesol, self.mapa)

class GUICanvas:
    def __init__(self, master):

        # Parametros de posicion
        ejeX = 7
        ejeY = 455

        # El robot
        robot = Robot()

        #-------------Grafica de movimiento----------

        frameSim = Frame(master)
        frameSim.pack(side = TOP, fill=BOTH, expand=1)
        frameSim.master.title("Simulacion robot movil")

        figSim = Figure(figsize=(6.7, 6), dpi = 75)
        plotSim = figSim.add_subplot(111)

        # Parametros de grafica de simulacion
        plotSim.set_title("Simulacion movimiento del robot")
        plotSim.set_xlabel("X [cm]")
        plotSim.set_ylabel("Y [cm]")
        #plotSim.axis([0, 10, 0 , 10])
        #plotSim.set_autoscale_on(False)

        ambiente = Ambiente()

        plotSim.matshow(ambiente.obst)
        robot.DibuRobot(figSim, plotSim, ambiente.ubicaRob)
        plotSim.plot()

        canvas = FigureCanvasTkAgg(figSim, master)
        canvas.show()
        canvas.get_tk_widget().place(x = ejeX, y = 0)

        #-----------Botones y labels------------------

        self.EtiquetaVelL = Label(frameSim, text = "Velocidad lineal maxima").place(x = ejeX, y = ejeY)
        self.EntradaVelL = Entry(master)
        self.EntradaVelL.place(x = ejeX + 180, y = ejeY)

        self.EtiquetaVelR = Label(frameSim, text = "Velocidad angular maxima").place(x = ejeX, y = ejeY + 30)
        self.EntradaVelR = Entry(master)
        self.EntradaVelR.place(x = ejeX + 180, y = ejeY + 30)

        self.EtiquetaTiempo = Label(frameSim, text = "Tiempo de simulacion").place(x = ejeX, y = ejeY + 60)
        self.EntradaTiempo = Entry(master)
        self.EntradaTiempo.place(x = ejeX + 180, y = ejeY + 60)

        self.BotonSalir = Button(frameSim, text = "Salir", command = frameSim.quit).place(x = 410, y = ejeY + 40)

        self.BotonEjecutar = Button(frameSim, text = "Ejecutar", command = self.ejecutar).place(x = 410, y = ejeY + 10)

        #---------Grafica de posicion en X------------

        figPlots1 = Figure(figsize=(6, 5.5), dpi = 40)
        plot1 = figPlots1.add_subplot(111)

        #FUNCION PARA OBTENER LA MEDIDA DEL MAPA
        #print(figPlots1.get_size_inches()*figPlots1.dpi)

        # Parametros de grafica de simulacion
        plot1.set_title("Posicion en X")
        plot1.set_xlabel("t [s]")
        plot1.set_ylabel("X [cm]")
        plot1.axis([0, 10, 0, 10])
        plot1.set_autoscale_on(False)

        # Datos inutiles BORRAR!!!!

        line1 = [(1,0), (2,2)]
        line2 = [(0,1), (2,2)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        """
        plot1.add_line(lines.Line2D(line1_xs, line1_ys, linewidth=2, color='blue'))
        plot1.add_line(lines.Line2D(line2_xs, line2_ys, linewidth=2, color='red'))

        plot1.plot()
        """
        canvas1 = FigureCanvasTkAgg(figPlots1, master)
        canvas1.show()
        canvas1.get_tk_widget().place(x = ejeX + 510, y = 0)

        #---------Grafica de posicion en Y------------

        figPlots2 = Figure(figsize=(6, 5.5), dpi = 40)
        plot2 = figPlots2.add_subplot(111)

        # Parametros de grafica de simulacion
        plot2.set_title("Posicion en Y")
        plot2.set_xlabel("t [s]")
        plot2.set_ylabel("Y [cm]")
        plot2.axis([0, 10, 0 , 10])
        plot2.set_autoscale_on(False)

        # Datos inutiles BORRAR!!!!
        #plot2.plot(t, s)

        canvas2 = FigureCanvasTkAgg(figPlots2, master)
        canvas2.show()
        canvas2.get_tk_widget().place(x = ejeX + 510, y = 230)

        #---------Grafica de velocidad lineal------------

        figPlots3 = Figure(figsize=(6, 5.5), dpi = 40)
        plot3 = figPlots3.add_subplot(111)

        # Parametros de grafica de simulacion
        plot3.set_title("Velocidad lineal")
        plot3.set_ylabel("v [cm/s]")
        plot3.set_xlabel("t [s]")
        plot3.axis([0, 10, 0 , 10])
        plot3.set_autoscale_on(False)

        # Datos inutiles BORRAR!!!!
        #plot3.plot(t, s)

        canvas3 = FigureCanvasTkAgg(figPlots3, master)
        canvas3.show()
        canvas3.get_tk_widget().place(x = ejeX + 765, y = 0)

        #---------Grafica de velocidad angular------------

        figPlots4 = Figure(figsize=(6, 5.5), dpi = 40)
        plot4 = figPlots4.add_subplot(111)

        # Parametros de grafica de simulacion
        plot4.set_title("Velocidad angular")
        plot4.set_ylabel("w [rad/s]")
        plot4.set_xlabel("t [s]")
        plot4.axis([0, 10, 0 , 10])
        plot4.set_autoscale_on(False)

        # Datos inutiles BORRAR!!!!
        #plot4.plot(t, s)

        canvas4 = FigureCanvasTkAgg(figPlots4, master)
        canvas4.show()
        canvas4.get_tk_widget().place(x = ejeX + 765, y = 230)

        #---------Grafica de aceleracion lineal------------

        figPlots5 = Figure(figsize=(6, 5.5), dpi = 40)
        plot5 = figPlots5.add_subplot(111)

        # Parametros de grafica de simulacion
        plot5.set_title("Aceleracion lineal")
        plot5.set_ylabel("a [cm/s^2]")
        plot5.set_xlabel("t [s]")
        plot5.axis([0, 10, 0 , 10])
        plot5.set_autoscale_on(False)

        # Datos inutiles BORRAR!!!!
        #plot5.plot(t, s)

        canvas5 = FigureCanvasTkAgg(figPlots5, master)
        canvas5.show()
        canvas5.get_tk_widget().place(x = ejeX + 1020, y = 0)

        #---------Grafica de aceleracion angular------------

        figPlots6 = Figure(figsize=(6, 5.5), dpi = 40)
        plot6 = figPlots6.add_subplot(111)

        # Parametros de grafica de simulacion
        plot6.set_title("Aceleracion algunar")
        plot6.set_ylabel("alfa [rad/s^2]")
        plot6.set_xlabel("t [s]")
        plot6.axis([0, 10, 0 , 10])
        plot6.set_autoscale_on(False)

        # Datos inutiles BORRAR!!!!
        #plot6.plot(t, s)

        canvas6 = FigureCanvasTkAgg(figPlots6, master)
        canvas6.show()
        canvas6.get_tk_widget().place(x = ejeX + 1020, y = 230)

    def ejecutar(self, ambiente, plotSim):
        VelR = self.EntradaVelR.get() #Valores de velocidad lineal
        VelL = self.EntradaVelL.get() #Valores de velocidad rotacional
        Tiempo = self.EntradaTiempo.get() #Valor de tiempo


    def simulacion(self, VelR, VelL, Tiempo, robot):

        VelDer = (2*VelL + VelR*robot.linea)/(2*R)
        VelIzq = (2*VelL - VelR*robot.linea)/(2*R)



    #def plotRobot(self, robot):


class Robot:
    def __init__(self):
        self.pos = [0, 0, 0] #vector de estados [X, Y, angulo]
        self.dibujo = patches.Circle((0, 0),4,color='white')
        self.radio = 5
        self.linea = 10

    def DibuRobot(self, fig, plot, ubic):
        self.pos[0] = ubic[0]
        self.pos[1] = ubic[1]
        self.dibujo = patches.Circle((self.pos[1],self.pos[0]),0.4,color='white')
        plot.add_patch(self.dibujo)


def main():
    rootSim = Tk()
    rootSim.geometry("1280x550")
    interfazSim = GUICanvas(rootSim)
    rootSim.mainloop()


if __name__ == '__main__':
    main()