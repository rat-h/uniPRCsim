##################################
#
# glmainwnd.py
# Copyright (C) Louisiana State University, Health Sciences Center
# Written by 2011-2013 Ruben Tikidji-Hamburyan <rth@nisms.krinc.ru>
#                  
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, GOOD TITLE or
# NON INFRINGEMENT.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
###################################
import sys
from PyQt4 import QtGui, QtCore
import glmodel
import icons
import uniprcsimversion

class glmainwnd(QtGui.QMainWindow):
	def __init__(self):
		super(glmainwnd, self).__init__()
		# Resize Window
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.resize(screen.width()/2, screen.height()/2)
		size = self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
		self.setWindowTitle('uniPRCsim')
		self.setWindowIcon(QtGui.QIcon(':/uniPRCsim.png'))
		#self.setToolTip('This is my <b>ToolTip</b> line')
		QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))
		self.statusBar().showMessage('Ready')
		self.model = None

		menubar = self.menuBar()
		toolbar = self.addToolBar('Main')
		self.tree = QtGui.QTreeWidget(self)
		self.setCentralWidget(self.tree)
		self.tree.setColumnCount(3)
		self.tree.setHeaderHidden(1)
		self.tree.setItemsExpandable(1)
		#Exit from APP
		exit = QtGui.QAction(QtGui.QIcon(':/exit.png'), 'Exit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit application')
		self.connect(exit, QtCore.SIGNAL('triggered()'), self.mclose)
		#About DLG
		about = QtGui.QAction(QtGui.QIcon(':/uniPRCsim.png'), 'About uniPRCsim', self)
		about.setStatusTip('About uniPRCsim')
		self.connect(about, QtCore.SIGNAL('triggered()'), self.about)

		file = menubar.addMenu('&File')
		self.model = glmodel.glmodel(parent = self, mainwnd = self, menubar = menubar, toolbar=toolbar, filemenu=file)
		file.addSeparator()
		file.addAction(exit)
		help = menubar.addMenu('&Help')
		help.addAction(about)
		

	def about(self):
		QtGui.QMessageBox.about(self,"About uniPRCsim",	uniprcsimversion.getlongversion())
		return
		
	def mclose(self):
		self.model.close()
		self.close()
		
		
			
if __name__ == '__main__' :
	app = QtGui.QApplication(sys.argv)
	main = glmainwnd()
	main.show()
	sys.exit(app.exec_())
