from PyQt4 import QtGui, QtCore
import glprc
import random as rnd
import icons

class odrprc:
	def __init__(self):
		self.name	= ""
		self.prc	= ""
		self.sd		= 0.0
		self.id		= None

class rprcviewer(glprc.prcviewer):
	def __init__(self,prc,sd, parent=None):
		super(rprcviewer, self).__init__(prc,parent)
		self.data = []

		for item in self.prc.data:
			self.data.append([ item[0],[],[] ])
			for cd in item[1]:
				self.data[-1][1].append([])
				while(len(self.data[-1][1][-1]) < 5):
					yitem = rnd.normalvariate(cd,sd)
					if yitem >= (self.data[-1][0] -1):
						self.data[-1][1][-1].append(yitem)
				idx = 0
				for f1 in self.data[-1][1]:
					for d in f1:
						if self.min > d and self.view[0][idx]:  self.min = d
						if self.max < d and self.view[0][idx]:  self.max = d
					idx+=1
			if not self.prc.f2: continue
			idx = 0
			for cd in item[2]:
				self.data[-1][2].append([ rnd.normalvariate(cd,sd) for x in xrange(5) ])
				idx = 0
				for f1 in self.data[-1][2]:
					for d in f1:
						if self.min > d and self.view[0][idx]:  self.min = d
						if self.max < d and self.view[0][idx]:  self.max = d
					idx+=1
		
	def paintEvent(self, event):
		super(rprcviewer, self).paintEvent(event)
		qp  = QtGui.QPainter()
		pen = QtGui.QPen(QtCore.Qt.black, self.linewidth, QtCore.Qt.SolidLine)
		h,w = self.size().height(), self.size().width()
		qp.begin(self)
		for xind in xrange( len( self.prc.data )):
			for pind in xrange( len (self.prc.data[xind][1] ) ):
				pen.setColor( self.colors[0][pind] )
				qp.setPen(pen)
				x0 = self.data[xind][0] / self.hscale + self.margins[0]
				for dot in self.data[xind][1][pind]:
					y0 = h - (dot-self.min)/self.vscale-self.margins[2]
					qp.drawPoints(QtCore.QPoint(x0,y0),QtCore.QPoint(x0-1,y0),QtCore.QPoint(x0+1,y0),QtCore.QPoint(x0,y0-1),QtCore.QPoint(x0,y0+1))
			if not self.prc.f2:continue
			for pind in xrange( len (self.prc.data[xind][1] ) ):
				pen.setColor( self.colors[1][pind] )
				qp.setPen(pen)
				x0 = self.data[xind][0] / self.hscale + self.margins[0]
				for dot in self.data[xind][2][pind]:
					y0 = h - (dot-self.min)/self.vscale-self.margins[2]
					qp.drawPoints(QtCore.QPoint(x0,y0),QtCore.QPoint(x0-1,y0),QtCore.QPoint(x0+1,y0),QtCore.QPoint(x0,y0-1),QtCore.QPoint(x0,y0+1))
			
		qp.end()
					
			




class prcviewdlg(QtGui.QDialog):
	def __init__(self, prc, sd, parent=None):
		super(prcviewdlg, self).__init__()
		self.setWindowTitle(prc.name + ' :: PRC Viewer')
		self.setGeometry(300, 300, 280, 270)
		self.view = rprcviewer(prc, sd, parent = self)
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.view)
		self.setLayout(vbox)				

