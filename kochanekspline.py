#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
import sys
import os.path

from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class VTKFrame(QtGui.QFrame):
    def __init__(self, parent = None):
        super(VTKFrame, self).__init__(parent)

        self.vtkWidget = QVTKRenderWindowInteractor(self)
        vl = QtGui.QVBoxLayout(self)
        vl.addWidget(self.vtkWidget)
        vl.setContentsMargins(0, 0, 0, 0)
 
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0.1, 0.2, 0.4)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
 
        # Create source
        pointSource = vtk.vtkPointSource()
        pointSource.SetNumberOfPoints(5)
        pointSource.Update()

        points = pointSource.GetOutput().GetPoints()
        xSpline = vtk.vtkKochanekSpline()
        ySpline = vtk.vtkKochanekSpline()
        zSpline = vtk.vtkKochanekSpline()

        spline = vtk.vtkParametricSpline()
        spline.SetXSpline(xSpline)
        spline.SetYSpline(ySpline)
        spline.SetZSpline(zSpline)
        spline.SetPoints(points)

        functionSource = vtk.vtkParametricFunctionSource()
        functionSource.SetParametricFunction(spline)
        functionSource.Update()
 
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(functionSource.GetOutputPort())
 
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
 
        self.ren.AddActor(actor)
        self.ren.ResetCamera()

        self._initialized = False

    def showEvent(self, evt):
        if not self._initialized:
            self.iren.Initialize()
            self.startTimer(30)
            self._initialized = True

    def timerEvent(self, evt):
        self.ren.GetActiveCamera().Azimuth(1)
        self.vtkWidget.GetRenderWindow().Render()
 
class MainPage(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainPage, self).__init__(parent)
        self.setCentralWidget(VTKFrame())

        self.setWindowTitle("Kochanek Spline example")

    def categories(self):
        return ['Demo']

    def mainClasses(self):
        return ['vtkParametricSpline', 'vtkParametricFunctionSource', 'vtkKochanekSpline', 'vtkPoints']

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = MainPage()
    w.show()
    sys.exit(app.exec_())