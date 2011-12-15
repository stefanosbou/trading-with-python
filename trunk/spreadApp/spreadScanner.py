'''
Created on 12 dec. 2011
Copyright: Jev Kuznetsov
License: BSD
'''

import sys, os

__version__ = "0.0.1"

from PyQt4.QtCore import (Qt, SIGNAL)
from PyQt4.QtGui import *

import widgets.ui_symbolChooser
from tradingWithPython.lib.yahooFinance import getScreenerSymbols
import qrc_resources

class SymbolChooser(QWidget,widgets.ui_symbolChooser.Ui_Form):
    def __init__(self,parent=None):
        super(SymbolChooser,self).__init__(parent)
        self.setupUi(self)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        # general vars
        self.filename = None
        self.actions = {} # actions list
        
        # build symbols dock
        dock = QDockWidget("Symbols",self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.symbolChooser =SymbolChooser()
        dock.setWidget(self.symbolChooser)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
       
        #fill central area
        self.setCentralWidget(QTextEdit())
        
        #create actions
        self.actions['loadScreener'] = self.createAction("Load symbols",self.loadScreenerSymbols,icon="fileopen")
        
        #set app menu
        self.createMenu()
        self.createToolbars()
        
        self._testFcn()
        
    def createMenu(self):
        menu = self.menuBar()
        menu.addMenu("File").addAction(self.actions['loadScreener'])
    
    def createToolbars(self):
        t = self.addToolBar("File")
        t.setObjectName("FileToolBar")  
        t.addAction(self.actions['loadScreener']) 
        
    def loadScreenerSymbols(self, fName = None):
        ' load symbols from screener csv'
        
        if fName is None:
            formats = ['*.csv']
            path = (os.path.dirname(self.filename)
                   if self.filename is not None else ".")
            
            fName = unicode(QFileDialog.getOpenFileName(self,"Open yahoo screener file",path,
                                                        "CSV files ({0})".format(" ".join(formats))))
        
        if fName:
            symbols = getScreenerSymbols(fName)
            self.symbolChooser.listSymbols.clear()
            self.symbolChooser.listSymbols.addItems(symbols)
            self.filename = fName
            
    
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    def _testFcn(self):
        self.loadScreenerSymbols('gold_stocks.csv')
        
    
def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()


main()
        