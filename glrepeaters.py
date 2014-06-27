##################################
#
# glenurons.py
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
from PyQt4 import QtGui, QtCore
import string as str
import icons

class odreadrep:
	def __init__(self):
		self.id				= -1
		self.pid			= -1
		self.name			= ""
		self.offset			= 0.0
		self.slope			= 0.0

class repedt(QtGui.QDialog):
	def __init__(self, rep=None, parent=None):
		super(repedt, self).__init__()
		self.rep = rep
		if self.rep == None :
			self.rep = odreadrep()
		self.setWindowTitle(self.rep.name + ' :: Repeater Editor')
		#self.setGeometry(300, 300, 280, 270)
		self.nameedit = QtGui.QLineEdit(self.rep.name)
		self.slopeedit = QtGui.QDoubleSpinBox(self)
		self.slopeedit.setValue(self.rep.slope)
		self.slopeedit.setMaximum(1000000000.0)
		self.slopeedit.setMinimum(-1000000000.0)
		self.slopeedit.setDecimals(10)
		self.slopeedit.setSingleStep(0.1)

		self.offsetedit = QtGui.QDoubleSpinBox(self)
		self.offsetedit.setValue(self.rep.offset)
		self.offsetedit.setMaximum(1000000000.0)
		self.offsetedit.setMinimum(0.0)
		self.offsetedit.setDecimals(10)
		self.offsetedit.setSingleStep(0.1)

		okButton	 = QtGui.QPushButton(QtGui.QIcon(':/dialog-ok.png'),"&OK",self)
		cancelButton = QtGui.QPushButton(QtGui.QIcon(':/dialog-cancel.png'),"&Cancel",self)

		hbox01 = QtGui.QHBoxLayout()
		hbox01.addWidget(QtGui.QLabel("Name:"))
		hbox01.addWidget(self.nameedit)
		hbox01.addStretch(1)
		hbox01.addWidget(QtGui.QLabel("TS-TR slope:"))
		hbox01.addWidget(self.slopeedit)
		hbox01.addStretch(1)
		hbox01.addWidget(QtGui.QLabel("TS-TR offset:"))
		hbox01.addWidget(self.offsetedit )

		hbox02 = QtGui.QHBoxLayout()
		hbox02.addWidget(okButton)
		hbox02.addWidget(cancelButton)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox01)
		vbox.addLayout(hbox02)
		self.setLayout(vbox)
		self.connect(okButton, QtCore.SIGNAL('clicked()'), self.ok)
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), self.cancel)
		self.connect(self.nameedit, QtCore.SIGNAL('editingFinished()'), self.rename)
		self.readrep()
	def rename(self):
		if self.rep == None: self.rep = odreadrep()
		self.rep.name = self.nameedit.text()
		self.setWindowTitle(self.rep.name + ' :: Repeaters Editor')

	def upDate(self):
		if self.nameedit.text().length() < 1:
			QtGui.QMessageBox.critical(self,"Critical ERROR!"," You should specify the name of neurons set ",QtGui.QMessageBox.Ok,0)
			return False
		self.rep.name=self.nameedit.text()
		
		self.rep.slope = self.slopeedit.value()
		self.rep.offset = self.offsetedit.value()
		self.readrep()
		return True
		
	def readrep(self, rep=None):
		if rep != None:
			self.rep=rep
		self.setWindowTitle(self.rep.name + ' :: Repeaters Editor')
		self.nameedit.setText(self.rep.name)
		self.slopeedit.setValue(self.rep.slope)
		self.offsetedit.setValue(self.rep.offset)

	def ok(self):
		if not self.upDate(): return
		self.accept()
	def cancel(self):
		self.reject()


