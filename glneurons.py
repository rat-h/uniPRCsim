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

class odneurons:
	def __init__(self):
		self.id				= -1
		self.pid			= -1
		self.name			= ""
		self.period			= 0.0
		self.number			= 0
		self.init_selector	= 0
		self.f2_selector	= 0
		self.ph0_all		= 0.0
		self.ph1_all		= 0.0
		self.ph0_sd			= 0.0
		self.ph1_sd			= 0.0
		self.ph0			= []
		self.ph1			= []

class nrnedt(QtGui.QDialog):
	def __init__(self, nrn=None, parent=None):
		super(nrnedt, self).__init__()
		self.nrn = nrn
		if self.nrn == None :
			self.nrn = odneurons()
		self.setWindowTitle(self.nrn.name + ' :: Neurons Editor')
		#self.setGeometry(300, 300, 280, 270)
		self.nameedit = QtGui.QLineEdit(self.nrn.name)
		self.numbedit = QtGui.QSpinBox(self)
		self.numbedit.setValue(self.nrn.number)
		self.numbedit.setMaximum(100000000)
		self.periodedit = QtGui.QDoubleSpinBox(self)
		self.periodedit.setValue(self.nrn.period)
		self.periodedit.setMaximum(1000000000.0)
		self.periodedit.setMinimum(0.0)
		self.periodedit.setDecimals(10)
		self.periodedit.setSingleStep(0.1)
		self.f2combo = QtGui.QComboBox(self)
		self.f2combo.addItems(["accumulate","last","off"])
		self.f2combo.setEditable(False)
		self.f2combo.setCurrentIndex(self.nrn.f2_selector)
		self.initcombo = QtGui.QComboBox(self)
		self.initcombo.addItems(["set for all","set randomly","individually"])
		self.initcombo.setEditable(False)
		self.initcombo.setCurrentIndex(self.nrn.init_selector)

		self.ph0_alledit = QtGui.QDoubleSpinBox(self)
		self.ph0_alledit.setValue(self.nrn.ph0_all)
		self.ph0_alledit.setMaximum(1.0)
		self.ph0_alledit.setMinimum(0.0)
		self.ph0_alledit.setDecimals(10)
		self.ph0_alledit.setSingleStep(0.01)
		self.ph1_alledit = QtGui.QDoubleSpinBox(self)
		self.ph1_alledit.setValue(self.nrn.ph1_all)
		self.ph1_alledit.setMaximum(1.0)
		self.ph1_alledit.setMinimum(0.0)
		self.ph1_alledit.setDecimals(10)
		self.ph1_alledit.setSingleStep(0.01)
		self.label01 = QtGui.QLabel("Phase for all neurons:")
		self.label02 = QtGui.QLabel("Correction from previous cycle for all neurons:")
		
		self.ph0_allsdedit = QtGui.QDoubleSpinBox(self)
		self.ph0_allsdedit.setValue(self.nrn.ph0_sd)
		self.ph0_allsdedit.setMaximum(1.0)
		self.ph0_allsdedit.setMinimum(0.0)
		self.ph0_allsdedit.setDecimals(10)
		self.ph0_allsdedit.setSingleStep(0.01)
		self.ph1_allsdedit = QtGui.QDoubleSpinBox(self)
		self.ph1_allsdedit.setValue(self.nrn.ph1_sd)
		self.ph1_allsdedit.setMaximum(1.0)
		self.ph1_allsdedit.setMinimum(0.0)
		self.ph1_allsdedit.setDecimals(10)
		self.ph1_allsdedit.setSingleStep(0.01)
		self.label03 = QtGui.QLabel("Snadard deviation of Phase:")
		self.label04 = QtGui.QLabel("Snadard deviation of Correction from previous cycle:")
		self.ph0_allsdedit.setVisible(False)
		self.ph1_allsdedit.setVisible(False)
		self.label03.setVisible(False)
		self.label04.setVisible(False)

		self.tbl = QtGui.QTableWidget()
		self.tbl.setColumnCount(2)
		self.tbl.setHorizontalHeaderLabels(["ph","correction"])
		self.tbl.setVisible(False)
		okButton	 = QtGui.QPushButton(QtGui.QIcon(':/dialog-ok.png'),"&OK",self)
		cancelButton = QtGui.QPushButton(QtGui.QIcon(':/dialog-cancel.png'),"&Cancel",self)

		hbox01 = QtGui.QHBoxLayout()
		hbox01.addWidget(QtGui.QLabel("Name:"))
		hbox01.addWidget(self.nameedit)
		hbox01.addStretch(1)
		hbox01.addWidget(QtGui.QLabel("Number of neurons:"))
		hbox01.addWidget(self.numbedit)
		hbox01.addStretch(1)
		hbox01.addWidget(QtGui.QLabel("Period:"))
		hbox01.addWidget(self.periodedit )

		hbox02 = QtGui.QHBoxLayout()
		hbox02.addWidget(QtGui.QLabel("The second resetting:"))
		hbox02.addWidget(self.f2combo)
		hbox02.addWidget(QtGui.QLabel("The policy of initiation:"))
		hbox02.addWidget(self.initcombo)
		hbox02.addWidget(okButton)
		hbox02.addWidget(cancelButton)
		

		hbox03 = QtGui.QHBoxLayout()
		hbox03.addWidget(self.label01)
		hbox03.addWidget(self.ph0_alledit)
		hbox03.addWidget(self.label02)
		hbox03.addWidget(self.ph1_alledit)

		hbox04 = QtGui.QHBoxLayout()
		hbox04.addWidget(self.label03)
		hbox04.addWidget(self.ph0_allsdedit)
		hbox04.addWidget(self.label04)
		hbox04.addWidget(self.ph1_allsdedit)
		

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox01)
		vbox.addLayout(hbox02)
		vbox.addLayout(hbox03)
		vbox.addLayout(hbox04)
		vbox.addWidget(self.tbl)
		self.setLayout(vbox)
		self.connect(okButton, QtCore.SIGNAL('clicked()'), self.ok)
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), self.cancel)
		self.connect(self.initcombo, QtCore.SIGNAL('currentIndexChanged (int)'), self.policyselected)
		self.connect(self.numbedit, QtCore.SIGNAL('valueChanged (int)'), self.numberchanched)
		self.connect(self.nameedit, QtCore.SIGNAL('editingFinished()'), self.rename)
		self.readnrn()
	def rename(self):
		if self.nrn == None: self.nrn = odneurons()
		self.nrn.name = self.nameedit.text()
		self.setWindowTitle(self.nrn.name + ' :: Neurons Editor')

	def upDate(self):
		if self.nameedit.text().length() < 1:
			QtGui.QMessageBox.critical(self,"Critical ERROR!"," You should specify the name of neurons set ",QtGui.QMessageBox.Ok,0)
			return False
		self.nrn.name=self.nameedit.text()
		self.nrn.number = self.numbedit.value()
		self.nrn.period = self.periodedit.value()
		self.nrn.init_selector	= self.initcombo.currentIndex()
		self.nrn.f2_selector	= self.f2combo.currentIndex()
		if self.nrn.init_selector == 0 or self.nrn.init_selector == 1:
			self.nrn.ph0_all = self.ph0_alledit.value()
			self.nrn.ph1_all = self.ph1_alledit.value()
		if self.nrn.init_selector == 1:
			self.nrn.ph0_sd = self.ph0_allsdedit.value()
			self.nrn.ph1_sd = self.ph1_allsdedit.value()
		if self.nrn.init_selector == 2:
			if self.nrn.number > len(self.nrn.ph0):
				self.nrn.ph0 += [ "0.0" for x in xrange( self.nrn.number - len(self.nrn.ph0)) ]
			if self.nrn.number > len(self.nrn.ph1):
				self.nrn.ph0 += [ "0.0" for x in xrange( self.nrn.number - len(self.nrn.ph1)) ]
			for i in xrange(self.nrn.number):
				data,ok = self.tbl.item(i,0).data(0).toDouble()
				if not ok:
					QtGui.QMessageBox.critical(self,"Critical ERROR!","The cell %dx%d isn't an number!"%(i,0),QtGui.QMessageBox.Ok,0)
					return False
				self.nrn.ph0[i] = "%9.7f"%data
				data,ok = self.tbl.item(i,1).data(0).toDouble()
				if not ok:
					QtGui.QMessageBox.critical(self,"Critical ERROR!","The cell %dx%d isn't an number!"%(i,1),QtGui.QMessageBox.Ok,0)
					return False
				self.nrn.ph1[i] = "%9.7f"%data
		self.readnrn()
		self.policyselected(self.nrn.init_selector)
		return True
		
	def readnrn(self, nrn=None):
		if nrn != None:
			self.nrn=nrn
		self.setWindowTitle(self.nrn.name + ' :: Neurons Editor')
		self.nameedit.setText(self.nrn.name)
		self.numbedit.setValue(self.nrn.number)
		self.periodedit.setValue(self.nrn.period)
		self.initcombo.setCurrentIndex(self.nrn.init_selector)
		self.f2combo.setCurrentIndex(self.nrn.f2_selector)
		self.ph0_alledit.setValue(self.nrn.ph0_all)
		self.ph1_alledit.setValue(self.nrn.ph1_all)
		self.ph0_allsdedit.setValue(self.nrn.ph0_sd)
		self.ph1_allsdedit.setValue(self.nrn.ph1_sd)
		if self.nrn.init_selector == 2:
			self.tbl.setRowCount(self.nrn.number)
			for row in xrange(self.nrn.number):
				item = QtGui.QTableWidgetItem(self.nrn.ph0[row])
				item.setData(0,self.nrn.ph0[row])
				self.tbl.setItem(row,0,item)
				item = QtGui.QTableWidgetItem(self.nrn.ph1[row])
				item.setData(0,self.nrn.ph1[row])
				self.tbl.setItem(row,1,item)
		self.policyselected(self.nrn.init_selector)

		
	def numberchanched(self, number):
		self.nrn.number = number
		self.tbl.setRowCount(number)
		if self.nrn.init_selector == 2:
			self.deepck()
			self.readnrn()
			
	def deepck(self):
		if self.nrn.number > len(self.nrn.ph0):
			self.nrn.ph0 += [ "0.0" for x in xrange( self.nrn.number - len(self.nrn.ph0)) ]
		if self.nrn.number > len(self.nrn.ph1):
			self.nrn.ph1 += [ "0.0" for x in xrange( self.nrn.number - len(self.nrn.ph1)) ]

	def policyselected(self, item):
		self.nrn.init_selector = item
		if item != 2:
			self.ph0_alledit.setVisible(True)
			self.ph1_alledit.setVisible(True)
			self.label01.setVisible(True)
			self.label02.setVisible(True)
			self.tbl.setVisible(False)
		else:
			self.ph0_alledit.setVisible(False)
			self.ph1_alledit.setVisible(False)
			self.label01.setVisible(False)
			self.label02.setVisible(False)
		if item == 1:
			self.ph0_allsdedit.setVisible(True)
			self.ph1_allsdedit.setVisible(True)
			self.label03.setVisible(True)
			self.label04.setVisible(True)
		else:
			self.ph0_allsdedit.setVisible(False)
			self.ph1_allsdedit.setVisible(False)
			self.label03.setVisible(False)
			self.label04.setVisible(False)
		if item == 2:
			self.tbl.setVisible(True)
			self.deepck()
	def ok(self):
		if not self.upDate(): return
		self.accept()
	def cancel(self):
		self.reject()


