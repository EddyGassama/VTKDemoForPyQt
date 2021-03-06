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
        sphere = vtk.vtkSphere()

        # Sample the function
        sample = vtk.vtkSampleFunction()
        sample.SetSampleDimensions(50, 50, 50)
        sample.SetImplicitFunction(sphere)
        sample.SetModelBounds(-2, 2, -2, 2, -2, 2)

        # Create the 0 isosurface
        contours = vtk.vtkContourFilter()
        contours.SetInputConnection(sample.GetOutputPort())
        contours.GenerateValues(1, 1, 1)

        # Map the contours to graphical primitives
        contourMapper = vtk.vtkPolyDataMapper()
        contourMapper.SetInputConnection(contours.GetOutputPort())
        contourMapper.SetScalarRange(0, 1.2)
 
        # Create an actor for the contours
        contourActor = vtk.vtkActor()
        contourActor.SetMapper(contourMapper)

        # -- Create a box around the function to indicated the sampling volume
        
        # Create outline
        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(sample.GetOutputPort())

        # Map it to graphics primitives
        outlineMapper = vtk.vtkPolyDataMapper()
        outlineMapper.SetInputConnection(outline.GetOutputPort())

        # Create an actor for it
        outlineActor = vtk.vtkActor()
        outlineActor.SetMapper(outlineMapper)
        outlineActor.GetProperty().SetColor(0, 0, 0)
 
        self.ren.AddActor(contourActor)
        self.ren.AddActor(outlineActor)
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

        self.setWindowTitle("Sample Function Example")

    def categories(self):
        return ['Implicit Function', 'Filters']

    def mainClasses(self):
        return ['vtkSphere', 'vtkSampleFunction', 'vtkContourFilter', 'vtkOutlineFilter']

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = MainPage()
    w.show()
    sys.exit(app.exec_())
