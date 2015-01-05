##################################
#
# glnoisyneurons.py
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
#########################################################
# process:
# 0 - OUP
# 1 - Feller
# 2 - Period Additive noise
# 3 - Phase Additive noise
# 4 - OUP + event updates
# 5 - Play from table
# 6 - Random choice from table
# >
# 100 - OUP + resetting
# 101 - Feller + resetting
#########################################################

from PyQt4 import QtGui, QtCore
import string as str
import icons

class odnoisyneurons:
	def __init__(self):
		self.id				= -1
		self.pid			= -1
		self.name			= ""
		self.period_mu		= 0.0
		self.period_sd		= 0.0
		self.period_tau		= 0.0
		self.process		= 0
		self.number			= 0
		self.init_selector	= 0
		self.f2_selector	= 0
		self.ph0_all		= 0.0
		self.ph1_all		= 0.0
		self.ph0_sd			= 0.0
		self.ph1_sd			= 0.0
		self.ph0			= []
		self.ph1			= []
		self.ptable			= []

class nynrnedt(QtGui.QDialog):
	def __init__(self, nrn=None, parent=None):
		super(nynrnedt, self).__init__()
		self.nrn = nrn
		if self.nrn == None :
			self.nrn = odnoisyneurons()
		self.setWindowTitle(self.nrn.name + ' :: Neurons Editor')
		#self.setGeometry(300, 300, 280, 270)
		self.nameedit = QtGui.QLineEdit(self.nrn.name)
		self.numbedit = QtGui.QSpinBox(self)
		self.numbedit.setValue(self.nrn.number)
		self.numbedit.setMaximum(100000000)

		self.mu_periodedit = QtGui.QDoubleSpinBox(self)
		self.mu_periodedit.setValue(self.nrn.period_mu)
		self.mu_periodedit.setMaximum(1000000000.0)
		self.mu_periodedit.setMinimum(0.0)
		self.mu_periodedit.setDecimals(10)
		self.mu_periodedit.setSingleStep(0.1)

		self.sd_periodedit = QtGui.QDoubleSpinBox(self)
		self.sd_periodedit.setValue(self.nrn.period_sd)
		self.sd_periodedit.setMaximum(1000000000.0)
		self.sd_periodedit.setMinimum(0.0)
		self.sd_periodedit.setDecimals(10)
		self.sd_periodedit.setSingleStep(0.1)

		self.tu_periodedit = QtGui.QDoubleSpinBox(self)
		self.tu_periodedit.setValue(self.nrn.period_tau)
		self.tu_periodedit.setMaximum(1000000000.0)
		self.tu_periodedit.setMinimum(0.0)
		self.tu_periodedit.setDecimals(10)
		self.tu_periodedit.setSingleStep(0.1)

		self.process = QtGui.QComboBox(self)