class rprcedit(QtGui.QDialog):
	def __init__(self, glprc , parent=None, rprc=None):
		super(rprcedit, self).__init__()
		self.rprc = rprc
		self.glprc = glprc
		if self.rprc == None :
			self.rprc = odrprc()
			self.setWindowTitle('Random PRC Editor')
		else:
			self.setWindowTitle(self.rprc.name + ' :: Random PRC Editor')
		self.nameedit = QtGui.QLineEdit(self.rprc.name)
		self.sdedit = QtGui.QDoubleSpinBox(self)
		self.sdedit.setValue(self.rprc.sd)
		self.sdedit.setMaximum(1000000000.0)
		self.sdedit.setMinimum(0.0)
		self.sdedit.setDecimals(10)
		self.sdedit.setSingleStep(0.0001)
		self.prc = QtGui.QComboBox(self)
		self.prc .addItems(glprc.getnames())
		self.prc .setEditable(False)
		id = self.prc.findText(self.rprc.prc)
		if id < 0:id = 0
		self.prc .setCurrentIndex(id)


		prevButton	 = QtGui.QPushButton(QtGui.QIcon(':/previewer.png'),"&Preview",self)
		okButton	 = QtGui.QPushButton(QtGui.QIcon(':/dialog-ok.png'),"&OK",self)
		cancelButton = QtGui.QPushButton(QtGui.QIcon(':/dialog-cancel.png'),"&Cancel",self)

		hbox01 = QtGui.QHBoxLayout()
		hbox01.addWidget(QtGui.QLabel("Name:"))
		hbox01.addWidget(self.nameedit)
		hbox01.addStretch(1)
		hbox01.addWidget(QtGui.QLabel("SD:"))
		hbox01.addWidget(self.sdedit)
		hbox01.addStretch(1)
		hbox01.addWidget(QtGui.QLabel("Base PRC:"))
		hbox01.addWidget(self.prc)
		hbox02 = QtGui.QHBoxLayout()
		hbox02.addWidget(prevButton)
		hbox02.addStretch(1)
		hbox02.addWidget(okButton)
		hbox02.addWidget(cancelButton)
		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox01)
		vbox.addLayout(hbox02)
		self.setLayout(vbox)

		self.connect(self.nameedit, QtCore.SIGNAL('editingFinished()'), self.rename)
		self.connect(prevButton, QtCore.SIGNAL('clicked()'), self.preview)
		self.connect(okButton, QtCore.SIGNAL('clicked()'), self.ok)
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), self.cancel)
	def rename(self):
		self.rprc.name = self.nameedit.text().toUtf8().data()
		self.setWindowTitle(self.rprc.name + ' :: Random PRC Editor')
	def readrprc(self, rprc = None):
		if rprc != None:
			self.rprc = rprc
		self.setWindowTitle(self.rprc.name + ' :: Random PRC Editor')
		self.nameedit.setText(self.rprc.name)
		self.sdedit.setValue(self.rprc.sd)
		id = self.prc.findText(self.rprc.prc)
		if id < 0:id = 0
		self.prc .setCurrentIndex(id)
		
		
	def ok(self):
		if self.nameedit.text().length() < 1:
			QtGui.QMessageBox.critical(self,"Critical ERROR!"," You should specify the name for Random PRC ",QtGui.QMessageBox.Ok,0)
		self.rprc.name	= self.nameedit.text().toUtf8().data()
		self.rprc.prc	= self.prc.currentText().toUtf8().data()
		self.rprc.sd	= self.sdedit.value()
		self.accept()
	def cancel(self):
		#do something to save
		self.reject()

	def preview(self):
		if self.prc == None: return
		sprc = self.glprc.getdata(self.prc.currentText().toUtf8().data())
		dprc = glprc.odprc()
		dprc.name = sprc.name
		dprc.gsyn = [ float(syn) for syn in sprc.gsyn]
		dprc.f2 = sprc.f2
		for data in sprc.data:
			dprc.data.append([ float(data[0]), [float(d1) for d1 in data[1] ], [float(d2) for d2 in data[2] ] ])
		viwer = prcviewdlg(dprc,self.sdedit.value(),parent=self)
		viwer.exec_()

