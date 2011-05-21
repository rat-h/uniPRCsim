from PyQt4 import QtGui, QtCore
from xml.sax import handler, make_parser
import glprc, glrprc, glpopulation, glneurons, glconnection
import gloutput, glrun, icons
import os

class glmodel:
	class parcerpxm(handler.ContentHandler):
		def __init__(self,model = None):
			self.model = model
			self.workobj = None
		def startElement(self, name, attr):
			if self.model == None: return
			if name =="model":
				self.workobj = self.model
				self.workobj.startpoint(name, attr)
			elif self.workobj != None:
				self.workobj.startpoint(name, attr)
			return
		def endElement(self, name):
			if self.workobj == None: return
			elif name == "model" and self.workobj == self.model:
				self.workobj = None
			else:
				self.workobj.stoppoint(name)
			return
	
	def __init__(self,parent=None, mainwnd = None, menubar = None, toolbar = None,filemenu = None):
		#GUI paramters
		self.parent	= parent
		self.model	= None
		#Acctions:
		#New Model
		newmdl = QtGui.QAction(QtGui.QIcon(':/new.png'), 'New Model', mainwnd)
		newmdl.setShortcut('Ctrl+N')
		newmdl.setStatusTip('Start New Model')
		mainwnd.connect(newmdl, QtCore.SIGNAL('triggered()'), self.newmodel)
		#Open Model
		openmdl = QtGui.QAction(QtGui.QIcon(':/open.png'), 'Open Model', mainwnd)
		openmdl.setShortcut('Ctrl+O')
		openmdl.setStatusTip('Opne Existed Model' )
		mainwnd.connect(openmdl, QtCore.SIGNAL('triggered()'), self.openmodel)
		#Save Model
		savemdl = QtGui.QAction(QtGui.QIcon(':/save.png'), 'Save Model', mainwnd)
		savemdl.setShortcut('Ctrl+S')
		savemdl.setStatusTip('Save Current Model')
		mainwnd.connect(savemdl, QtCore.SIGNAL('triggered()'), self.savemodel)
		savemdlas = QtGui.QAction(QtGui.QIcon(':/save.png'), 'Save Model As', mainwnd)
		savemdlas.setStatusTip('Save Current Model As')
		mainwnd.connect(savemdlas, QtCore.SIGNAL('triggered()'), self.savemodelas)
		#Close Model
		exit = QtGui.QAction(QtGui.QIcon(':/close.png'), 'Close Model', mainwnd)
		exit.setShortcut('Ctrl+W')
		exit.setStatusTip('Close Model')
		mainwnd.connect(exit, QtCore.SIGNAL('triggered()'), self.close)
		#Run Model
		runmdl = QtGui.QAction(QtGui.QIcon(':/media-playback-start.png'), 'Save and Run Model', mainwnd)
		runmdl.setShortcut('Ctrl+R')
		runmdl.setStatusTip('Save and Run Model')
		mainwnd.connect(runmdl, QtCore.SIGNAL('triggered()'), self.runmodel)

		showrst = QtGui.QAction(QtGui.QIcon(':/grath.png'), 'Show graths', mainwnd)
		showrst.setShortcut('Ctrl+S')
		showrst.setStatusTip('Show grathical outputs')
		mainwnd.connect(showrst, QtCore.SIGNAL('triggered()'), self.show)
		
		#insert output
		#insoutmdl = QtGui.QAction(QtGui.QIcon(':/insert.png'), 'Insert new output from model', mainwnd)
		#insoutmdl.setShortcut('Ctrl+Shift+O')
		#insoutmdl.setStatusTip('Insert New output stream from model')
		#mainwnd.connect(insoutmdl, QtCore.SIGNAL('triggered()'), self.newoutput)
		#remove output
		#rmoutmdl = QtGui.QAction(QtGui.QIcon(':/remove.png'), 'Remove output', mainwnd)
		#rmoutmdl.setShortcut('Alt+Shift+O')
		#rmoutmdl.setStatusTip('Remove output stream ')
		#mainwnd.connect(rmoutmdl, QtCore.SIGNAL('triggered()'), self.removeoutput)
		#remove
		rmobj = QtGui.QAction(QtGui.QIcon(':/close.png'), 'Remove Object', mainwnd)
		rmobj.setShortcut('Delete')
		rmobj.setStatusTip('Remove selected object')
		mainwnd.connect(rmobj, QtCore.SIGNAL('triggered()'), self.removeobject)
		mainwnd.connect(mainwnd.tree, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem *,int)'), self.click)
		
	
	
		filemenu.addAction(newmdl)
		filemenu.addAction(openmdl)
		filemenu.addAction(savemdl)
		filemenu.addAction(savemdlas)
		filemenu.addAction(exit)
		toolbar.addAction(newmdl)
		toolbar.addAction(openmdl)
		toolbar.addAction(savemdl)
		toolbar.addAction(exit)
		toolbar.addSeparator()
		editmu = menubar.addMenu('&Edit')
		self.glprc	= glprc.glprc( parent=self, mainwnd=mainwnd, menubar=editmu, toolbar=toolbar )
		self.glrprc	= glrprc.glrprc( parent=self, mainwnd=mainwnd, menubar=editmu, toolbar=toolbar )
		self.glpopulation = glpopulation.glpopulation( parent=self, mainwnd=mainwnd, menubar=editmu, toolbar=toolbar )
		self.glneurons = glneurons.glneurons( parent=self, mainwnd=mainwnd, menubar=editmu, toolbar=toolbar )
		self.glconnection = glconnection.glconnection( parent=self, mainwnd=mainwnd, menubar=editmu, toolbar=toolbar )
		self.gloutput = gloutput.gloutput( parent=self, mainwnd=mainwnd, menubar=editmu, toolbar=toolbar )
		self.registered = (self.glprc, self.glrprc, self.glpopulation, self.glneurons, self.glconnection,self.gloutput)
		editmu.addAction(rmobj)
		toolbar.addAction(rmobj)
		toolbar.addSeparator()
		run = menubar.addMenu('&Run')
		run.addAction(runmdl)
		run.addAction(showrst)
		toolbar.addAction(runmdl)
		toolbar.addAction(showrst)
		#Data
		self.isactive	= 0
		self.name		= "***"
		self.maxspikes	= -1
		self.filename	= None
		self.workobj	= None
		self.ischanged	= False
		self.outfilename= None