#		self.process.addItems(["Ornstein-Uhlenbeck","Feller","Additive noise","Ornstein-Uhlenbeck + resetting","Feller + resetting"])
		self.process.addItems(["Ornstein-Uhlenbeck","Feller","Period Additive noise", "Phase Additive noise","Ornstein-Uhlenbeck with event updates","Play from Table","Random choice from Table"])
		self.process.setEditable(False)
		self.process.setCurrentIndex(self.nrn.process)
		
		self.f2combo = QtGui.QComboBox(self)
		self.f2combo.addItems(["accumulate","last","off"])
		self.f2combo.setEditable(False)
		self.f2combo.setCurrentIndex(self.nrn.f2_selector)
		self.initcombo = QtGui.QComboBox(self)
		self.initcombo.addItems(["set for all","set randomly","individually"])
		self.initcombo.setEditable(False)
		self.initcombo.setCurrentIndex(self.nrn.init_selector)
		self.label00 =QtGui.QLabel("Tau:")

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

		self.plabel = QtGui.QLabel("Periods Table")
		self.ploadbutton = QtGui.QPushButton(QtGui.QIcon(':/import.png'),"Load &Table from File",self)
		self.pinsertrow  = QtGui.QPushButton(QtGui.QIcon(':/insert-row.png'),"Insert Row",self)
		self.pdeleterow  = QtGui.QPushButton(QtGui.QIcon(':/remove-row.png'),"Remove Row",self)
		self.ptbl = QtGui.QTableWidget()
		self.ptbl.setColumnCount(1)
		self.ptbl.setHorizontalHeaderLabels(["period"])
		self.plabel.setVisible(False)
		self.ploadbutton.setVisible(False)
		self.pinsertrow.setVisible(False)
		self.pdeleterow.setVisible(False)
		self.ptbl.setVisible(False)

		hbox01 = QtGui.QHBoxLayout()
		hbox01.addWidget(QtGui.QLabel("Name:"))
		hbox01.addWidget(self.nameedit)
		hbox01.addStretch(1)
		hbox01.addWidget(QtGui.QLabel("Number of neurons:"))
		hbox01.addWidget(self.numbedit)
		hbox01.addStretch(1)
		hbox01.addWidget(okButton)
		hbox01.addWidget(cancelButton)

		hbox05 = QtGui.QHBoxLayout()
		hbox05.addWidget(QtGui.QLabel("Period Parameters"))
		hbox05.addStretch(1)
		hbox05.addWidget(QtGui.QLabel("Mean:"))
		hbox05.addWidget(self.mu_periodedit )
		hbox05.addWidget(QtGui.QLabel("SD:"))
		hbox05.addWidget(self.sd_periodedit )
		hbox05.addWidget(self.label00)
		hbox05.addWidget(self.tu_periodedit )
		hbox05.addWidget(QtGui.QLabel("Process:"))
		hbox05.addWidget(self.process )

		hbox02 = QtGui.QHBoxLayout()
		hbox02.addWidget(QtGui.QLabel("The second resetting:"))
		hbox02.addWidget(self.f2combo)
		hbox02.addWidget(QtGui.QLabel("The policy of initiation:"))
		hbox02.addWidget(self.initcombo)
		

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
		
		hbox07 = QtGui.QHBoxLayout()
		hbox07.addWidget(self.plabel)
		hbox07.addWidget(self.ploadbutton)
		hbox07.addWidget(self.pinsertrow)
		hbox07.addWidget(self.pdeleterow)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox01)
		vbox.addLayout(hbox05)
		vbox.addLayout(hbox02)
		vbox.addLayout(hbox03)
		vbox.addLayout(hbox04)
		vbox.addWidget(self.tbl)
		vbox.addLayout(hbox07)
		vbox.addWidget(self.ptbl)
		self.setLayout(vbox)
		self.connect(okButton, QtCore.SIGNAL('clicked()'), self.ok)
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), self.cancel)
		self.connect(self.initcombo, QtCore.SIGNAL('currentIndexChanged (int)'), self.policyselected)
		self.connect(self.numbedit, QtCore.SIGNAL('valueChanged (int)'), self.numberchanched)
		self.connect(self.nameedit, QtCore.SIGNAL('editingFinished()'), self.rename)
		self.connect(self.process, QtCore.SIGNAL('currentIndexChanged (int)'), self.procselected)
		self.connect(self.ploadbutton, QtCore.SIGNAL('clicked()'), self.ptablload)
		self.connect(self.pinsertrow, QtCore.SIGNAL('clicked()'), self.ptablinsert)
		self.connect(self.pdeleterow, QtCore.SIGNAL('clicked()'), self.ptabldelete)
		self.connect(self.ptbl, QtCore.SIGNAL('cellChanged(int, int)'), self.perUpDate)
		self.readnrn()
	def rename(self):
		if self.nrn == None: self.nrn = odnoisyneurons
		self.nrn.name = self.nameedit.text()
		self.setWindowTitle(self.nrn.name + ' :: Neurons Editor')

	def upDate(self):
		if self.nameedit.text().length() < 1:
			QtGui.QMessageBox.critical(self,"Critical ERROR!"," You should specify the name of neurons set ",QtGui.QMessageBox.Ok,0)
			return False
		self.nrn.name=self.nameedit.text()
		self.nrn.number = self.numbedit.value()
		self.nrn.period_mu  = self.mu_periodedit.value()
		self.nrn.period_sd  = self.sd_periodedit.value()
		self.nrn.period_tau = self.tu_periodedit.value()
		self.nrn.process = self.process.currentIndex()
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

	def readptable(self):
		if len(self.nrn.ptable) == 0:
			return
		self.ptbl.setRowCount( len(self.nrn.ptable) )
		for ind,p in enumerate(self.nrn.ptable):
			self.ptbl.setItem(ind,0,QtGui.QTableWidgetItem(p))
			self.ptbl.item(ind,0).setData(0,p)
			#DB>>
			#print "IND=",ind,"GET ITEM=",self.ptbl.item(ind,0)
			#print "TABLE row x col=",self.ptbl.rowCount()," x ",self.ptbl.columnCount()
			#<<DB
	
	def readnrn(self, nrn=None):
		if nrn != None:
			self.nrn=nrn
		self.setWindowTitle(self.nrn.name + ' :: Neurons Editor')
		self.nameedit.setText(self.nrn.name)
		self.numbedit.setValue(self.nrn.number)
		self.mu_periodedit.setValue(self.nrn.period_mu)
		self.sd_periodedit.setValue(self.nrn.period_sd)
		self.tu_periodedit.setValue(self.nrn.period_tau)
		self.process.setCurrentIndex(self.nrn.process)
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
		self.procselected(self.nrn.process)
		self.readptable()
		
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
	
	def procselected(self,proc):
		self.nrn.process = proc
		self.tu_periodedit.setVisible(proc != 2 and proc != 3)
		self.label00.setVisible(proc != 2 and proc != 3)
		self.plabel.setVisible(proc == 5 or proc == 6)
		self.ploadbutton.setVisible(proc == 5 or proc == 6)
		self.pinsertrow.setVisible(proc == 5 or proc == 6)
		self.pdeleterow.setVisible(proc == 5 or proc == 6)
		self.ptbl.setVisible(proc == 5 or proc == 6)
		self.mu_periodedit.setVisible(proc != 5 and proc != 6)
		self.sd_periodedit.setVisible(proc != 5 and proc != 6)
		self.tu_periodedit.setVisible(proc != 5 and proc != 6)

		
	def ptablload(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '',
		"Data file (*.dat *.data);; Coma Separated Value (*.csv *.CSV)")
		if len(filename) == 0: return 
		self.nrn.ptable = []
		with open(filename,"r") as fd:
			for l in fd.readlines():
				d=l[:-1].split(",")[0].split("\t")[0].split(" ")[0]
				self.nrn.ptable.append(d)
		self.readptable()
		return
	def ptablinsert(self):
		self.nrn.ptable.append(0)
		self.readptable()
		return

	def ptabldelete(self):
		#didx = self.tbl.currentRow()
		#if didx < 0 : return
		#self.prc.data = self.prc.data[0:didx]+self.prc.data[didx+1:]
		#self.readprc()
		return
	def perUpDate(self, idx, c):
		data,ok = self.ptbl.item(idx,c).data(0).toDouble()
		if not ok:
			QtGui.QMessageBox.critical(self,"Critical ERROR!","The Row %d isn't an number!"%idx,QtGui.QMessageBox.Ok,0)
			return False
		self.nrn.ptable[idx] =  "{}".format(data)
		#DB>>
		print "DB: ptable:", self.nrn.ptable
		#<<DB

	def ok(self):
		if not self.upDate(): return
		self.accept()
	def cancel(self):
		self.reject()