class glrprc:
	def __init__(self,parent = None, mainwnd = None, menubar = None, toolbar = None):
		self.parent		= parent
		self.mainwnd	= mainwnd
		self.object		= "rprc"
		prcinsr = QtGui.QAction(QtGui.QIcon(':/rprc.png'), 'Insert/Edit Random PRC', mainwnd)
		prcinsr.setShortcut('Ctrl+Shift+P')
		prcinsr.setStatusTip('Insert or Edit selected Random PRC')
		mainwnd.connect(prcinsr, QtCore.SIGNAL('triggered()'), self.insert)
		prcprvw = QtGui.QAction(QtGui.QIcon(':/previewer.png'), 'Preview Random PRC', mainwnd)
		prcprvw.setShortcut('Alt+Shift+P')
		prcprvw.setStatusTip('Preview PRC')
		mainwnd.connect(prcprvw, QtCore.SIGNAL('triggered()'), self.preview)
		prcmenu = menubar.addMenu('rPRC')
		prcmenu.addAction(prcinsr)
		prcmenu.addAction(prcprvw)
		toolbar.addAction(prcinsr)
		toolbar.addAction(prcprvw)
		self.prclst		= []
		self.ischanged	= False

	def clean(self):
		del self.prclst
		self.prclst		= []
		self.ischanged	= False
	def insert(self):
		if not self.parent.isactive : return
		edit = rprcedit(self.parent.glprc, parent = self.mainwnd)
		item = self.mainwnd.tree.currentItem()
		ok = False
		if item.data(1,QtCore.Qt.UserRole) == self.object:
			prcid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
			if not ok:
				print "Collapes PRC item((("
			else:
				edit.readrprc(rprc=self.prclst[prcid])
		if not edit.exec_(): return
		self.ischanged	= True
		if ok :
			self.prclst[prcid] = edit.rprc
			item.setText(2,edit.rprc.name)
		else:
			newprc = QtGui.QTreeWidgetItem(self.parent.root)
			self.parent.root.addChild(newprc)
			newprc.setIcon(0,QtGui.QIcon(':/rprc.png'))
			newprc.setText(1,'Random PRC:')
			newprc.setText(2,edit.rprc.name)
			newprc.setData(1,QtCore.Qt.UserRole,self.object)
			newprc.setData(2,QtCore.Qt.UserRole,len(self.prclst))
			edit.rprc.id = newprc
			self.prclst.append(edit.rprc)

		
	def preview(self):
		if self.prclst == None: return
		item = self.mainwnd.tree.currentItem()
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		prcid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		sprc = self.parent.glprc.getdata(self.prclst[prcid].prc)
		dprc = glprc.odprc()
		dprc.name = sprc.name
		dprc.gsyn = [ float(syn) for syn in sprc.gsyn]
		dprc.f2 = sprc.f2
		for data in sprc.data:
			dprc.data.append([ float(data[0]), [float(d1) for d1 in data[1] ], [float(d2) for d2 in data[2] ] ])
		viwer = prcviewdlg(dprc,self.prclst[prcid].sd,parent=self)
		viwer.exec_()
	def remove(self, item):
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		prcid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		if len(self.prclst) <= prcid : return
		self.prclst[prcid].id = None
		self.ischanged	= True
	def click(self):
		self.preview()	
	def save(self):
		result = []
		for prc in self.prclst:
			if prc.id == None: continue
			result.append("<rprc name=\"%s\" prc=\"%s\" sd=\"%g\" />"%(prc.name, prc.prc, prc.sd) )
		return result
	def startpoint(self,name,attr={}):
		if name != self.object:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
			return
		if attr.get("name",0 ) == 0 or attr.get("prc",0 ) == 0 or attr.get("sd",0 ) == 0:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Tag <%s> should have attributes:\n name - sd -  prc!"%name,QtGui.QMessageBox.Ok,0)
			return
		tmp = odrprc()
		tmp.name	= attr["name"]
		tmp.sd		= float(attr["sd"])
		tmp.prc		= attr["prc"]
		newprc = QtGui.QTreeWidgetItem(self.parent.root)
		self.parent.root.addChild(newprc)
		newprc.setIcon(0,QtGui.QIcon(':/rprc.png'))
		newprc.setText(1,'Random PRC:')
		newprc.setText(2,tmp.name)
		newprc.setData(1,QtCore.Qt.UserRole,self.object)
		newprc.setData(2,QtCore.Qt.UserRole,len(self.prclst))
		tmp.id = newprc
		self.prclst.append(tmp)
		
	def stoppoint(self,name):
		if name != self.object:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected closing of tag <%s>!"%name,QtGui.QMessageBox.Ok,0)

	def getnames(self):
		result = []
		for x in self.prclst:
			if x.id == None: continue
			result.append(x.name)
		return result
	


