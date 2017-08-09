#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of py_Qt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt4 import QtCore, QtGui


NoTransformation, Translate, Rotate, Scale = range(4)

class RenderArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RenderArea, self).__init__(parent)

        newFont = self.font()
        newFont.setPixelSize(12)
        self.setFont(newFont)

        fontMetrics = QtGui.QFontMetrics(newFont)
        self.xBoundingRect = fontMetrics.boundingRect("x")
        self.yBoundingRect = fontMetrics.boundingRect("y")
        self.shape = QtGui.QPainterPath()
        self.operations = []

    def setOperations(self, operations):
        self.operations = operations
        self.update()

    def setShape(self, shape):
        self.shape = shape
        self.update()

    def minimumSizeHint(self):
        return QtCore.QSize(182, 182)

    def sizeHint(self):
        return QtCore.QSize(232, 232)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtCore.Qt.white))

        painter.translate(66, 66)

        painter.save()
        self.transformPainter(painter)
        self.drawShape(painter)
        painter.restore()

        self.drawOutline(painter)

        self.transformPainter(painter)
        self.drawCoordinates(painter)

    def drawCoordinates(self, painter):
        painter.setPen(QtCore.Qt.red)

        painter.drawLine(0, 0, 50, 0)
        painter.drawLine(48, -2, 50, 0)
        painter.drawLine(48, 2, 50, 0)
        painter.drawText(60 - self.xBoundingRect.width() / 2,
                         0 + self.xBoundingRect.height() / 2, "x")

        painter.drawLine(0, 0, 0, 50)
        painter.drawLine(-2, 48, 0, 50)
        painter.drawLine(2, 48, 0, 50)
        painter.drawText(0 - self.yBoundingRect.width() / 2,
                         60 + self.yBoundingRect.height() / 2, "y")

    def drawOutline(self, painter):
        painter.setPen(QtCore.Qt.darkGreen)
        painter.setPen(QtCore.Qt.DashLine)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(0, 0, 100, 100)

    def drawShape(self, painter):
        painter.fillPath(self.shape, QtCore.Qt.blue)

    def transformPainter(self, painter):
        for operation in self.operations:
            if operation == Translate:
                painter.translate(50, 50)

            elif operation == Scale:
                painter.scale(0.75, 0.75)

            elif operation == Rotate:
                painter.rotate(60)


class Window(QtGui.QWidget):

    operationTable = (NoTransformation, Rotate, Scale, Translate)
    NumTransformedAreas = 3

    def __init__(self):
        super(Window, self).__init__()

        self.originalRenderArea = RenderArea()

        self.shapeComboBox = QtGui.QComboBox()
        self.shapeComboBox.addItem("Clock")
        self.shapeComboBox.addItem("House")
        self.shapeComboBox.addItem("Text")
        self.shapeComboBox.addItem("Truck")

        layout = QtGui.QGridLayout()
        layout.addWidget(self.originalRenderArea, 0, 0)
        layout.addWidget(self.shapeComboBox, 1, 0)

        self.transformedRenderAreas = list(range(Window.NumTransformedAreas))
        self.operationComboBoxes = list(range(Window.NumTransformedAreas))

        for i in range(Window.NumTransformedAreas):
            self.transformedRenderAreas[i] = RenderArea()

            self.operationComboBoxes[i] = QtGui.QComboBox()
            self.operationComboBoxes[i].addItem("No transformation")
            self.operationComboBoxes[i].addItem("Rotate by 60\xB0")
            self.operationComboBoxes[i].addItem("Scale to 75%")
            self.operationComboBoxes[i].addItem("Translate by (50, 50)")

            self.operationComboBoxes[i].activated.connect(self.operationChanged)

            layout.addWidget(self.transformedRenderAreas[i], 0, i + 1)
            layout.addWidget(self.operationComboBoxes[i], 1, i + 1)

        self.setLayout(layout)
        self.setupShapes()
        self.shapeSelected(0)

        self.setWindowTitle("Transformations")

    def setupShapes(self):
        truck = QtGui.QPainterPath()
        truck.setFillRule(QtCore.Qt.WindingFill)
        truck.moveTo(0.0, 87.0)
        truck.lineTo(0.0, 60.0)
        truck.lineTo(10.0, 60.0)
        truck.lineTo(35.0, 35.0)
        truck.lineTo(100.0, 35.0)
        truck.lineTo(100.0, 87.0)
        truck.lineTo(0.0, 87.0)
        truck.moveTo(17.0, 60.0)
        truck.lineTo(55.0, 60.0)
        truck.lineTo(55.0, 40.0)
        truck.lineTo(37.0, 40.0)
        truck.lineTo(17.0, 60.0)
        truck.addEllipse(17.0, 75.0, 25.0, 25.0)
        truck.addEllipse(63.0, 75.0, 25.0, 25.0)

        clock = QtGui.QPainterPath()
        clock.addEllipse(-50.0, -50.0, 100.0, 100.0)
        clock.addEllipse(-48.0, -48.0, 96.0, 96.0)
        clock.moveTo(0.0, 0.0)
        clock.lineTo(-2.0, -2.0)
        clock.lineTo(0.0, -42.0)
        clock.lineTo(2.0, -2.0)
        clock.lineTo(0.0, 0.0)
        clock.moveTo(0.0, 0.0)
        clock.lineTo(2.732, -0.732)
        clock.lineTo(24.495, 14.142)
        clock.lineTo(0.732, 2.732)
        clock.lineTo(0.0, 0.0)

        house = QtGui.QPainterPath()
        house.moveTo(-45.0, -20.0)
        house.lineTo(0.0, -45.0)
        house.lineTo(45.0, -20.0)
        house.lineTo(45.0, 45.0)
        house.lineTo(-45.0, 45.0)
        house.lineTo(-45.0, -20.0)
        house.addRect(15.0, 5.0, 20.0, 35.0)
        house.addRect(-35.0, -15.0, 25.0, 25.0)

        text = QtGui.QPainterPath()
        font = QtGui.QFont()
        font.setPixelSize(50)
        fontBoundingRect = QtGui.QFontMetrics(font).boundingRect("Qt")
        text.addText(-QtCore.QPointF(fontBoundingRect.center()), font, "Qt")

        self.shapes = (clock, house, text, truck)

        self.shapeComboBox.activated.connect(self.shapeSelected)

    def operationChanged(self):
        operations = []
        for i in range(Window.NumTransformedAreas):
            index = self.operationComboBoxes[i].currentIndex()
            operations.append(Window.operationTable[index])
            self.transformedRenderAreas[i].setOperations(operations[:])

    def shapeSelected(self, index):
        shape = self.shapes[index]
        self.originalRenderArea.setShape(shape)
        for i in range(Window.NumTransformedAreas):
            self.transformedRenderAreas[i].setShape(shape)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())