#		self.prclst		= []
#		self.neuronlst	= []
#		self.connectlst	= []
	def newmodel(self):
#		print "newmodel"
		if self.isactive:
			msgBox = QtGui.QMessageBox.information(self.parent,"The Model is Active.","Do you want to save current model?",
				QtGui.QMessageBox.Save, QtGui.QMessageBox.Discard, QtGui.QMessageBox.Cancel)
			if msgBox == QtGui.QMessageBox.Cancel:
				return
			if msgBox == QtGui.QMessageBox.Save:
				self.savemodel()
				self.isactive = 0
			self.close()
		
		self.name, ok = QtGui.QInputDialog.getText(self.parent,
			'uniPRCsim: New Model Name', 'Enter the name for new model:')
		if not ok: return
		
		self.root = QtGui.QTreeWidgetItem(self.parent.tree)
		self.parent.tree.addTopLevelItem(self.root)
		self.root.setText(1,'Model:')
		self.root.setIcon(0,QtGui.QIcon(':/model.png'))
		self.nameedit=QtGui.QLineEdit(self.parent.tree)
		self.parent.tree.setItemWidget(self.root,2,self.nameedit)
		self.nameedit.setText(self.name)
		self.parent.connect(self.nameedit, QtCore.SIGNAL('editingFinished()'), self.selected)
		self.version = QtGui.QTreeWidgetItem(self.root)
		self.root.addChild(self.version)
		self.version.setText(1,'Version:')
		self.version.setText(2,'0.1')
		self.countspike = QtGui.QSpinBox(self.parent.tree)
		self.countspike.setMinimum(-1)
		self.countspike.setMaximum(100000000)
		self.countspike.setValue(5000)
		self.countspikewid = QtGui.QTreeWidgetItem(self.root)
		self.root.addChild(self.countspikewid)
		self.countspikewid.setText(1,'Number of spikes:')
		self.parent.tree.setItemWidget(self.countspikewid,2,self.countspike)		
		self.seededit = QtGui.QSpinBox(self.parent.tree)
		self.seededit.setMinimum(-1)
		self.seededit.setMaximum(100000000)
		self.seededit.setValue(-1)
		self.seededitwid = QtGui.QTreeWidgetItem(self.root)
		self.root.addChild(self.seededitwid)
		self.seededitwid.setText(1,'SEED:')
		self.parent.tree.setItemWidget(self.seededitwid,2,self.seededit)

		self.parent.setWindowTitle(self.name+' :: uniPRCsim')
		self.isactive = 1
	def readfile(self, filename):
		self.name = "<----->"
		if len(filename) == 0: return
		dirname,self.filename = os.path.split( filename.toUtf8().data() )
		if len(dirname) > 2 :os.chdir(dirname)
		pparser = self.parcerpxm(model=self)
		parser=make_parser()
		parser.setContentHandler(pparser)
		parser.parse(self.filename)
		self.parent.setWindowTitle(self.name+' :: uniPRCsim')
		self.isactive = 1
		self.parent.tree.expandAll()
	def openmodel(self):
		self.close()
		filename = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open file', '', "Prc Xml Model(*.pxm)")
		if filename.length() < 1: return
		self.readfile(filename)

	def savemodel(self):
		#self.maxspikes = self
		if self.filename == None:
			self.savemodelas()
			return
		fd = open(self.filename,"w")
		fd.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
		fd.write("<model version=\"0.1\" name=\"%s\">\n"%self.name)
		fd.write("\t<simulation ")
		if self.countspike.value() >= 1:
			fd.write("maxspikes=\"%d\" "%self.countspike.value())
		if self.seededit.value() >= 1:
			fd.write("SEED=\"%d\" "%self.seededit.value())
		fd.write(" />\n")
		for prog in self.registered:
			for prn in prog.save():	fd.write("\t"+prn+"\n")
		fd.write("</model>")
		self.ischanged = False
		
	def savemodelas(self):
		filename = QtGui.QFileDialog.getSaveFileName(self.parent, 'Open file', '', "Prc Xml Model(*.pxm)")
		if filename.length() < 1: return
		dirname,self.filename = os.path.split( filename.toUtf8().data() )
		if len(dirname) > 2 :os.chdir(dirname)
		self.parent.setWindowTitle(self.name+' :: uniPRCsim')
		self.savemodel()
	def close(self):
		ischanged = self.ischanged | reduce(lambda x,y: x+y.ischanged, self.registered, False)
		if ischanged:
			msgBox = QtGui.QMessageBox.information(self.parent,"uniPRCsim The Model is Active.","The model \"%s\" has been modified.\nDo you want to save current model?"%self.name,
				QtGui.QMessageBox.Save, QtGui.QMessageBox.Discard, QtGui.QMessageBox.Cancel)
			if msgBox == QtGui.QMessageBox.Cancel: return
			elif msgBox == QtGui.QMessageBox.Save:
				self.savemodel()
				self.isactive = 0
		for item in self.registered:
			item.clean()
		self.parent.tree.clear()
		self.isactive	= 0
		self.name		= "***"
		self.maxspikes	= -1
		self.filename	= None
		self.workobj	= None
		self.ischanged	= False
		self.parent.setWindowTitle('uniPRCsim')
		self.countspike = None
		self.seededit = None

	def runmodel(self):
		if not self.isactive: return
		saveflg = self.ischanged
		for comp in self.registered:
			saveflg |= comp.ischanged
		####DB####
		#for comp in self.registered:
		#	print comp.object,": ischanged=",comp.ischanged
		##########
		if saveflg:
			msgBox = QtGui.QMessageBox.information(self.parent,"uniPRCsim The Model is Active.","The model \"%s\" has been modified.\nDo you want to save current model?"%self.name,
				QtGui.QMessageBox.Save, QtGui.QMessageBox.Discard, QtGui.QMessageBox.Cancel)
			if msgBox == QtGui.QMessageBox.Cancel: return
			elif msgBox == QtGui.QMessageBox.Save:
				self.savemodel()
				self.ischanged = False
		if len(self.glprc.prclst) == 0 and len(self.glrprc.prclst) == 0:
			QtGui.QMessageBox.critical(self.parent,"Critical ERROR!"," You should have at least one PRC function! ",QtGui.QMessageBox.Ok,0)
			return
		if len(self.glpopulation.poplst) == 0 and len(self.glneurons.nrnlst) == 0:
			QtGui.QMessageBox.critical(self.parent,"Critical ERROR!"," You should have at least one Population or neuron set! ",QtGui.QMessageBox.Ok,0)
			return
		if len(self.glconnection.cnntlst) == 0:
			QtGui.QMessageBox.critical(self.parent,"Critical ERROR!"," You should have at least one connection! ",QtGui.QMessageBox.Ok,0)
			return
		if len(self.gloutput.outlst) == 0:
			QtGui.QMessageBox.critical(self.parent,"Critical ERROR!"," You should have at least one Output stream! ",QtGui.QMessageBox.Ok,0)
			return
		runer = glrun.glrun(self.name,self.filename,self.countspike.value())
		if not runer.exec_(): return
		self.gloutput.show()
	def show(self):
		self.gloutput.show()
		
	def newoutput(self):
		print "new output"
	def removeoutput(self):
		print "new output"
	def removeobject(self):
		if not self.isactive: return
		item = self.parent.tree.currentItem()
		for gl in self.registered:
			if item.data(1,QtCore.Qt.UserRole) == gl.object:
					gl.remove(item)
					self.root.removeChild(item)
	def selected(self):
		self.name = self.nameedit.text()
		self.parent.setWindowTitle(self.name+' :: uniPRCsim')
	def click(self,item,col):
		if item == None: return
		for prog in self.registered:
			if item.data(1, QtCore.Qt.UserRole) == prog.object:
				prog.click()
				break
	####TODO: ADD Other
	def startpoint(self, name, attr ={}):
		if self.workobj != None:
			self.workobj.startpoint(name,attr)
		elif name == "model":
			self.workobj = None
			if attr.get("version",0) == 0 or attr["version"] != "0.1":
				QtGui.QMessageBox.critical(self.parent,"Critical ERROR!","Bad version of model\n   ABBORT!   ",QtGui.QMessageBox.Ok,0)
				return
			if attr.get("name",0): self.name = attr["name"]
			else:self.name = "<--*-->"
			self.root = QtGui.QTreeWidgetItem(self.parent.tree)
			self.parent.tree.addTopLevelItem(self.root)
			self.root.setText(1,'Model:')
			self.root.setIcon(0,QtGui.QIcon(':/model.png'))
			self.nameedit=QtGui.QLineEdit(self.parent.tree)
			self.parent.tree.setItemWidget(self.root,2,self.nameedit)
			self.nameedit.setText(self.name)
			self.parent.connect(self.nameedit, QtCore.SIGNAL('editingFinished()'), self.selected)
			self.version = QtGui.QTreeWidgetItem(self.root)
			self.root.addChild(self.version)
			self.version.setText(1,'Version:')
			self.version.setText(2,'0.1')
			self.countspike = QtGui.QSpinBox(self.parent.tree)
			     
			self.countspike.setMinimum(-1)
			self.countspike.setMaximum(100000000)
			self.countspike.setValue(5000)
			self.countspikewid = QtGui.QTreeWidgetItem(self.root)
			self.root.addChild(self.countspikewid)
			self.countspikewid.setText(1,'Number of spikes:')
			self.parent.tree.setItemWidget(self.countspikewid,2,self.countspike)		
			self.seededit = QtGui.QSpinBox(self.parent.tree)
			self.seededit.setMinimum(-1)
			self.seededit.setMaximum(100000000)
			self.seededit.setValue(-1)
			self.seededitwid = QtGui.QTreeWidgetItem(self.root)
			self.root.addChild(self.seededitwid)
			self.seededitwid.setText(1,'SEED:')
			self.parent.tree.setItemWidget(self.seededitwid,2,self.seededit)
		elif name == "simulation" :
			if attr.get("maxspikes",0):
				if int(attr["maxspikes"]) >= 1 :
					self.countspike.setValue( int(attr["maxspikes"]) )
			if attr.get("SEED",0):
				if int(attr["SEED"]) >= 1 :
					self.seededit.setValue( int(attr["SEED"]) )
		elif self.workobj == None:
			for prog in self.registered:
				if name == prog.object:
					prog.startpoint(name,attr)
					self.workobj = prog
					break
#			if self.workobj == None

		

				
		return
	def stoppoint(self, name):
		if self.workobj != None and name == self.workobj.object:
			self.workobj.stoppoint(name)
			self.workobj = None
		elif name == "model" :#or name == "simulation" or name == "output"
			return
		elif self.workobj != None:
			self.workobj.stoppoint(name)
			return
		#QtGui.QMessageBox.critical(self.parent,"Critical ERROR!","Bad or unexpected tag slosing <%s>!"%name,QtGui.QMessageBox.Ok,0)
		#print "close item <%s>"%name
		return
	def getnames(self, lst=[]):
		result = []
		if len(lst) == 0:
			for prog in self.registered:
				result += prog.getnames()
		else:
			for name in lst:
				for prog in self.registered:
					if name != prog.object: continue
					result += prog.getnames()
		return result
			
			