class glneurons:
	def __init__(self,parent = None, mainwnd = None, menubar = None, toolbar = None):
		self.parent		= parent
		self.mainwnd	= mainwnd
		self.object		= "neurons"
		insertppl = QtGui.QAction(QtGui.QIcon(':/neurons.png'), 'Insert Neurons', mainwnd)
		insertppl.setShortcut('Alt+K')
		insertppl.setStatusTip('Insert Set of Neurons')
		mainwnd.connect(insertppl, QtCore.SIGNAL('triggered()'), self.insert)
		menu = menubar.addMenu('&Neurons')
		menu.addAction(insertppl)
		toolbar.addAction(insertppl)
		self.nrnlst = []
		self.ischanged	= False
		self.tmpnrn = None
	def clean(self):
		del self.nrnlst
		self.nrnlst = []
		self.ischanged	= False
		self.tmpnrn = None

	def insert(self):
		if not self.parent.isactive : return
		edit=nrnedt(parent=self.mainwnd)
		item = self.mainwnd.tree.currentItem()
		ok = False
		if item.data(1,QtCore.Qt.UserRole) == self.object:
			nrnid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
			if not ok:
				print "Collapes PRC item((("
			else:
				edit.readnrn(nrn=self.nrnlst[nrnid])
		if not edit.exec_(): return
		self.ischanged	= True
		if ok:
			self.nrnlst[nrnid] = edit.nrn
			item.setText(2,edit.nrn.name)
		else:
			if item.data(1,QtCore.Qt.UserRole) == "population":
				popid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
				if not ok:
					print "Collapes POP item((("
					return
				newnrn = QtGui.QTreeWidgetItem(self.parent.glpopulation.poplst[popid].id)
				edit.nrn.pid = popid
				self.parent.glpopulation.poplst[popid].id.addChild(newnrn)
			else:
				newnrn = QtGui.QTreeWidgetItem(self.parent.root)
				self.parent.root.addChild(newnrn)
			newnrn.setIcon(0,QtGui.QIcon(':/neurons.png'))
			newnrn.setText(1,'Neurons set:')
			newnrn.setText(2,edit.nrn.name)
			newnrn.setData(1,QtCore.Qt.UserRole,self.object)
			newnrn.setData(2,QtCore.Qt.UserRole,len(self.nrnlst))
			edit.nrn.id = newnrn
			self.nrnlst.append(edit.nrn)
		

	def remove(self,item):
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		nrnid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		if len(self.nrnlst) <= nrnid : return
		self.nrnlst[nrnid].id = None
		self.nrnlst[nrnid].pid = None
		self.ischanged	= True

	def click(self):
		self.insert()

	def save(self, pid = -1):
		result=[]
		f2_selector=["accumulate","last","off"]
		for nrn in self.nrnlst:
			if nrn.pid != pid: continue
			if nrn.id == None: continue
			result.append("<neurons name=\"%s\" number=\"%d\" period=\"%g\" f2=\"%s\">"%(nrn.name, nrn.number, nrn.period,f2_selector[nrn.f2_selector]))
			if nrn.init_selector == 0:
				result.append("\t<init ph0_all=\"%g\" ph1_all=\"%g\" />"%(nrn.ph0_all, nrn.ph1_all))
			elif nrn.init_selector == 1:
				result.append("\t<init ph0_all=\"%g\" ph0_sd=\"%g\" ph1_all=\"%g\" ph1_sd=\"%g\"/>"%(nrn.ph0_all, nrn.ph0_sd, nrn.ph1_all, nrn.ph1_sd))
			else :
				result.append("\t<init ph0=\"%s\" ph1=\"%s\" />"%(str.join(nrn.ph0,","), str.join(nrn.ph1,",")) )
			result.append("</neurons>")
		self.ischanged	= False
		return result
	def startpoint(self,name,attr={},pid = -1):
		if name == "init":
			if attr.get("ph0", 0) and attr.get("ph1", 0):
				self.tmpnrn.ph0 = str.split(attr["ph0"],",")
				self.tmpnrn.ph1 = str.split(attr["ph1"],",")
				self.tmpnrn.init_selector = 2
			elif attr.get("ph0", 0) and attr.get("ph1", 0) == 0:
				self.tmpnrn.ph0 = str.split(attr["ph0"],",")
				self.tmpnrn.ph1 = ["0.0" for x in xrange(self.tmpnrn.number) ]
				self.tmpnrn.init_selector = 2
			elif attr.get("ph0_all", -1.0) >= 0.0 and attr.get("ph0_sd", -1.0) >= 0.0 and attr.get("ph1_all", -1.0) >= 0.0 and attr.get("ph1_sd", -1.0) >= 0.0 :
				self.tmpnrn.ph0_all = float(attr["ph0_all"])
				self.tmpnrn.ph0_sd  = float(attr["ph0_sd"])
				self.tmpnrn.ph1_all = float(attr["ph1_all"])
				self.tmpnrn.ph1_sd  = float(attr["ph1_sd"])
				self.tmpnrn.init_selector = 1
			elif attr.get("ph0_all", -1.0) >= 0.0 and attr.get("ph1_all", -1.0) >= 0.0:
				self.tmpnrn.ph0_all = float(attr["ph0_all"])
				self.tmpnrn.ph1_all = float(attr["ph1_all"])
				self.tmpnrn.init_selector = 0
			elif attr.get("ph0_all", -1.0) >= 0.0:
				self.tmpnrn.ph0_all = float(attr["ph0_all"])
				self.tmpnrn.ph1_all = 0.0
				self.tmpnrn.init_selector = 0
			else:
				QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected subtag <%s> in tag <%s>!"%(name,self.tmpnrn.name),QtGui.QMessageBox.Ok,0)
				return
		elif name == self.object:
			if self.tmpnrn != None:
				QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
				return
			self.tmpnrn = odneurons()
			self.tmpnrn.pid = pid
			if attr.get("name",0): self.tmpnrn.name = attr["name"]
			if attr.get("period", -1.0) >= 0.0: self.tmpnrn.period = float(attr["period"])
			if attr.get("number", -1)   >= 0  : self.tmpnrn.number = int(attr["number"])
			if attr.get("f2", -1)   >= 0  :
				if attr["f2"] == "off": self.tmpnrn.f2_selector = 2
				elif attr["f2"] == "last": self.tmpnrn.f2_selector = 1
			
			
		else:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
			return
		
	def stoppoint(self,name):
		if name == "init": return
		if name == self.object:
			if self.tmpnrn != None:
				if self.tmpnrn.pid < 0:
					newnrn = QtGui.QTreeWidgetItem(self.parent.root)
					self.parent.root.addChild(newnrn)
				else:
					newnrn = QtGui.QTreeWidgetItem(self.parent.glpopulation.tmppop.id)
					self.parent.glpopulation.tmppop.id.addChild(newnrn)
				newnrn.setIcon(0,QtGui.QIcon(':/neurons.png'))
				newnrn.setText(1,'Neurons set:')
				newnrn.setText(2,self.tmpnrn.name)
				newnrn.setData(1,QtCore.Qt.UserRole,self.object)
				newnrn.setData(2,QtCore.Qt.UserRole,len(self.nrnlst))
				#Truncate ph0 and ph1 sequences
				self.tmpnrn.ph0 = self.tmpnrn.ph0[:self.tmpnrn.number]
				self.tmpnrn.ph1 = self.tmpnrn.ph1[:self.tmpnrn.number]
				#print self.tmpnrn.name,"ph0:",self.tmpnrn.ph1
				#print self.tmpnrn.name,"ph1:",self.tmpnrn.ph0
				self.nrnlst.append(self.tmpnrn)
				self.tmpnrn = None
				return
		QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
		return
	def getnames(self):
		result=[]
		for nrn in self.nrnlst:
			if nrn.pid >= 0: continue
			result.append(nrn.name)
		return result

