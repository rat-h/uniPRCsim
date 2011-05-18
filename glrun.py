from PyQt4 import QtGui, QtCore

import engine
import icons
class glrun(QtGui.QDialog):
	def __init__(self, name, fname, maxspikes, parent=None):
		super(glrun, self).__init__(parent)
		self.setWindowTitle("Run :: "+name)
		self.progress = QtGui.QProgressBar(self)
		self.progress.setMaximum(maxspikes)
		self.timer	= QtCore.QTimer(self);
		cancelButton = QtGui.QPushButton(QtGui.QIcon(':/dialog-cancel.png'),"&Stop",self)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.progress)
		hbox.addWidget(cancelButton)
		self.setLayout(hbox)
		size = self.size()
		self.resize(size.width()*3/4, 30)
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), self.stop)
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.update)
		self.engine	= engine.engine(filename=fname,mode="NONSTD")
		self.timer.setInterval(500)
		self.timer.start()
		self.engine.start()
	def stop(self):
		del self.engine
		self.timer.stop()
		self.reject()
	def update(self):
		if self.engine.model.runer_flg == 0:
			self.timer.stop()
			if self.engine.model.error == None:
				self.accept()
			else:
				QtGui.QMessageBox.critical(self,"Critical ERROR!"," Engine return an ERROR:\n=== %s ==="%self.engine.model.error,QtGui.QMessageBox.Ok,0)
				self.reject()
		else:
			self.progress.setValue(self.engine.model.cnt)
			
		
		
		
