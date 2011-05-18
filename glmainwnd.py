import sys
from PyQt4 import QtGui, QtCore
import glmodel
import icons

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
		file = menubar.addMenu('&File')
		self.model = glmodel.glmodel(parent = self, mainwnd = self, menubar = menubar, toolbar=toolbar, filemenu=file)
		file.addSeparator()
		file.addAction(exit)
		

		
	def mclose(self):
		self.model.close()
		self.close()
		
		
			
if __name__ == '__main__' :
	app = QtGui.QApplication(sys.argv)
	main = glmainwnd()
	main.show()
	sys.exit(app.exec_())