class glrepeaters:
	def __init__(self,parent = None, mainwnd = None, menubar = None, toolbar = None):
		self.parent		= parent
		self.mainwnd	= mainwnd
		self.object		= "repeaters"
		insertppl = QtGui.QAction(QtGui.QIcon(':/repeaters.png'), 'Insert Neurons', mainwnd)
		insertppl.setShortcut('Alt+R')
		insertppl.setStatusTip('Insert Set of Neurons')
		mainwnd.connect(insertppl, QtCore.SIGNAL('triggered()'), self.insert)
		menu = menubar.addMenu('&Repeaters')
		menu.addAction(insertppl)
		toolbar.addAction(insertppl)
		self.replst = []
		self.ischanged	= False
		self.tmprep = None
	def clean(self):
		del self.replst
		self.replst = []
		self.ischanged	= False
		self.tmprep = None

	def insert(self):
		if not self.parent.isactive : return
		edit=repedt(parent=self.mainwnd)
		item = self.mainwnd.tree.currentItem()
		ok = False
		if item.data(1,QtCore.Qt.UserRole) == self.object:
			repid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
			if not ok:
				print "Collapes PRC item((("
			else:
				edit.readrep(rep=self.replst[repid])
		if not edit.exec_(): return
		self.ischanged	= True
		if ok:
			self.replst[repid] = edit.rep
			item.setText(2,edit.rep.name)
		else:
			if item.data(1,QtCore.Qt.UserRole) == "population":
				popid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
				if not ok:
					print "Collapes POP item((("
					return
				newrep = QtGui.QTreeWidgetItem(self.parent.glpopulation.poplst[popid].id)
				edit.rep.pid = popid
				self.parent.glpopulation.poplst[popid].id.addChild(newrep)
			else:
				newrep = QtGui.QTreeWidgetItem(self.parent.root)
				self.parent.root.addChild(newrep)
			newrep.setIcon(0,QtGui.QIcon(':/repeaters.png'))
			newrep.setText(1,'Repeater:')
			newrep.setText(2,edit.rep.name)
			newrep.setData(1,QtCore.Qt.UserRole,self.object)
			newrep.setData(2,QtCore.Qt.UserRole,len(self.replst))
			edit.rep.id = newrep
			self.replst.append(edit.rep)
		

	def remove(self,item):
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		repid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		if len(self.replst) <= repid : return
		self.replst[repid].id = None
		self.replst[repid].pid = None
		self.ischanged	= True

	def click(self):
		self.insert()

	def save(self, pid = -1):
		result=[]
		for rep in self.replst:
			if rep.pid != pid: continue
			if rep.id == None: continue
			result.append("<repeaters name=\"%s\" offset=\"%g\" slope=\"%g\"/>"%(rep.name, rep.offset,rep.slope))
			#if nrn.init_selector == 0:
				#result.append("\t<init ph0_all=\"%g\" ph1_all=\"%g\" />"%(nrn.ph0_all, nrn.ph1_all))
			#elif nrn.init_selector == 1:
				#result.append("\t<init ph0_all=\"%g\" ph0_sd=\"%g\" ph1_all=\"%g\" ph1_sd=\"%g\"/>"%(nrn.ph0_all, nrn.ph0_sd, nrn.ph1_all, nrn.ph1_sd))
			#else :
				#result.append("\t<init ph0=\"%s\" ph1=\"%s\" />"%(str.join(nrn.ph0,","), str.join(nrn.ph1,",")) )
			#result.append("</neurons>")
		self.ischanged	= False
		return result
	def startpoint(self,name,attr={},pid = -1):
		#if name == "init":
			#if attr.get("ph0", 0) and attr.get("ph1", 0):
				#self.tmpnrn.ph0 = str.split(attr["ph0"],",")
				#self.tmpnrn.ph1 = str.split(attr["ph1"],",")
				#self.tmpnrn.init_selector = 2
			#elif attr.get("ph0", 0) and attr.get("ph1", 0) == 0:
				#self.tmpnrn.ph0 = str.split(attr["ph0"],",")
				#self.tmpnrn.ph1 = ["0.0" for x in xrange(self.tmpnrn.number) ]
				#self.tmpnrn.init_selector = 2
			#elif attr.get("ph0_all", -1.0) >= 0.0 and attr.get("ph0_sd", -1.0) >= 0.0 and attr.get("ph1_all", -1.0) >= 0.0 and attr.get("ph1_sd", -1.0) >= 0.0 :
				#self.tmpnrn.ph0_all = float(attr["ph0_all"])
				#self.tmpnrn.ph0_sd  = float(attr["ph0_sd"])
				#self.tmpnrn.ph1_all = float(attr["ph1_all"])
				#self.tmpnrn.ph1_sd  = float(attr["ph1_sd"])
				#self.tmpnrn.init_selector = 1
			#elif attr.get("ph0_all", -1.0) >= 0.0 and attr.get("ph1_all", -1.0) >= 0.0:
				#self.tmpnrn.ph0_all = float(attr["ph0_all"])
				#self.tmpnrn.ph1_all = float(attr["ph1_all"])
				#self.tmpnrn.init_selector = 0
			#elif attr.get("ph0_all", -1.0) >= 0.0:
				#self.tmpnrn.ph0_all = float(attr["ph0_all"])
				#self.tmpnrn.ph1_all = 0.0
				#self.tmpnrn.init_selector = 0
			#else:
				#QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected subtag <%s> in tag <%s>!"%(name,self.tmpnrn.name),QtGui.QMessageBox.Ok,0)
				#return
		if name == self.object:
			if self.tmprep != None:
				QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
				return
			self.tmprep = odreadrep()
			self.tmprep.pid = pid
			if attr.get("name",0): self.tmprep.name = attr["name"]
			if attr.get("offset", None) != None: self.tmprep.offset = float(attr["offset"])
			if attr.get("slope",  None) != None: self.tmprep.slope  = float(attr["slope"])
		else:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
			return
		
	def stoppoint(self,name):
		if name == self.object:
			if self.tmprep != None:
				if self.tmprep.pid < 0:
					newrep = QtGui.QTreeWidgetItem(self.parent.root)
					self.parent.root.addChild(newrep)
				else:
					newrep = QtGui.QTreeWidgetItem(self.parent.glpopulation.tmppop.id)
					self.parent.glpopulation.tmppop.id.addChild(newrep)
				newrep.setIcon(0,QtGui.QIcon(':/repeaters.png'))
				newrep.setText(1,'Repeaters:')
				newrep.setText(2,self.tmprep.name)
				newrep.setData(1,QtCore.Qt.UserRole,self.object)
				newrep.setData(2,QtCore.Qt.UserRole,len(self.replst))
				#Truncate ph0 and ph1 sequences
				#self.tmprep.ph0 = self.tmprep.ph0[:self.tmprep.number]
				#self.tmprep.ph1 = self.tmprep.ph1[:self.tmprep.number]
				#print self.tmprep.name,"ph0:",self.tmprep.ph1
				#print self.tmprep.name,"ph1:",self.tmprep.ph0
				self.replst.append(self.tmprep)
				self.tmprep = None
				return
		QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
		return
	def getnames(self):
		result=[]
		for rep in self.replst:
			if rep.pid >= 0: continue
			result.append(rep.name)
		return result