class glnoisyneurons:
	def __init__(self,parent = None, mainwnd = None, menubar = None, toolbar = None):
		self.parent		= parent
		self.mainwnd	= mainwnd
		self.object		= "noisyneurons"
		insertppl = QtGui.QAction(QtGui.QIcon(':/noisyneurons.png'), 'Insert Noisy Neurons', mainwnd)
		insertppl.setShortcut('Alt+K')
		insertppl.setStatusTip('Insert or Edit Set of Noisy Neurons')
		mainwnd.connect(insertppl, QtCore.SIGNAL('triggered()'), self.insert)
		menu = menubar.addMenu('Nois&y Neurons')
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
		edit=nynrnedt(parent=self.mainwnd)
		item = self.mainwnd.tree.currentItem()
		ok = False
		if item.data(1,QtCore.Qt.UserRole) == self.object:
			nrnid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
			if not ok:
				print "Collapes Noise Neurons item((("
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
			newnrn.setIcon(0,QtGui.QIcon(':/noisyneurons.png'))
			newnrn.setText(1,'Noisy Neurons set:')
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
			result.append("<noisyneurons name=\"%s\" number=\"%d\" period_mu=\"%g\" period_sd=\"%g\" period_tau=\"%g\" process=\"%d\" f2=\"%s\">"%(nrn.name, nrn.number, nrn.period_mu, nrn.period_sd,  nrn.period_tau,  nrn.process, f2_selector[nrn.f2_selector]))
			if nrn.init_selector == 0:
				result.append("\t<init ph0_all=\"%g\" ph1_all=\"%g\" />"%(nrn.ph0_all, nrn.ph1_all))
			elif nrn.init_selector == 1:
				result.append("\t<init ph0_all=\"%g\" ph0_sd=\"%g\" ph1_all=\"%g\" ph1_sd=\"%g\"/>"%(nrn.ph0_all, nrn.ph0_sd, nrn.ph1_all, nrn.ph1_sd))
			else :
				result.append("\t<init ph0=\"%s\" ph1=\"%s\" />"%(str.join(nrn.ph0,","), str.join(nrn.ph1,",")) )
			if len(nrn.ptable) != 0:
				result.append("\t<periodtable items=\"%s\" />"%str.join(nrn.ptable,","))
			result.append("</noisyneurons>")
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
		elif name == "periodtable":
			self.tmpnrn.ptable = attr["items"].split(",")
		elif name == self.object:
			if self.tmpnrn != None:
				QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
				return
			self.tmpnrn = odnoisyneurons()
			self.tmpnrn.pid = pid
			if attr.get("name",0): self.tmpnrn.name = attr["name"]
			if attr.get("period_mu", -1.0) >= 0.0: self.tmpnrn.period_mu = float(attr["period_mu"])
			if attr.get("period_sd", -1.0) >= 0.0: self.tmpnrn.period_sd = float(attr["period_sd"])
			if attr.get("period_tau", -1.0) >= 0.0: self.tmpnrn.period_tau = float(attr["period_tau"])
			if attr.get("process", -1.0) >= 0.0: self.tmpnrn.process = int(attr["process"])
			if attr.get("number", -1)   >= 0  : self.tmpnrn.number = int(attr["number"])
			if attr.get("f2", -1)   >= 0  :
				if attr["f2"] == "off": self.tmpnrn.f2_selector = 2
				elif attr["f2"] == "last": self.tmpnrn.f2_selector = 1
			
			
		else:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
			return
		
	def stoppoint(self,name):
		if name == "init" or name == "periodtable": return
		if name == self.object:
			if self.tmpnrn != None:
				if self.tmpnrn.pid < 0:
					newnrn = QtGui.QTreeWidgetItem(self.parent.root)
					self.parent.root.addChild(newnrn)
				else:
					newnrn = QtGui.QTreeWidgetItem(self.parent.glpopulation.tmppop.id)
					self.parent.glpopulation.tmppop.id.addChild(newnrn)
				newnrn.setIcon(0,QtGui.QIcon(':/noisyneurons.png'))
				newnrn.setText(1,'Noisy Neurons set:')
				newnrn.setText(2,self.tmpnrn.name)
				newnrn.setData(1,QtCore.Qt.UserRole,self.object)
				newnrn.setData(2,QtCore.Qt.UserRole,len(self.nrnlst))
				
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

